import simplegui
import math
import random

WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0


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
        global a_missile
        forward = angle_to_vector(self.angle)
        pos = list(self.pos)
        vel = [0, 0]
        missile_speed = 10
        pos[0] += self.vel[0] + self.radius * forward[0]
        pos[1] += self.vel[1] + self.radius * forward[1]
        vel[0] = forward[0] * missile_speed
        vel[1] = forward[1] * missile_speed
        a_missile = Sprite(pos, vel, self.angle, 0,
                           missile_image, missile_info, missile_sound)


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

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT


def rock_spawner():
    global a_rock
    a_rock = Sprite([random.randrange(WIDTH), random.randrange(HEIGHT)], [
                    random.randrange(-1, 1), random.randrange(-1, 1)], 0.05, 0.05, asteroid_image, asteroid_info)


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


def draw(canvas):
    global time
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

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()


frame = simplegui.create_frame('Asteroid', WIDTH, HEIGHT)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.05,
                asteroid_image, asteroid_info)  # 0.05秒旋转一下
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1, 1],
                   0, 0, missile_image, missile_info, missile_sound)


frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)  # 添加键盘控制
frame.set_keyup_handler(key_up)
timer = simplegui.create_timer(1000, rock_spawner)
timer.start()
frame.start()
