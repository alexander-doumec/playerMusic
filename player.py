import os
import tkinter as tk
from tkinter import filedialog
import pygame
from pygame import mixer

class LecteurAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecteur Audio")

        self.playlist = []
        self.current_track = 0

        # Initialiser Pygame
        pygame.init()
        mixer.init()

        # Créer des widgets
        self.create_widgets()

    def create_widgets(self):
        # Boutons
        tk.Button(self.root, text="Choisir une piste", command=self.choose_track).pack(pady=10)
        tk.Button(self.root, text="Lancer la lecture", command=self.play).pack(pady=5)
        tk.Button(self.root, text="Mettre en pause", command=self.pause).pack(pady=5)
        tk.Button(self.root, text="Arrêter la lecture", command=self.stop).pack(pady=5)
        tk.Button(self.root, text="Suivant", command=self.next_track).pack(pady=5)
        tk.Button(self.root, text="Lecture aléatoire", command=self.shuffle_playlist).pack(pady=5)

        # Barre de progression
        self.progress_bar = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.progress_bar.set(50)
        self.progress_bar.pack(pady=10)

        # Barre de progression pour suivre l'avancée de la lecture
        self.playback_progress = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL)
        self.playback_progress.pack(pady=10)

        # Liste des pistes audio
        self.playlistbox = tk.Listbox(self.root, selectmode=tk.SINGLE, selectbackground="yellow", selectforeground="black")
        self.playlistbox.pack(pady=10)

        # Ajouter des pistes à la playlist par défaut (vous pouvez charger des pistes ici)
        self.add_track("chemin/vers/votre/musique1.mp3")
        self.add_track("chemin/vers/votre/musique2.mp3")

    def choose_track(self):
        file_path = filedialog.askopenfilename(title="Choisir une piste audio", filetypes=[("Fichiers audio", "*.mp3;*.wav")])
        if file_path:
            self.add_track(file_path)

    def add_track(self, track_path):
        self.playlist.append(track_path)
        track_name = os.path.basename(track_path)
        self.playlistbox.insert(tk.END, track_name)

    def play(self):
        if self.playlist:
            mixer.music.load(self.playlist[self.current_track])
            mixer.music.play()
            self.root.after(1000, self.update_progress)

    def pause(self):
        mixer.music.pause()

    def stop(self):
        mixer.music.stop()

    def next_track(self):
        self.current_track = (self.current_track + 1) % len(self.playlist)
        self.play()

    def shuffle_playlist(self):
        import random
        random.shuffle(self.playlist)
        self.current_track = 0
        self.play()

    def set_volume(self, val):
        volume = int(val) / 100
        mixer.music.set_volume(volume)

    def update_progress(self):
        current_time = pygame.mixer.music.get_pos() / 1000  # convert milliseconds to seconds
        total_time = pygame.mixer.Sound(self.playlist[self.current_track]).get_length()
        progress_percent = (current_time / total_time) * 100
        self.playback_progress.set(progress_percent)

        if pygame.mixer.music.get_busy():
            self.root.after(1000, self.update_progress)

if __name__ == "__main__":
    root = tk.Tk()
    app = LecteurAudio(root)
    root.mainloop()
