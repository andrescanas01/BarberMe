from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from functools import partial
from specialbuttons import LabelButton, ImageButton
import kivy.utils
from kivy.graphics import Color, Rectangle
import requests
import json


class SearchResultsBanner(FloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__()
        with self.canvas.before:
            Color(rgb=(kivy.utils.get_color_from_hex("#67697C")))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        shop = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + str(kwargs['shop_result']) + ".json")
        shopres= kwargs['shop_result']
        shopid = json.loads(shop.content.decode())
        image = ImageButton(source="images/barber2.png", size_hint=(.3, 1), pos_hint={"top": 1, "right": .3})
        label = LabelButton(text=shopid['shopname'], size_hint=(.7, 1), pos_hint={"top": 1, "right": 1},
                            on_release=partial(App.get_running_app().load_shop_page, shopid, shopres))
        self.add_widget(image)
        self.add_widget(label)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
