import random

import pygame
import pygame.freetype
import sprites



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800,800))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Samurai Jump')
        self.big_font = pygame.freetype.Font(r'C:\Users\erazz\OneDrive\Рабочий стол\KAWARA-PersonalUse.ttf',75)
        self.small_font = pygame.freetype.Font(r'C:\Users\erazz\OneDrive\Рабочий стол\KAWARA-PersonalUse.ttf',25)
        self.midle_font = pygame.freetype.Font(r'C:\Users\erazz\OneDrive\Рабочий стол\KAWARA-PersonalUse.ttf',40)
        self.number_font = pygame.freetype.Font(r'C:\Users\erazz\OneDrive\Рабочий стол\OtomanopeeOne-Regular.ttf',25)

        self.highscore=0
        self.speed = 0
        self.player = None
        self.on_ground = False

        self.menu()

    def draw_overlay(self):
        pygame.draw.rect(self.screen, (128,0,0),(0,0,150,800),0)
        pygame.draw.rect(self.screen, (128,0,0),(650,0,150,800),0)
        pygame.draw.rect(self.screen, (0,0,0),(0,0,150,800),10)
        pygame.draw.rect(self.screen, (0,0,0),(650,0,1500,800),10)

    def draw_menu_header(self):
        text_surf, text_rect = self.big_font.render('Samurai jump', (0,0,0))
        self.screen.blit(text_surf,((self.screen.get_rect().w - text_rect.w) / 2,
            200,), )

        text_surf, text_rect = self.number_font.render(f'Highscore:{self.highscore}',(0,0,0))
        self.screen.blit(
            text_surf,
            ((self.screen.get_rect().w - text_rect.w) / 2,
            300,),
        )
    def menu(self):
        play_button = sprites.Button(400,540,'Play',self.midle_font)

        menu_run = True
        while menu_run:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.be_inside(mouse_pos[0],mouse_pos[1]):
                        menu_run=self.game()


            play_button.update(mouse_pos[0], mouse_pos[1])

            self.screen.fill((128,128,128))
            self.draw_overlay()
            self.draw_menu_header()
            self.screen.blit(play_button.image, play_button.rect)
            pygame.display.flip()
            self.clock.tick(60)

    def boundaries(self, platforms):

        for platform in platforms.sprites():
            if (
                    self.player.rect.right >= platform.rect.left and
                    self.player.rect.left <= platform.rect.right and
                    platform.rect.bottom >= self.player.rect.bottom >= platform.rect.top
            ):
                if self.speed >= 0:
                    self.speed = 0
                    self.on_ground = True

    def draw_result(self,score):
        text_surf, _ = self.number_font.render(f'Score:{score}', (0, 0, 0))
        self.screen.blit(text_surf, (20,50,),)

    def game(self):
        pygame.mixer.music.load(r"C:\Users\erazz\PycharmProjects\проект Ерасыла\misora-traditional-japanese-music_03-141356.mp3")
        pygame.mixer.music.play(-1)

        self.player = sprites.Sprite(400,540,85,85, 'DarkSamurai (50x50).png')
        power = 3
        platforms = pygame.sprite.Group(
            [sprites.Sprite(random.randint(230,550),(i*100)+100,150,35,'platform1.png')for i in range(10)]
        )

        upper_platform = platforms.sprites()[0]

        self.speed=0
        score  = 0
        game_run = True
        fail=False

        while game_run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.rect.x-=5
            if keys[pygame.K_d]:
                self.player.rect.x+=5

            self.player.rect.y+=self.speed

            if self.player.rect.y >820:
                game_run = False
                fail=True

            self.boundaries(platforms)

            if not self.on_ground:
                self.speed += 0.1
            else:
                self.speed = -power
                self.on_ground = False

            for platform in platforms.sprites():
                if self.speed<0:
                    platform.rect.y-= self.speed-5
                if platform.rect.y>820:
                    platform.kill()
                    score+=1

            if upper_platform.rect.y > 100:
                upper_platform = sprites.Sprite(random.randint(230,550),20,150,35,'platform1.png')
                platforms.add(upper_platform)


            self.screen.fill((128,128,128))
            self.draw_overlay()
            self.draw_result(score)
            platforms.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            pygame.display.flip()
            self.clock.tick(60)
        if score>self.highscore:
            self.highscore=score


        return   fail

Game()
