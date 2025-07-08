from engine import *

ALPHA_MAX = 255
ScreenCoords = Vector2 | tuple[int]

class InterfaceController:
    def __init__(self, context: GameContext, target: Surface = None):
        self.context = context
        self.target = target

    def screen_coords_as_tuple(self, position: ScreenCoords):
        return position[0], position[1]

    def target_from(self, chosen_target: Surface = None):
        return chosen_target or self.target or self.context.get_screen()
    
    def position_from(self, position: ScreenCoords, target: Surface):
        return self.screen_coords_as_tuple(position or target.get_rect().center)

    # dibuja una superficie usando el sistema de anclas
    def draw_surface(
            self,
            source: Surface,
            position: ScreenCoords = None,
            anchor: Vector2 = anchors.center,
            special_flags: int = 0,
            target: Surface = None):
        target = self.target_from(target)
        position = self.position_from(position, target)
        source_rect = source.get_rect()
        anchor_offset_x = source_rect.width * anchor.x
        anchor_offset_y = source_rect.height * anchor.y
        target.blit(source, (position[0] - anchor_offset_x, position[1] - anchor_offset_y), special_flags=special_flags)

    # dibuja una superficie con un efecto de aparación progresiva
    def draw_fade_out(
            self,
            source: Surface,
            position: ScreenCoords = None,
            anchor: Vector2 = anchors.center,
            ticks: int = None,
            duration: int = 500,
            special_flags: int = 0,
            target: Surface = None):
        # establecer valores iniciales
        if ticks is None:
            ticks = game.get_current_ticks()

        # calcular transición y aplicarlo en la transparencia de la superficie
        alpha = interpolation_by_ticks(ALPHA_MAX, 0, ticks, duration)
        source.set_alpha(alpha)
        
        # dibujar en objetivo
        self.draw_surface(source, position, anchor, special_flags, target)

    # dibuja una superficie con un efecto de desaparación progresiva
    def draw_fade_in(
            self,
            source: Surface,
            position: ScreenCoords = None,
            anchor: Vector2 = anchors.center,
            ticks: int = None,
            duration: int = 500,
            special_flags: int = 0,
            target: Surface = None):
        # establecer valores iniciales
        if ticks is None:
            ticks = game.get_current_ticks()

        # calcular transición y aplicarlo en la transparencia de la superficie
        alpha = interpolation_by_ticks(0, ALPHA_MAX, ticks, duration)
        source.set_alpha(alpha)
        
        # dibujar en objetivo
        self.draw_surface(source, position, anchor, special_flags, target)

# calcula interpolación entre un inicio y fin dado los milisegundos
# transcurridos con respecto a una duración especifica
def interpolation_by_ticks(start: int, end: int, ticks: int, duration: int):
    if ticks > duration:
        return end
    return round(start + (end - start) * ticks / duration)