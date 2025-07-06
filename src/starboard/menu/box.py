import pygame as pg
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
BOX_WIDTH = 140
BOX_HEIGHT = 32
pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

class InputBox:

    def __init__(self, pos:tuple, dim:tuple, head:str='', text:str='', id:int=0):
        self.rect = pg.Rect(pos[0],pos[1], dim[0],dim[1])
        self.id = id
        self.color = COLOR_INACTIVE
        self.head = head
        self.text = text
        self.head_surface = FONT.render(head, True, '#ffffff')
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        mouse_pos = pg.mouse.get_pos()
        
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    pass
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.head_surface, (self.rect.x, self.rect.y-35))
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

class Text:
    def __init__(self,text:str,pos:tuple, dim:tuple):
        self.text = text
        self.rect = pg.Rect(pos[0],pos[1],dim[0],dim[1])
        self.font = pg.font.SysFont('Arial', 40)

    def draw(self, screen):
            
        text_surf = self.font.render(self.text, True, '#ffffff')
        text_rect = text_surf.get_rect(center=self.rect.center)

        screen.blit(text_surf, text_rect)

class Button:
    def __init__(self, pos:tuple, dim:tuple, inactive_color:str, active_color:str, text:str='', action=None):
        """
        pos 0 = x
        pos 1 = y

        dim 0 = width
        dim 1 = height
        """
        self.text = text
        self.rect = pg.Rect(pos[0],pos[1],dim[0],dim[1])
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.current_color = inactive_color
        self.action = action
        self.font = pg.font.SysFont('Arial', 40)

    def draw(self, screen):
            
        text_surf = self.font.render(self.text, True, self.current_color)
        text_rect = text_surf.get_rect(center=self.rect.center)

        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        mouse_pos = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.active_color
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.action:
                    self.action()
        else:
            self.current_color = self.inactive_color