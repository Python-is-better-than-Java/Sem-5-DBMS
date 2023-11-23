import pygame
from pygame.font import SysFont
import webbrowser
import mysql.connector
from Game import gameplay
pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("PRAAJEQT")

# Create a connection object
conn_new = mysql.connector.connect(host="localhost", user="root", password="mysql", database="shootergame")
cursor_new = conn_new.cursor()

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        image = pygame.transform.scale(image, (500, 100))
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def login_page():
    player_name = ''
    password = ''
    pswd_prev_len = len(password)
    password_hash = ''
    enter_again = ''
    key = 0 # To change from entering username to entering password
    player_rect = pygame.Rect(200, 120, 600, 60)
    password_rect = pygame.Rect(200, 320, 600, 60)
    colour = pygame.Color("Purple")
    while True:
        login_mouse_pos = pygame.mouse.get_pos()
        screen.fill((125, 0, 0))

        PLAY_TEXT = SysFont("Calibri", 45).render("Enter username of the player", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(500, 50))
        screen.blit(PLAY_TEXT, PLAY_RECT)

        PASSWORD_TEXT = SysFont("Calibri", 45).render("Enter password", True, "White")
        PASSWORD_RECT = PASSWORD_TEXT.get_rect(center=(500, 250))
        screen.blit(PASSWORD_TEXT, PASSWORD_RECT)

        AGAIN_TEXT = SysFont("Calibri", 30).render(enter_again, True, "White")
        AGAIN_RECT = PLAY_TEXT.get_rect(center=(500, 700))
        screen.blit(AGAIN_TEXT, AGAIN_RECT)

        pygame.draw.rect(screen, colour, player_rect)
        text_player_name = SysFont("Calibri", 50).render(player_name, True, (255, 255, 255)) 
        screen.blit(text_player_name, (player_rect.x+5, player_rect.y+5))

        pygame.draw.rect(screen, colour, password_rect)
        text_password_hash = SysFont("Calibri", 50).render(password_hash, True, (255, 255, 255)) 
        screen.blit(text_password_hash, (password_rect.x+5, password_rect.y+5))

        START_BUTTON = Button(image=pygame.image.load("Rectangle.png"), pos=(500, 450), 
                            text_input="Start", font=SysFont("Calibri", 70), base_color="#d7fcd4", hovering_color="Green")
        START_BUTTON.changeColor(login_mouse_pos)
        START_BUTTON.update(screen)
        PLAY_BACK = Button(image=pygame.image.load("Rectangle.png"), pos=(500, 600), 
                           text_input="Back", font=SysFont("Calibri", 70), base_color="#d7fcd4", hovering_color="Green")
        PLAY_BACK.changeColor(login_mouse_pos)
        PLAY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
      
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(login_mouse_pos):
                    home_screen()
                if START_BUTTON.checkForInput(login_mouse_pos):
                    # check if user exists in the player_profile table
                    query = f"SELECT Username FROM player_profile WHERE Username = '{player_name}' AND Passkey = '{password}';"
                    cursor_new.execute(query)
                    results = cursor_new.fetchall()
                    if (len(results) > 0):
                        gameplay(screen, player_name)
                    else:
                        enter_again = "Incorrect username and/or password. Try Again."
                        key = 0 # Reset to entering username

                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if (key == 0):
                        player_name = player_name[:-1]
                    else:
                        password = password[:-1]
                        password_hash = password_hash[:-1]
                        pswd_prev_len = len(password)
                elif event.key == pygame.K_RETURN:
                    key = 1  # Username entered, now enter password
                else:
                    if (key == 0):
                        player_name += event.unicode # Unicode standard is used for string formation
                    else:
                        password += event.unicode
                        if (len(password) == pswd_prev_len + 1):
                            password_hash += '*'
                            pswd_prev_len = len(password)

        pygame.display.flip()

def home_screen():
    while True:
        screen.fill((125, 0, 0))

        home_mouse_pos = pygame.mouse.get_pos()

        home_text = SysFont("Calibri", 70).render("Start Game", True, "White")
        home_button = home_text.get_rect(center=(500, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Rectangle.png"), pos=(500, 250), 
                            text_input="Play", font=SysFont("Calibri", 70), base_color="#d7fcd4", hovering_color="Green")
        TABLE_BUTTON = Button(image=pygame.image.load("Rectangle.png"), pos=(500, 400), 
                            text_input="Display Tables", font=SysFont("Calibri", 70), base_color="#d7fcd4", hovering_color="Green")
        QUIT_BUTTON = Button(image=pygame.image.load("Rectangle.png"), pos=(500, 550), 
                            text_input="Quit", font=SysFont("Calibri", 70), base_color="#d7fcd4", hovering_color="Green")

        screen.blit(home_text, home_button)

        for button in [PLAY_BUTTON, TABLE_BUTTON, QUIT_BUTTON]:
            button.changeColor(home_mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(home_mouse_pos):
                    login_page()
                if TABLE_BUTTON.checkForInput(home_mouse_pos):
                    webbrowser.open("http://localhost:8501")
                if QUIT_BUTTON.checkForInput(home_mouse_pos):
                    pygame.quit()

        pygame.display.update()

home_screen()
