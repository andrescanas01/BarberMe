from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from functools import partial
from specialbuttons import LabelButton, ImageButton
import kivy.utils
from kivy.graphics import Color, Rectangle
import requests
import json


class BookingBanner(FloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__()
        with self.canvas.before:
            Color(rgb=(kivy.utils.get_color_from_hex("#67697C")))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        print("CHECKING BOOKING SLOTS FUNCTION CALL")

        picked = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + str(kwargs['shop_result']) + "/availability/" + str(kwargs['date_result']) + ".json")
        #print(self.shopid)
        #print(self.date)
        print(str(kwargs['shop_result']))
        print(str(kwargs['date_result']))
        #print(str(kwargs['booking_result']))
        print("CHECKING BOOKING SLOTS")

        timeid = json.loads(picked.content.decode())
        if timeid[str(kwargs['booking_result'])]:
            # image = ImageButton(source="images/barber2.png", size_hint=(.3, 1), pos_hint={"top": 1, "right": .3})
            label = LabelButton(text=str(kwargs['booking_result']), size_hint=(.7, 1), pos_hint={"top": 1, "right": 1},
                                on_release=partial(App.get_running_app().load_confirmation_page, kwargs['booking_result'], kwargs['date_result']))
            # self.add_widget(image)
            self.add_widget(label)


        print(timeid)


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
