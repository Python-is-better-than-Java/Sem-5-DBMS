import pygame
from pygame.font import SysFont
from Game import gameplay
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("PRAAJEQT")

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
                #sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(home_mouse_pos):
                    gameplay(screen)
                if TABLE_BUTTON.checkForInput(home_mouse_pos):
                    #options()
                    pass
                if QUIT_BUTTON.checkForInput(home_mouse_pos):
                    pygame.quit()
                    #sys.exit()

        pygame.display.update()

home_screen()