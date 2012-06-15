import shutil
import os

name = 'Add "RSS Large" image (22x22)'

def run(tweakdir, workingdir, ini):
	#adds a "RSS Large" image so that normal size buttons with the feed icon
	#can be created
	ini.Boxes['RSS Large'] = 'buttons/feed_large.png'
	buttons = os.path.join(workingdir, 'buttons')
	if not os.path.isdir(buttons):
		os.mkdir(buttons)
	shutil.copyfile(os.path.join(tweakdir, 'buttons/feed_large.png'), os.path.join(buttons, 'feed_large.png'))
	