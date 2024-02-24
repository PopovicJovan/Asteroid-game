import random
import pygame as pg
import math


class Asteroid:
    def __init__(self, x, y, radius=30, color="white"):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.randangle = random.randint(-1000, 1000) / 1000

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x -= 2.5*math.cos(self.randangle * math.pi)
        self.y += 2.5*math.sin(self.randangle * math.pi)


class Player:
    def __init__(self, screen, angle=math.pi / 2, x=None, y=None, color="white"):
        if x is None: x = [0, 0, 0]
        if y is None: y = [0, 0, 0]
        self.x = [screen.get_width() / 2 - 50, screen.get_width() / 2 + 50, screen.get_width() / 2]
        self.y = [screen.get_height() * 0.9, screen.get_height() * 0.9, screen.get_height() * 0.9 - 25 * (3 ** 0.5)]
        self.color = color
        self.angle = angle

    def draw(self, screen):
        pg.draw.polygon(surface=screen, color=self.color,
                        points=[(self.x[0], self.y[0]),
                                (self.x[1], self.y[1]),
                                (self.x[2], self.y[2])])

    def move(self, screen):
        keys = pg.key.get_pressed()
        xc, yc = sum(self.x) / 3, sum(self.y) / 3

        main_vector = [self.x[2] - xc, self.y[2] - yc]

        if self.x[2] > screen.get_width() - 2: return
        if self.x[2] < 2: return
        if self.y[2] < 2: return
        if self.y[2] > screen.get_height() - 2: return
        if self.x[2] < 200 and self.y[2] < 100: return

        if keys[pg.K_UP]:
            for i in range(len(self.y)):
                self.x[i] += 0.35 * main_vector[0]
                self.y[i] += 0.35 * main_vector[1]

    def rotate(self):
        keys = pg.key.get_pressed()
        angle = math.pi / 180
        if keys[pg.K_LCTRL]: angle = math.pi / 54
        COS, SIN = math.cos(angle), math.sin(angle)
        xc, yc = sum(self.x) / 3, sum(self.y) / 3

        if keys[pg.K_RIGHT]:
            print()
            for i in range(len(self.x)):
                x_old, y_old = self.x[i], self.y[i]
                self.x[i] = (x_old - xc) * COS - (y_old - yc) * SIN + xc
                self.y[i] = (x_old - xc) * SIN + (y_old - yc) * COS + yc
            self.angle -= angle
        if keys[pg.K_LEFT]:
            for i in range(len(self.x)):
                x_old, y_old = self.x[i], self.y[i]
                self.x[i] = (x_old - xc) * COS + (y_old - yc) * SIN + xc
                self.y[i] = -1 * (x_old - xc) * SIN + (y_old - yc) * COS + yc
            self.angle += angle

    def game_over(self, asteorids, screen):
        end = False
        for asteroid in asteorids:
            if (asteroid.x + asteroid.radius >= self.x[2] and asteroid.x - asteroid.radius <= self.x[2]
                    and asteroid.y + asteroid.radius >= self.y[2] and asteroid.y - asteroid.radius <= self.y[2]):
                end = True
                break
        return end


class Wepon:

    def __init__(self, x, y, angle, score=0):
        self.x, self.y = x, y
        self.angle, self.score = angle, score
        self.exists = False

    def shot(self, screen, asteroids):
        if not self.exists: return
        if self.y < 0 or self.y > screen.get_height(): self.exists = False
        if self.x < 0 or self.x > screen.get_width(): self.exists = False
        self.x += 20 * math.cos(self.angle)
        self.y -= 20 * math.sin(self.angle)
        pg.draw.circle(screen, "red", (self.x, self.y), 10)

        for i in range(len(asteroids)):
            if (math.sqrt((asteroids[i].x - self.x) ** 2 +
                          (asteroids[i].y - self.y) ** 2) <= asteroids[i].radius):
                if asteroids[i].radius == 15:
                    self.score += 1
                    asteroids[i].radius = 0
                    self.exists = False
                    break
                elif asteroids[i].radius != 0:
                    self.score += 1
                    asteroids[i].radius = 15
                    asteroids.append(Asteroid(self.x + 30, self.y + 30, 15))
                    self.exists = False
                    break

    def get_score(self):
        return str(self.score)


class Button:
    def __init__(self, coords, dimensions, color, text_color):
        self.coords = coords
        self.dimensions = dimensions
        self.color = color
        self.text_color = text_color

    def draw_text(self, font, color, surface, x, y):
        text_obj = font.render(self, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)

    def draw(self, surface):
        pg.draw.rect(surface, self.color, (self.coords[0], self.coords[1], self.dimensions[0], self.dimensions[1]))

    def is_clicked(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            return True
        elif keys[pg.K_ESCAPE]:
            exit()
