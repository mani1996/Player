#PLAYER
###A programmable MP3 player(wrapper over MPG123) for Linux that does the job with minimal overhead
Thanks to Rhythmbox for inspiring me to create this player

## HOW TO USE:
**player.py** is the entry point of the app.
When the app is started, the songs in the **Playlist** are shuffled
and played in the shuffled sequence, one by one. 

There are 2 modes of operation:
* **Player mode**
* **Command mode(Invoked by Ctrl + C)**

Calling command mode pauses the song being played.
The commands available in command mode are:
* **y** - Exit the player
* **p** - Previous song
* **n** - Next song
* **r** - Replay song
* **c** - Resume song

##PLAYLIST:
Playlists are at the heart of this app. Each invocation of the app
fetches a playlist and plays songs from it.

Playlist data is fetched from **playlist.json**

* This JSON file stores a collection of **Playlist** . 
  How you store the collection of Playlist 
  (JSON structure) is up to you. You need to change 
  the logic of finding **playlistSongs** in 
  **player.py(line 42)** accordingly.

* Each Playlist is a JSON Array of **Song** objects.

* Each Song object is a key-value pair of
    * **name** : Name of song
    * **pathName** : path of song in fileSystem

* **favoriteFinder.py** is a sample script that adds a **Playlist**               It searches the current directory for files ending with .mp3 and 
  asks your decision on adding it to playlist. Run it as :

  **python favoriteFinder.py**

## FIRST TIME SETUP:
* Clone the app on to your system

* Populate the **playlist.json** file as you see fit(Check
  the section above on structure of the file). You can use
  **favoriteFinder.py** for a start

* Once you set up **playlist.json**, run
  **python player.py**

* In **player.py**, the **playListSongs** variable(line 42)
  must be of type **list** and each object in the list must
  be of type **dict** with keys  *pathName* and *name*

* Once these are done,enjoy the app :)
