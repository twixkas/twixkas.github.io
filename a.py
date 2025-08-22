from screeninfo import get_monitors
import time, random, math, pygame
from pygame import mixer

pygame.init()
mixer.init()

width, height = get_monitors()[0].width, get_monitors()[0].height

dis = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

font = pygame.font.SysFont("Arial", 48)

mouse_x = 0
mouse_y = 0 


class Rect:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = (255, 255, 255)
        self.checked = False
        
    def mouse_check(self):
        return self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h

    def render(self):
        pygame.draw.rect(dis, self.color, [self.x, self.y, self.w, self.h])

    def collision_check(self, other):
        return self.collision_check_for_point([other.x, other.y]) or self.collision_check_for_point([other.x+other.w, other.y]) or \
         self.collision_check_for_point([other.x, other.y + other.h]) or self.collision_check_for_point([other.x+other.w, other.y + other.h])

    def collision_check_for_point(self, point):
        return self.x < point[0] < self.x + self.w and self.y < point[1] < self.y + self.h

step = 20

x = width // 2
y = height - step*5

rects = []
for i in range(40):

    w = random.randrange(step-i//5, 100-i*2)
    h = random.randrange(step, 100-i*2)

    while True:

        d = random.randrange(-step*2, step*2)
        rect = Rect(x+d, y-step*0.9, w, h)

        if len(rects) == 0 or rect.collision_check(rects[-1]):
            rects.append(rect)

            x += d
            y -= step*0.9
            break

first_rect = rects[0]
last_rect = rects[-1]

texture1 = pygame.image.load("c.jpg")
texture2 = pygame.image.load("d.jpg")


h = (width / texture1.get_height()) * texture1.get_height()
texture1 = pygame.transform.scale(texture1, (width, h))
texture2 = pygame.transform.scale(texture2, (width, h))

done = False

c = 0

while True:

    c += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

    dis.fill((0, 0, 0))

    if done:
        if c % 6 == 0:
            dis.blit(texture1, (0, 0))
        else:
            dis.blit(texture2, (0, 0))
    else:
        img = font.render(f"ВЕДИ МЫШКУ СНИЗУ ВВЕРХ", True, (255, 255, 255))
        dis.blit(img, ((width-img.get_width())/2, height*0.15, 0, 0))

        mouse_check_result = False
        for rect in rects:
            if rect.mouse_check():
                rect.color = (255, 0, 0)
                rect.checked = True
                mouse_check_result = True

        if mouse_check_result == False:
            for rect in rects:
                rect.color = (255, 255, 255)
                rect.checked = False

        is_filled = True
        for rect in rects:
            if not rect.checked:
                is_filled = False
                break

        if is_filled:
            if last_rect.mouse_check():
                done = True
                pygame.mixer.music.load('b.mp3')
                pygame.mixer.music.play(0)
            else:
                for rect in rects:
                    rect.color = (255, 255, 255)
                    rect.checked = False
        else:
            for rect in rects:
                rect.render()


    pygame.display.update()
    time.sleep(0.001)
