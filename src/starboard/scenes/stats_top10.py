from engine import *
from engine.controllers.ui import Button, InputBox, Text, InterfaceController
from ..constants import *
from .. import resources
from ..logic.search_c import search_c

BOX_WIDTH = 140
BOX_HEIGHT = 32

class Top10Stats(Scene):
    def load(self, context: GameContext):
        self.img_bg = pygame.image.load(resources.images.MENU_BG)
        self.font = pygame.font.Font(resources.fonts.COINY, 24)
        self.button_sound_sel = pygame.mixer.Sound(resources.sounds.BUTTON_SEL)
        self.button_sound_pressed = pygame.mixer.Sound(resources.sounds.BUTTON_PRESSED)
        self.success_text = self.font.render(resources.locale.REPORT_SUCCESS_MSG, True, "white")

    def start(self, context: GameContext):
        screen = context.get_screen()
        pygame.mixer.music.play(-1)
        self.interface = InterfaceController(context)
        self.success = False
        self.text = Text(
            context,
            text="Genere el reporte del TOP 10 de expediciones",
            pos=(400,100),
            dim=(140,32),
            font=self.font)
        self.button_back = Button(
            context,
            pos=(100,screen.get_height() - 100),
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Atras',
            action=lambda: context.scene.change(SCENE_STATS),
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        self.button_search = Button(
            context,
            pos=(100,200),
            dim=(100,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Generar Reporte',
            action=self.id_input,
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)

    def update(self, context: GameContext):
        self.button_back.update()
        self.button_search.update()
    
    def draw(self, context: GameContext):
        screen = context.get_screen()
        screen.fill("white")
        screen.blit(self.img_bg,(0,0))
        self.button_back.draw(screen)
        self.button_search.draw(screen)
        self.text.draw(screen)
        if self.success:
            self.interface.draw_surface(self.success_text)
            
    def exit(self, context: GameContext):
        pygame.mixer.music.stop()
        pass

    def id_input(self):
        self.success = search_c()