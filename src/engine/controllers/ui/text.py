from engine import *

class Text:
    def __init__(
            self,
            context: GameContext,
            text: str,
            pos: tuple,
            dim: tuple,
            font: Font):
        self.context = context
        self.text = text
        self.rect = pygame.Rect(pos[0], pos[1], dim[0], dim[1])
        self.font = font

    def draw(self, screen: pygame.Surface):
        text_surf = self.font.render(self.text, True, '#ffffff')
        text_rect = text_surf.get_rect(center=self.rect.center)

        screen.blit(text_surf, text_rect)