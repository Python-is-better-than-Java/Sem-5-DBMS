import pygame
from pygame.font import SysFont
import time
import random
import mysql.connector
pygame.init()

conn = mysql.connector.connect(host="localhost", user="root", password="S@ah1th!", database="shootergame")
cur = conn.cursor()

def check_dir(p_dir): # To check which direction player is facing
    if (p_dir == 0):   # Player facing up
        return (0, -10) 
    elif (p_dir == 1): # Player facing left
        return (-10, 0)
    elif (p_dir == 2): # Player facing down
        return (0, 10)
    else:              # Player facing right
        return (10, 0)

def gameplay(screen, player_name, map_image, enemy_colour):
    pygame.display.set_caption("PRAAJEQT")
    game_map = pygame.transform.scale(pygame.image.load(map_image), (1000, 700))
    player = pygame.Rect(475, 325, 50, 50)
    player_health = 500
    shots_fired = 0
    shots_hit = 0
    kills = 0

    p_bullet = pygame.image.load("Bullets/Pistol_bullet.png")
    p_bullet = (pygame.transform.rotate(pygame.transform.scale(p_bullet, (20, 10)), 90), pygame.transform.rotate(pygame.transform.scale(p_bullet, (20, 10)), 180), pygame.transform.rotate(pygame.transform.scale(p_bullet, (20, 10)), 270), pygame.transform.scale(p_bullet, (20, 10)))
    a_bullet = pygame.image.load("Bullets/Assault_bullet.png")
    a_bullet = (pygame.transform.rotate(pygame.transform.scale(a_bullet, (30, 10)), 90), pygame.transform.rotate(pygame.transform.scale(a_bullet, (30, 10)), 180), pygame.transform.rotate(pygame.transform.scale(a_bullet, (30, 10)), 270), pygame.transform.scale(a_bullet, (30, 10)))
    s_bullet = pygame.image.load("Bullets/Sniper_bullet.png")
    s_bullet = (pygame.transform.rotate(pygame.transform.scale(s_bullet, (50, 10)), 90), pygame.transform.rotate(pygame.transform.scale(s_bullet, (50, 10)), 180), pygame.transform.rotate(pygame.transform.scale(s_bullet, (50, 10)), 270), pygame.transform.scale(s_bullet, (50, 10)))

    cur.execute("SELECT W_type, Damage FROM Weapons;")
    bullet_damage = cur.fetchall()

    enemy1 = pygame.image.load(f"Enemies/{enemy_colour}/Enemy1.jpg")
    enemy2 = pygame.image.load(f"Enemies/{enemy_colour}/Enemy2.jpg")
    enemy3 = pygame.image.load(f"Enemies/{enemy_colour}/Enemy3.jpg")
    enemy = [pygame.transform.scale(enemy1, [100, 100]), pygame.transform.scale(enemy2, [100, 100]), pygame.transform.scale(enemy3, [100, 100])] # Red enemy images
    enemy_rect = [pygame.Rect([200, 10, 100, 100]), pygame.Rect([200, 200, 100, 100]), pygame.Rect([200, 400, 100, 100])] # add new pygame.Rect here for red enemies
    enemy_health = [200, 200, 200]
    bullet_coord = [] # coordinates of every bullet (can take inspiration of implementation to make enemy images move) -> [x_coord, y_coord, facing left/right, facing up/down, bullet image]
    bullet_coord_rect = [] # Bullet rectangles (superimposed with bullet images always) so that collision can be checked with enemy rectangle
    direction = 3  # used as p_dir arguement in check_dir, default facing right
    start = end = time.time() # start reload time, end - start = number of seconds left to reload (in seconds)
    enemy_spawn_start = enemy_spawn_end = time.time()
    true = True

    while true == True:
        screen.fill((0, 0, 0)) 
        screen.blit(game_map, (0,0))
        end = time.time()
        enemy_spawn_end = time.time()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                true = False
                pygame.quit()
            
        key = pygame.key.get_pressed()
        p_dir = check_dir(direction)
        if ((key[pygame.K_w] or key[pygame.K_UP]) and (player.y >= 0)):
            player.y -= 5
            direction = 0
        if ((key[pygame.K_a] or key[pygame.K_LEFT]) and (player.x >= 150)):
            player.x -= 5
            direction = 1
        if ((key[pygame.K_s] or key[pygame.K_DOWN]) and (player.y <= 650)):
            player.y += 5
            direction = 2
        if ((key[pygame.K_d] or key[pygame.K_RIGHT]) and (player.x <= 800)):
            player.x += 5
            direction = 3
        if (key[pygame.K_RETURN]):
            player.x = 475
            player.y = 325

        if (key[pygame.K_1] and (end - start >= 0.75)): # pistol bullet fired
            p_damage = 0
            for dam in bullet_damage:
                if dam[0] == "Pistol":
                    p_damage = dam[1]
            bullet_coord.append([player.x + 25, player.y + 25, p_dir[0], p_dir[1], p_bullet[direction], p_damage])
            bullet_coord_rect.append(pygame.Rect(player.x + 25, player.y + 25, 20, 10))
            shots_fired += 1
            start = end
        if (key[pygame.K_2] and (end - start >= 0.2)): # assault rifle bullet fired
            a_damage = 0
            for dam in bullet_damage:
                if dam[0] == "Assault Rifle":
                    a_damage = dam[1]
            bullet_coord.append([player.x + 25, player.y + 25, p_dir[0], p_dir[1], a_bullet[direction], a_damage])
            bullet_coord_rect.append(pygame.Rect(player.x + 25, player.y + 25, 30, 10))
            shots_fired += 1
            start = end
        if (key[pygame.K_3] and (end - start >= 2)): # sniper rifle bullet fired
            s_damage = 0
            for dam in bullet_damage:
                if dam[0] == "Sniper":
                    s_damage = dam[1]
            bullet_coord.append([player.x + 25, player.y + 25, p_dir[0], p_dir[1], s_bullet[direction], s_damage])
            bullet_coord_rect.append(pygame.Rect(player.x + 25, player.y + 25, 50, 10))
            shots_fired += 1
            start = end
        
        if (enemy_spawn_end - enemy_spawn_start >= 6):
            enemy.append(pygame.transform.scale([enemy1, enemy2, enemy3][random.randint(0, 2)], [100, 100]))
            enemy_rect.append(pygame.Rect([random.choice([10, 200]), random.choice([10, 200]), 100, 100]))
            enemy_health.append(200)
            enemy_spawn_start = enemy_spawn_end

        pygame.draw.ellipse(screen, (0, 125, 0), player)
        
        for enemy_i in enemy:
            enemy_rect_i = enemy_rect[enemy.index(enemy_i)] # Get the red enemy rectangle from enemy_red_rect
            screen.blit(enemy_i, (enemy_rect_i.x, enemy_rect_i.y)) # display the red enemy character

            if(abs(enemy_rect_i.x - player.x) >= abs(enemy_rect_i.y - player.y)):
                if(enemy_rect_i.x - player.x < 0):
                    enemy_rect_i.x += 3
                else:
                    enemy_rect_i.x -= 3
            else:
                if(enemy_rect_i.y - player.y < 0):
                    enemy_rect_i.y += 3
                else:
                    enemy_rect_i.y -= 3

            for bullet in bullet_coord:
                screen.blit(bullet[4], (bullet[0], bullet[1])) # bullet[4] = image, bullet[0] and bullet[1] are x_coord and y_coord respectively
                bullet_rect = bullet_coord_rect[bullet_coord.index(bullet)]

                if ((bullet[0] >= -50 and bullet[0] <= 1000) and (bullet[1] >= -50 and bullet[1] <= 700)):
                    bullet_coord[bullet_coord.index(bullet)][0] += bullet_coord[bullet_coord.index(bullet)][2] # Move bullet image horizontally
                    bullet_coord[bullet_coord.index(bullet)][1] += bullet_coord[bullet_coord.index(bullet)][3] # Move bullet image vertically
                    bullet_coord_rect[bullet_coord.index(bullet)].x += bullet_coord[bullet_coord.index(bullet)][2] # move bullet rectangle horizontally
                    bullet_coord_rect[bullet_coord.index(bullet)].y += bullet_coord[bullet_coord.index(bullet)][3] # move bullet rectangle vertically
                else:
                    bullet_coord.remove(bullet)
                    bullet_coord_rect.remove(bullet_rect)
            
                if (bullet_rect.colliderect(enemy_rect_i)): # bullet collide with enemy
                    bullet_coord_rect.remove(bullet_rect) # Remove bullet rectangle
                    bullet_coord.remove(bullet) # Remove bullet image
                    if enemy_health[enemy.index(enemy_i)] <= 0:
                        enemy_rect.remove(enemy_rect_i) # Remove red enemy rectangle
                        enemy_health.remove(enemy_health[enemy.index(enemy_i)])
                        enemy.remove(enemy_i) # remove red enemy image
                        kills += 1
                    else:
                        enemy_health[enemy.index(enemy_i)] -= bullet[5]
                    shots_hit += 1
            
            if(enemy_rect_i.colliderect(player)):
                if(player_health != 0):
                    player_health -= 10
                else:
                    true = False
                    game_over(screen, shots_fired, shots_hit, kills, player_name)
                    return
        
        PLAYER_NAME = SysFont("Calibri", 45).render(player_name, True, "White")
        screen.blit(PLAYER_NAME, (500, 720)) # display player name below the game screen
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)

def game_over(screen, shots_fired, shots_hit, kills, player_name):
    true = True
    achievement_message = ""
    accuracy = shots_hit/shots_fired if shots_fired > 0 else 0
    query = f"SELECT Username FROM player_statistics WHERE Username = '{player_name}';"
    cur.execute(query)
    results = cur.fetchall()
    if len(results) == 0:
        query = f"INSERT INTO player_statistics VALUES('{player_name}', {accuracy}, {kills}, 1);"
        cur.execute(query)
        conn.commit()
    else:
        query = f"UPDATE player_statistics SET Accuracy = {accuracy} WHERE Username = '{player_name}';"
        cur.execute(query)
        conn.commit()

        query = f"UPDATE player_statistics SET Kills = {kills} WHERE Username = '{player_name}';"
        cur.execute(query)
        conn.commit()
    
    if kills >= 50 and kills < 100:
        achievement_message = "Gold"
    elif kills >= 100 and kills < 150:
        achievement_message = "Platinum"
    else:
        achievement_message = "Diamond"
    
    query = f"SELECT Username FROM player_achievements WHERE Username = '{player_name}';"
    cur.execute(query)
    results = cur.fetchall()
    if len(results) == 0:
        query = f"INSERT INTO player_achievements VALUES('{player_name}', '{achievement_message}')"
        cur.execute(query)
        conn.commit()
    else:
        query = f"UPDATE player_achievements SET Achievements = '{achievement_message}' WHERE Username = '{player_name}'"
        cur.execute(query)
        conn.commit()
        
    while true == True:
        screen.fill((125, 0, 0))
        game_over_text = SysFont("Calibri", 70).render("Game Over", True, "White")
        accuracy_text = SysFont("Calibri", 50).render("Accuracy: {}".format(accuracy), True, "White")
        kills_text = SysFont("Calibri", 50).render("Kills: {}".format(kills), True, "White")
        kills_button = kills_text.get_rect(center = (500, 400))
        accuracy_button = accuracy_text.get_rect(center=(500, 200))
        game_over_button = game_over_text.get_rect(center=(500, 50))
        screen.blit(game_over_text, game_over_button)
        screen.blit(accuracy_text, accuracy_button)
        screen.blit(kills_text, kills_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                true = False
                return

        pygame.display.flip()
#gameplay()