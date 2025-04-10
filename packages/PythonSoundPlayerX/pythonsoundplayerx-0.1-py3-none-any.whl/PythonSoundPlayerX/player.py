import pygame
from .utils import file_exists, get_extension

class SoundPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.supported_formats = ['.mp3', '.wav']

    def play(self, file_path):
        if not file_exists(file_path):
            print("[HATA] Dosya bulunamadi:", file_path)
            return

        ext = get_extension(file_path)
        if ext not in self.supported_formats:
            print("[HATA] Desteklenmeyen format:", ext)
            return

        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            print("[BILGI] Caliniyor:", file_path)

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print("[HATA] Oynatma hatasi:", e)
