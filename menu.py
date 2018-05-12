from pygame.event import Event
from settings import *
from eventtypes import *
from menuitem import MenuItem

# parent menus
MENU_TOP = "TOP_MENU"
MENU_DIFFICULTY = "DIFFICULTY_MENU"
MENU_LEVEL_SELECT = "LEVEL_SELECT_MENU"

# menu items
# top menu
ITEM_NEW_GAME = "NEW_GAME"
ITEM_LEVEL_SELECT = "LEVEL_SELECT"
ITEM_OPTIONS = "OPTIONS"
ITEM_EXIT = "EXIT"

# difficulty
ITEM_EASY = "EASY"
ITEM_MEDIUM = "MEDIUM"
ITEM_HARD = "HARD"

# levels
ITEM_LEVEL_1 = "LEVEL_1"
ITEM_LEVEL_2 = "LEVEL_2"
ITEM_BONUS_LEVEL = "BONUS_LEVEL"

top_menu = [
    MenuItem("New Game", ITEM_NEW_GAME),
    MenuItem("Level Select", ITEM_LEVEL_SELECT),
    MenuItem("Options", ITEM_OPTIONS),
    MenuItem("Exit", ITEM_EXIT)
]

difficulty_menu = [
    MenuItem("Easy", ITEM_EASY),
    MenuItem("Medium", ITEM_MEDIUM),
    MenuItem("Hard", ITEM_HARD)
]

level_select_menu = [
    MenuItem("Level 1", ITEM_LEVEL_1),
    MenuItem("Level 2", ITEM_LEVEL_2),
    MenuItem("Bonus Level", ITEM_BONUS_LEVEL)
]

class Menu:
    def __init__(self,
                 screen,
                 clock,
                 bg_color=(252, 179, 53),
                 font='helsinki.ttf',
                 font_size=60,
                 font_color=(0, 0, 0),
                 disabled_color=(100, 100, 100)):

        self._screen_width, self._screen_height = (WIDTH, HEIGHT)
        self.screen = screen
        self.clock = clock
        self._disabled_color = disabled_color
        self._font_color = font_color
        self.bg_color = bg_color
        self.font_size = font_size
        self.font = pygame.font.Font(font, font_size)
        self._items = []
        self._cur_menu = MENU_TOP

        self._menus = {
            MENU_TOP: self._render_items(top_menu),
            MENU_DIFFICULTY: self._render_items(difficulty_menu),
            MENU_LEVEL_SELECT: self._render_items(level_select_menu)
        }

    def _render_items(self, menu_items):
        items = []

        for index, menu_item in enumerate(menu_items):
            label_surface = menu_item.surface()
            (label_w, label_h) = label_surface.get_size()

            posx = (self._screen_width / 2) - (label_w / 2)
            total_height = len(menu_items) * label_h
            posy = (self._screen_height / 2 - total_height / 2) + (index * label_h)
            items.append([label_surface, (posx, posy), menu_item])

        return items

    def _render_header(self, screen):
        pass

    def _render(self):
        self.screen.fill(self.bg_color)

        for label_surface, (posx, posy), _ in self._menus[self._cur_menu]:
            self.screen.blit(label_surface, (posx, posy))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_click()
        if event.type == MENU_CLICK_EVENT:
            self.handle_menu_click(event.menu_item)

    def handle_menu_click(self, menu_item):
        if menu_item.item_id == ITEM_NEW_GAME:
            self._cur_menu = MENU_DIFFICULTY
        elif menu_item.item_id == ITEM_LEVEL_SELECT:
            self._cur_menu = MENU_LEVEL_SELECT
        elif (menu_item.item_id == ITEM_EASY or
              menu_item.item_id == ITEM_HARD or
              menu_item.item_id == ITEM_MEDIUM):
            pygame.event.post(Event(START_LEVEL1_EVENT, dict()))
        elif menu_item.item_id == ITEM_LEVEL_1:
            pygame.event.post(Event(START_LEVEL1_EVENT, dict()))
        elif menu_item.item_id == ITEM_LEVEL_2:
            pygame.event.post(Event(START_LEVEL2_EVENT, dict()))
        elif menu_item.item_id == ITEM_BONUS_LEVEL:
            pygame.event.post(Event(START_BONUS_LEVEL_EVENT, dict()))

    def handle_mouse_click(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()

        for label_surface, (posx, posy), menu_item in self._menus[self._cur_menu]:
            (label_w, label_h) = label_surface.get_size()
            label_rect = pygame.Rect(posx, posy, label_w, label_h)

            if label_rect.collidepoint(mouse_x, mouse_y):
                pygame.event.post(Event(MENU_CLICK_EVENT, {'menu_item': menu_item}))


    def check_mouse(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()

        for label_surface, (posx, posy), menu_item in self._menus[self._cur_menu]:
            (label_w, label_h) = label_surface.get_size()
            label_rect = pygame.Rect(posx, posy, label_w, label_h)

            if label_rect.collidepoint(mouse_x, mouse_y):
                menu_item.mouse_over()
                label_surface.blit(menu_item.surface(), (0, 0))
            else:
                menu_item.mouse_off()
                label_surface.blit(menu_item.surface(), (0, 0))


    def run(self):
        self.clock.tick(FPS)
        self.check_mouse()
        self._render()
        pygame.display.flip()
