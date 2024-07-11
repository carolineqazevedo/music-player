from io import BytesIO
from threading import Thread
from tkinter import StringVar, filedialog
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from PIL import Image, ImageTk
import pygame
import os

class MusicPlayer:
    def __init__(self):
        # Inicializa os atributos do MusicPlayer | Initializes the MusicPlayer attributes
        self.playlist = []  # Lista de reprodução | Playlist
        self.current_song_index = 0  # Índice da música atual | Current song index
        self.song_listbox = None  # Lista de músicas | Song listbox
        self.current_song_name = StringVar(value="Name")  # Nome da música atual | Current song name
        self.current_artist_name = StringVar(value="Artist")  # Nome do artista atual | Current artist name
        self.current_duration = StringVar(value="00:00")  # Duração da música atual | Current song duration
        self.current_album_image = None  # Imagem do álbum atual | Current album image
        self.progress_bar = None  # Barra de progresso | Progress bar
        self.is_playing = False  # Estado de reprodução | Playback state
        self.is_paused = False  # Adicionado para rastrear se a música está pausada | Added to track if the music is paused

        # Inicializa o mixer do Pygame | Initializes Pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)  # Define o volume inicial | Sets the initial volume

    def add_music(self):
        # Função para adicionar músicas à playlist | Function to add music to the playlist
        selected_directory = filedialog.askdirectory()  # Abre um diálogo para selecionar o diretório | Opens a dialog to select the directory
        if not selected_directory:
            return
        
        def add_to_playlist(filepath):
            # Adiciona uma música à playlist | Adds a song to the playlist
            if filepath.endswith(".mp3"):
                try:
                    artist, duration, title = self.get_metadata(filepath)
                    formatted_title = f"- {title.ljust(10)}"
                    self.playlist.append(filepath)
                    self.song_listbox.insert("end", formatted_title)
                except Exception as e:
                    print(f"Erro ao adicionar música à playlist: {e} | Error adding music to playlist: {e}")
        
        def add_music_async():
            # Adiciona músicas de forma assíncrona | Adds music asynchronously
            for root, _, files in os.walk(selected_directory):
                for file in files:
                    add_to_playlist(os.path.join(root, file))
                    if len(self.playlist) > 100:
                        break
                if len(self.playlist) > 100:
                    break
        
        # Inicia a thread para adicionar músicas | Starts the thread to add music
        t = Thread(target=add_music_async)
        t.start()

        if self.playlist:
            self.current_song_index = 0
            self.play_music()

    def play_pause_music(self):
        # Alterna entre tocar e pausar a música | Toggles between playing and pausing the music
        if self.is_paused:
            self.resume_music()
        elif self.is_playing:
            self.pause_music()
        else:
            self.play_music()

    def play_music(self):
        # Toca a música atual | Plays the current song
        if not self.playlist:
            print("Playlist vazia. | Empty playlist.")
            return
        
        try:
            pygame.mixer.music.load(self.playlist[self.current_song_index])  # Carrega a música | Loads the music
            pygame.mixer.music.play()  # Toca a música | Plays the music
            self.update_current_song_info()  # Atualiza as informações da música atual | Updates the current song information
            self.update_progress_bar()  # Atualiza a barra de progresso | Updates the progress bar
            self.is_playing = True
            self.is_paused = False
        except pygame.error as e:
            print(f"Erro ao carregar ou reproduzir música: {e} | Error loading or playing music: {e}")

    def pause_music(self):
        # Pausa a música | Pauses the music
        pygame.mixer.music.pause()
        self.is_playing = False
        self.is_paused = True

    def resume_music(self):
        # Retoma a música | Resumes the music
        pygame.mixer.music.unpause()
        self.is_playing = True
        self.is_paused = False

    def stop_music(self):
        # Para a música | Stops the music
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
    
    def set_volume(self, volume):
        # Define o volume da música | Sets the music volume
        pygame.mixer.music.set_volume(volume)
    
    def next_music(self):
        # Toca a próxima música da playlist | Plays the next song in the playlist
        if self.playlist:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self.play_music()

    def prev_music(self):
        # Toca a música anterior da playlist | Plays the previous song in the playlist
        if self.playlist:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.play_music()

    def get_metadata(self, filepath):
        # Obtém os metadados da música | Gets the music metadata
        try:
            audio = MP3(filepath)
            artist = audio['TPE1'].text[0] if 'TPE1' in audio else 'Unknown Artist'
            duration = self.format_time(audio.info.length)
            title = audio['TIT2'].text[0] if 'TIT2' in audio else 'Unknown Title'
            return artist, duration, title
        except Exception as e:
            print(f"Erro ao obter metadados: {e} | Error getting metadata: {e}")
            return 'Unknown Artist', '--:--', 'Unknown Title'
        
    def format_time(self, seconds):
        # Formata o tempo em minutos e segundos | Formats the time into minutes and seconds
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes):02}:{int(seconds):02}"
    
    def update_current_song_info(self):
        # Atualiza as informações da música atual | Updates the current song information
        if self.current_song_index < len(self.playlist):
            filepath = self.playlist[self.current_song_index]
            filename = os.path.basename(filepath)
            artist, duration, _ = self.get_metadata(filepath)
            self.current_song_name.set(self.clean_song_title(filename))
            self.current_artist_name.set(artist)
            self.current_duration.set(duration)
            album_image = self.get_album_image(filepath)
            if album_image:
                self.current_album_image_label.config(image=album_image)
                self.current_album_image_label.image = album_image
            else:
                self.current_album_image_label.config(image='')

    def clean_song_title(self, song_title):
        # Limpa o título da música | Cleans the song title
        song_title = song_title.replace('.mp3', '')
        last_hyphen_index = song_title.rfind('-')

        if last_hyphen_index != -1:
            cleaned_title = song_title[last_hyphen_index + 1:].strip()
        else:
            cleaned_title = song_title.strip()

        return cleaned_title

    def update_album_image(self):
        # Atualiza a imagem do álbum (implementação vazia) | Updates the album image (empty implementation)
        try:
            pass
        except Exception as e:
            print(f"Erro ao carregar imagem do álbum: {e} | Error loading album image: {e}")

    def update_progress_bar(self):
        # Atualiza a barra de progresso | Updates the progress bar
        if self.progress_bar is not None:
            try:
                if pygame.mixer.music.get_busy():
                    song_length = self.get_song_length()
                    if song_length > 0:
                        progress = (self.get_song_position() / song_length) * 100
                        self.progress_bar["value"] = progress
                    else:
                        self.progress_bar["value"] = 0
                    
                    self.progress_bar.after(1000, self.update_progress_bar)
            except Exception as e:
                print(f"Erro ao atualizar barra de progresso: {e} | Error updating progress bar: {e}")
    
    def get_song_length(self):
        # Obtém a duração da música | Gets the length of the song
        try:
            audio = MP3(self.playlist[self.current_song_index])
            return audio.info.length
        except Exception as e:
            print(f"Erro ao obter duração da música: {e} | Error getting song length: {e}")
            return 0
    
    def get_song_position(self):
        # Obtém a posição atual da música | Gets the current position of the song
        try:
            return pygame.mixer.music.get_pos() / 1000
        except Exception as e:
            print(f"Erro ao obter posição da música: {e} | Error getting song position: {e}")
            return 0

    def get_album_image(self, filepath):
        # Obtém a imagem do álbum da música | Gets the album image of the song
        try:
            audio = ID3(filepath)
            for tag in audio.values():
                if isinstance(tag, APIC):
                    album_image = Image.open(BytesIO(tag.data))
                    album_image = album_image.resize((130, 130), Image.LANCZOS)
                    return ImageTk.PhotoImage(album_image)
        except Exception as e:
            print(f"Erro ao obter imagem do álbum: {e} | Error getting album image: {e}")
            return None
