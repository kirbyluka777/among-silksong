from engine import *
from engine.controllers.ui import Button
from ..constants import *
from .. import resources

class MainMenu(Scene):
    def load(self, context: GameContext):
        self.img_bg = pygame.image.load(resources.images.MENU_BG)
        self.title = pygame.font.SysFont('Arial', 60).render(resources.locale.GAME_TITLE, True, "white")
        
    def start(self, context: GameContext):
        screen = context.get_screen()

        # Crear botones
        button_x = screen.get_width() // 4
        button_y = screen.get_height() // 2
        self.button_play = Button(
            context=context,
            pos=(button_x, button_y - 80),
            dim=(200,50),
            inactive_color=resources.colors.GREEN,
            active_color=resources.colors.BRIGHT_GREEN,
            text='Hola',
            action=lambda: context.scene.change(SCENE_GAME_CONFIG))
        self.button_registro = Button(
            context=context,
            pos=(button_x, button_y),
            dim=(200,50),
            inactive_color="white",
            active_color=resources.colors.BRIGHT_GREEN,
            text='Registrar equipo',
            action=lambda: context.scene.change(SCENE_CREATE_TEAM))
        self.button_estadisticas = Button(
            context=context,
            pos=(button_x, button_y + 80),
            dim=(200,50),
            inactive_color="white",
            active_color=resources.colors.BRIGHT_GREEN,
            text='Estadisticas',
            action=lambda: context.scene.change(SCENE_STATS))
        self.button_options = Button(
            context=context,
            pos=(button_x, button_y + 160),
            dim=(200, 70),
            inactive_color="white",
            active_color=resources.colors.BRIGHT_GREEN,
            text='OPCIONES',
            action=lambda: context.scene.change(SCENE_OPTIONS))
        self.button_quit = Button(
            context=context,
            pos=(button_x, button_y + 240),
            dim=(200, 70),
            inactive_color=resources.colors.RED,
            active_color=resources.colors.BRIGHT_RED,
            text="QUIT",
            action=lambda: context.quit())
        
        self.buttons = [
            self.button_play,
            self.button_registro,
            self.button_estadisticas,
            self.button_options,
            self.button_quit,
        ]

    def update(self, context: GameContext):
        # Actualizar lógica de botones
        for button in self.buttons:
            button.update()

    def draw(self, context: GameContext):
        screen = context.get_screen()

        # Dibujar fondo
        screen.fill("black")
        screen.blit(self.img_bg, (0, 0))
        screen.blit(self.title, (screen.get_width() // 2, screen.get_height() // 4))
        
        # Dibujar botones
        for button in self.buttons:
            button.draw(screen)
            
    def exit(self, context: GameContext):
        pass
