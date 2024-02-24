import pygame as pg
from random import randint
from Class import Asteroid, Player, Wepon, Button


def main():
    def draw_square_with_text(surface, color, rect, text, text_color):
        pg.draw.rect(surface, color, rect)
        font = pg.font.SysFont(None, 36)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    pg.init()
    clock, dt = 0, 0
    screen = pg.display.set_mode((1280, 720))
    player = Player(screen)

    weps = [Wepon(player.x[2], player.y[2], player.angle, False) for i in range(15)]
    weps[0].score = 0
    clock = pg.time.Clock()

    asteroids = []
    for i in range(1):
        randx = randint(-screen.get_width()//2, screen.get_width()-50)
        randy = randint(-screen.get_height()//2, screen.get_height()- 250)
        asteroids.append(Asteroid(randx, randy, 30))

    bg = pg.image.load("../../PycharmProjects/PFE/images/14637.jpg")
    bg = pg.transform.scale(bg, (1280, 720))
    button = Button((screen.get_width()//2-100, screen.get_height()//2-100), (200, 200), "white", "white")
    run, lose = True, False
    t = 0
    while run:
        if(t - int(t) > 0.99 or t - int(t) < 0.00019 ):
            for i in range(3):
                randx = randint(-screen.get_width() // 2, screen.get_width() - 50)
                randy = randint(-screen.get_height() // 2, screen.get_height() - 250)
                asteroids.append(Asteroid(randx, randy, 30))

        keys = pg.key.get_pressed()
        lose = False
        screen.blit(bg, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT: exit()

        square_rect = pg.Rect(0, 0, 200, 100)
        message_rect = pg.Rect(screen.get_width()//2-200,30, 400,200)
        player.draw(screen)
        player.move(screen)
        player.rotate()

        for i in range(len(weps)):
            weps[i].shot(screen, asteroids)
            b = False
            if keys[pg.K_SPACE] and not weps[i].exists:
                weps[i].x = player.x[2]
                weps[i].y = player.y[2]
                weps[i].angle = player.angle
                b = True
                weps[i].exists = True
            if b: break


        for i in asteroids:
            i.move()
            i.draw(screen)
        draw_square_with_text(screen, "black", square_rect, f'SCORE: {weps[0].get_score()}', "white")
        lose = player.game_over(asteroids, screen)
        run = not lose

        dt = clock.tick(60) / 1000
        t += dt
        pg.display.flip()

    while lose:
        bg = pg.image.load("../../PycharmProjects/PFE/images/14637.jpg")
        bg = pg.transform.scale(bg, (1280, 720))
        for event in pg.event.get():
            if event.type == pg.QUIT: lose = False
        screen.fill("white")
        button.draw(screen)
        draw_square_with_text(screen, "black", square_rect, f'SCORE: {weps[0].get_score()}', "white")
        draw_square_with_text(screen, "white", message_rect, f'Press SPACE if you want to try again', "black")
        img = pg.image.load("../../PycharmProjects/PFE/images/again.png")
        screen.blit(img, (button.coords[0], button.coords[1]))
        if button.is_clicked():
            main()
        pg.display.flip()


main()
