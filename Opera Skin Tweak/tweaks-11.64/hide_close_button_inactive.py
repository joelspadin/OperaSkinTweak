
name = 'Hide close button on inactive tabs'

def run(tweakdir, workingdir, ini):
	ini['Pagebar Close Button Skin']['Width'] = '0'
	ini['Pagebar Close Button Skin']['Height'] = '0'
	ini['Pagebar Close Button Skin']['Margin Left'] = '4'
	
	ini['Pagebar Close Button Skin.selected']['Clone'] = 'Pagebar Close Button Skin'
	ini['Pagebar Close Button Skin.selected']['Width'] = '16'
	ini['Pagebar Close Button Skin.selected']['Height'] = '16'
	ini['Pagebar Close Button Skin.selected']['Margin Left'] = '0'
	
	ini['Pagebar Close Button Skin.selected.hover']['Clone'] = 'Pagebar Close Button Skin.hover'
	ini['Pagebar Close Button Skin.selected.hover']['Width'] = '16'
	ini['Pagebar Close Button Skin.selected.hover']['Height'] = '16'
	ini['Pagebar Close Button Skin.selected.hover']['Margin Left'] = '0'
	
	ini['Pagebar Maximize Button Skin']['Width'] = '16'
	ini['Pagebar Maximize Button Skin']['Height'] = '16'
	
	ini['Pagebar Minimize Button Skin']['Width'] = '16'
	ini['Pagebar Minimize Button Skin']['Height'] = '16'
	
	
	