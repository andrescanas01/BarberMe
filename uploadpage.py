from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.textinput import TextInput
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import json
import requests
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
import datetime
from kivy.clock import Clock
import functools
from threading import Thread
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from shutil import copyfile
import os

class ChooseFile(FloatLayout):
    close = ObjectProperty(None)

class UploadPageScreen(Screen):

    def closeChooser(self):
        self.popupWindow.dismiss()

    def openFileChooser(self):
        content = ChooseFile(close = self.closeChooser)
        self.popupWindow = Popup(title="Select an image/video", content = content)
        self.popupWindow.open()