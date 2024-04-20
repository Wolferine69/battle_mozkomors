import pygame
import random

# Initialize Pygame
pygame.init()

# Set the screen dimensions
width = 1200
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battle with mozkomors")  # Set the window caption

# Set frames per second
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

        # Background music setup
        pygame.mixer.music.load("media/bg-music-hp.wav")
        pygame.mixer.music.play(-1)  # Loop the background music indefinitely

        # Load custom font
        self.potter_font = pygame.font.Font("fonts/Harry.ttf", 24)

        # Load background image
        self.bg_image = pygame.image.load("img/bg-dementors.png")

        # Load images for different types of 'mozkomors'
        blue_image = pygame.image.load("img/mozkomor-modry.png")
        green_image = pygame.image.load("img/mozkomor-zeleny.png")
        purple_image = pygame.image.load("img/mozkomor-ruzovy.png")
        yellow_image = pygame.image.load("img/mozkomor-zluty.png")
        self.mozkomors_images = [blue_image, green_image, purple_image, yellow_image]

        # Randomly select a target 'mozkomor' for catching
        self.mozkomor_catcht = random.randint(0, 3)
        self.mozkomor_catch_image = self.mozkomors_images[self.mozkomor_catcht]
        self.mozkomor_catch_image_rect = self.mozkomor_catch_image.get_rect(center=(width // 2, 57))

    def update(self):
        self.slow_down_cycle += 1
        if self.slow_down_cycle == fps:  # Increment round time every second
            self.round_time += 1
            self.slow_down_cycle = 0

        self.check_collision()  # Check for collisions between player and mozkomors

    def draw(self):
        # Define colors for text and UI elements
        dark_yellow = pygame.Color("#938f0c")
        colors = [pygame.Color(21, 31, 217), pygame.Color(24, 194, 38), pygame.Color(195, 23, 189),
                  pygame.Color(195, 181, 23)]

        # Render and place text for game info
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

        # Draw the target 'mozkomor' and highlight it
        screen.blit(self.mozkomor_catch_image, self.mozkomor_catch_image_rect)
        pygame.draw.rect(screen, colors[self.mozkomor_catcht], (0, 100, width, height - 200), 4)

    def check_collision(self):
        # Collision detection logic
        colidded_mozkomor = pygame.sprite.spritecollideany(self.player, self.group_mozkomors)
        if colidded_mozkomor:
            if colidded_mozkomor.type == self.mozkomor_catcht:
                self.player.catch_sound.play()
                self.score += 5 * self.round
                colidded_mozkomor.remove(self.group_mozkomors)
                if self.group_mozkomors:
                    self.choose_new_target()
                else:
                    self.player.reset()
                    self.start_new_round()
            else:
                self.player.wrong_sound.play()
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.pause(f"Achieved score: {self.score}", "Press enter to play again!")
                    self.reset()
                self.player.reset()

    def start_new_round(self):
        # Logic to start a new game round
        self.score += int(100 * (self.round / (1 + self.round_time)))
        self.round_time = 0
        self.slow_down_cycle = 0
        self.round += 1
        self.player.safezones += 1
        for deleted_mozkomor in self.group_mozkomors:
            self.group_mozkomors.remove(deleted_mozkomor)
        for _ in range(self.round):
            for i in range(4):
                self.group_mozkomors.add(
                    Mozkomor(random.randint(0, width - 64), random.randint(100, height - 164), self.mozkomors_images[i],
                             i))
        self.choose_new_target()

    def choose_new_target(self):
        # Select a new target mozkomor from the group
        new_mozkomor_catch = random.choice(self.group_mozkomors.sprites())
        self.mozkomor_catcht = new_mozkomor_catch.type
        self.mozkomor_catch_image = new_mozkomor_catch.image

    def pause(self, heading, subheading):
        # Pause and display game over screen
        global lets_continue
        dark_yellow = pygame.Color("#938f0c")
        heading_text = self.potter_font.render(heading, True, dark_yellow)
        heading_rect = heading_text.get_rect(center=(width // 2, height // 2))
        subheading_text = self.potter_font.render(subheading, True, dark_yellow)
        subheading_rect = subheading_text.get_rect(center=(width // 2, height // 2 + 60))
        screen.fill("black")
        screen.blit(heading_text, heading_rect)
        screen.blit(subheading_text, subheading_rect)
        pygame.display.update()
        paused = True
        while paused:
            for event_paused in pygame.event.get():
                if event_paused.type == pygame.KEYDOWN:
                    if event_paused.key == pygame.K_RETURN:
                        paused = False
                if event_paused.type == pygame.QUIT:
                    paused = False
                    lets_continue = False

    def reset(self):
        # Reset the game state
        self.score = 0
        self.round = 0
        self.player.lives = 5
        self.player.safezones = 3
        pygame.mixer.music.play(-1)
        self.start_new_round()


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
        self.wrong_sound = pygame.mixer.Sound("media/wrong.wav")
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


lets_continue = True

mozkomor_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
one_player = Player()
player_group.add(one_player)

my_game = Game(one_player, mozkomor_group)
my_game.pause("Harry Potter and battle with mozkomors", "Press enter to play!")
my_game.start_new_round()

while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                one_player.safe_zone()

    screen.blit(my_game.bg_image, (0,0))
    mozkomor_group.draw(screen)
    mozkomor_group.update()
    player_group.draw(screen)
    player_group.update()
    my_game.update()
    my_game.draw()

    pygame.display.update()
    clock.tick(fps)
pygame.quit()
