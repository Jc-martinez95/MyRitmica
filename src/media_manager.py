import pyglet.media as media
import pyglet.resource as resource
from typing import Optional
from csv import reader as csv_reader
from .config import ASSETS_PATH

beat_timestamps_path = f'{ASSETS_PATH}/beat_timestamps'

def load_source(level_index: int) -> Optional[media.StreamingSource]:
    video_filename = f'video_levels/Ex{level_index}.mp4'
    source = resource.media(video_filename, streaming=True)
    return source

def load_timestamps(level_index: int) -> list:
    # with open(f'{beat_timestamps_path}/Ex{level_index}.txt', newline='') as file:
    #     reader = csv_reader(file, delimiter = '\t')
    #     data = list(reader)
    txt_filename = f'beat_timestamps/Ex{level_index}.txt'
    with resource.file(txt_filename, 'rt') as file:
        reader = csv_reader(file, delimiter= '\t')
        data = list(reader)
    timestamps = [float(row[0]) for row in data]
    return timestamps

def hit_sound(duration: float, freq: int, amp: float) -> Optional[media.StaticSource]:
    synth_envelope = media.synthesis.FlatEnvelope(amplitude=amp)
    hit_sound = media.synthesis.Square(
        duration=duration,frequency = freq,
        sample_rate = 44100,
        envelope = synth_envelope
    )
    return hit_sound
