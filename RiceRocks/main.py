import simplegui
import math
import random

WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        # 生命周期
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan
# 动画

    def get_animated(self):
        return self.animated

# 导入图片
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim


# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
# 碎片               debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
# 星云
# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")
# 飞溅
# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
# 飞船
# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
# 导弹
# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
# 小行星
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
# 爆炸
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
# 声音
# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
# soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")


# 创建飞船类

class Ship(object):
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self, canvas):
        if self.thrust:
            canvas.draw_image(
                self.image, [130, 45], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center,
                              self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        c = 0.1
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)

        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0]
            self.vel[1] += forward[1]

    def set_thrust(self, on):
        self.thrust = on  # 添加声音
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()

# 增加或减少角速度
    def increase_angvel(self):
        self.angle_vel += 0.05

    def decrease_angvel(self):
        self.angle_vel -= 0.05

# 射击
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        pos = list(self.pos)
        vel = [0, 0]
        missile_speed = 15
        pos[0] += self.vel[0] + self.radius * forward[0]
        pos[1] += self.vel[1] + self.radius * forward[1]
        vel[0] = forward[0] * missile_speed
        vel[1] = forward[1] * missile_speed
        missile_group.add(Sprite(pos, vel, self.angle, 0,
                                 missile_image, missile_info, missile_sound))


# 角度转为向量
# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]
# p，q距离，(a^2+b^2)^0.5


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


class Sprite(object):
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = list(pos)
        self.vel = list(vel)
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center,
                          self.image_size, self.pos, self.image_size, self.angle)
        if self.animated:
            image_tile = (self.age % 24) // 1  # 动画效果 由24个图像组成
            self.image_center = [
                self.image_center[0] + image_tile * self.image_size[0], self.image_center[1]]
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        if self.lifespan:
            if self.age > self.lifespan:
                return True
            else:
                self.age += 1
        return False

    def collide(self, other_object):
        if dist(self.pos, other_object.pos) <= self.radius + other_object.radius:
            return True
        else:
            return False

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius


def group_collide(group, other_object):
    global explosion_group
    for sprite in list(group):
        if sprite.collide(other_object):
            explosion_group.add(Sprite(sprite.get_position(
            ), (0, 0), 0, 0, explosion_image, explosion_info, explosion_sound))
            group.remove(sprite)
            return True
        else:
            return False


def group_group_collide(group1, group2):
    global score
    for sprite in list(group2):
        if group_collide(group1, sprite):  # 调用物体与组的碰撞函数
            group2.remove(sprite)
            score += 1  # 每击中1次，子弹与星石消失，分数加1


# 绘制，放在draw中


def process_sprite_group(canvas, group):
    for sprite in set(group):
        sprite.draw(canvas)
        if sprite.update():
            group.remove(sprite)


def rock_spawner():
    global rock_group, started
    if len(rock_group) < 12 and started:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_avel = random.random() * .2 - .1

    while dist(rock_pos, my_ship.pos) < 60:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel,
                    asteroid_image, asteroid_info)
    rock_group.add(a_rock)


def key_down(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrease_angvel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increase_angvel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()


def key_up(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.increase_angvel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrease_angvel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)


def click(pos):
    global started, score, lives, my_ship, rock_group, missile_group
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:  # 重置多个参数，添加音效
        started = True
        score = 0
        lives = 3
        timer.start()
        soundtrack.rewind()
        soundtrack.play
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0],
                       0, ship_image, ship_info)


def draw(canvas):

    global time, started, lives, rock_group
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(
    ), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size,
                      (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size,
                      (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text('Lives:' + str(lives), (50, 50), 28, "Red")
    canvas.draw_text('Score:' + str(score), (625, 50), 28, "Red")
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    # update ship and sprites
    my_ship.update()

    if group_collide(rock_group, my_ship):
        lives -= 1
    group_group_collide(rock_group, missile_group)
    if lives < 1:
        started = False
        rock_group = set([])
        soundtrack.pause()
        timer.stop()
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())


frame = simplegui.create_frame('Asteroid', WIDTH, HEIGHT)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])


frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)  # 添加键盘控制
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000, rock_spawner)
timer.start()
frame.start()
