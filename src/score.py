from pyglet.text import Label
from collections.abc import Callable
from .config import GAME_STATE_SCORE

def on_video_end(app: 'GameApp') -> Callable:

    def video_end_handler():
        app.misses += app.total_beats - app.hits
        app.game_state = GAME_STATE_SCORE
        app.final_score = final_score_label(app)
    return video_end_handler

def final_score_label(app: 'GameApp') -> Label:

    score_percentage = (app.hits / app.total_beats) * 100
    
    final_score_text = (f'''
        --Resultados--\n
        Aciertos: {app.hits}\n
        Fallos: {app.misses}\n
        Puntuación: {score_percentage:.2f}%
        '''
    )
    score_label = Label(
        final_score_text,
        font_name= 'Arial',
        font_size= 30,
        x = app.width // 2,
        y = app.height // 2,
        anchor_x = 'center',
        anchor_y = 'center',
        multiline=True,
        width = 500,
        color = (255,255,255,255) 
    )
    return score_label 