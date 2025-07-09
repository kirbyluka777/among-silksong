from engine import *

class Button:
    def __init__(
            self,
            context: GameContext,
            pos: tuple,
            dim: tuple,
            inactive_color: str,
            active_color: str,
            text: str = '',
            action = None,
            font: Font = None,
            sound_sel = None,
            sound_press = None,
            flag = None):
        """
        pos 0 = x
        pos 1 = y

        dim 0 = width
        dim 1 = height
        """
        self.context = context
        self.text = text
        self.rect = pygame.Rect(pos[0],pos[1],dim[0],dim[1])
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.current_color = inactive_color
        self.action = action
        self.font = font
        self.sound_sel = sound_sel
        self.sound_press = sound_press
        self.flag = flag

    def draw(self, screen: pygame.Surface):
        text_surf = self.font.render(self.text, True, self.current_color)
        text_rect = text_surf.get_rect(center=self.rect.center)

        screen.blit(text_surf, text_rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.active_color
            if self.flag:
                self.sound_sel.play()
                self.flag = False
            for event in self.context.get_events():
                if self.action and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.sound_press.play()
                    self.action()
        else:
            self.current_color = self.inactive_color
            self.flag = True