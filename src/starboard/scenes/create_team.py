from engine import *
from engine.controllers.ui import Button, InputBox, DropDown, InterfaceController
from ..constants import *
from .. import resources
from .. import globals
from ..logic import teams
from ..logic.teams import Team
from ..logic.teams import TEAM_FILE
from ..logic.records import increment_records_len

BOX_WIDTH = 140
BOX_HEIGHT = 32

class CreateTeam(Scene):
    def load(self, context: GameContext):
        self.toggle_xor = False
        self.img_bg = pygame.image.load(resources.images.MENU_BG)
        self.font = pygame.font.Font(resources.fonts.COINY, 24)
        self.button_sound_sel = pygame.mixer.Sound(resources.sounds.BUTTON_SEL)
        self.button_sound_pressed = pygame.mixer.Sound(resources.sounds.BUTTON_PRESSED)
        self.button_sound_pressed = pygame.mixer.Sound(resources.sounds.BUTTON_PRESSED)

        self.warnings = ["La contraseña debe tener entre 6 y 10 caracteres",
                         "La contraseña solo puede tener *,-,_,#.",
                         "La contraseña debe tener números",
                         "La contraseña debe tener letras minúsculas",
                         "La contraseña debe tener letras mayúsculas",
                         "La contraseña debe tener carácteres especiales",
                         "La contraseña posee 3 caracteres repetidos de manera secuencial"]
        self.warning_flags = [False for _ in range(7)]

        self.warnings_text = [self.font.render(self.warnings[0], True, '#ffffff'),
                              self.font.render(self.warnings[1], True, '#ffffff'),
                              self.font.render(self.warnings[2], True, '#ffffff'),
                              self.font.render(self.warnings[3], True, '#ffffff'),
                              self.font.render(self.warnings[4], True, '#ffffff'),
                              self.font.render(self.warnings[5], True, '#ffffff'),
                              self.font.render(self.warnings[6], True, '#ffffff')]
        
        self.text_not_registered_warning = self.font.render(resources.locale.NOT_REGISTERED_WARNING, True, "white")

    def start(self, context: GameContext):
        screen = context.get_screen()
        pygame.mixer.music.load(resources.music.REGISTER_THEME)
        pygame.mixer.music.play(-1)
        self.failed = False
        self.interface = InterfaceController(context)
        # Crear botones
        self.button_xor = Button(
            context,
            pos=(100,340), 
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='No encriptar',
            action=self.xor_toggle,
            font=self.font,
            sound_sel=self.button_sound_sel,
            sound_press=self.button_sound_pressed,
            flag=True)
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

        # crear lista
        self.sel_ods = None
        self.dropdown_ods = DropDown(context,
                                     ['#696969', '#ffffff'],
                                     ['#696969', '#ffffff'],
                                     400, 80,350,32,
                                     pygame.font.Font(resources.fonts.COINY, 18),
                                     'ODS',
                                     list(m for n,m in enumerate(globals.ods)))
        self.sel_country = None
        self.dropdown_country = DropDown(context,
                                     ['#696969', '#ffffff'],
                                     ['#696969', '#ffffff'],
                                     800,80,200,30,
                                     self.font,
                                     'Pais',
                                     list(c.name for c in globals.countries))

    def update(self, context: GameContext):
        for box in self.input_boxes:
            box.update()
        index = self.dropdown_ods.update()
        if index >= 0:
            self.sel_ods = index
            self.dropdown_ods.main = self.dropdown_ods.options[index]
        index = self.dropdown_country.update()
        if index >= 0:
            self.sel_country = globals.countries[index]
            self.dropdown_country.main = self.dropdown_country.options[index]
        self.button_back.update()
        self.button_registrar.update()
        self.verificacion()
        self.button_xor.update()
    
    def draw(self, context: GameContext):
        screen = context.get_screen()
        screen_rect = context.get_screen_rect()
        screen.fill("white")
        screen.blit(self.img_bg,(0,0))
        for box in self.input_boxes:
            box.draw(screen)
        self.button_xor.draw(screen)
        self.button_back.draw(screen)
        self.button_registrar.draw(screen)
        self.text_not_registered_warning
        for i,j in enumerate(self.warning_flags):
            if j:
                screen.blit(self.warnings_text[i], (100, 400 + 30*i))
        self.dropdown_ods.draw(screen)
        self.dropdown_country.draw(screen)
        if self.failed:
            self.interface.draw_surface(self.text_not_registered_warning, (screen_rect.centerx, screen_rect.bottom - 20))
            
    def exit(self, context: GameContext):
        pygame.mixer.music.stop()
        pass

    def xor_toggle(self):
        self.toggle_xor = not self.toggle_xor
        self.button_xor.text = 'Encriptar' if self.toggle_xor else 'No encriptar'
        print(self.toggle_xor)

    def verificacion(self):
        password = self.input_password.text
        
        self.warning_flags[0] = len(password) < 6 or len(password) > 10
        self.warning_flags[1] = not teams.allowed_chars(password, "*=_#")
        self.warning_flags[2] = not teams.contain_number(password)
        self.warning_flags[3] = not teams.contain_lowercase(password)
        self.warning_flags[4] = not teams.contain_uppercase(password)
        self.warning_flags[5] = not teams.contain_specials(password)
        self.warning_flags[6] = teams.repeat_3(password)

    def register_team(self):
        self.failed = False
        name = self.input_name.text
        email  = self.input_email.text
        password = self.input_password.text

        if name and email and password and self.sel_country and self.sel_ods is not None and not any(self.warning_flags):
            if self.toggle_xor:
                password = teams.XOR_Encrypt(password) # lo intentamos
                print(password)
            team_id = increment_records_len(TEAM_FILE)
            new_team = Team(team_id, name, email.strip(), password.strip(), self.sel_country.code.strip(), self.sel_ods)
            globals.teams.append(new_team)
            teams.save_record(new_team)
            print(f'registrado: {new_team.name}\n'
                  f'correo: {new_team.email}\n'
                  f'contrasena: {new_team.password}\n'
                  f'pais: {new_team.country_code, self.sel_country.name}')
            self.input_name.text = self.input_email.text = self.input_password.text = ''
            for box in self.input_boxes:
                box.txt_surface = pygame.font.SysFont(None, 32).render(box.text, True, box.color)
        else:
            self.failed = True
            print("No registrado")
