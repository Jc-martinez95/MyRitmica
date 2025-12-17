import os
import pyglet
from .config import *
from .main_menu import MainMenu, LevelMenu
from .game_scene import *
from .media_manager import hit_sound, load_timestamps
from .score import final_score_label, on_video_end

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pyglet.resource.path.append(os.path.join(base_path, 'assets'))
pyglet.resource.reindex()

class GameApp(pyglet.window.Window):
    def __init__(self):
        super().__init__(width = 1280, height = 720, resizable = False)

        self.game_state = GAME_STATE_MENU
        self.menu = MainMenu(title= 'My juego rítmico',title_font_size= 60)
        self.levels = LevelMenu(y_position= 1.2, y_separation= 70)
        self.menu_selection = 0
        self.level = 0
        self.player = pyglet.media.Player()
        self.hit_feedback_message = None
        self.message_text = str()
        self.message_color = (0,0,0,0)
        self.message_start_time = 0.0
        self.beat_timestamps = load_timestamps(self.menu_selection)
        self.total_beats = len(self.beat_timestamps)
        self.last_checked_beat_index = 0
        self.hits = 0
        self.misses = 0
        self.error_margin = ERROR_MARGIN
        self.final_score = None
        self.player.push_handlers(on_eos = on_video_end(self))
        self.active_beat = 0
        self.is_checker_scheduled = False
    def reset_game_state(self):
        self.hits = 0
        self.misses = 0
        self.last_checked_beat_index = 0
        if self.hit_feedback_message:
            self.hit_feedback_message.delete()
            self.hit_feedback_message = None
        if self.final_score:
            self.final_score.delete()
            self.final_score = None
    def on_draw(self):
        self.clear()
        if self.game_state == GAME_STATE_MENU:
            self.menu.draw_menu_title(self)
            self.menu.draw_menu_options(self)
        elif self.game_state == GAME_STATE_LEVELS:
            self.levels.draw_menu_options(self)
        elif self.game_state == GAME_STATE_PLAYING:
            if self.player.texture:
                self.player.texture.blit(0,0)
            if self.hit_feedback_message:
                self.hit_feedback_message.draw()
        elif self.game_state == GAME_STATE_SCORE:
            self.final_score.draw()
       
    def on_key_press(self, symbol, modifiers):
        if self.game_state == GAME_STATE_MENU:
            self.menu.handle_main_menu_navigation(self, symbol, modifiers)
        elif self.game_state == GAME_STATE_LEVELS:
            self.levels.handle_level_menu_navigation(self, symbol, modifiers)
        elif self.game_state == GAME_STATE_PLAYING:
            hit_score_logic(self, symbol, modifiers)
            hit_feedback(self, symbol, modifiers)
            hit_sound(duration=0.1, freq=440,amp=0.1).play()
        elif self.game_state == GAME_STATE_SCORE:
            self.reset_game_state()
            self.game_state = GAME_STATE_MENU

        
    def update(self, dt):

        if self.game_state == GAME_STATE_PLAYING and not self.is_checker_scheduled:
            # Programar la verificación de beats para que se ejecute continuamente (60 veces por segundo)
            pyglet.clock.schedule_interval(beat_checker, 1/60.0, self)
            self.is_checker_scheduled = True
        
        if self.game_state != GAME_STATE_PLAYING and self.is_checker_scheduled:
            # Desprogramar si salimos del estado de juego
            pyglet.clock.unschedule(beat_checker)
            self.is_checker_scheduled = False

if __name__ == '__main__':
    window = GameApp()
    pyglet.clock.schedule_interval(window.update, 1/60.0)    
    pyglet.app.run()