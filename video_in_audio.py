import os

from pytube import YouTube
from pytube.exceptions import VideoUnavailable


def video_in_audio(url: str):
    """Функция, позволяющая закгрузить видео с YouTube и конверитровать
    его в аудиофайл"""

    try:
        yt = YouTube(url)
    except VideoUnavailable:
        return f'Видео по ссылке {url} не найдено.'

    stream = yt.streams.get_audio_only()
    audio_file = stream.download()
    audio_file_path = os.path.abspath(audio_file)
    audio_file_path = audio_file_path.split('\\')[-1]
    return audio_file, audio_file_path


def del_create_file(filename: str):
    """Функция, позволяющая удалить ранее созданный файл"""

    os.remove(filename)


