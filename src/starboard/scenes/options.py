from engine import *
from engine.controllers.ui import Button, InputBox, InterfaceController
from ..constants import *
from .. import resources
from .. import globals
from ..logic import countries
from ..logic.countries import Country

BOX_WIDTH = 140
BOX_HEIGHT = 32

class Options(Scene):
    def load(self, context: GameContext):
        self.img_bg = pygame.image.load(resources.images.MENU_BG)
        self.font = pygame.font.Font(resources.fonts.COINY, 24)
        self.button_sound_sel = pygame.mixer.Sound(resources.sounds.BUTTON_SEL)
        self.button_sound_pressed = pygame.mixer.Sound(resources.sounds.BUTTON_PRESSED)
        self.text_not_registered_warning = self.font.render(resources.locale.NOT_REGISTERED_WARNING, True, "white")

    def start(self, context: GameContext):
        screen = context.get_screen()
        pygame.mixer.music.load(resources.music.OPTIONS_THEME)
        pygame.mixer.music.play(-1)
        self.interface = InterfaceController(context)
        self.pais = False
        self.failed = False
        
        # Crear botones
        self.button_volume = Button(
            context=context,
            pos=(screen.get_width()//2,200),
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Volumen',
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        self.button_registrar = Button(
            context=context,
            pos=(screen.get_width()//2,250),
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Registrar país',
            action=self.toggle_countries,
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        self.button_done = Button(
            context=context,
            pos=(screen.get_width() // 2 + 200,350), 
            dim=(140,32), 
            inactive_color="white", 
            active_color=resources.colors.RED, 
            text='Listo', 
            action=self.register_country,
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        self.button_back = Button(
            context=context,
            pos=(100,screen.get_height() - 100),
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Atras',
            action=lambda: context.scene.change(SCENE_MAIN_MENU),
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        
        # Crear cajas de entrada
        self.input_code = InputBox(
            context=context,
            pos=(screen.get_width() // 2 - 200,350),
            dim=(BOX_WIDTH, BOX_HEIGHT),
            head='Código',
            font=self.font)
        self.input_name = InputBox(
            context=context,
            pos=(screen.get_width() // 2, 350),
            dim=(BOX_WIDTH, BOX_HEIGHT),
            head='Nombre',
            font=self.font)

        self.buttons =[
            self.button_volume,
            self.button_registrar,
            self.button_back,
        ]

        self.input_boxes = [
            self.input_code,
            self.input_name,
        ]

    def update(self, context: GameContext):
        for box in self.input_boxes:
            box.update()
        for button in self.buttons:
            button.update()
        if self.pais:
            self.button_done.update()
    
    def draw(self, context: GameContext):
        screen = context.get_screen()
        screen_rect = context.get_screen_rect()
        screen.fill("white")
        screen.blit(self.img_bg,(0,0))
        for button in self.buttons:
            button.draw(screen)
        if self.pais:
            for box in self.input_boxes:
                box.draw(screen)
            self.button_done.draw(screen)
        if self.failed:
            self.interface.draw_surface(self.text_not_registered_warning, (screen_rect.centerx, screen_rect.bottom - 20))
            
    def exit(self, context: GameContext):
        pygame.mixer.music.stop()
        pass
    
    def toggle_countries(self):
        self.pais = False if self.pais else True
    
    def register_country(self):
        self.failed = False
        code = self.input_code.text
        name = self.input_name.text

        if code and name:
            new_country = Country(code, name)
            globals.countries.append(new_country)
            countries.save_record(new_country)
            print(f'registrado: {new_country.name}\n'
                f'codigo: {new_country.code}')
            self.input_code.reset()
            self.input_name.reset()
            self.toggle_countries()
        else:
            self.failed = True
            print("No registrado")
