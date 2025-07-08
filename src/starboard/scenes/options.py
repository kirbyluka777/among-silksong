from engine import *
from engine.controllers.ui import Button, InputBox
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
        self.font = pygame.font.Font(resources.fonts.BEACH_BALL, 40)

    def start(self, context: GameContext):
        screen = context.get_screen()

        self.pais = False
        
        # Crear botones
        self.button_volume = Button(
            context=context,
            pos=(screen.get_width()//2,200),
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Volumen',
            font=self.font)
        self.button_registrar = Button(
            context=context,
            pos=(screen.get_width()//2,250),
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Registrar pais',
            action=self.toggle_countries,
            font=self.font)
        self.button_done = Button(
            context=context,
            pos=(screen.get_width() // 2 + 200,350), 
            dim=(140,32), 
            inactive_color="white", 
            active_color=resources.colors.RED, 
            text='Listo', 
            action=self.register_country,
            font=self.font)
        self.button_back = Button(
            context=context,
            pos=(100,screen.get_height() - 100),
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Back',
            action=lambda: context.scene.change(SCENE_MAIN_MENU),
            font=self.font)
        
        # Crear cajas de entrada
        self.input_code = InputBox(
            context=context,
            pos=(screen.get_width() // 2 - 200,350),
            dim=(BOX_WIDTH, BOX_HEIGHT),
            head='Codigo',
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
        screen.fill("white")
        screen.blit(self.img_bg,(0,0))
        for button in self.buttons:
            button.draw(screen)
        if self.pais:
            for box in self.input_boxes:
                box.draw(screen)
            self.button_done.draw(screen)
            
    def exit(self, context: GameContext):
        pass
    
    def toggle_countries(self):
        self.pais = False if self.pais else True
    
    def register_country(self):
        code  = self.input_code.text
        name = self.input_name.text

        if code and name:
            # countries=country.read_countries()
            # if (code in countries) or (name in countries):
            #     print("Pais ya existente")
            # else:
            new_country = Country(code, name)
            globals.countries.append(new_country)
            countries.save_record(new_country)
            print(f'registrado: {new_country.name}\n'
                f'codigo: {new_country.code}')
        else:
            print("No registrado")
        self.toggle_countries()
