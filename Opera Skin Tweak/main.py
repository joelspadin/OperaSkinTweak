
__author__="Joel Spadin"
__date__ ="$Jun 30, 2011 8:50:18 PM$"
__version__="1.2"

from iniparse import INIConfig
from Tkinter import *
import os
import os.path
import shutil
import tkFileDialog
import zipfile


 
def recursive_zip(zipf, directory, folder = ""):
	"""zips all the files in directory to zipf"""
	for item in os.listdir(directory):
		if os.path.isfile(os.path.join(directory, item)):
			zipf.write(os.path.join(directory, item), folder + os.sep + item)
		elif os.path.isdir(os.path.join(directory, item)):
			recursive_zip(zipf, os.path.join(directory, item), folder + os.sep + item)

 

class App:
	
	#debug True shows full error message in console. False shows error message
	#in app and error without stacktrace in console.
	debug = True
	
	#experimental feature to create a skin that overrides only the changed
	#sections. Doesn't quite work yet.
	custom_skin = False
	
	width = 400
	height = 244
	
	working = './working/'
	tweaks = './tweaks/'
	tempskin = './skin.zip'
	tweak_modules = []
	
	default_output = tempskin
	
	default_filenames = [
		'/Program Files/Opera/skin/standard_skin.zip',
		'/Program Files (x86)/Opera/skin/standard_skin.zip',
		'/usr/share/opera/skin/standard_skin.zip',
		'/Applications/Opera.app/Contents/Resources/Skin/standard_skin.zip',
	]
	
	original_skin_tag = '{ORIGINAL_NAME}'
	
	def __init__(self, root):
		root.minsize(self.width, self.height)
		sys.path.insert(0, self.tweaks)

		if sys.platform == 'win32':
			self.default_output = os.path.realpath(os.path.expandvars('%AppData%/Opera/Opera/skin/tweaked_skin.zip')) 
		
		self.root = root
		self.filename = StringVar()
		self.output = StringVar()
		self.output.set(self.default_output)
		self.skin_name = StringVar()
		self.skin_name.set(self.original_skin_tag + ' Tweaked')
		self.message = StringVar()
		
		#Look for a default skin file
		for fname in self.default_filenames:
			if os.path.isfile(fname):
				self.filename.set(os.path.realpath(fname))
				break;
		
		#build GUI
		frame = Frame(root)
		frame.pack(fill=BOTH, expand=1);
		
		#input/output boxes
		input = Frame(frame)
		self.input_file = Entry(input, textvariable=self.filename, width=35)
		self.input_file.pack(side=LEFT, fill=X, expand=1, padx=4, pady=4)
		
		self.input_button = Button(input, text='Load', command=self.open_file)
		self.input_button.pack(side=RIGHT, padx=4, pady=4, ipadx=8)
		input.pack(side=TOP, fill=X, padx=4);
		
		output = Frame(frame)
		self.output_file = Entry(output, textvariable=self.output)
		self.output_file.pack(side=LEFT, fill=X, expand=1, padx=4, pady=4)
		
		self.output_button = Button(output, text='Save', command=self.save_file)
		self.output_button.pack(side=RIGHT, padx=4, pady=4, ipadx=9)
		output.pack(side=TOP, fill=X, padx=4);
		
		#skin name
		name = Frame(frame)
		self.skin_name_label = Label(name, text='Skin Name')
		self.skin_name_label.pack(side=LEFT, padx=4)
		
		self.skin_name_entry = Entry(name, textvariable=self.skin_name)
		self.skin_name_entry.pack(side=RIGHT, fill=X, expand=1)
		name.pack(side=TOP, fill=X, padx=4)
		
		#tweaks list
		self.tweak_list = Listbox(frame, selectmode=MULTIPLE, height=6)
		self.tweak_list.pack(side=TOP, fill=BOTH, expand=1, padx=4, pady=4)
		
		for fname in os.listdir(self.tweaks):
			self.import_tweak(fname)
		
		#buttons and status text
		buttons = Frame(frame)
		self.run_button = Button(buttons, text='Run', command=self.run if self.debug else self.tryrun)
		self.run_button.pack(side=RIGHT, padx=4, ipadx=8)
		
		self.close_button = Button(buttons, text="Quit", command=frame.quit)
		self.close_button.pack(side=RIGHT, padx=4, ipadx=8)
		
		self.select_all_button = Button(buttons, text='Select All Tweaks', command=self.select_all)
		self.select_all_button.pack(side=RIGHT, padx=4, ipadx=8)
		
		self.message_text = Label(buttons, textvariable=self.message, anchor=W, width=25)
		self.message_text.pack(side=LEFT, fill=X, expand=1, padx=4)
		buttons.pack(side=RIGHT, fill=X, expand=1, padx=4, pady=4)
		
		#set options for open/save dialogs
		self.file_options = options = {}
		options['defaultextension'] = '.zip'
		options['filetypes'] = [('skin file', '.zip'), ('all files', '.*')]
		options['initialfile'] = 'skin.zip'
		options['parent'] = root
		options['title'] = 'Open Skin'
	
	def open_file(self):
		self.filename.set(tkFileDialog.askopenfile(mode='r', **self.file_options).name)
		
	def save_file(self):
		self.output.set(tkFileDialog.asksaveasfile(mode='w', **self.file_options).name)
		
	def import_tweak(self, fname):
		fnameinfo = os.path.splitext(fname)
		if fnameinfo[1] != '.py':
			return
		tweak = __import__(fnameinfo[0])
		
		#get the tweak's name
		try:
			name = tweak.name
		except:
			name = fname
			tweak.name = name
			
		#add the tweak to the list
		self.tweak_list.insert(END, name)
		self.tweak_modules.append(tweak)
		
		#grow the window with the number of tweaks
		if 5 < len(self.tweak_modules) < 19:
			self.height += 18
			root.minsize(self.width, self.height)
		
	def update_msg(self, text):
		print text
		self.message.set(text)
		self.root.update_idletasks()
		
	def select_all(self):
		self.tweak_list.select_set(0, END)
		
	def tryrun(self):
		try:
			self.run()
		except Exception as e:
			self.update_msg('Error.')
			print e
		
	def run(self):
		#remove the working directory if it exists
		if os.path.isdir(self.working):
			self.update_msg('Cleaning...')
			shutil.rmtree(self.working, True)
		
		if not self.custom_skin:
			self.update_msg('Extracting...')
			self.extract()
		
			#open and parse the skin's skin.ini
			self.update_msg('Opening skin.ini...')
			ini = INIConfig(open(self.working + 'skin.ini'))
		else:
			ini = self.setup_custom_skin()
		
		current_name = str(ini.Info.Name)
		ini.Info.Name = self.skin_name.get().replace(self.original_skin_tag, current_name);
		
		#run the selected tweaks
		list = self.tweak_list.curselection()
		for i in list:
			tweak = self.tweak_modules[int(i)]
			print 'Running ' + tweak.name
			self.update_msg('Running ' + tweak.name + '...')
			tweak.run(self.tweaks, self.working, ini)
		
		#save skin.ini
		self.update_msg('Saving skin.ini...')
		f = open(self.working + 'skin.ini', 'w')
		print >>f, ini
		f.close()
		
		self.update_msg('Compressing...')
		self.compress()
			
		#move the temporary skin.zip to the output location
		if os.path.realpath(self.tempskin) != os.path.realpath(self.output.get()):
			self.update_msg('Moving to output file...')
			if os.path.isfile(self.output.get()):
				os.remove(self.output.get())
			os.rename(os.path.realpath(self.tempskin), os.path.realpath(self.output.get()))
		
		#remove the working directory
		self.update_msg('Cleaning...')
		shutil.rmtree(self.working, True)
		self.update_msg('Done.')

	
	def extract(self):
		#extract the skin to the working directory
		zip = zipfile.ZipFile(self.filename.get(), 'r')
		try:
			zip.extractall(self.working)
		finally:
			zip.close()
		
	def compress(self):
		#compress the working directory to a temporary location
		if os.path.isfile(self.tempskin):
			os.remove(self.tempskin)
		zip = zipfile.ZipFile(self.tempskin, 'w', compression=zipfile.ZIP_DEFLATED)
		try:
			recursive_zip(zip, self.working)
		finally:
			zip.close()

	def setup_custom_skin(self):
		os.mkdir(self.working)
		open(self.working + 'skin.ini', 'wt').close()
		ini = INIConfig(open(self.working + 'skin.ini'))
		ini.Info.Version = '3'
		return ini
		

if __name__ == "__main__":
	root = Tk()
	root.title('Opera Skin Tweak (Featherweight)')
	
	app = App(root)
	
	root.mainloop()
