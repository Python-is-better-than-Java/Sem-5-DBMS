import pygame
import time
pygame.init()

def check_dir(p_dir):
    if (p_dir == 0):
        return (0, -1)
    elif (p_dir == 1):
        return (-1, 0)
    elif (p_dir == 2):
        return (0, 1)
    else:
        return (1, 0)

def gameplay(screen):
    pygame.display.set_caption("PRAAJEQT")
    game_map = pygame.Rect(0, 0, 1000, 700)
    player = pygame.Rect(475, 325, 50, 50)

    p_bullet = pygame.image.load("Pistol_bullet.png")
    p_bullet = (pygame.transform.rotate(pygame.transform.scale(p_bullet, (20, 10)), 90), pygame.transform.rotate(pygame.transform.scale(p_bullet, (20, 10)), 180), pygame.transform.rotate(pygame.transform.scale(p_bullet, (20, 10)), 270), pygame.transform.scale(p_bullet, (20, 10)))
    a_bullet = pygame.image.load("Assault_bullet.png")
    a_bullet = (pygame.transform.rotate(pygame.transform.scale(a_bullet, (30, 10)), 90), pygame.transform.rotate(pygame.transform.scale(a_bullet, (30, 10)), 180), pygame.transform.rotate(pygame.transform.scale(a_bullet, (30, 10)), 270), pygame.transform.scale(a_bullet, (30, 10)))
    s_bullet = pygame.image.load("Sniper_bullet.png")
    s_bullet = (pygame.transform.rotate(pygame.transform.scale(s_bullet, (50, 10)), 90), pygame.transform.rotate(pygame.transform.scale(s_bullet, (50, 10)), 180), pygame.transform.rotate(pygame.transform.scale(s_bullet, (50, 10)), 270), pygame.transform.scale(s_bullet, (50, 10)))
    
    enemy1_red = pygame.image.load("Enemy1_red.png")
    enemy1_blue = pygame.image.load("Enemy1_blue.png")
    enemy2_red = pygame.image.load("Enemy2_red.png")
    enemy2_blue = pygame.image.load("Enemy2_blue.png")
    enemy_red = [pygame.transform.scale(enemy1_red, [100, 100]), pygame.transform.scale(enemy2_red, [100, 100])] # Red enemy images
    enemy_red_rect = [pygame.Rect([200, 10, 100, 100]), pygame.Rect([200, 200, 100, 100])] # add new pygame.Rect here for red enemies
    enemy_blue = [pygame.transform.scale(enemy1_blue, (100, 100)), pygame.transform.scale(enemy2_blue, (100, 100))] # Blue enemy images
    enemy_blue_rect = [pygame.Rect([10, 10, 100, 100]), pygame.Rect([10, 200, 100, 100])] # add new pygame.Rect here for blue enemies

    bullet_coord = [] # coordinates of every bullet (can take inspiration of implementation to make enemy images move)
    bullet_coord_rect = [] # Bullet rectangles so that collision can be checked with enemy rectangle
    direction = 3
    start = end = time.time()
    true = True

    while true == True:
        screen.fill((0, 0, 0)) 
        end = time.time()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                true = False
                pygame.quit()
            
        key = pygame.key.get_pressed()
        p_dir = check_dir(direction)
        if ((key[pygame.K_w] or key[pygame.K_UP]) and (player.y >= 0)):
            player.y -= 1
            direction = 0
        if ((key[pygame.K_a] or key[pygame.K_LEFT]) and (player.x >= 150)):
            player.x -= 1
            direction = 1
        if ((key[pygame.K_s] or key[pygame.K_DOWN]) and (player.y <= 650)):
            player.y += 1
            direction = 2
        if ((key[pygame.K_d] or key[pygame.K_RIGHT]) and (player.x <= 800)):
            player.x += 1
            direction = 3
        if (key[pygame.K_RETURN]):
            player.x = 475
            player.y = 325

        if (key[pygame.K_1] and (end - start >= 0.75)):
            bullet_coord.append([player.x + 25, player.y + 25, p_dir[0], p_dir[1], p_bullet[direction]])
            bullet_coord_rect.append(pygame.Rect(player.x + 25, player.y + 25, 20, 10))
            start = end
        if (key[pygame.K_2] and (end - start >= 0.5)):
            bullet_coord.append([player.x + 25, player.y + 25, p_dir[0], p_dir[1], a_bullet[direction]])
            bullet_coord_rect.append(pygame.Rect(player.x + 25, player.y + 25, 30, 10))
            start = end
        if (key[pygame.K_3] and (end - start >= 2)):
            bullet_coord.append([player.x + 25, player.y + 25, p_dir[0], p_dir[1], s_bullet[direction]])
            bullet_coord_rect.append(pygame.Rect(player.x + 25, player.y + 25, 50, 10))
            start = end

        pygame.draw.ellipse(screen, (0, 125, 0), player)
        for enemy in enemy_red:
            enemy_rect = enemy_red_rect[enemy_red.index(enemy)] # Get the red enemy rectangle from enemy_red_rect
            screen.blit(enemy, (enemy_rect.x, enemy_rect.y)) # display the red enemy character
            for bullet in bullet_coord:
                screen.blit(bullet[4], (bullet[0], bullet[1]))
                bullet_rect = bullet_coord_rect[bullet_coord.index(bullet)]

                if ((bullet[0] >= -50 and bullet[0] <= 1000) and (bullet[1] >= -50 and bullet[1] <= 700)):
                    bullet_coord[bullet_coord.index(bullet)][0] += bullet_coord[bullet_coord.index(bullet)][2] # Move bullet image horizontally
                    bullet_coord[bullet_coord.index(bullet)][1] += bullet_coord[bullet_coord.index(bullet)][3] # Move bullet image vertically
                    bullet_coord_rect[bullet_coord.index(bullet)].x += bullet_coord[bullet_coord.index(bullet)][2] # move bullet rectangle horizontally
                    bullet_coord_rect[bullet_coord.index(bullet)].y += bullet_coord[bullet_coord.index(bullet)][3] # move bullet rectangle vertically
                else:
                    bullet_coord.remove(bullet)
                    bullet_coord_rect.remove(bullet_rect)
            
                if (bullet_rect.colliderect(enemy_rect)): # bullet collide with enemy
                    bullet_coord_rect.remove(bullet_rect) # Remove bullet rectangle
                    bullet_coord.remove(bullet) # Remove bullet image
                    enemy_red_rect.remove(enemy_rect) # Remove red enemy rectangle
                    enemy_red.remove(enemy) # remove red enemy image
        
        pygame.display.flip()
#gameplay()