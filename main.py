import pygame
import random

pygame.init()

width = 1200
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bitva s mozkomory")

fps = 60
clock = pygame.time.Clock()


class Game:
    def __init__(self, player, group_mozkomors):
        self.score = 0
        self.round = 0
        self.round_time = 0
        self.slow_down_cycle = 0
        self.player = player
        self.group_mozkomors = group_mozkomors
        pygame.mixer.music.load("media/bg-music-hp.wav")
        pygame.mixer.music.play(-1)
        self.potter_font = pygame.font.Font("fonts/Harry.ttf", 24)

        blue_image = pygame.image.load("img/mozkomor-modry.png")
        green_image = pygame.image.load("img/mozkomor-zeleny.png")
        purple_image = pygame.image.load("img/mozkomor-ruzovy.png")
        yellow_image = pygame.image.load("img/mozkomor-zluty.png")
        self.mozkomors_images = [blue_image, green_image, purple_image, yellow_image]
        self.mozkomor_catcht = random.randint(0, 3)
        self.mozkomor_catch_image = self.mozkomors_images[self.mozkomor_catcht]
        self.mozkomor_catch_image_rect = self.mozkomor_catch_image.get_rect(center=(width // 2, 57))

    def update(self):
        self.slow_down_cycle += 1
        if self.slow_down_cycle == fps:
            self.round_time += 1
            self.slow_down_cycle = 0

        self.check_collision()

    def draw(self):
        dark_yellow = pygame.Color("#938f0c")
        blue = pygame.Color(21, 31, 217)
        green = pygame.Color(24, 194, 38)
        purple = pygame.Color(195, 23, 189)
        yellow = pygame.Color(195, 181, 23)
        colors = [blue, green, purple, yellow]

        catch_text = self.potter_font.render("Catch this mozkomor!", True, dark_yellow)
        catch_text_rect = catch_text.get_rect(center=(width // 2, 17))
        screen.blit(catch_text, catch_text_rect)

        score_text = self.potter_font.render(f"Score: {self.score}", True, dark_yellow)
        score_text_rect = score_text.get_rect(topleft=(10, 4))
        screen.blit(score_text, score_text_rect)

        lives_text = self.potter_font.render(f"Lives: {self.player.lives}", True, dark_yellow)
        lives_text_rect = lives_text.get_rect(topleft=(10, 30))
        screen.blit(lives_text, lives_text_rect)

        round_text = self.potter_font.render(f"Round: {self.round}", True, dark_yellow)
        round_text_rect = round_text.get_rect(topleft=(10, 60))
        screen.blit(round_text, round_text_rect)

        time_text = self.potter_font.render(f"Round time: {self.round_time}", True, dark_yellow)
        time_text_rect = time_text.get_rect(topright=(width - 10, 4))
        screen.blit(time_text, time_text_rect)

        back_szone_text = self.potter_font.render(f"Safe zone: {self.player.safezones}", True, dark_yellow)
        back_szone_text_rect = back_szone_text.get_rect(topright=(width - 10, 30))
        screen.blit(back_szone_text, back_szone_text_rect)

        screen.blit(self.mozkomor_catch_image, self.mozkomor_catch_image_rect)

        pygame.draw.rect(screen, colors[self.mozkomor_catcht], (0, 100, width, height-200), 4)

    def check_collision(self):
        pass

    def start_new_round(self):
        pass

    def choose_new_target(self):
        pass

    def pause(self):
        pass

    def reset(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/potter-icon.png")
        self.rect = self.image.get_rect(center=(width // 2, height - 34))
        self.lives = 5
        self.safezones = 3
        self.speed = 8
        self.catch_sound = pygame.mixer.Sound("media/expecto-patronum.mp3")
        self.catch_sound.set_volume(0.1)
        self.wrong_sound = pygame.mixer.Sound("media/success_click.wav")
        self.wrong_sound.set_volume(0.1)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < height - 100:
            self.rect.y += self.speed

    def safe_zone(self):
        if self.safezones > 0:
            self.safezones -= 1
            self.rect.bottom = height

    def reset(self):
        self.rect.center = (width // 2, height - 34)


class Mozkomor(pygame.sprite.Sprite):
    def __init__(self, x, y, image, m_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = m_type
        self.x = random.choice([-1, 1])
        self.y = random.choice([-1, 1])
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.x += self.x * self.speed
        self.rect.y += self.y * self.speed

        if self.rect.left < 0 or self.rect.right > width:
            self.x *= -1
        if self.rect.top < 100 or self.rect.bottom > height - 100:
            self.y *= -1


mozkomor_group = pygame.sprite.Group()
one_mozkomor = Mozkomor(500, 500, pygame.image.load("img/mozkomor-modry.png"), 0)
mozkomor_group.add(one_mozkomor)
one_mozkomor = Mozkomor(500, 500, pygame.image.load("img/mozkomor-zeleny.png"), 1)
mozkomor_group.add(one_mozkomor)
one_mozkomor = Mozkomor(500, 500, pygame.image.load("img/mozkomor-ruzovy.png"), 2)
mozkomor_group.add(one_mozkomor)
one_mozkomor = Mozkomor(500, 500, pygame.image.load("img/mozkomor-zluty.png"), 3)
mozkomor_group.add(one_mozkomor)

player_group = pygame.sprite.Group()
one_player = Player()
player_group.add(one_player)

my_game = Game(one_player, mozkomor_group)

pokracovat = True
while pokracovat:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pokracovat = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                one_player.safe_zone()

    screen.fill("black")
    mozkomor_group.draw(screen)
    mozkomor_group.update()
    player_group.draw(screen)
    player_group.update()
    my_game.update()
    my_game.draw()

    pygame.display.update()
    clock.tick(fps)
pygame.quit()
