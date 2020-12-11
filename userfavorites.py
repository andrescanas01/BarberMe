from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle, Line
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatIconButton, MDIconButton
from kivy.uix.image import Image
from kivy.graphics import BorderImage

class UserFavorite(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__()
        self.pos_hint= {"x": .07}
        self.size_hint = (.86,1)
        with self.canvas.before:
            Color(rgba = (0/255,51/255,78/255,.03))
            self.rect = RoundedRectangle(radius=[(20, 20)])

        self.bind(pos=self.update_rect, size=self.update_rect)

        self.name = MDLabel(text="[color=00334e][size=45]%s[/size][/color]" % kwargs["name"],
                            pos_hint={"center_x": .5, "top": .95}, size_hint=(.5, .025)
                            ,halign="center", markup = True)

        self.description = MDLabel(text="[color=00334e][size=28]%s[/size][/color]" % kwargs["description"],
                            pos_hint={"center_x": .5, "top": .08}, size_hint=(.95, .025),
                             halign="center", markup = True)

        self.image = Image(pos_hint={"center_x": .5, "center_y": .5}, size_hint=(.7, .7),
                           source=kwargs["source"], allow_stretch=True)


        self.add_widget(self.name)
        self.add_widget(self.image)
        self.add_widget(self.description)


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size