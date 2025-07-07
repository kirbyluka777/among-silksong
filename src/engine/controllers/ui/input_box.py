from engine import *

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

class InputBox:
    def __init__(
            self, 
            context: GameContext, 
            pos: tuple, 
            dim: tuple, 
            head: str = '', 
            text: str = '', 
            id: int = 0,
            font: Font = None):
        self.context = context
        self.rect = pygame.Rect(pos[0],pos[1], dim[0],dim[1])
        self.id = id
        self.color = COLOR_INACTIVE
        self.head = head
        self.text = text
        self.font = font
        self.head_surface = self.font.render(head, True, '#ffffff')
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in self.context.get_events():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(mouse_pos):
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            if self.active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pass
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    self.txt_surface = self.font.render(self.text, True, self.color)
        
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Dibujar el texto
        screen.blit(self.head_surface, (self.rect.x, self.rect.y-35))
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Dibujar bordes
        pygame.draw.rect(screen, self.color, self.rect, 2)