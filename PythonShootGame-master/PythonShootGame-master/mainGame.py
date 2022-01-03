import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random



pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BerkiboGame')


bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy_bullet_sound = pygame.mixer.Sound('resources/sound/get_bomb.mp3')
bomb_sound = pygame.mixer.Sound('resources/sound/use_bomb.mp3')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy_bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


background = pygame.image.load('resources/image/background.png').convert()
game_over_lost = pygame.image.load('resources/image/gameover.png')
game_over_win = pygame.image.load('resources/image/win.png')
filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)


player_rect = []   
player_rect.append(pygame.Rect(0, 99, 98, 126))        
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]   
player = Player(plane_img, player_rect, player_pos)


bullet_rect = pygame.Rect(68, 70, 10, 29)
bullet_img = plane_img.subsurface(bullet_rect)

bomb_rect = pygame.Rect(99, 100, 59, 121) 
bomb_img = plane_img.subsurface(bomb_rect)

enemy_bullet_rect = pygame.Rect(1004, 987, 9, 21)
enemy_bullet_img = plane_img.subsurface(enemy_bullet_rect)


enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))


enemies1 = pygame.sprite.Group()
enemy_bullets= pygame.sprite.Group() 
enemies_down = pygame.sprite.Group()

bombs_down = pygame.sprite.Group()
bombs= pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0
bomb_frequency = 0
enemy_shoot_frequency = 0
enemy_frequency_const =100
bomb_frequency_const = 400
player_down_index = 16


score = 0
level = 1
bullet_count=15
enemy_speed= 2

clock = pygame.time.Clock()

running = True

while running: 
    
    
    clock.tick(55) 

    key_pressed = pygame.key.get_pressed()   
    if not player.is_hit:
        if shoot_frequency % 8 == 0:
            if (bullet_count > 0):
                if key_pressed[K_SPACE]:
                    bullet_sound.play()
                    player.shoot(bullet_img)
                    bullet_count = bullet_count-1                    
        shoot_frequency += 1
        if shoot_frequency >= 8:
            shoot_frequency = 0
    
    level = int( score/10000 ) +1
    
    
    if(level>=2):
        enemy_speed=((level*2000)/10000)+2
        

    if enemy_frequency % enemy_frequency_const == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos,enemy_speed)
        enemies1.add(enemy1)
    
        if(level>=3):
            if enemy_shoot_frequency % 2 == 0:  
                enemy_bullet_sound.play()
                bullet = EnemyBullet(enemy_bullet_img, enemy1.rect.midbottom)
                enemy_bullets.add(bullet)
            enemy_shoot_frequency += 1
            if enemy_shoot_frequency >= 2:
                shoot_frequency = 0
    enemy_frequency += 1
    if enemy_frequency >= enemy_frequency_const:
        enemy_frequency = 0

    if(level>=4):
        enemy_frequency_const=50

    if(level>=5):
        if bomb_frequency % bomb_frequency_const == 0:
            bomb_pos = [random.randint(0, SCREEN_WIDTH - bomb_rect.width), 0]
            bomb = Bomb(bomb_img, bomb_pos)
            bombs.add(bomb)
        bomb_frequency += 1
        if bomb_frequency >= bomb_frequency_const:
            bomb_frequency = 0    

  
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

       
    for bomb in bombs:
        bomb.move()
        if len(bombs)>0 and bomb.rect.bottom < 0:
            bomb.remove(bullet)

   
    for bullet in enemy_bullets:
        bullet.move()
    if len(enemy_bullets)>0 and bullet.rect.bottom < 0:
        enemy_bullets.remove(bullet)

    for enemy in enemies1:
        enemy.move()
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT: 
            enemies1.remove(enemy)

    
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1) 
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)
        bullet_count+=2
    
    bombs1_down = pygame.sprite.groupcollide(bombs, player.bullets, 1, 1)
    for bomb_down in bombs1_down:
        bombs_down.add(bomb_down)  
    
    for bullet in enemy_bullets:     
        if pygame.sprite.collide_circle(bullet, player):
            player.is_hit=True
            enemy_bullets.remove(bullet)
            game_over_sound.play()
            break
    

    for bomb in bombs:   
        if pygame.sprite.collide_circle(bomb, player):
            player.is_hit=True
            bombs.remove(bomb)
            game_over_sound.play()
            break

    screen.fill(0)
    screen.blit(background, (0, 0))

   
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        player.img_index = shoot_frequency // 8  
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47: 
            running = False

    
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    for bomb_down in bombs_down:
        bomb_sound.play()
        bombs_down.remove(bomb_down)
        score += 500
   
    player.bullets.draw(screen)
    enemies1.draw(screen)
    enemy_bullets.draw(screen)
    bombs.draw(screen)


   
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 20]
    screen.blit(score_text, text_rect)

    level_font = pygame.font.Font(None, 36)
    level_str = "Level: " + str(level)
    level_text = level_font.render(level_str, True, (128, 128, 128))
    level_text_rect = level_text.get_rect()
    level_text_rect.topright = [470, 20]
    screen.blit(level_text, level_text_rect)

    enemy_speed_font = pygame.font.Font(None, 20)
    enemy_speed_str = "Speed of Enemies: " + str(enemy_speed)
    enemy_speed_text = enemy_speed_font.render(enemy_speed_str, True, (128, 128, 128))
    enemy_speed_text_rect = enemy_speed_text.get_rect()
    enemy_speed_text_rect.bottomleft = [10, 770]
    screen.blit(enemy_speed_text, enemy_speed_text_rect)

    bullet_font = pygame.font.Font(None, 20)
    bullet_str = "Bullet Count: " + str(bullet_count)
    bullet_text = bullet_font.render(bullet_str, True, (128, 128, 128))
    bullet_text_rect = enemy_speed_text.get_rect()
    bullet_text_rect.topright = [500, 45]
    screen.blit(bullet_text, bullet_text_rect)
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            

    key_pressed = pygame.key.get_pressed()

    if not player.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()

if (level >= 6):
    font = pygame.font.Font(None, 58)
    text = font.render('You Win', True, (0, 255, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(game_over_win, (0, 0))
    screen.blit(text, text_rect)
else:
    font = pygame.font.Font(None, 48)
    text = font.render('Score: '+ str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(game_over_lost, (0, 0))
    screen.blit(text, text_rect)



   


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
