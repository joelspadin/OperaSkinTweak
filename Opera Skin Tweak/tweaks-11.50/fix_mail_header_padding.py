
name = 'Fix Mail Header Padding'

def run(tweakdir, workingdir, ini):
	ini['Mail Header Toolbar']['Padding Top'] = '5'
	ini['Mail Header Toolbar']['Padding Bottom'] = '5'
	ini['Mail Header Toolbar']['Padding Left'] = '8'
	ini['Mail Header Toolbar']['Padding Right'] = '8'

	