import shutil
import os

name = 'Add "RSS Large" image (22x22)'

def run(tweakdir, workingdir, ini):
	#adds a "RSS Large" image so that normal size buttons with the feed icon
	#can be created
	ini.Boxes['RSS Large'] = 'toolbar_buttons/feed_large.png'
	icons = os.path.join(workingdir, 'toolbar_buttons')
	if not os.path.isdir(icons):
		os.mkdir(icons)
	shutil.copyfile(os.path.join(tweakdir, 'icons/feed_large.png'), os.path.join(icons, 'feed_large.png'))
	