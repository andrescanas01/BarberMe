
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivymd.uix.list import MDList, OneLineListItem, BaseListItem, TwoLineAvatarIconListItem, TwoLineAvatarListItem
from kivy.uix.scrollview import ScrollView
import requests
import json
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
import requests
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
from threading import Thread

class FavoriteScreen(Screen):

    show_search = False

    def Search(self):
        # TODO switch to shop search
        print("search works")
        self.show_search = True
        self.ids['favorites_label'].opacity = 1 - self.ids['favorites_label'].opacity
        self.ids['favorites_search'].opacity = 1 - self.ids['favorites_search'].opacity

    def addFavorite(self):
        # TODO switch to favorite
        print("add works")

    def remove_widget(self, widget):
        self.remove_widget(widget)




class FavoriteListItem(TwoLineAvatarIconListItem):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.app = MDApp.get_running_app()
        fave = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + str(kwargs['favorite_shop']) + ".json")
        self.shop_id = kwargs['favorite_shop']
        self.favorite = json.loads(fave.content.decode())
        self.text = "[size=35]%s[/size]" % self.favorite['shopname']
        self.secondary_text = "[size=25]%s[/size]" % self.favorite['post']
        #self.source = "images/barber.png"
        self.height = "80dp"


    def on_release(self):


        App.get_running_app().load_shop_page(self.favorite, self.shop_id)

        #except:
        #    print("Didnt work")


    # TODO go to shop page screen
    def accessShop(self):
        print("it works")

    def onButtonPress(self):
        print(App.get_running_app().user_localId)
        layout = GridLayout(cols = 1, padding = 10)

        self.dialog = MDDialog(
            title="Remove Shop?",
            text="This will remove the shop from your favorites list.",
            size_hint=(.7, .7),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=partial(self.cancel)
                ),
                MDFlatButton(

                    text="REMOVE",
                    on_release=partial(self.confirm)


                ),
            ],

        )
        self.dialog.open()


   # def confirm(self, popup, button):
    def confirm(self, button):
        req = requests.delete("https://nappyhour-6eb5d.firebaseio.com/" + str(App.get_running_app().user_localId) +
                              "/favorites/" + str(self.shop_id) + ".json")
        print(self.shop_id)
        print(req.ok)
        self.parent.remove_widget(self)

        #self.parent.parent.ids['userpage'].refresh_carousel()
        #popup.dismiss()
        #App.get_running_app().favorites_list.remove(self.shop_id)
        App.get_running_app().favorites_list.remove(self.shop_id)
        App.get_running_app().root.ids['userpage'].ids['favorites_carousel'].clear_widgets()
        App.get_running_app().root.ids['userpage'].load_carousel()

        self.dialog.dismiss()

    #def cancel(self, popup, button):
    def cancel(self, button):
        self.dialog.dismiss()

class FavoriteList(MDList):
    pass


class FavoriteApp(MDApp):
    def build(self):
        return FavoriteScreen()


if __name__ == '__main__':
    FavoriteApp().run()