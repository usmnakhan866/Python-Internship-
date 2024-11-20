import os
import tkinter as tk
from tkinter import filedialog, Listbox
from tkinter import ttk
from pygame import mixer
import time

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x400")
        
        mixer.init()
        
        self.playlist = []
        self.current_song_index = 0
        self.is_paused = False
        
        self.song_label = tk.Label(root, text="No song playing", font=("Helvetica", 12))
        self.song_label.pack(pady=10)
        
        self.load_button = tk.Button(root, text="Load Playlist", command=self.load_playlist, width=15)
        self.load_button.pack(pady=5)
        
        self.playlist_box = Listbox(root, selectmode=tk.SINGLE, width=60, height=10)
        self.playlist_box.pack(pady=10)
        self.playlist_box.bind('<Double-1>', self.play_selected_song)
        
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=5)
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)
        
        self.prev_button = tk.Button(control_frame, text="Previous", command=self.prev_song, width=10)
        self.prev_button.grid(row=0, column=0, padx=5)
        
        self.play_button = tk.Button(control_frame, text="Play", command=self.play_song, width=10)
        self.play_button.grid(row=0, column=1, padx=5)
        
        self.pause_button = tk.Button(control_frame, text="Pause", command=self.pause_song, width=10)
        self.pause_button.grid(row=0, column=2, padx=5)
        
        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop_song, width=10)
        self.stop_button.grid(row=0, column=3, padx=5)
        
        self.next_button = tk.Button(control_frame, text="Next", command=self.next_song, width=10)
        self.next_button.grid(row=0, column=4, padx=5)
        
        volume_frame = tk.Frame(root)
        volume_frame.pack(pady=8)
        
        tk.Label(volume_frame, text="Volume").pack(side=tk.LEFT)
        self.volume_slider = tk.Scale(volume_frame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.1, command=self.set_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(side=tk.LEFT)
        
         
        
        
        # Update progress bar
        self.update_progress()

    def load_playlist(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.playlist = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".mp3")]
            self.playlist_box.delete(0, tk.END)
            for song in self.playlist:
                self.playlist_box.insert(tk.END, os.path.basename(song))
            
            if self.playlist:
                self.current_song_index = 0
                self.play_song()
    
    def play_selected_song(self, event):
        self.current_song_index = self.playlist_box.curselection()[0]
        self.play_song()
    
    def play_song(self):
        if not self.playlist:
            return
        
        mixer.music.load(self.playlist[self.current_song_index])
        mixer.music.play()
        self.is_paused = False
        song_name = os.path.basename(self.playlist[self.current_song_index])
        self.song_label.config(text=f"Playing: {song_name}")
        self.playlist_box.select_clear(0, tk.END)
        self.playlist_box.select_set(self.current_song_index)

        # Reset and start updating progress
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = self.get_song_length()
        self.update_progress()

    def get_song_length(self):
        # Get the length of the currently playing song in seconds
        # Note: This is a placeholder; you may need to use a different method to get the actual length
        return mixer.Sound(self.playlist[self.current_song_index]).get_length()

    def update_progress(self):
        if mixer.music.get_busy():
            current_position = mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
            self.progress_bar['value'] = current_position
            self.root.after(1000, self.update_progress)  # Update progress every second

    def pause_song(self):
        if self.is_paused:
            mixer.music.unpause()
            self.is_paused = False
            self.song_label.config(text=f"Playing: {os.path.basename(self.playlist[self.current_song_index])}")
        else:
            mixer.music.pause()
            self.is_paused = True
            self.song_label.config(text="Paused")
    
    def stop_song(self):
        mixer.music.stop()
        self.song_label.config(text="Stopped")
        self.progress_bar['value'] = 0
    
    def next_song(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self.play_song()
    
    def prev_song(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.play_song()
    
    def set_volume(self, val):
        mixer.music.set_volume(float(val))

root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
