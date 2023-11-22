import tkinter as tk
from tkinter import ttk
import pygame
from threading import Thread
import time
import mysql.connector

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        root.title("Music Player")
        self.root.geometry('665x300')
        self.root.resizable(width=False, height=False)
        self.current_song_index = 0
        self.paused = False
        self.music_names = []
        self.db_connection = None
        self.cursor = None

        self.root.configure(bg='orange')
        

        pygame.init()

        self.init_ui()
        self.init_database_connection()

    def init_ui(self):
        self.button_style = {
            'bg': '#bdc3c7',  
            'fg': 'Blue',
            'font': ('Arial', 12, 'bold'),
            'bd': 3,
            'relief': 'raised'
        }

        self.music_progress_style = ttk.Style()
        self.music_progress_style.configure("Horizontal.TProgressbar", troughcolor='#bdc3c7')

        self.music_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=475, mode='determinate', style="Horizontal.TProgressbar", )
        self.music_progress_bar.grid(row=1, column=0, columnspan=4, padx=10, pady=(10, 0), sticky='ew')

        self.current_file_label = tk.Label(self.root, bg="orange", text="", font=('Arial', 12))
        self.current_file_label.grid(row=0, column=0, columnspan=4, pady=(10, 0))

        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=2, column=0, columnspan=4, pady=(5, 30))

        self.create_button('Previous', self.play_previous)
        self.play_button = self.create_button('Play', self.play_music)
        self.pause_button = self.create_button('Pause', self.pause_music)
        self.resume_button = self.create_button('Resume', self.resume_music, state='disabled')
        self.create_button('Next', self.play_next)

        self.root.grid_rowconfigure(1, weight=1)

    def create_button(self, text, command, **kwargs):
        button = tk.Button(self.button_frame, text=text, command=command, width=10, height=2, **kwargs)
        button.pack(side=tk.LEFT, padx=10)
        button.configure(**self.button_style)
        return button

    def init_database_connection(self):
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin@123',
            database='music_database'
        )
        self.cursor = self.db_connection.cursor()

    def get_music_paths_from_database(self):
        self.cursor.execute("SELECT file_path FROM MusicFile")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def get_music_names_from_database(self):
        self.cursor.execute("SELECT file_name FROM MusicFile")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def display_file_names(self):
        self.music_names = self.get_music_names_from_database()
        self.current_file_label.config(text=self.get_current_song_name())

    def play_music(self):
        self.file_paths = self.get_music_paths_from_database()
        self.current_file_label.config(text=self.get_current_song_name())

        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.load(self.file_paths[self.current_song_index])
            pygame.mixer.music.play()

        self.resume_button.config(state='normal')
        self.music_progress_bar.config(maximum=self.get_music_length())
        progress_thread = Thread(target=self.update_progress_bar)
        progress_thread.start()

    def get_current_song_name(self):
        return self.music_names[self.current_song_index]

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
        if len(self.file_paths) == 0:
            return

        self.current_song_index = (self.current_song_index + 1) % len(self.file_paths)
        pygame.mixer.music.load(self.file_paths[self.current_song_index])
        pygame.mixer.music.play()
        self.current_file_label.config(text=self.get_current_song_name())
        self.resume_button.config(state='normal')
        self.music_progress_bar.config(maximum=self.get_music_length())

    def play_previous(self):
        if len(self.file_paths) == 0:
            return

        self.current_song_index = (self.current_song_index - 1) % len(self.file_paths)
        pygame.mixer.music.load(self.file_paths[self.current_song_index])
        pygame.mixer.music.play()
        self.current_file_label.config(text=self.get_current_song_name())
        self.resume_button.config(state='normal')
        self.music_progress_bar.config(maximum=self.get_music_length())

    def get_music_length(self):
        audio = pygame.mixer.Sound(self.file_paths[self.current_song_index])
        return int(audio.get_length())

    def update_progress_bar(self):
        while pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000
            self.music_progress_bar['value'] = current_time
            time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    obj = MusicPlayer(root)
    obj.display_file_names()
    obj.play_music()
    root.mainloop()
