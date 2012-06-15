
name = 'Fix typos in skin.ini'

def run(tweakdir, workingdir, ini):
	ini['Infobar Button Skin']['StretchBorder'] = '5'
	ini['Extensions Panel List Item Button']['StretchBorder'] = '6'

	