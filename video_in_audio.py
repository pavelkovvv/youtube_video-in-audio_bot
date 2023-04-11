import os
import subprocess

from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from pydub import AudioSegment


NEED_SIZE: int = 50000000


def video_in_audio(url: str):
    """Функция, позволяющая загрузить видео с YouTube и конверитровать
    его в аудиофайл"""

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        audio_file = stream.download(output_path='.', filename='audio.mp3')
        audio_file_path = os.path.abspath(audio_file)
        audio_file_path = audio_file_path.split('\\')[-1]
        file_size = os.path.getsize(audio_file_path)
        if file_size < 49500000:
            return audio_file_path, audio_file
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=bit_rate',
             '-of', 'default=noprint_wrappers=1:nokey=1', audio_file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        bit_rate = int(result.stdout.decode('utf-8').strip()) / 1000
        bitrate = ((NEED_SIZE * bit_rate) / file_size)
        output_file = audio_file_path
        sound = AudioSegment.from_file(output_file)
        sound.export(output_file, format="mp3", bitrate=f'{int(bitrate)}k')
        return audio_file_path, audio_file
    except VideoUnavailable:
        raise_message = f'Видео по ссылке {url} не найдено.'
        none_type = None
        return raise_message, none_type


def del_create_file(filename: str):
    """Функция, позволяющая удалить ранее созданный файл"""

    os.remove(filename)
