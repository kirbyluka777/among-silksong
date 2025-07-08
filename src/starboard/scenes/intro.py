from engine import *
from engine.controllers.ui import InterfaceController
from ..constants import *
from .. import resources

ALPHA_MAX = 255

class Intro(Scene):
    def load(self, context: GameContext):
        screen_rect = context.get_screen_rect()

        self.img_white_fill = pygame.Surface(screen_rect.size, pygame.SRCALPHA)
        self.img_white_fill.fill("white")
        self.img_black_fill = pygame.Surface(screen_rect.size, pygame.SRCALPHA)
        self.img_black_fill.fill("black")
      
        self.img_ucab = pygame.image.load(resources.images.UCAB_LOGO)
        self.img_ucab = pygame.transform.scale(self.img_ucab, (screen_rect.width, screen_rect.width * self.img_ucab.get_height() // self.img_ucab.get_width()))
        self.img_pygame = pygame.image.load(resources.images.PYGAME_LOGO)
        self.img_pygame = pygame.transform.scale(self.img_pygame, (screen_rect.width, screen_rect.width * self.img_pygame.get_height() // self.img_pygame.get_width()))

    def start(self, context: GameContext):
        screen = context.get_screen()

        self.interface = InterfaceController(context)

        self.intro_timer = TimerController(context)
        self.intro_timer.start(50000)

        pygame.mixer.music.load(resources.music.INTRO_THEME)
        pygame.mixer.music.play(-1)

    def update(self, context: GameContext):
        pass
    
    def draw(self, context: GameContext):
        if self.intro_timer.ticks_elapsed > 2900 and self.intro_timer.ticks_elapsed < 3400:
            self.interface.draw_fade_in(self.img_ucab, ticks=self.intro_timer.ticks_elapsed - 2900, duration=500)

        if self.intro_timer.ticks_elapsed > 3400 and self.intro_timer.ticks_elapsed < 7100:
            self.img_ucab.set_alpha(255)
            self.interface.draw_surface(self.img_ucab)

        if self.intro_timer.ticks_elapsed > 7100 and self.intro_timer.ticks_elapsed < 7600:
            self.interface.draw_fade_out(self.img_ucab, ticks=self.intro_timer.ticks_elapsed - 7100, duration=500)

        if self.intro_timer.ticks_elapsed > 8400 and self.intro_timer.ticks_elapsed < 8900:
            self.interface.draw_fade_in(self.img_pygame, ticks=self.intro_timer.ticks_elapsed - 8400, duration=500)

        if self.intro_timer.ticks_elapsed > 8900 and self.intro_timer.ticks_elapsed < 12600:
            self.img_pygame.set_alpha(255)
            self.interface.draw_surface(self.img_pygame)

        if self.intro_timer.ticks_elapsed > 12600 and self.intro_timer.ticks_elapsed < 13100:
            self.interface.draw_fade_out(self.img_pygame, ticks=self.intro_timer.ticks_elapsed - 12600, duration=500)
        
        if context.is_any_key_down():
            context.scene.change(SCENE_MAIN_MENU)
            
    def exit(self, context: GameContext):
        pygame.mixer.music.stop()
