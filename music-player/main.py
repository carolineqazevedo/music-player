from pathlib import Path
from tkinter import Label
from components.gui import create_gui

# Define os caminhos | Define paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def main():
    # Inicializa a GUI | Initialize the GUI
    gui = create_gui(relative_to_assets)
    
    # Labels para exibir informações da música atual | Labels to display current song information
    Label(gui.window, textvariable=gui.music_player.current_song_name, bg="#1B1B1B", fg="#DEDEDE", font=("Inter Bold", 20)).place(x=246, y=57)
    Label(gui.window, textvariable=gui.music_player.current_artist_name, bg="#1B1B1B", fg="#626262", font=("Inter SemiBold", 12)).place(x=247, y=39)
    Label(gui.window, textvariable=gui.music_player.current_duration, bg="#1B1B1B", fg="#606060", font=("Inter Medium", 9)).place(x=588, y=93)
    Label(gui.window, text="PLAYLIST", bg="#181818", fg="#606060", font=("Inter Bold", 13)).place(x=75, y=237)

    gui.run()  # Inicia o loop principal da GUI | Start the main loop of the GUI

if __name__ == "__main__":
    main()
