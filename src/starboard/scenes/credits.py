from engine import *
from engine.controllers.ui import InterfaceController
from ..constants import *
from .. import resources

ALPHA_MAX = 255

class Credits(Scene):
    def load(self, context: GameContext):
        self.font = pygame.font.Font(resources.fonts.COINY, 24)
        self.credits_text = [self.font.render(m, True, "white") for m in resources.locale.CREDITS]
        self.press_any_text = self.font.render("Presiona cualquier tecla para continuar...", True, "white")

    def start(self, context: GameContext):
        self.interface = InterfaceController(context)

        self.music_start_timer = TimerController(context)
        self.intro_timer = TimerController(context)
        self.intro_timer.start(50000)
        self.music_start_timer.start(500)

        pygame.mixer.music.stop()

    def update(self, context: GameContext):
        pass
    
    def draw(self, context: GameContext):
        screen_rect = context.get_screen_rect()

        if self.music_start_timer.has_finished:
            self.music_start_timer.reset()
            pygame.mixer.music.load(resources.music.CREDITS_THEME)
            pygame.mixer.music.play(0)
        
        ticks_offset = 2000
        for i in range(0, len(self.credits_text), +1):
            text = self.credits_text[i]
            card_ticks_offset = 4500 * i

            if self.intro_timer.ticks_elapsed > ticks_offset + card_ticks_offset and self.intro_timer.ticks_elapsed < ticks_offset + 500 + card_ticks_offset:
                self.interface.draw_fade_in(text, ticks=self.intro_timer.ticks_elapsed - (ticks_offset + card_ticks_offset), duration=500)

            if self.intro_timer.ticks_elapsed >= ticks_offset + 500 + card_ticks_offset and self.intro_timer.ticks_elapsed <= ticks_offset + 4000 + card_ticks_offset:
                text.set_alpha(255)
                self.interface.draw_surface(text)

            if self.intro_timer.ticks_elapsed > ticks_offset + 4000 + card_ticks_offset and self.intro_timer.ticks_elapsed < ticks_offset + 4500 + card_ticks_offset:
                self.interface.draw_fade_out(text, ticks=self.intro_timer.ticks_elapsed - (ticks_offset + 4000 + card_ticks_offset), duration=500)
        
        ticks_offset = ticks_offset + len(self.credits_text) * 4500

        if self.intro_timer.ticks_elapsed >= 2000 + 4500 * 7:
            if self.intro_timer.ticks_elapsed // 500 % 2 == 0:
                self.interface.draw_surface(self.press_any_text, (screen_rect.centerx, screen_rect.centery + 300))

        if self.intro_timer.ticks_elapsed >= ticks_offset + 1000 or context.is_any_key_down():
            context.scene.change(SCENE_INTRO)
            
    def exit(self, context: GameContext):
        pygame.mixer.music.stop()
