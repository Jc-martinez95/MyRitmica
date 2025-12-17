from pyglet.text import Label
from pyglet.window import key
from pyglet.app import exit
from typing import List
from .config import GAME_STATE_LEVELS, GAME_STATE_PLAYING, COLOR_SELECTED, COLOR_UNSELECTED
from .media_manager import load_source, load_timestamps

class Menu:
    def __init__(self, options: List['str'], font_size:int = 30, y_position:int = 2, y_separation: int = 50):
        self.options = options
        self.font_size = font_size
        self.y_position = y_position
        self.y_separation = y_separation

    def draw_menu_options(self, app: 'GameApp') -> None:
        
        for i, option in enumerate(self.options):
            option_color = COLOR_SELECTED if i == app.menu_selection else COLOR_UNSELECTED
            option_label = Label(
                option,
                font_size = self.font_size,
                x = app.width // 2.5,
                y = app.height // self.y_position - (i * self.y_separation),
                color = option_color
            )
            option_label.draw()


    def handle_menu_navigation(self, app: 'GameApp', options, symbol, modifiers) -> None:
            if symbol == key.DOWN:
                app.menu_selection = (app.menu_selection + 1) % len(options)
            elif symbol == key.UP:
                app.menu_selection = (app.menu_selection - 1) % len(options)

class MainMenu(Menu):
    def __init__(self, title: str, title_font_size: int, **kwargs):
    
        self.title = title
        self.title_font_size = title_font_size
        self.options = ['INICIAR JUEGO', 'SALIR']
        self.font_size = 30
        self._title_y_position = 1
        super().__init__(options = self.options, font_size= self.font_size, **kwargs)
    
    def draw_menu_title(self, app: 'GameApp') -> None:
        
        title_label = Label(
            self.title,
            font_size = self.title_font_size,
            x = app.width // 2,
            y = app.height // self._title_y_position - 100,
            anchor_x='center',
            anchor_y='center',
            color = COLOR_UNSELECTED
        )
        title_label.draw()
        
    def handle_main_menu_navigation(self, app: 'GameApp', symbol, modifiers) -> None:
        
        self.handle_menu_navigation(app, self.options, symbol, modifiers)

        if symbol == key.ENTER:
            if app.menu_selection == 0:
                app.menu_selection = 0
                app.game_state = GAME_STATE_LEVELS
            elif app.menu_selection == 1:
                exit()

class LevelMenu(Menu):
    def __init__(self,**kwargs):
        self.options = [f'NIVEL {i}' for i in range(10)]
        
        super().__init__(options = self.options,**kwargs)
    def handle_level_menu_navigation(self, app: 'GameApp', symbol, modifiers) -> None:
        self.handle_menu_navigation(app, self.options, symbol, modifiers)

        if symbol == key.ENTER:
            app.beat_timestamps = load_timestamps(app.menu_selection)
            app.game_state = GAME_STATE_PLAYING
            app.player.queue(load_source(app.menu_selection))
            app.player.play()
