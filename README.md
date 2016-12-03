#PLAYER
###A programmable MP3 player(wrapper over MPG123) for Linux that does the job with minimal overhead
Thanks to Rhythmbox for inspiring me to create this player

## HOW TO USE:
**player.py** is the entry point of Player.
When Player is started, the songs in the **Playlist** are shuffled
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

## PLAYLIST:
Playlists are at the heart of Player. Each invocation of Player
fetches a playlist and plays songs from it.

Playlist data is fetched from **playlist.json**

* This JSON file stores a collection of **Playlist** . 
  How you store the collection of Playlist 
  (JSON structure) is up to you.

* Each Playlist is a JSON Array of **Song** objects.

* Each Song object is a key-value pair of
    * **name** : Name of song
    * **pathName** : path of song in fileSystem

* **favoriteFinder.py** is a sample script that adds a **Playlist**               .It searches the current directory for files ending with .mp3 and 
  asks your decision on adding it to playlist. Run it as :

  **python favoriteFinder.py**


## COMBINING PLAYLISTS:
**Player** allows you to combine multiple playlists to form your custom playlist for a single session.

The playlists can added as command-line arguments to **player.py**

Command-line argument for a playlist **P** is specified as 
*param1+param2+..+paramN*, if

           P = playlistJSON[param1][param2]..[paramN]


The app also allows **recursive playlist addition with partial
specifications**.

I'll explain how to use these with a simple example.
Consider the **playlist.json** in the repository. We have 3 playlists,
represented by
* **melody + 80s**
* **melody + 90s**
* **rock**

The command **python player.py melody+80s** runs the playlistJSON\["melody"]["80s"] playlist

The command **python player.py melody** is a partial specification. It includes both the **melody+80s** and **melody+90s** playlists. Easy right? :)

The command **python player.py melody rock** includes the **melody** playlists
as well as the only **rock** playlist in **playlist.json** 

## FIRST TIME SETUP:
* Clone the app on to your system

* Populate the **playlist.json** file as you see fit(Check
  the section above on structure of the file). You can use
  **favoriteFinder.py** for a start

* Once you set up **playlist.json**, run
  **python player.py** (Check instructions above to
  combine playlists).

* Enjoy :)
