# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from os.path import dirname, join, basename
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
import os
import re
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import zipfile
import shutil
from kivy.base import EventLoop
from kivy.utils import platform

EventLoop.ensure_window()





class ImagenScreen(BoxLayout):
	source = StringProperty(None)
	indice = NumericProperty(0)
	lista = ListProperty()
	maximo = NumericProperty(0)
	slider_value = NumericProperty(0)
	label_text=StringProperty("")
	
	#lista length
	def largo_lista(self):
		return len(self.lista) -1
		
	def on_lista(self, instance, value):
		self.maximo=self.largo_lista()
		
	def put_image(self, lista, indice):
		self.indice =(int)(indice)
		self.lista = lista
		self.label_text = (str)(self.indice+1)+"/"+(str)(self.largo_lista()+1)
		self.slider_value = (int)(indice)
		if(self.indice != -1) and (lista != []):
			self.source = self.lista[self.indice]
		else: print "indice: ", indice, "error no esperado"
	
	def previous(self):
		if(self.indice==0):
			error_anterior = Popup(title="Error", content=Label(text="No previous"), size_hint=(0.5,0.5))
			error_anterior.open()
		else:
			self.clear_widgets()
			self.__init__()
			self.put_image(self.lista, self.indice -1)
			
	def next(self):
		if(self.indice==(len(self.lista)-1)):
			error_siguiente = Popup(title="Error", content=Label(text="No next"), size_hint=(0.5,0.5))
			error_siguiente.open()
		else:
			self.clear_widgets()
			self.__init__()
			self.put_image(self.lista, self.indice +1)
			
	def backToMenu(self):
		self.clear_widgets()
		self.add_widget(MenuScreen(path_dir = dirname(self.lista[self.indice])))

	def change_image_slider(self, instance, value):
	#the if is because the function is called too much times
		if(value!=self.slider_value):
			self.clear_widgets()
			self.__init__()
			self.put_image(self.lista, value)


class ImagenScreen_archivo(BoxLayout):
	source = StringProperty(None)
	indice = NumericProperty(0)
	lista = ListProperty()
	maximo = NumericProperty(0)
	archivo = ObjectProperty()
	slider_value = NumericProperty(0)
	label_text=StringProperty("")
	directory = ".mangavisor_tmp"
	path_dir = StringProperty("/")
	
	#lista length
	def largo_lista(self):
		return len(self.lista) -1	
		
	def on_lista(self, instance, value):
		self.maximo=self.largo_lista()
		
	def put_image(self, lista, indice, archivo_objeto):
		self.indice =(int)(indice)
		self.lista = lista
		self.archivo =  archivo_objeto
		self.slider_value = (int)(indice)
		self.label_text = (str)(self.indice+1)+"/"+(str)(self.largo_lista()+1)
		shutil.rmtree(self.directory, True)
		if(self.indice != -1) and (self.lista != []):
			imagen = archivo_objeto.extract(unicode(self.lista[self.indice]), ".mangavisor_tmp")
			filename = self.lista[self.indice]
			self.source = join(self.directory, filename.replace("\\", "/"))
		else: print "error inesperado"
		
	
	def previous(self):
		if(self.indice==0):
			error_anterior = Popup(title="Error", content=Label(text="No previous"), size_hint=(0.5,0.5))
			error_anterior.open()
		else:
			self.clear_widgets()
			self.__init__(path_dir = self.path_dir)
			self.put_image(self.lista, self.indice -1, self.archivo)
		
	def next(self):
		if(self.indice==(len(self.lista)-1)):
			error_siguiente = Popup(title="Error", content=Label(text="No next"), size_hint=(0.5,0.5))
			error_siguiente.open()
		else:
			self.clear_widgets()
			self.__init__(path_dir = self.path_dir)
			self.put_image(self.lista, self.indice +1, self.archivo)
	
	def backToMenu(self):
		self.clear_widgets()
		self.add_widget(MenuScreen(path_dir = self.path_dir))
		
	def change_image_slider(self, instance, value):
	#the if is because the function is called too much times
		if(value!=self.slider_value):
			self.clear_widgets()
			self.__init__(path_dir = self.path_dir)
			self.put_image(self.lista, value, self.archivo)


class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)
	filechooser = ObjectProperty(None)
	def __init__(self, **kwargs):
		super(LoadDialog, self).__init__(**kwargs)
		self.drives_list.adapter.bind(on_selection_change=self.drive_selection_changed)
	def get_win_drives(self):
		if platform == 'win':
			import win32api
			drives = win32api.GetLogicalDriveStrings()
			drives = drives.split('\000')[:-1]
			return drives
		else:    
			return []

	def drive_selection_changed(self, *args):
		selected_item = args[0].selection[0].text
		self.filechooser.path = selected_item

class MenuScreen(StackLayout):
	
	loadfile = ObjectProperty(None)
	text_input = ObjectProperty(None)
	path_dir = StringProperty("/")

	def dismiss_popup(self):
		self._popup.dismiss()

	def show_load_archivo(self):
		content = LoadDialog(load=self.load_archivo, cancel=self.dismiss_popup, path_dir= self.path_dir)
		self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
		self._popup.open()
		
	def load_archivo(self, path, filename):
		self.dismiss_popup()
		if(filename==[]):
			error_no_encontrado = Popup(title="Error", content=Label(text="No file"), size_hint=(0.5,0.5))
			error_no_encontrado.open()
		else:
			self.clear_widgets()
			#Zipfile part
			if(zipfile.is_zipfile(filename[0])):
				archivo = zipfile.ZipFile(filename[0], mode="r")
				#regular expression to select jpg, bmp, png, jpeg, and gif, in lower or upper case
				#Now works with Every zip and cbz
				lista = archivo.namelist()
				res = [unicode(f) for f in lista if re.match(u".+(\\.(?i)([jJ][pP][gG]|[pP][nN][gG]|[gG][iI][fF]|[bB][mM][pP]|[jJ][pP][eE][gG]))$", f)]
				if(res==[]):
					error_no_encontrado = Popup(title="Error", content=Label(text="No compatible files inside the file"), size_hint=(0.5,0.5))
					error_no_encontrado.open()
					self.add_widget(MenuScreen())
				else:
					res.sort()
					self.clear_widgets()
					img_archivo = ImagenScreen_archivo(path_dir = path)
					img_archivo.put_image(lista=res, indice=0, archivo_objeto=archivo)
					self.add_widget(img_archivo)
					
			#End Zipfile part	
			
			
			else:
				error_no_encontrado = Popup(title="Error", content=Label(text="Don't select compatible file"), size_hint=(0.5,0.5))
				error_no_encontrado.open()
				self.add_widget(MenuScreen())	
	
		
	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup, path_dir= self.path_dir)
		self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
		self._popup.open()

	def load(self, path, filename):
		self.path_dir = path
		res = [f for f in os.listdir(unicode(path)) if re.match(".+(\\.(?i)([jJ][pP][gG]|[pP][nN][gG]|[gG][iI][fF]|[bB][mM][pP]|[jJ][pP][eE][gG]))$", f)]
		self.dismiss_popup()
		res.sort()
		lista_res = []
		indice=0
		#Search for the selected file, if not, select the first one
		for x in xrange(len(res)):
			lista_res.append(join(path, res[x]))
			if(filename!=[]) and (filename[0]==lista_res[x]):
				indice=x
			if(filename== []):
				indice=0
		if (lista_res == []):
			error_no_encontrado = Popup(title="Error", content=Label(text="No compatible files in the folder"), size_hint=(0.5,0.5))
			error_no_encontrado.open()
		else:
			self.clear_widgets()
			img = ImagenScreen()
			img.put_image(lista=lista_res, indice=indice)
			self.add_widget(img)
		


class main(App):
	def build(self):
		return MenuScreen()
		
	def on_pause(self):
		return True
	
	def on_resume(self):
		pass
		
if __name__ == '__main__':
    main().run()
