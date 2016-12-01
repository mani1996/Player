import os
import json
import sys
import copy

files = []
for fi in os.listdir(os.getcwd()):
	if os.path.isfile(os.path.join(os.getcwd(),fi)) and fi.lower().endswith('.mp3'):
		files.append((fi, os.path.join(os.getcwd(),fi)))


f = open('playlist.json','rw+')
playLists = json.loads(f.read()) # Assumption: playlists are organized as an array,to which we will append
newData = []

print 'NEW PLAYLIST'

for fi in files:
	prompt = raw_input(fi[0] + '? (y/n):')
	while prompt not in ['y','n']:
		print 'Invalid choice'
		prompt = raw_input(fi[0] + '? (y/n):')

	if prompt == 'y':
		name = raw_input('Name of song?(Leave blank to take same name):')	
		Name = name if name != '' else fi[0]
		newData.append({'name':Name, 'pathName':fi[1]})
		data1 = copy.deepcopy(playLists)
		data1.append(newData)
		f.seek(0)
		f.write(json.dumps(data1))
		f.flush()