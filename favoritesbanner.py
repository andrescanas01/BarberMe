from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from functools import partial
from specialbuttons import LabelButton, ImageButton
import kivy.utils
from kivy.graphics import Color, Rectangle
import requests
import json


class FavoritesBanner(FloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__()
        with self.canvas.before:
            Color(rgb=(kivy.utils.get_color_from_hex("#67697C")))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        fave = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + str(kwargs['favorite_shop']) + ".json")
        faveid = json.loads(fave.content.decode())
        print(kwargs['favorite_shop'])
        image = ImageButton(source="images/barber.png", size_hint=(.3, 1), pos_hint={"top": 1, "right": .3})
        label = LabelButton(text=faveid['shopname'], size_hint=(.7, 1), pos_hint={"top": 1, "right": 1},
                            on_release=partial(App.get_running_app().load_shop_page, str(kwargs['favorite_shop'])))
        self.add_widget(image)
        self.add_widget(label)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
