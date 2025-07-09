from engine import *
from engine.controllers.ui import Button
from ..constants import *
from .. import resources

class MainMenu(Scene):
    def load(self, context: GameContext):
        self.img_bg = pygame.image.load(resources.images.MENU_BG)
        self.font = Font(resources.fonts.BEACH_BALL, 40)
        self.title_text = self.font.render(resources.locale.GAME_TITLE, True, "white")
        self.menu_theme = pygame.mixer.music
        self.button_sound_sel = pygame.mixer.Sound(resources.sounds.BUTTON_SEL)
        self.button_sound_pressed = pygame.mixer.Sound(resources.sounds.BUTTON_PRESSED)
        
    def start(self, context: GameContext):
        screen = context.get_screen()
        pygame.mixer.music.load(resources.music.MENU_THEME)
        pygame.mixer.music.play(-1)
        # Crear botones
        button_x = screen.get_width() // 4
        button_y = screen.get_height() // 2
        self.button_play = Button(
            context=context,
            pos=(button_x, button_y - 80),
            dim=(200,50),
            inactive_color=resources.colors.GREEN,
            active_color=resources.colors.BRIGHT_GREEN,
            text='Jugar',
            action=lambda: context.scene.change(SCENE_GAME_CONFIG),
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        self.button_registro = Button(
            context=context,
            pos=(button_x, button_y),
            dim=(200,50),
            inactive_color="white",
            active_color=resources.colors.BRIGHT_GREEN,
            text='Registrar equipo',
            action=lambda: context.scene.change(SCENE_CREATE_TEAM),
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        self.button_estadisticas = Button(
            context=context,
            pos=(button_x, button_y + 80),
            dim=(200,50),
            inactive_color="white",
            active_color=resources.colors.BRIGHT_GREEN,
            text='Estadisticas',
            action=lambda: context.scene.change(SCENE_STATS),
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        self.button_options = Button(
            context=context,
            pos=(button_x, button_y + 160),
            dim=(200, 70),
            inactive_color="white",
            active_color=resources.colors.BRIGHT_GREEN,
            text='OPCIONES',
            action=lambda: context.scene.change(SCENE_OPTIONS),
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        self.button_quit = Button(
            context=context,
            pos=(button_x, button_y + 240),
            dim=(200, 70),
            inactive_color=resources.colors.RED,
            active_color=resources.colors.BRIGHT_RED,
            text="QUIT",
            action=lambda: context.quit(),
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        
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
        screen.blit(self.title_text, (screen.get_width() // 2, screen.get_height() // 4))
        
        # Dibujar botones
        for button in self.buttons:
            button.draw(screen)
            
    def exit(self, context: GameContext):
        pygame.mixer.music.stop()
        pass
