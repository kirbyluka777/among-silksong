from engine import *
from engine.controllers.ui import Button, InputBox
from ..constants import *
from .. import resources
from .. import globals
from ..logic import teams
from ..logic.teams import Team

BOX_WIDTH = 140
BOX_HEIGHT = 32

class CreateTeam(Scene):
    def load(self, context: GameContext):
        self.img_bg = pygame.image.load(resources.images.MENU_BG)
        self.font = pygame.font.Font(resources.fonts.BEACH_BALL, 24)
        self.button_sound_sel = pygame.mixer.Sound(resources.sounds.BUTTON_SEL)
        self.button_sound_pressed = pygame.mixer.Sound(resources.sounds.BUTTON_PRESSED)

    def start(self, context: GameContext):
        screen = context.get_screen()
        pygame.mixer.music.load(resources.music.REGISTER_THEME)
        pygame.mixer.music.play(-1)
        # Crear botones
        self.button_back = Button(
            context,
            pos=(100,screen.get_height() - 100), 
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Back',
            action=lambda: context.scene.change(SCENE_MAIN_MENU),
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        self.button_registrar = Button(
            context,
            pos=(screen.get_width() // 2, screen.get_height() - 100),
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Registrar',
            action=self.register_team,
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
        
        # Crear cajas de entrada
        self.input_name = InputBox(
            context,
            pos=(100, 100), 
            dim=(BOX_WIDTH, BOX_HEIGHT), 
            head='Nombre del equipo',
            font=self.font)
        self.input_email = InputBox(
            context,
            pos=(100,200),
            dim=(BOX_WIDTH, BOX_HEIGHT),
            head='Correo electronico',
            font=self.font)
        self.input_password = InputBox(
            context,
            pos=(100, 300), 
            dim=(BOX_WIDTH, BOX_HEIGHT), 
            head='Clave de acceso',
            font=self.font)

        self.input_boxes = [
            self.input_name,
            self.input_email,
            self.input_password
        ]

    def update(self, context: GameContext):
        for box in self.input_boxes:
            box.update()
        self.button_back.update()
        self.button_registrar.update()
    
    def draw(self, context: GameContext):
        screen = context.get_screen()
        screen.fill("white")
        screen.blit(self.img_bg,(0,0))
        for box in self.input_boxes:
            box.draw(screen)
        self.button_back.draw(screen)
        self.button_registrar.draw(screen)
            
    def exit(self, context: GameContext):
        pygame.mixer.music.stop()
        pass

    def register_team(self):
        name = self.input_name.text
        email  = self.input_email.text
        password = self.input_password.text

        if name and email and password:
            password=teams.verification(password)
            new_team = Team(name,email,password)
            globals.teams.append(new_team)
            teams.save_record(new_team)
            print(f'registrado: {new_team.name}\n'
                  f'correo: {new_team.email}\n'
                  f'contrasena: {new_team.password}')
            self.input_name.text = self.input_email.text = self.input_password.text = ''
            for box in self.input_boxes:
                box.txt_surface = pygame.font.SysFont(None, 32).render(box.text, True, box.color)
        else:
            print("No registrado")
