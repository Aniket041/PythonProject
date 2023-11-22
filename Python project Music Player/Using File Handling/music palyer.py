from tkinter import *
import pygame
from threading import Thread
import time

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.geometry('575x300')
        self.root.resizable(width=False, height=False)
        self.file_paths = [
            r"C:\Users\anike\AppData\Local\Programs\Python\Python312\Python project Music Player\Music Files\Ae-Dil-Hai-Mushkil-Title-Track_320(PagalWorldl).mp3",
            r"C:\Users\anike\AppData\Local\Programs\Python\Python312\Python project Music Player\Music Files\Jo-Tu-Mera-Humdard-Hai_320(PagalWorldl).mp3"
            r"C:\Users\anike\AppData\Local\Programs\Python\Python312\Python project Music Player\Music Files\Zara-Zara_320(PagalWorldl).mp3"
            r"C:\Users\anike\AppData\Local\Programs\Python\Python312\Python project Music Player\Music Files\Aigiri-Nandini_320(PagalWorldl).mp3"
            r"C:\Users\anike\AppData\Local\Programs\Python\Python312\Python project Music Player\Music Files\Sach-Keh-Raha-Hai-Deewana-(Cover-Version)(PaglaSongs).mp3"
        ]
        self.current_song_index = 0
        self.paused = False

        pygame.init()

        # Bootstrap CSS classes for buttons
        self.button_style = {
            'bg': '#FFA500',
            'fg': 'white',
            'font': ('Arial', 12),
            'padx': 10,
            'pady': 5,
            'bd': 2,
            'relief': 'flat',
        }

        self.music_progress_bar = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, length=475)
        self.music_progress_bar.grid(row=1, column=0, columnspan=4, padx=10, pady=(10, 0), sticky='ew')

        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=2, column=0, columnspan=4, pady=(5, 10))

        self.prev_button = Button(self.button_frame, text='Previous', command=self.play_previous, **self.button_style)
        self.prev_button.pack(side=LEFT, padx=10)

        self.play_button = Button(self.button_frame, text='Play', command=self.play_music, **self.button_style)
        self.play_button.pack(side=LEFT, padx=10)

        self.pause_button = Button(self.button_frame, text='Pause', command=self.pause_music, **self.button_style)
        self.pause_button.pack(side=LEFT, padx=10)

        self.resume_button = Button(self.button_frame, text='Resume', command=self.resume_music, state=DISABLED, **self.button_style)
        self.resume_button.pack(side=LEFT, padx=10)

        self.next_button = Button(self.button_frame, text='Next', command=self.play_next, **self.button_style)
        self.next_button.pack(side=LEFT, padx=10)

        self.loop_button = Button(self.button_frame, text='Loop', command=self.toggle_loop, **self.button_style)
        self.loop_button.pack(side=LEFT, padx=10)

        self.loop_enabled = False

        self.root.grid_rowconfigure(1, weight=1)

    def get_music_length(self):
        audio = pygame.mixer.Sound(self.file_paths[self.current_song_index])
        return int(audio.get_length())

    def update_progress_bar(self):
        while pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000
            self.music_progress_bar.set(current_time)
            time.sleep(1)

    def play_music(self):
        pygame.mixer.music.load(self.file_paths[self.current_song_index])
        pygame.mixer.music.play()
        self.resume_button.config(state=NORMAL)
        self.music_progress_bar.config(to=self.get_music_length())
        progress_thread = Thread(target=self.update_progress_bar)
        progress_thread.start()

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def resume_music(self):
        pygame.mixer.music.unpause()
        self.paused = False

    def toggle_loop(self):
        self.loop_enabled = not self.loop_enabled
        if self.loop_enabled:
            print('Loop enabled: Play one song multiple times')
        else:
            print('Loop disabled: Play each song once')

    def play_next(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.file_paths)
        self.play_music()

    def play_previous(self):
        self.current_song_index = (self.current_song_index - 1) % len(self.file_paths)
        self.play_music()

root = Tk()
obj = MusicPlayer(root)
root.mainloop()
