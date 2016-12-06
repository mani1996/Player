import json
import subprocess
import pynotify
import termios
import copy
import sys
import signal
import random
import time

fd = sys.stdin.fileno()
old = termios.tcgetattr(fd)
new = copy.deepcopy(old)
new[3] = new[3] & ~termios.ECHO
pynotify.init('Player-notification')

def closeHandler(a=None,b=None):
	echo(True)
	print
	print 'Thanks for using this player'
	sys.exit(0)

signal.signal(signal.SIGTSTP, closeHandler)



def intro():
	print 'PLAYER'
	print 'A programmable MP3 Player(wrapper over MPG123) that does the job with minimal overhead\n'
	print 'Press Ctrl+C for settings'


def echo(value):
	global old
	global new
	if value:
		termios.tcsetattr(fd, termios.TCSADRAIN, old)
	else:
		termios.tcsetattr(fd, termios.TCSADRAIN, new)


def songFormat(song):
	songParams = ['name', 'pathName']
	return isinstance(song,dict) and sorted(songParams) == sorted(song.keys())


'''
2 sanity checks are done below:
*	At least 1 song must be selected in playlist
*	Every song must fit the specified format for songs. This
	will help you debug if your playlist.json needs correction
'''
def sanity(playlistSongs):
	return len(playlistSongs)>0 and all(songFormat(song) for song in playlistSongs)


# Add all playlists in this dict
def recursiveAddPlaylist(playlistData):
	global playlistSongs
	if sanity(playlistData):
		playlistSongs+=playlistData
	else:
		if isinstance(playlistData,list):
			for data in playlistData:
				recursiveAddPlaylist(data)
		elif isinstance(playlistData,dict):
			for data in playlistData.values():
				recursiveAddPlaylist(data)


'''
Feature to combine playlists

Each playlist is specified as a command-line argument and
must be of format  "param1+param2+param3+..+paramN".
The above argument denotes the playlist represented by:

	playlistData[param1][param2]..[paramN]

where playlistData is the JSON object in playlist.json

NOTE: Don't use "+" in naming keys in playlist.json
'''

def addPlaylist(description):
	global playlistData
	global playlistSongs
	params = description.split('+')
	data = playlistData

	for param in params:
		try:
			if isinstance(data, list):
				data = data[int(param)]
			else:
				data = data[param]
		except Exception:
			print 'Invalid description : %s' %(description)
			return

	if sanity(data):
		playlistSongs+=data
	else:
		recursiveAddPlaylist(data)


def getNextFromPattern(pattern, sequence, index):
	global playlistSongs
	playlistLength = len(playlistSongs)
	pattern = pattern.lower()
	backupIndex = index
	index = (index + 1)%playlistLength
	while index != backupIndex:
		if playlistSongs[sequence[index]]['name'].lower().find(pattern) > -1:
			return index
		index = (index + 1)%playlistLength

	return (backupIndex if playlistSongs[sequence[backupIndex]]['name'].lower().find(pattern) 
		> -1 else -1)


def resumable(commandData):
	global playlistSongs
	global resumableCommands
	return (commandData['command'] in resumableCommands) or (commandData['command']=='f' and commandData['nextIndex'] == -1)	


playlistData = json.loads(open('playlist.json').read())
playlistSongs = []

if len(sys.argv) > 1:
	for arg in sys.argv[1:]:
		addPlaylist(arg)
else:
	recursiveAddPlaylist(playlistData)


if not sanity(playlistSongs):
	print 'Sanity check fail'
	sys.exit(0)

length = len(playlistSongs)
done = False
sequence = range(length)
notification = None
skipFrames = None
loop = False
nextIndex = -1
commands = ['y','n','p','r','c','l','f']
resumableCommands = ['c','l']

intro()

while not done:
	index = 0
	random.shuffle(sequence)
	skipFrames = None

	while index < length:
		song = playlistSongs[sequence[index]]

		if not skipFrames:
			print
			print 'Currently playing : %s' %(song['name'])

		if not notification:
			notification = pynotify.Notification('Currently playing', song['name'])
		else:
			notification.update('Currently playing', song['name'])

		notification.show()
		echo(False)

		try:
			start = time.time()

			if skipFrames != None:
				# Resume song by skipping specified number of frames
				proc = subprocess.Popen(
					['mpg123', '-k', str(skipFrames), song['pathName']],
					stdout = subprocess.PIPE,
					stderr = subprocess.PIPE
				)
			else:
				proc = subprocess.Popen(
					['mpg123', song['pathName']],
					stdout = subprocess.PIPE,
					stderr = subprocess.PIPE
				)

			err,out = proc.communicate()
			echo(True)
			if err or out.find('error') > -1:
				print
				print 'Error in playing song %s' %(song['name'])
			skipFrames = None

			if not loop:
				index = (index + 1 + length)%length
				if index == 0:
					random.shuffle(sequence)

		except KeyboardInterrupt:
			end = time.time()
			echo(True)
			prompt = 'Press (y - exit,n - next,p - previous,r - replay,c - resume,l - loop %s,f - find) and then Enter:' %('Off' if loop else 'On')
			print
			next = raw_input(prompt)

			while next not in commands:
				print
				print 'Invalid choice'
				next = raw_input(prompt)

			if next == 'y':
				done = True
				break
			elif next == 'p':
				index = (index - 1 + length)%length
			elif next in ['r','c']:
				pass
			elif next == 'n':
				index = (index + 1 + length)%length
			elif next == 'l':
				loop = not loop
			elif next == 'f':
				pattern = raw_input('Enter search string:')
				nextIndex = getNextFromPattern(pattern,sequence,index)

			data = {'command':next}
			if next == 'f':
				data['nextIndex'] = nextIndex
				if nextIndex > -1:
					index = nextIndex
				nextIndex = -1

			skipFrames = ((((end-start)*1000)/26) + (0 if skipFrames == None else skipFrames) if resumable(
				data) else None)

		except Exception as e:
			print e.message
			skipFrames = None
		finally:
			echo(True)

closeHandler()