from engine import *
from engine.controllers.ui import InterfaceController
from ..constants import *
from .. import resources
from ..logic import teams

ALPHA_MAX = 255

class Intro(Scene):
    def load(self, context: GameContext):
        screen_rect = context.get_screen_rect()

        self.font_big = pygame.font.Font(resources.fonts.COINY, 48)
        self.font = pygame.font.Font(resources.fonts.COINY, 24)
      
        self.img_ucab = pygame.image.load(resources.images.UCAB_LOGO)
        self.img_ucab = pygame.transform.scale(self.img_ucab, (screen_rect.width, screen_rect.width * self.img_ucab.get_height() // self.img_ucab.get_width()))
        self.img_pygame = pygame.image.load(resources.images.PYGAME_LOGO)
        self.img_pygame = pygame.transform.scale(self.img_pygame, (screen_rect.width, screen_rect.width * self.img_pygame.get_height() // self.img_pygame.get_width()))

        self.cards_text = [[self.font.render(m, True, "white") for m in card.split("\n")] for card in resources.locale.INTRO_MSG]
        self.cards = [self.draw_card(screen_rect, texts) for texts in self.cards_text]

        self.title_text = self.font_big.render(resources.locale.GAME_TITLE, True, "white")
        self.cosmic_learn_text = self.font.render("Por Cosmic Learn", True, "white")
        self.press_any_text = self.font.render("Presiona cualquier tecla para empezar...", True, "white")

        self.teams = teams.load_records()

    def start(self, context: GameContext):
        screen = context.get_screen()

        self.interface = InterfaceController(context)

        self.music_start_timer = TimerController(context)
        self.intro_timer = TimerController(context)
        self.intro_timer.start(50000)
        self.music_start_timer.start(1500)

        pygame.mixer.music.stop()

    def update(self, context: GameContext):
        pass
    
    def draw(self, context: GameContext):
        screen_rect = context.get_screen_rect()

        if self.music_start_timer.has_finished:
            self.music_start_timer.reset()
            pygame.mixer.music.load(resources.music.INTRO_THEME)
            pygame.mixer.music.play(-1)

        if self.intro_timer.ticks_elapsed > 1000 and self.intro_timer.ticks_elapsed < 1500:
            self.interface.draw_fade_in(self.img_ucab, ticks=self.intro_timer.ticks_elapsed - 1000, duration=500)

        if self.intro_timer.ticks_elapsed >= 1500 and self.intro_timer.ticks_elapsed <= 5000:
            self.img_ucab.set_alpha(255)
            self.interface.draw_surface(self.img_ucab)

        if self.intro_timer.ticks_elapsed > 5000 and self.intro_timer.ticks_elapsed < 5500:
            self.interface.draw_fade_out(self.img_ucab, ticks=self.intro_timer.ticks_elapsed - 5000, duration=500)

        if self.intro_timer.ticks_elapsed > 6500 and self.intro_timer.ticks_elapsed < 7000:
            self.interface.draw_fade_in(self.img_pygame, ticks=self.intro_timer.ticks_elapsed - 6500, duration=500)

        if self.intro_timer.ticks_elapsed >= 7000 and self.intro_timer.ticks_elapsed <= 10500:
            self.img_pygame.set_alpha(255)
            self.interface.draw_surface(self.img_pygame)

        if self.intro_timer.ticks_elapsed > 10500 and self.intro_timer.ticks_elapsed < 11000:
            self.interface.draw_fade_out(self.img_pygame, ticks=self.intro_timer.ticks_elapsed - 10500, duration=500)
        
        ticks_offset = 12000
        for i in range(0, len(self.cards), +1):
            card = self.cards[i]
            card_ticks_offset = 4500 * i

            if self.intro_timer.ticks_elapsed > ticks_offset + card_ticks_offset and self.intro_timer.ticks_elapsed < ticks_offset + 500 + card_ticks_offset:
                self.interface.draw_fade_in(card, ticks=self.intro_timer.ticks_elapsed - (ticks_offset + card_ticks_offset), duration=500)

            if self.intro_timer.ticks_elapsed >= ticks_offset + 500 + card_ticks_offset and self.intro_timer.ticks_elapsed <= ticks_offset + 4000 + card_ticks_offset:
                card.set_alpha(255)
                self.interface.draw_surface(card)

            if self.intro_timer.ticks_elapsed > ticks_offset + 4000 + card_ticks_offset and self.intro_timer.ticks_elapsed < ticks_offset + 4500 + card_ticks_offset:
                self.interface.draw_fade_out(card, ticks=self.intro_timer.ticks_elapsed - (ticks_offset + 4000 + card_ticks_offset), duration=500)
        
        ticks_offset = ticks_offset + len(self.cards) * 4500

        if self.intro_timer.ticks_elapsed > ticks_offset and self.intro_timer.ticks_elapsed < ticks_offset + 500:
            self.interface.draw_fade_in(self.title_text, ticks=self.intro_timer.ticks_elapsed - ticks_offset, duration=500)
            self.interface.draw_fade_in(self.cosmic_learn_text, (screen_rect.centerx, screen_rect.centery + 100), ticks=self.intro_timer.ticks_elapsed - ticks_offset, duration=500)

        if self.intro_timer.ticks_elapsed >= ticks_offset + 500:
            self.img_pygame.set_alpha(255)
            self.interface.draw_surface(self.title_text)
            self.interface.draw_surface(self.cosmic_learn_text, (screen_rect.centerx, screen_rect.centery + 100))

        if self.intro_timer.ticks_elapsed >= ticks_offset + 1500:
            if self.intro_timer.ticks_elapsed // 500 % 2 == 0:
                self.interface.draw_surface(self.press_any_text, (screen_rect.centerx, screen_rect.centery + 300))

        if context.is_any_key_down():
            if len(self.teams) < 2:
                context.scene.change(SCENE_CREATE_TEAM)
            else:
                context.scene.change(SCENE_MAIN_MENU)
            
    def exit(self, context: GameContext):
        pygame.mixer.music.stop()
    
    def draw_card(self, screen_rect: Rect, texts: list[Surface]):
        card = Surface(screen_rect.size, pygame.SRCALPHA)
        first_height = texts[0].get_height()
        total_height = first_height * len(texts)
        for i in range(0, len(texts), +1):
            card.blit(texts[i], (card.get_width() // 2 - texts[i].get_width() // 2, card.get_height() // 2 - total_height // 2 + i * first_height))
        return card
