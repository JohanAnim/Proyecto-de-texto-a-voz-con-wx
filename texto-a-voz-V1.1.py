# /usr/bin/python
# -*- encoding: utf-8 -*-

import wx
# importar la librería de El lector de pantalla
import accessible_output2.outputs.auto

# importar el módulo requerido para convertir texto a voz
import pyttsx3
# Inicializar el motor de el lector
nvda = accessible_output2.outputs.auto.Auto()
# Inicializador del motor de voz
engine = pyttsx3.init()

class simpleapp_wx(wx.Frame):
   def __init__(self, parent, id, title):
      wx.Frame.__init__(self, parent, id, title)
      self.parent = parent

      self.initialize()
   def initialize(self):
      self.SetSize((400, 300))      

      self.panel_1 = wx.Panel(self)

      # el menubar
      self.menubar = wx.MenuBar()
      self.hablar = wx.Menu()
      hablar_1 = self.hablar.Append(wx.ID_ANY, "&Comenzar la converción de texto a voz...\tF5", "")
      self.Bind(wx.EVT_MENU, self.siPulsaBoton, hablar_1)

      hablar_3 = self.hablar.Append(wx.ID_ANY, "Borrar el historial", "")
      self.Bind(wx.EVT_MENU, self.listaBorra, hablar_3)

      hablar_2 = self.hablar.Append(wx.ID_ANY, "&Salir...\tCtrl+Q", "")
      self.Bind(wx.EVT_MENU, self.Cerrar, hablar_2)
      self.hablar.AppendSeparator()
      self.menubar.Append(self.hablar, "Acciones principales")

      self.ayuda = wx.Menu()
      ayuda_1 = self.ayuda.Append(wx.ID_ANY, "Acerca de", "")
      self.Bind(wx.EVT_MENU, self.OnButton, ayuda_1)
      ayuda_2 = self.ayuda.Append(wx.ID_ANY, "Escuchar mensaje de bienvenida", "")
      self.Bind(wx.EVT_MENU, self.HablaVoz, ayuda_2)
      self.ayuda.AppendSeparator()
      self.menubar.Append(self.ayuda, "Ayuda")
      
      self.SetMenuBar(self.menubar)
      # Aqui termina la barra de menu

      # El botón de serrar
      self.button_4 = wx.Button(self.panel_1, wx.ID_ANY, "&Cerrar", size=(150,75), pos=(10,20))
      self.button_4.Bind(wx.EVT_BUTTON, self.Cerrar)

      # Las pestañas de la app
      self.pestañas = wx.Notebook(self.panel_1, wx.ID_ANY, size=(600,800), pos=(10,100))
      # Creando los paneles contenedores
      pestaña_1 = wx.Panel(self.pestañas)
      pestaña_2 = wx.Panel(self.pestañas)
      # Añadiendo a los paneles las pestañas correspondientes
      self.pestañas.AddPage(pestaña_1, "Texto a voz")
      self.pestañas.AddPage(pestaña_2, "Historial de palabras")

      # El elemento de texto junto con sus configuraciones
      self.etiquetaLabel = wx.StaticText(pestaña_1, wx.ID_ANY, "&Escribe tu texto", size=(300,150), pos=(70,250))
      self.entrada_1 = wx.TextCtrl(pestaña_1, wx.ID_ANY, value=u"", style=wx.TE_MULTILINE)
      self.entrada_1.Bind(wx.EVT_TEXT, self.mostrarBoton)
      self.entrada_1.SetFocus()
      self.entrada_1.SetSelection(-1, -1)

      # Los botones principales
      self.button_borrar = wx.Button(pestaña_1, wx.ID_ANY, "&Borrar")
      self.button_borrar.Bind(wx.EVT_BUTTON, self.borrarTexto)
      self.button_borrar.Disable()

      self.button_1 = wx.Button(pestaña_1, wx.ID_ANY, "&Texto a voz")
      self.button_1.SetToolTip("Comienza a combertir texto a voz")
      self.button_1.Bind(wx.EVT_BUTTON, self.siPulsaBoton)

      self.etiqueta_2 = wx.StaticText(pestaña_2, wx.ID_ANY, "&Historial de palabras")
      self.lista = wx.ListBox(pestaña_2, wx.ID_ANY)
      self.lista.Bind(wx.EVT_CONTEXT_MENU, self.historialMenu)
      self.lista.Bind(wx.EVT_KEY_UP, self.historialItemsTeclas)
      self.lista.Bind(wx.EVT_SET_FOCUS, self.listaFoco)

      self.button_lista = wx.Button(pestaña_2, wx.ID_ANY, "&Vaciar historial")
      self.button_lista.Bind(wx.EVT_BUTTON, self.listaBorra)

      self.Centre()
      self.Maximize()
      self.Show(True)


   #Acción que abilita e inabilita el botón de borrar del cuadro de edición
   def mostrarBoton(self, event):
      if self.entrada_1.GetValue() == "":
         self.button_borrar.Disable()
      else:
         self.button_borrar.Enable()

   # El evento del botón que inicializa el habla y mueve la palabra en la lista del historial
   def siPulsaBoton(self, event):
      if self.entrada_1.GetValue() == "":
         wx.MessageBox("¡No se puede reproducir el contenido porque el campo de texto está bacío!, debe escribir algo.", "error.", wx.ICON_ERROR)
         self.entrada_1.SetFocus()
      else:
         engine.say(self.entrada_1.GetValue())
         agregarLista = self.lista.Append(self.entrada_1.GetValue())

   # Evento del botón que borra el texto
   def borrarTexto(self, event):
      if self.entrada_1.GetValue() == "":
         nvda.speak("No hay texto para eliminar")
      else:
         nvda.speak("Se a eliminado el texto: "+self.entrada_1.GetValue())
         self.entrada_1.Clear()
      self.entrada_1.SetFocus()

   # El submenu del historial con varias opciones
   def historialMenu(self, event):
      if self.lista.GetSelection() >= 0:
         self.historial = wx.Menu()
         historial_1 = self.historial.Append(wx.ID_ANY, "&Reproducir")
         self.Bind(wx.EVT_MENU, self.reproduceItem, historial_1)

         historial_2 = self.historial.Append(wx.ID_COPY, "&Copiar al portapapeles", "")

         historial_3 = self.historial.Append(wx.ID_ANY, "&Eliminar", "")
         self.Bind(wx.EVT_MENU, self.borrarItem, historial_3)

         position = self.lista.GetPosition()
         self.PopupMenu(self.historial, position)
         pass

   # Funcionalidad que dice el rango de la lista cuando está enfocado
   def listaFoco(self, event):
      if self.lista.GetCount() == 0:
         nvda.speak("No hay elementos en el historial")
      else:
         nvda.speak("Hay en total "+str(self.lista.GetCount())+ " elementos.")

   # Cuando se reproduce el item actual
   def reproduceItem(self, event):
      if self.lista.GetSelection() >= 0:
         engine.say(self.lista.GetString(self.lista.GetSelection()))

# Cuando se presiona el item de eliminar
   def borrarItem(self, event):
      if self.lista.GetSelection() >= 0:
         self.lista.Delete(self.lista.GetSelection())   

   def historialItemsTeclas(self, event):
      event.Skip()
      if event.GetKeyCode() == 32:
         engine.say(self.lista.GetString(self.lista.GetSelection()))

      if event.GetKeyCode() == 127:
         self.lista.Delete(self.lista.GetSelection())
         nvda.speak("Elemento eliminado, quedan "+str(self.lista.GetCount())+" elementos")

   # Botón que elimina el historial
   def listaBorra(self, event):
      rango = self.lista.GetCount()
      rango = str(rango)

      dlg = wx.MessageDialog(self, u"¿Está apunto de eliminar del historial aproximadamente "+rango+" elementos, ¿desea proseder? Está acción no se puede desacer.", u"Atención:", wx.YES_NO | wx.ICON_ASTERISK)
      if self.lista.GetCount() == 0:
         wx.MessageBox("No hay elementos que borrar", "Error", wx.ICON_ERROR)
      elif dlg.ShowModal()==wx.ID_YES:
         engine.say("Listo, se han eliminado en total "+rango+" elementos")
         self.lista.Clear()

   # Evento del botón que abre la ventana de mensaje
   def OnButton(self, event):
      dlg = wx.MessageDialog(self, 'Nombre del programa: Conversor texto a voz. Autor: Johan G. Descripción: Un pequeño programa echo en WxPython que convierte de texto a voz las palabras y la guarda en una lista.',
      'acerca de',
      wx.OK | wx.ICON_INFORMATION
      #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
      )
      dlg.ShowModal()
      dlg.Destroy()

   # Botón que da el mensaje por voz
   def HablaVoz(self, event):
      engine.say("Hola, bienvenidos a mi interfaz grafica hecho con WxPython")

   # evento del botón para serrar la ventana
   def Cerrar(self, event):
      dlg = wx.MessageDialog(self, u"¿Deseas salir del programa?", u"Pregunta:", wx.YES_NO | wx.ICON_ASTERISK)
      if dlg.ShowModal()==wx.ID_YES:
         engine.say("Hasta luego.")
         self.Close()
      else:
         self.pestañas.SetFocus()

   def ejecutarVoz(self, event):
      engine.runAndWait()

if __name__ == "__main__":
   app = wx.App()
   frame = simpleapp_wx(None,wx.ID_ANY, "Simple conversor de texto a voz.")


   app.MainLoop()