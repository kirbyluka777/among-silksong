from engine import *
from engine.controllers.ui import Button, InputBox, Text
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
        self.font = pygame.font.Font(resources.fonts.BEACH_BALL, 40)

    def start(self, context: GameContext):
        screen = context.get_screen()
        self.not_found = False
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
            pos=(250,200),
            dim=(100,32),
            inactive_color="white",
            active_color=resources.colors.RED,
            text='Buscar',
            action=self.search(self.input_id.text),
            font=self.font)

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

    def search(self, code: str):
        country = countries.search_country_by_code(code)

        if not country:
            self.show_data = False
            self.not_found = True
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
                longest_str = f"{longest} km"
                report += f"{team.name:<20} | {longest_str:>12} | {expedition_detail}\n"

        print(report)

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
