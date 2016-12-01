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


def intro():
	print 'PLAYER'
	print 'A programmable MP3 Player(wrapper over MPG123) that does the job with minimal overhead\n'
	print 'Press Ctrl+C for settings'


def closeHandler(a=None,b=None):
	echo(True)
	print
	print 'Thanks for using this player'
	sys.exit(0)


def echo(value):
	global old
	global new
	if value:
		termios.tcsetattr(fd, termios.TCSADRAIN, old)
	else:
		termios.tcsetattr(fd, termios.TCSADRAIN, new)


signal.signal(signal.SIGTSTP, closeHandler)

playlistSongs = json.loads(open('playlist.json').read())[0]
length = len(playlistSongs)

done = False
sequence = range(length)
notification = None
skipFrames = None
intro()

while not done:
	random.shuffle(sequence)
	index = 0
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
		except KeyboardInterrupt:
			end = time.time()
			echo(True)
			prompt = 'Press (y - exit,n - next,p - previous,r - replay,c - resume) and then Enter:'
			print
			next = raw_input(prompt)
			while next not in ['y','n','p','r','c']:
				print
				print 'Invalid choice'
				next = raw_input(prompt)

			if next == 'y':
				done = True
				break
			elif next == 'p':
				index = (index - 2 + length)%length
			elif next in ['r','c']:
				index = (index - 1 + length)%length

			skipFrames = ((((end-start)*1000)/26) + (0 if skipFrames == None else skipFrames) if next == 'c' 
				else None)

		except Exception as e:
			print e.message
			skipFrames = None
		finally:
			echo(True)
			index = (index + 1)%length

closeHandler()