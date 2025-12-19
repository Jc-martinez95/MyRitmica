import pyglet
import time
from .config import HIT_FEEDBACK_DURATION, GAME_STATE_PLAYING, COLOR_HIT, COLOR_MISS
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from.main import GameApp

def beat_checker(dt, app: 'GameApp'):
    if app.game_state != GAME_STATE_PLAYING:
        pyglet.clock.unschedule(beat_checker)
        return
    app.total_beats = len(app.beat_timestamps)
    if app.last_checked_beat_index >= app.total_beats:
        app.active_beat = False
        return
    
    current_time = app.player.time
    beat_time = app.beat_timestamps[app.last_checked_beat_index]
    low_bound = beat_time - app.error_margin
    high_bound = beat_time + app.error_margin

    if low_bound <= current_time <= high_bound:
        app.active_beat = True
    elif current_time > high_bound:
        app.active_beat = False
        app.last_checked_beat_index += 1
    else:
        app.active_beat = False

    # print(f'beat_timestamp:{app.beat_timestamps[app.last_checked_beat_index]}. current_time:{round(app.player.time,3)}. Active_beat:{app.active_beat}')
    # print(f'total_beats{app.total_beats}. current_beat_index: {app.last_checked_beat_index}')
    
def hit_score_logic(app: 'GameApp', symbol, modifiers):
    
    if app.active_beat:
        app.message_text = 'Acierto'
        app.message_color = COLOR_HIT
        app.hits += 1
        # CRÍTICO: Si acertamos, avanzamos el índice y desactivamos el beat inmediatamente 
        # para que no se registre otro acierto en el mismo frame.
        print(f'beat_timestamp:{app.beat_timestamps[app.last_checked_beat_index]}. current_time:{round(app.player.time,3)}. Active_beat:{app.active_beat} Msg:{app.message_text}')
        app.last_checked_beat_index += 1 # !!!!!
        app.active_beat = False
    else:
        app.message_text = 'Fallo'
        app.message_color = COLOR_MISS
        print(f'beat_timestamp:{app.beat_timestamps[app.last_checked_beat_index]}. current_time:{round(app.player.time,3)}. Active_beat:{app.active_beat} Msg:{app.message_text}')

def clear_hit_feedback(dt, app: 'GameApp') -> None:

    app.hit_feedback_message = None

def hit_feedback(app: 'GameApp', symbol, modifiers) -> None:
    if app.hit_feedback_message:
        pyglet.clock.unschedule(update_message_fade)
    pyglet.clock.unschedule(clear_hit_feedback)
    app.hit_feedback_message = pyglet.text.Label(
        app.message_text,
        font_name='Arial',
        font_size=50,
        x = app.width // 4,
        y = app.height // 4,
        anchor_x= 'center',
        anchor_y='center',
        color = app.message_color
    )
    app.message_start_time = time.time() # Este es el tiempo en que se activó esta función
    
    pyglet.clock.schedule_interval(update_message_fade, 1/60.0, app)
 
def update_message_fade(dt, app:'GameApp') -> None:
    if app.hit_feedback_message:
      
        elapsed_time = time.time() - app.message_start_time # El tiempo que transcurre desde que se llamó a la función hit_feedback y cada actualización de está función
        remaining_ratio = 1 - (elapsed_time / HIT_FEEDBACK_DURATION)

        if remaining_ratio < 0:
            remaining_ratio = 0

        opacity = int(255 * remaining_ratio)
        app.hit_feedback_message.opacity = opacity

        if elapsed_time >= HIT_FEEDBACK_DURATION:
            clear_hit_feedback(dt, app)
            pyglet.clock.unschedule(update_message_fade)

