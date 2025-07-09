from engine import *
from engine.controllers.ui import Button, InputBox, Text, InterfaceController
from ..constants import *
from .. import resources
from ..logic import countries
from ..logic import teams
from ..logic import expeditions
from ..logic import details

BOX_WIDTH = 140
BOX_HEIGHT = 32

class BestStats(Scene):
    def load(self, context: GameContext):
        self.img_bg = pygame.image.load(resources.images.MENU_BG)
        self.font = pygame.font.Font(resources.fonts.BEACH_BALL, 24)
        self.not_found_text = self.font.render("País no encontrado", True, "white")
        self.no_data_text = self.font.render("No hay datos para este país", True, "white")

    def start(self, context: GameContext):
        screen = context.get_screen()
        self.interface = InterfaceController(context)
        self.search_tried = False
        self.show_data = False
        self.report_text = None
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
            font=self.font)
        self.button_search = Button(
            context,
            pos=(1000,200),
            dim=(100,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Buscar',
            action=lambda: self.search(self.input_id.text),
            font=self.font)

    def update(self, context: GameContext):
        self.input_id.update()
        self.button_back.update()
        self.button_search.update()
    
    def draw(self, context: GameContext):
        screen = context.get_screen()
        screen_rect = context.get_screen_rect()
        screen.fill("white")
        screen.blit(self.img_bg,(0,0))
        self.input_id.draw(screen)
        self.button_back.draw(screen)
        self.button_search.draw(screen)
        self.text.draw(screen)
        if self.search_tried and not self.report_text:
            self.interface.draw_surface(self.not_found_text)
        elif self.report_text is not None and len(self.report_text) == 0:
            self.interface.draw_surface(self.no_data_text)
        elif self.report_text:
            for i in range(0, len(self.report_text), +1):
                self.interface.draw_surface(self.report_text[i], (screen_rect.centerx - 500, screen_rect.centery - 100 + 30 * i), anchor=anchors.leftmiddle)
            
    def exit(self, context: GameContext):
        pass

    def search(self, code: str):
        self.search_tried = False

        if not code:
            self.report_text = None
            return

        country = countries.search_country_by_code(code)

        if not country:
            self.report_text = None
            self.search_tried = True
            return

        report = ""
        for team in teams.load_records():
            if team.country_code == country.code:
                longest = 0
                expedition_detail = None
                for expedition in expeditions.read_expeditions():
                    player_turn = None
                    if expedition.team_name_1 == team.name:
                        player_turn = 0
                    elif expedition.team_name_2 == team.name:
                        player_turn = 1
                    if player_turn is not None:
                        km = details.get_total_km_from_expedition(expedition.id, 0)
                        current_detail = get_expedition_detail_as_str(expedition)
                        if km > longest:
                            longest = km
                            expedition_detail = current_detail
                if longest:
                    longest_str = f"{longest} km"
                    report += f"{team.name:<20} | {longest_str:>12} | {expedition_detail}\n"

        self.report_text = [self.font.render(line, True, "white") for line in report.split("\n")] if report else []

def get_expedition_detail_as_str(expedition: expeditions.Expedition):
    dir = "Horario" if expedition.board_dir == BOARD_DIR_OCLOCK else "Antihorario"
    diff = get_difficulty_by_id(expedition.difficulty)
    return f"{expedition.id:>8} | {expedition.date:<8} | {dir:<12} | {diff:<8} | {expedition.board_size:>2}"

def get_difficulty_by_id(id: int):
    if id == BOARD_DIFFICULTY_EASY:
        return "Fácil"
    elif id == BOARD_DIFFICULTY_MEDIUM:
        return "Media"
    else:
        return "Díficil"
