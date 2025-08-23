# import requests
from tkinter import filedialog, Tk, Menu, Listbox, Button, Frame, PhotoImage, END
import pygame
import os

# def download_image(image_url, file_name):
#     response = requests.get(image_url)
#     with open(file_name, 'wb') as file:
#         file.write(response.content)

# Initialize the Tkinter window
app = Tk()
app.title('Music Player with Tkinter and Pygame in Python')
app.geometry('500x300')

# Change the application icon
app_icon = PhotoImage(file='spootify.png')
app.iconphoto(False, app_icon)

# Initialize Pygame's mixer module for playing audio
pygame.init()
pygame.mixer.init()

# Define an event for when a song ends
SONG_END_EVENT = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END_EVENT)

# Create a menu bar
menu_bar = Menu(app)
app.config(menu=menu_bar)

# Define global variables
playlist = [] # List to store name of songs
current_song = "" # Store the currrently playing song
is_paused = False # Flag to indicate if music is paused

# Function to load music from a directory
def load_music():
    global current_song
    app.directory = filedialog.askdirectory()

    if not app.directory:
        return

    # Clear the current list of songs
    playlist.clear()
    song_listbox.delete(0,END)

    # Iterate through files in the directory and add MP3 files to the playlist
    for file in os.listdir(app.directory):
        name, ext = os.path.splitext(file)
        if ext.lower() == '.mp3':
            playlist.append(file)
    
    # Add songs to the listbox
    for song in playlist:
        song_listbox.insert("end", song)

    # Select the first song in the list by default, if there are any songs
    if playlist:
        song_listbox.selection_set(0)
        current_song = playlist[song_listbox.curselection()[0]]

# Function to play music
def play_music(event=None):
    global current_song, is_paused

    if not playlist:
        return
    
    # Get the selected song from the listbox
    current_selection = song_listbox.curselection()
    if current_selection:
        current_song = playlist[current_selection[0]]

    # If not paused, load and play the current song
    if not is_paused:
        pygame.mixer.music.load(os.path.join(app.directory, current_song))
        pygame.mixer.music.play()
    else:
        # If paused, unpause the music
        pygame.mixer.music.unpause()
        is_paused = False

# Function to pause music
def pause_music():
    global is_paused
    if not playlist:
        return
    pygame.mixer.music.pause()
    is_paused = True

# Function to play the next song
def next_music():
    global current_song, is_paused

    if not playlist:
        return
    
    # Clear previous selection and select the next song in the list
    try:
        song_listbox.selection_clear(0,END)
        next_index = (playlist.index(current_song)+ 1) % len(playlist)
        song_listbox.selection_set(next_index)
        current_song = playlist[song_listbox.curselection()[0]]
        is_paused = False
        play_music()
    except Exception as e:
        print("Error:", e)

def previous_music():
    global current_song, is_paused

    if not playlist:
        return
    try:
        song_listbox.selection_clear(0,END)
        next_index = (playlist.index(current_song) - 1) % len(playlist)
        song_listbox.selection_set(next_index)
        current_song = playlist[song_listbox.curselection()[0]]
        is_paused = False
        play_music()
    except Exception as e:
        print("Error:", e)

# Function to check if the music has ended
def check_music_end():
    if not pygame.mixer.music.get_busy() and not is_paused and playlist:
        next_music()
    app.after(100, check_music_end)

# Create a menu for adding songs
add_songs_menu = Menu(menu_bar, tearoff=False)
add_songs_menu.add_command(label='Select Folder', command=load_music)
menu_bar.add_cascade(label='Add Songs', menu=add_songs_menu)

# Create a listbox to display songs
song_listbox = Listbox(app, bg='green', fg='white', width=100, height=13)
song_listbox.pack()

# Bind a selection event to the listbox
song_listbox.bind('<<ListboxSelect>>', play_music)

# Load images for control buttons
play_button_image = PhotoImage(file='play_button.png')
pause_button_image = PhotoImage(file='pause_button.png')
next_button_image = PhotoImage(file='next_button.png')
previous_button_image = PhotoImage(file='previous_button.png')

# Create control buttons
control_frame = Frame(app)
control_frame.pack()

play_button = Button(control_frame, image=play_button_image, borderwidth=0, command=play_music)
pause_button = Button(control_frame, image=pause_button_image, borderwidth=0, command=pause_music)
next_button = Button(control_frame, image=next_button_image, borderwidth=0, command=next_music)
previous_button = Button(control_frame, image=previous_button_image, borderwidth=0, command=previous_music)

# Keep image references so Tkinter doesn't garbage-collect them
play_button.image = play_button_image
pause_button.image = pause_button_image
next_button.image = next_button_image
previous_button.image = previous_button_image

# Pack buttons side by side
previous_button = Button(app, text="⏮", width=15, height=3)
play_button = Button(app, text="▶", width=15, height=3)
pause_button = Button(app, text="⏸", width=15, height=3)
next_button = Button(app, text="⏭", width=15, height=3)

previous_button.pack(side="left", padx=5, pady=5)
play_button.pack(side="left", padx=5, pady=5)
pause_button.pack(side="left", padx=5, pady=5)
next_button.pack(side="left", padx=5, pady=5)

# Start checking for the end of song event
app.after(100, check_music_end)

# Start Tkinter event loop
app.mainloop()
