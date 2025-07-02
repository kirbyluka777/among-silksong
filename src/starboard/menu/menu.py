import pygame as pg

# consts
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BOX_WIDTH = 140
BOX_HEIGHT = 32

class TitleScreen:
    pass


class OptionsScreen:
    pass

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pg.display.set_caption("AMONG SILKSONG")
        self.clock = pg.time.Clock()

        self.teams = [] # Que llame una funcion load que retorne la lista de equipos registrados
        
        self.title_screen = TitleScreen(self)
        self.registrer_screen = RegisterScreen(self)
        self.options_screen = OptionsScreen(self)

class InputBox:

    def __init__(self, pos:tuple, dim:tuple, head:str='', text:str='', action=None, id:int=0):
        self.rect = pg.Rect(pos[0],pos[1], dim[0],dim[1])
        self.action = action
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
                    if self.action:
                        self.action()
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
        screen.blit(self.head_surface, (self.rect.x, self.rect.y-50))
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

class RegisterScreen:
    def __init__(self):
        input_name = InputBox((100, 100), (BOX_WIDTH, BOX_HEIGHT), 'Nombre del equipo')
        input_email = InputBox((100,200), (BOX_WIDTH, BOX_HEIGHT))
        input_password = InputBox((100, 300), (BOX_WIDTH, BOX_HEIGHT))
        input_boxes = [input_name,
                    input_email,
                    input_password]
    
    def handle_events(self, event):
        mouse_pos = pg.mouse.get_pos()

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            pass



def main():
    clock = pg.time.Clock()
    input_name = InputBox((100, 100), (BOX_WIDTH, BOX_HEIGHT), 'Nombre del equipo')
    input_email = InputBox((100,200), (BOX_WIDTH, BOX_HEIGHT))
    input_password = InputBox((100, 300), (BOX_WIDTH, BOX_HEIGHT))
    input_boxes = [input_name,
                   input_email,
                   input_password]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()