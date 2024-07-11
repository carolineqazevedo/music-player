import tkinter as tk
from tkinter import PhotoImage, Scale, Scrollbar
from tkinter.ttk import Progressbar, Style
from .player import MusicPlayer

class MusicPlayerGUI:
    def __init__(self, relative_to_assets):
        self.window = self.create_window()
        self.canvas = self.create_canvas()
        self.music_player = MusicPlayer()
        self.relative_to_assets = relative_to_assets

        self.volume_slider = self.create_volume_slider()
        self.buttons = self.create_buttons()
        self.song_listbox, self.scrollbar = self.create_song_listbox()
        self.progress_bar = self.create_progress_bar()
        self.album_image_label = self.create_album_image_label()

    def create_window(self):
        # Cria a janela principal | Creates the main window
        window = tk.Tk()
        window.geometry("650x750")
        window.configure(bg="#1B1B1B")
        window.resizable(False, True)
        window.maxsize(width=650, height=750)
        window.minsize(width=650, height=200)
        return window

    def create_canvas(self):
        # Cria o canvas para desenhar na janela | Creates the canvas to draw in the window
        canvas = tk.Canvas(
            self.window,
            bg="#1B1B1B",
            height=750,
            width=650,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.create_rectangle(0, 200, 650, 750, fill="#181818", outline="")
        canvas.place(x=0, y=0)
        return canvas

    def create_buttons(self):
        # Configurações dos botões | Button configurations
        button_configurations = [
            ("volume.png", 556, 123, 35, 35, self.toggle_volume_slider),
            ("next.png", 465, 125, 38, 38, self.music_player.next_music),
            ("prev.png", 333, 125, 38, 38, self.music_player.prev_music),
            ("add.png", 241, 123, 35, 35, self.music_player.add_music)
        ]

        buttons = []
        for image_file, x, y, width, height, command in button_configurations:
            button_image = PhotoImage(file=self.relative_to_assets(image_file))
            button = tk.Button(
                self.window,
                image=button_image,
                cursor="hand2",
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                command=command
            )
            button.image = button_image
            button.place(x=x, y=y, width=width, height=height)
            buttons.append(button)

        # Botão de play/pause | Play/pause button
        play_image = PhotoImage(file=self.relative_to_assets("play.png"))
        pause_image = PhotoImage(file=self.relative_to_assets("pause.png"))

        play_pause_button = tk.Button(
            self.window,
            image=play_image,
            cursor="hand2",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.toggle_play_pause(play_pause_button, play_image, pause_image)
        )
        play_pause_button.image = play_image
        play_pause_button.place(x=389, y=114, width=58, height=58)
        buttons.append(play_pause_button)

        return buttons

    def toggle_play_pause(self, button, play_image, pause_image):
        # Alterna entre play e pause | Toggle between play and pause
        if self.music_player.is_playing:
            self.music_player.pause_music()
            button.config(image=play_image)
            button.image = play_image
        else:
            self.music_player.resume_music()
            button.config(image=pause_image)
            button.image = pause_image

    def toggle_volume_slider(self):
        # Alterna a exibição do controle de volume | Toggle volume control display
        if self.volume_slider.winfo_viewable():
            self.volume_slider.place_forget()
        else:
            self.volume_slider.place(x=556, y=163, width=35, height=100)

    def create_volume_slider(self):
        # Cria o controle deslizante de volume | Creates the volume slider
        volume_slider = Scale(
            self.window,
            from_=0, to=100,
            orient='vertical',
            bg='#333333', fg='#DEDEDE',
            highlightthickness=0,
            troughcolor='#5A5E5C',
            command=lambda v: self.music_player.set_volume(float(v) / 100)
        )
        volume_slider.set(100)
        volume_slider.place_forget()
        return volume_slider

    def create_progress_bar(self):
        # Cria a barra de progresso | Creates the progress bar
        style = Style()
        style.theme_use('alt')
        style.configure(
            'TProgressbar',
            darkcolor='#861315',
            lightcolor='#861315',
            foreground="#861315",
            troughcolor='#5A5E5C',
            background='#861315',
            troughrelief='solid',
            pbarrelief='solid'
        )

        progress_bar = Progressbar(
            self.window,
            style='TProgressbar',
            orient="horizontal",
            mode="determinate",
            length=550
        )
        progress_bar.place(x=246, y=101, width=340, height=5)

        self.music_player.progress_bar = progress_bar
        return progress_bar

    def create_song_listbox(self):
        # Cria a lista de músicas e o scrollbar | Creates the song listbox and scrollbar
        listbox = tk.Listbox(
            self.window,
            bg="#181818",
            fg="#DEDEDE",
            font=("Inter SemiBold", 14),
            bd=0,
            highlightthickness=0,
            relief="flat",
            selectbackground="#333333",
            selectforeground="#DEDEDE",
            activestyle="none"
        )

        scrollbar = Scrollbar(
            self.window,
            activebackground='black',
            background='black',
            bg='#333333',
            troughcolor='#333333',
            command=listbox.yview,
            width=5
        )
        listbox.config(yscrollcommand=scrollbar.set)
        listbox.place(x=75, y=281, width=500, height=415)
        scrollbar.place(x=575, y=281, height=415)

        self.music_player.song_listbox = listbox

        listbox.bind("<<ListboxSelect>>", lambda event: self.update_current_song(event, listbox))

        return listbox, scrollbar

    def update_current_song(self, event, listbox):
        # Atualiza a música atual quando selecionada | Updates the current song when selected
        selected_index = listbox.curselection()
        if selected_index:
            self.music_player.current_song_index = selected_index[0]
            self.music_player.play_music()

    def create_album_image_label(self):
        # Cria o label para a imagem do álbum | Creates the label for the album image
        album_image_label = tk.Label(self.window, bg="#1B1B1B")
        album_image_label.place(x=50, y=39, width=130, height=130)
        self.music_player.current_album_image_label = album_image_label
        return album_image_label

    def run(self):
        # Inicia o loop principal da GUI | Starts the main loop of the GUI
        self.window.mainloop()

def create_gui(relative_to_assets):
    # Função para criar a GUI | Function to create the GUI
    gui = MusicPlayerGUI(relative_to_assets)
    return gui
