from engine import *
from engine.controllers.ui import Button, InputBox, Text
from ..constants import *
from .. import resources

BOX_WIDTH = 140
BOX_HEIGHT = 32

class BestStats(Scene):
    def load(self, context: GameContext):
        self.img_bg = pygame.image.load(resources.images.MENU_BG)
        self.font = pygame.font.Font(resources.fonts.BEACH_BALL, 40)
        self.button_sound_sel = pygame.mixer.Sound(resources.sounds.BUTTON_SEL)
        self.button_sound_pressed = pygame.mixer.Sound(resources.sounds.BUTTON_PRESSED)

    def start(self, context: GameContext):
        screen = context.get_screen()    
        pygame.mixer.music.play(-1)
        self.text = Text(
            context,
            text="Ingrese el codigo de un pais para ver su mejor recorrido",
            pos=(400,100),
            dim=(140,32),
            font=self.font)
        self.input_id = InputBox(
            context,
            pos=(100, 200),
            dim=(BOX_WIDTH, BOX_HEIGHT),
            head='Codigo de Pais',
            font=self.font)
        self.button_back = Button(
            context,
            pos=(100,screen.get_height() - 100),
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Back',
            action=lambda: context.scene.change(SCENE_STATS),
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        self.button_search = Button(
            context,
            pos=(250,200),
            dim=(100,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Buscar',
            action=self.id_input(),
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)

    def update(self, context: GameContext):
        self.input_id.update()
        self.button_back.update()
        self.button_search.update()
    
    def draw(self, context: GameContext):
        screen = context.get_screen()
        screen.fill("white")
        screen.blit(self.img_bg,(0,0))
        self.input_id.draw(screen)
        self.button_back.draw(screen)
        self.button_search.draw(screen)
        self.text.draw(screen)
            
    def exit(self, context: GameContext):
        pass

    def id_input(self):
        pass
