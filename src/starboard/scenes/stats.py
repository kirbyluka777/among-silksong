from engine import *
from engine.controllers.ui import Button, InputBox, Text
from ..constants import *
from .. import resources
from .. import globals
from ..logic import countries
from ..logic.countries import Country

BOX_WIDTH = 140
BOX_HEIGHT = 32

class Stats(Scene):
    def load(self, context: GameContext):
        self.img_bg = pygame.image.load(resources.images.MENU_BG)
        self.font = pygame.font.Font(resources.fonts.BEACH_BALL, 40)

    def start(self, context: GameContext):
        screen = context.get_screen()

        self.text = Text(
            context,
            text="Seleccione la opcion que desee ver",
            pos=(400,100),
            dim=(140,32),
            font=self.font)
        self.button_best_exp = Button(
            context,
            pos=(200,screen.get_height() - 500),
            dim=(140,70),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Mejor expedicion de un pais',
            action=lambda: context.scene.change(SCENE_STATS_BEST),
            font=self.font)
        self.button_team_exp = Button(
            context,
            pos=(200,screen.get_height() - 400),
            dim=(140,70),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Expediciones de un equipo',
            action=lambda: context.scene.change(SCENE_STATS_TEAM),
            font=self.font)
        self.button_top10_exp = Button(
            context,
            pos=(160,screen.get_height() - 300),
            dim=(140,60),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Top 10 expediciones',
            action=lambda: context.scene.change(SCENE_STATS_TOP10),
            font=self.font)
        self.button_back = Button(
            context,
            pos=(100,screen.get_height() - 100),
            dim=(140,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Back',
            action=lambda: context.scene.change(SCENE_MAIN_MENU),
            font=self.font)

    def update(self, context: GameContext):
        self.button_back.update()
        self.button_best_exp.update()
        self.button_team_exp.update()
        self.button_top10_exp.update()
    
    def draw(self, context: GameContext):
        screen = context.get_screen()
        screen.fill("white")
        screen.blit(self.img_bg,(0,0))
        self.button_best_exp.draw(screen)
        self.button_team_exp.draw(screen)
        self.button_top10_exp.draw(screen)
        self.button_back.draw(screen)
        self.text.draw(screen)
            
    def exit(self, context: GameContext):
        pass
