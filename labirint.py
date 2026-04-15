from pygame import *

bg = (112, 225, 221)
window = display.set_mode((700, 500))
display.set_caption("Labyrinth")
window.fill(bg)

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, filename, width, height, x_pos, y_pos, x_speed, y_speed):
        super().__init__(filename, width, height, x_pos, y_pos)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        if self.rect.x < 639 and self.x_speed > 0 or self.rect.x > 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        #Collision x
        platform_touched = sprite.spritecollide(self, barriers, False)
        for p in platform_touched:
            if self.x_speed > 0:
                self.rect.right = min(self.rect.right, p.rect.left)
            elif self.x_speed < 0:
                self.rect.left = max(self.rect.left, p.rect.right)

        if self.rect.y < 439 and self.y_speed > 0 or self.rect.y > 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        
        #Collision y
        platform_touched = sprite.spritecollide(self, barriers, False)
        for p in platform_touched:
            if self.y_speed > 0:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
            elif self.y_speed < 0:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def Fire(self):
        bullet = Bullet("bullet.png", 20, 10, self.rect.right, self.rect.centery, 10)
        bullets.add(bullet)

class enemy(GameSprite):
    def __init__(self, filename, width, height, x_pos, y_pos, speed, hitcol1, hitcol2):
        super().__init__(filename, width, height, x_pos, y_pos)
        self.speed = speed
        self.direction = 'left'
        self.collision_1 = hitcol1
        self.collision_2 = hitcol2

    def update(self):
        if self.rect.x >= self.collision_1:
            self.direction = 'left'

        if self.rect.x <= self.collision_2:
            self.direction = 'right'

        if self.direction == 'left':
            self.rect.x -= self.speed

        elif self.direction == 'right':
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, filename, width, height, x_pos, y_pos, speed):
        super().__init__(filename, width, height, x_pos, y_pos)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed

        if self.rect.x > 700:
            self.kill()


wall_2 = GameSprite('platform2_v.png', 360, 40, 120, 357)
wall_4 = GameSprite('platform2_v.png', 275, 40, 270, 170)
wall_1 = GameSprite('platform2.png', 49, 420, 120, 150)
wall_3 = GameSprite('platform2.png', 49, 210, 260, 0)
locked_wall = GameSprite('platform2_lock.png', 160, 50, -10, 380)
target = GameSprite('pac-1.png', 75, 75, 169, 417)
hero = Player('hero.png', 60, 60, 50, 300, 0, 0)
cyborg = enemy('cyborg.png', 70, 70, 600, 80, 2, 639, 309)
cyborg2 = enemy('cyborg.png', 70, 70, 550, 210, 4, 639, 169)
cyborg3 = enemy('cyborg.png', 70, 70, 575, 420, 3, 639, 169)
win_image = transform.scale(image.load('thumb.jpg'), (700, 500))
lose_image = transform.scale(image.load('game-over_1.png'), (700, 500))
gun = GameSprite('gun.png', 50, 30, 40, 450)
key = GameSprite('key.png', 50, 30, 310, 40)
retry_button = GameSprite("retry_btn.png", 117, 50, 5, 5)



barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)
barriers.add(wall_4)
barriers.add(locked_wall)

bullets = sprite.Group()

cyborgs = sprite.Group()
cyborgs.add(cyborg)
cyborgs.add(cyborg2)
cyborgs.add(cyborg3)

target_vis = False

has_gun = False
has_key = False
run = True
finish = False
count = 0

level = 1
game_over = False

def reset_game():
    global hero, cyborg, cyborg2, cyborg3, target, target_vis
    global barriers, bullets, cyborgs, has_gun, has_key, finish, run, count
    global wall_1, wall_2, wall_3, wall_4, locked_wall, key, gun

    hero = Player('hero.png', 60, 60, 50, 300, 0, 0)
    cyborg = enemy('cyborg.png', 70, 70, 600, 80, 2, 639, 309)
    cyborg2 = enemy('cyborg.png', 70, 70, 550, 210, 4, 639, 169)
    cyborg3 = enemy('cyborg.png', 70, 70, 575, 420, 3, 639, 169)
    target = GameSprite('pac-1.png', 75, 75, 169, 417)
    target_vis = False

    wall_2 = GameSprite('platform2_v.png', 360, 40, 120, 357)
    wall_4 = GameSprite('platform2_v.png', 275, 40, 270, 170)
    wall_1 = GameSprite('platform2.png', 49, 420, 120, 150)
    wall_3 = GameSprite('platform2.png', 49, 210, 260, 0)
    locked_wall = GameSprite('platform2_lock.png', 160, 50, -10, 380)
    key = GameSprite('key.png', 50, 30, 310, 40)
    gun = GameSprite('gun.png', 50, 30, 40, 450)

    barriers = sprite.Group()
    barriers.add(wall_1, wall_2, wall_3, wall_4, locked_wall)

    bullets = sprite.Group()

    cyborgs = sprite.Group()
    cyborgs.add(cyborg, cyborg2, cyborg3)

    has_gun = False
    has_key = False
    finish = False
    count = 0

while run:
    
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            if e.key == K_a:
                hero.x_speed = -5
            if e.key == K_d:
                hero.x_speed = 5
            if e.key == K_w:
                hero.y_speed = -5
            if e.key == K_s:
                hero.y_speed = 5
            if e.key == K_SPACE:
                if has_gun == True:
                    hero.Fire()
            
        
        if e.type == KEYUP:
            if e.key == K_a:
                hero.x_speed = 0
            if e.key == K_d:
                hero.x_speed = 0
            if e.key == K_w:
                hero.y_speed = 0
            if e.key == K_s:
                hero.y_speed = 0
                
        if e.type == MOUSEBUTTONDOWN:
                if retry_button.rect.collidepoint(e.pos):
                    reset_game()
            
                
    if finish != True:
        window.fill(bg)
        hero.update()
        hero.reset()
        wall_2.reset()
        wall_1.reset()
        wall_3.reset()
        wall_4.reset()

        bullets.update()
        bullets.draw(window)

        cyborgs.update()
        cyborgs.draw(window)

        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, cyborgs, True, True)
        
        if len(cyborgs) == 0:
            target_vis = True
        
        if sprite.collide_rect(hero, key):
            has_key = True
            locked_wall.kill()
        else:
            if has_key == False:
                key.reset()
                locked_wall.reset()

        if sprite.collide_rect(hero, gun):
            has_gun = True
        else:
            if has_gun == False:
                gun.reset()
                
        if target_vis == True:
            target.reset()

        if target_vis and sprite.collide_rect(hero, target):
            finish = True
        if sprite.spritecollide(hero, cyborgs, False):
            finish = True


    else:
        if target_vis and sprite.collide_rect(hero, target):
            window.blit(win_image, (0, 0))
        else:
            window.blit(lose_image, (0, 0))
        retry_button.reset()

    display.update()

