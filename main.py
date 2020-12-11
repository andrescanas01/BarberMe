# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from FirebaseLoginScreen import firebaseloginscreen as fb
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import glob
from plyer import notification
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
from favoritesbanner import FavoritesBanner
from searchresultsbanner import SearchResultsBanner
from specialbuttons import ImageButton, LabelButton
from favorites import *
from uploadpage import *
import datetime
from kivy.clock import Clock
import functools
from threading import Thread
from kivymd.uix.picker import MDDatePicker, MDTimePicker
import certifi
from json import dumps
from userfavorites import UserFavorite
from kivy.uix.screenmanager import SlideTransition
from kivy.properties import BooleanProperty, StringProperty
import os
import webbrowser
from pgeocode import GeoDistance
from operator import itemgetter
from send_sms import *
from bookingbanner import BookingBanner

class UserPage(Screen):

    carousel: object

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_kv_post(self, base_widget):
        self.carousel = self.ids["favorites_carousel"]
        Clock.schedule_interval(self.carousel.load_next, 7)

    def refresh_carousel(self, *args):
        Clock.schedule_once(self.load_carousel())

    def load_carousel(self, *args):

        print("YESSSSSSSS")
        print(self.app.favorites_list)
        if not self.app.favorites_list:
            self.carousel.add_widget(MDLabel(text="Start searching for shops below!", halign="center"))

        else:

            for favorite in self.app.favorites_list:
                if favorite != " ":
                    fave = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + favorite + ".json")
                    fave_json = json.loads(fave.content.decode())
                    print(fave_json)
                    print("OOOOKKKKK")


                    layout = UserFavorite(name=fave_json['shopname'], source=f"{fave_json['content']}", description=fave_json['post'])
                    self.carousel.add_widget(layout)





class UploadPageScreen(Screen):
    pass


class ShopScreen(Screen):

    shop_id= None
    user_localId = None
    content = ""
    post = ""
    shopname = ""
    flink = ""
    ilink = ""


    # add_fave function
    def add_fave(self):



        faves = []
        req = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + "/favorites.json")
        data = json.loads(req.content.decode())
        data_keys = data.keys()

        if self.shop_id in data_keys:
            return


        fave_info = '{"%s": "true"}' % (self.shop_id)
        follower_info = '{"%s": "true"}' % (self.user_localId)



            # fave_info = '{"%s": "true"}' % (fave_addition)
            #fave_info = '{"8h6FXOxXT4SU3WcAGNb5rsddr8w1": "true"}'
        requests.patch("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + "/favorites.json",
                           data=fave_info)

        requests.patch("https://nappyhour-6eb5d.firebaseio.com/" + self.shop_id + "/favorites.json",
                       data=follower_info)

        display_new_star = self.ids['star']
        display_new_star.icon = "star"

        self.parent.parent.ids['fscreen'].ids['favorites_grid'].add_widget(FavoriteListItem(favorite_shop=self.shop_id))

        self.parent.parent.ids['userpage'].ids["favorites_carousel"].add_widget(UserFavorite(name=self.shopname, source=self.content, description=self.post))
        App.get_running_app().favorites_list.append(self.shop_id)
        #print(data)


    def open_media(self, media_id, media):

        url = ""
        if media == "facebook":
            url = "https://www.facebook.com/"
        else:
            url = "https://www.instagram.com/"
        try:
            request = webbrowser.open(url + media_id)

        except:
            print("Not open")






class ShopHomePage(Screen):
    pass


class SearchResultsScreen(Screen):
    pass


class SearchPageScreen(Screen):
    pass


class PostPageScreen(Screen):
    pass


class AddOrDeleteDeal(Screen):
    pass


class EditAccountScreen(Screen):

    #firebase project api key
    api_key = "AIzaSyBAz-5OMQ7lo0kbXvWn-rFCo39IkUUgwkM"

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    #confirmation diaglog for account sensitive edit options
    def confirmation(self, title, text, confirm):
        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(.7, .7),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=partial(self.cancel)
                ),
                MDFlatButton(

                    text="CONFIRM",
                    on_release=partial(confirm)

                ),
            ],

        )
        self.dialog.open()

    def cancel(self,button):
        self.dialog.dismiss()

    #send an email to user to reset password. Email template can be changed on Firebase Project.
    def reset_password(self, button):

        email = ""

        try:
            #get email
            email = self.get_account_info()['users'][0]['email']

        except:
            pass

        reset_pw_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key=" + self.api_key
        reset_pw_data = dumps({"email": email, "requestType": "PASSWORD_RESET"})

        UrlRequest(reset_pw_url, req_body=reset_pw_data,
                   on_success=self.successful_reset,
                   on_failure=self.reset_failure,
                   ca_file=certifi.where())
        self.dialog.dismiss()

    #function to obtain account info from user id using google api
    def get_account_info(self):

        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={0}".format(
            self.api_key)
        data = json.dumps({"idToken": self.app.user_idToken})
        request_object = requests.post(request_ref,  data=data)
        return request_object.json()

    #if reset fails
    def reset_failure(self, *args):

        print("INVALID: TRY AGAIN")

    #sign out of app - revert to welcome screen
    def sign_out(self, button):

        refresh_token_file = App.get_running_app().user_data_dir + "/refresh_token.txt"
        #remove automatic login token
        if os.path.exists(refresh_token_file):
            os.remove(refresh_token_file)

        #switch firebase login screenmanager to welcome screen
        self.app.root.ids['firebase_login_screen'].ids['screen_manager'].current = "welcome_screen"
        self.dialog.dismiss()
        #switch main screenmanager to firebase_login_screen
        Clock.schedule_once(functools.partial(self.app.change_screen,"firebase_login_screen"))
        #reset all app logic
        self.app.reset()



    def delete_account(self, button):

        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/deleteAccount?key={0}".format(
            self.api_key)
        data = json.dumps({"idToken": self.app.user_idToken})
        request_object = requests.post(request_ref, data=data)
        refresh_token_file = App.get_running_app().user_data_dir + "/refresh_token.txt"
        if os.path.exists(refresh_token_file):
            os.remove(refresh_token_file)
        self.app.delete_account()
        self.dialog.dismiss()
        #exit app
        self.app.stop()




    def successful_reset(self, urlrequest, reset_data):
        """Notifies the user that a password reset email has been sent to them.
        """
        print("Successfully sent a password reset email", reset_data)





class ForgotPasswordScreen(Screen):
    pass


class BookApptScreen(Screen):
    pass

class PromotionPageScreen(Screen):
    pass

class AddOrDeleteVideo(Screen):
    pass

class ChooseSocialPage(Screen):
    pass

class FacebookPage(Screen):

    insta_message = StringProperty()
    insta = BooleanProperty(False)
    fb_message = StringProperty()
    fb = BooleanProperty(False)

    def insta_check(self, text, confirm):

        if not text:
            self.insta_message = "Please enter an Instagram link"
            self.insta = True

        else:
            confirm(text)

    def fb_check(self,text,confirm):

        if not text:

            self.fb_message = "Please enter a Facebook link"
            self.fb = True

        else:
            confirm(text)

    def set_fb(self, fbtext):

        try:
            url = "https://www.facebook.com/"
            request = webbrowser.open(url + fbtext)

            if not request:
                self.fb_message = "Invalid Facebook URL"
                self.fb = True
            print("OH SO WE GOT HERE")
            print(request)

        except:

            self.fb_message = "Invalid Facebook URL"
            self.fb = True

    def confirm_fb(self, fbtext):

        facebook_data = '{"facebook_id": "%s"}' % (fbtext)
        requests.patch("https://nappyhour-6eb5d.firebaseio.com/" + App.get_running_app().user_localId + ".json", data=facebook_data)

    def set_insta(self, instatext):

        try:
            url = "https://www.instagram.com/"
            request = webbrowser.open(url + instatext)

            if not request:
                self.insta_message = "Invalid Facebook URL"
                self.insta = True

        except:

            self.insta_message = "Invalid Facebook URL"
            self.insta = True

    def confirm_insta(self, instatext):
        insta_data = '{"insta_id": "%s"}' % (instatext)
        requests.patch("https://nappyhour-6eb5d.firebaseio.com/" + App.get_running_app().user_localId + ".json", data=insta_data)



class InstagramPage(Screen):
    pass

class ChangePasswordPage(Screen):
    pass

class BookApptScreen(Screen):

    shop_id = None
    user_localId = None

    # def time_slot_display(self):
    #     shops = []
    #
    #     results = requests.get("https://nappyhour-6eb5d.firebaseio.com/.json" + self.shopid + "/timeslots.json")
    #     user_info = json.loads(results.content.decode())
    #
    #     user_info_keys = user_info.keys()
    #     for key in user_info_keys:
    #         try:
    #             if user_info[key]['admin']:
    #                 if searchedText in user_info[key]['shopname']:
    #                     shops.append(key)
    #         except:
    #             print("error11111")
    #
    #     print(shops)
    #     search_results_grid = self.root.ids['srscreen'].ids['search_results_grid']
    #     for result in shops:
    #         print(result)
    #         result_item = SearchResultsBanner(shop_result=result)
    #         search_results_grid.add_widget(result_item)
    #
    #     self.change_screen("srscreen")


class DatePickerScreen(Screen):
    pass

class DistanceOrNameScreen(Screen):
    pass


class SearchByDistScreen(Screen):
    pass

class ConfirmationApptScreen(Screen):
    pass




Builder.load_file("kvs/userpage.kv")
Builder.load_file("kvs/favorites.kv")
Builder.load_file("kvs/shopscreen.kv")
Builder.load_file("kvs/searchpage.kv")
Builder.load_file("kvs/uploadpage.kv")
Builder.load_file("kvs/postpage.kv")
Builder.load_file("kvs/searchresults.kv")
Builder.load_file("kvs/shophomepage.kv")
Builder.load_file("kvs/addordeletepage.kv")
Builder.load_file("kvs/editaccount.kv")
Builder.load_file("kvs/forgotpassword.kv")
Builder.load_file("kvs/bookapptscreen.kv")
Builder.load_file("kvs/promotionpage.kv")
Builder.load_file("kvs/addordeletevideopage.kv")
Builder.load_file("kvs/datepicker.kv")
Builder.load_file("kvs/choosesocialmedia.kv")
Builder.load_file("kvs/facebookpage.kv")
Builder.load_file("kvs/instagrampage.kv")
Builder.load_file("kvs/changepassword.kv")
Builder.load_file("kvs/distanceorname.kv")
Builder.load_file("kvs/searchbydist.kv")
Builder.load_file("kvs/confirmationapptpage.kv")



# gui = Builder.load_file("main.kv")

class MainApp(MDApp):

    favorites_list = []
    url = 'https://nappyhour-6eb5d.firebaseio.com/.json'
    dialog = None
    user_localId = None
    user_idToken = None
    user_info = {}
    screen_stack = []

    def __init__(self):
        Window.size = (400, 600)
        super().__init__()

    def on_start(self):
        try:
            print(self.user_localId)
        except:
            print("error")

    def notify_users(self, Notify_Title, Notify_Content):

        notification.notify(title=Notify_Title, message=Notify_Content, timeout=10, app_icon=None)

    def post_deal(self, dealText, duration):

        try:
            now = datetime.datetime.now()
            date_time = datetime.datetime.combine(now.date(), datetime.time(int(duration), 0))
            exptime = date_time.strftime("%m/%d/%Y, %H:%M:%S")
            shop_info = '{"post":"%s", "expiration":"%s"}' % (dealText,  exptime)
            requests.patch("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + ".json", data=shop_info)

            # req = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + "/favorites.json")
            req = requests.get("https://nappyhour-6eb5d.firebaseio.com/.json")
            data = json.loads(req.content.decode())
            shop_data = data[self.user_localId]['favorites']
            data_keys = shop_data.keys()

            for fave in data_keys:
                try:
                    usernum = data[fave]['phone']
                    username = data[fave]['username']
                    shopname = data[self.user_localId]['shopname']
                    send_test(usernum, username, shopname)
                except:
                    print("invalid phone number or shop id")

        except:
            pass

        self.change_screen("shophomepage")


    def set_up(self):

        result = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + ".json")
        data = json.loads(result.content.decode())
        self.user_info = data
        self.screen_stack = []
        try:
            print("SETTING UPPP")
            if data['admin']:
                welcome_label = self.root.ids['shophomepage'].ids['welcome_label']
                welcome_label.text = "Hi, %s shop!" % (data['shopname'])
                self.change_screen("shophomepage")
                self.root.ids['editaccount'].ids['addmedia'].opacity = 1
                self.root.ids['editaccount'].ids['addmedia'].disabled = False

            else:
                welcome_label = self.root.ids['userpage'].ids['welcome_label']
                welcome_label.text = "Hi, %s!" % (data['username'])
                print("SET UP FUNCTIOM")
                self.favorites_list = list(data['favorites'].keys())
                if self.favorites_list[0].strip() == "":
                    self.favorites_list.pop(0)
                print(self.favorites_list)
                print(self.favorites_list)
                print("BEFREEEE")
                self.load_usergrid()
                self.change_screen("userpage")

                # Clock.schedule_once(functools.partial(self.show_favorites), 1.5)
                self.show_favorites()

        except:
            pass

            # t = Thread(target=self.show_favorites).start()

    def load_usergrid(self):
        userpage_grid = self.root.ids['userpage']
        userpage_grid.load_carousel()

    def show_favorites(self, *args):

        #result = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + ".json")
        #data = json.loads(result.content.decode())
        data = self.user_info

        # Get friends list
        favorites_grid = self.root.ids['fscreen'].ids['favorites_grid']
        favorites_dict = data['favorites']
        favorites_keys = favorites_dict.keys()
        for favorite in favorites_keys:
            if favorite != " ":
                faveitem = FavoriteListItem(favorite_shop=favorite)
                favorites_grid.add_widget(faveitem)

    def change_screen(self, screen_name, *args):

        screen = self.root.ids['screen_manager']
        self.screen_stack.append(screen.current)
        screen.current = screen_name

    #HEREEEEEEEEEEEE
    def load_shop_page(self, data, shop_id, *args):
        #fave_req = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + str(friendid) + ".json")
        global shopid
        shopid = shop_id
        shop_name = self.root.ids['shopscreen'].ids['shop_name']
        print(data)
        shop_name.text = data['shopname']

        #print(data)

        shop_image = self.root.ids['shopscreen'].ids['shop_image']
        shop_image.source = data['content']

        #store all shop info on shop screen
        ShopScreen.shop_id = shop_id
        ShopScreen.shopname = data['shopname']
        ShopScreen.content = data['content']
        ShopScreen.post = data['post']
        ShopScreen.flink = data['facebook_id']
        ShopScreen.ilink = data['insta_id']
        ShopScreen.user_localId = self.user_localId

        BookApptScreen.shop_id = shop_id
        BookApptScreen.user_localId = self.user_localId

        print(ShopScreen.shop_id)

        exp = datetime.datetime.strptime(data['expiration'], "%m/%d/%Y, %H:%M:%S")
        now = datetime.datetime.strptime(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "%m/%d/%Y, %H:%M:%S")
        timecompare = now > exp
        shop_expiration = self.root.ids['shopscreen'].ids['shop_deal']
        if timecompare:
            shop_expiration.text = "This shop currently does not offer any promotions."
        else:
            shop_expiration.text = data['post']

        self.root.ids['screen_manager'].transition = SlideTransition(direction="left")
        self.change_screen("shopscreen")

    def search_by_name(self, searchedText):

        shops = []

        results = requests.get("https://nappyhour-6eb5d.firebaseio.com/.json")
        user_info = json.loads(results.content.decode())

        user_info_keys = user_info.keys()
        for key in user_info_keys:
            try:
                if user_info[key]['admin']:
                    if searchedText in user_info[key]['shopname']:
                        shops.append(key)
            except:
                print("error11111")

        print(shops)
        search_results_grid = self.root.ids['srscreen'].ids['search_results_grid']
        for result in shops:
            print(result)
            result_item = SearchResultsBanner(shop_result=result)
            search_results_grid.add_widget(result_item)

        self.change_screen("srscreen")


    def delete_promotion(self):
        #now = datetime.datetime.now()
        #date_time = datetime.datetime.combine(now.date(), datetime.time(int(duration), 0))
        #exptime = date_time.strftime("%m/%d/%Y, %H:%M:%S")

        #now = datetime.datetime.strptime(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "%m/%d/%Y, %H:%M:%S")
        now= datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print(now)
        empty_promo = "This shop currently does not offer any promotions."
        shop_info = '{"post":"%s", "expiration":"%s"}' % (empty_promo, now)
        requests.patch("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + ".json", data=shop_info)

        self.change_screen("shophomepage")

    def delete_account(self):
        # requests.delete("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + ".json")
        #print("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + ".json")
        # auth.delete_user(self.user_localId)
        results = requests.get("https://nappyhour-6eb5d.firebaseio.com/.json")

        user_info = json.loads(results.content.decode())

        user_info_keys = user_info.keys()
        for key in user_info_keys:
            try:
                if key is not self.user_localId:
                    favorites_keys = user_info[key]['favorites'].keys()
                    #for favorite in favorites_keys:
                    if self.user_localId in favorites_keys:
                        requests.delete("https://nappyhour-6eb5d.firebaseio.com/" + key +
                          "/favorites/" + self.user_localId + ".json")

            except:
                print("error11111")

        requests.delete("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + ".json")



    def add_fave(self):

        faves = []
        req = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + "/favorites.json")
        data = json.loads(req.content.decode())
        data_keys = data.keys()

        for fave in data_keys:
            faves.append(fave)

        for fave_addition in faves:
            print(fave_addition)
            #fave_info = '{"%s": "true"}' % (fave_addition)
            fave_info = '{"8h6FXOxXT4SU3WcAGNb5rsddr8w1": "true"}'
            requests.patch("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + "/favorites.json", data = fave_info)



        print(data)

    def pick_appt_date(self, custname):
        date_picker = MDDatePicker(callback=self.date_chosen)
        date_picker.open()

        #name = self.root.ids['datepicker'].ids['customer_name']
       # name.text = custname

        name = custname

    def date_chosen(self,date_chosen):
        # print(date)
        global shopid
        # self.load_shop_page()
        print(str(date_chosen))
        timeslots = []

        results = requests.get(
            "https://nappyhour-6eb5d.firebaseio.com/" + shopid + "/availability/" + str(date_chosen) + ".json")
        user_info = json.loads(results.content.decode())
        print(str(user_info) + "USER INFO HERE")
        user_info_keys = user_info.keys()
        print(user_info_keys)

        for key in user_info_keys:
            timeslots.append(key)
        booking_grid = self.root.ids['bookappt'].ids['booking_grid']
        for eachtime in timeslots:
            if user_info[eachtime]:
                print(eachtime)
                result_time = BookingBanner(shop_result=shopid, date_result=str(date_chosen), booking_result=eachtime)
                booking_grid.add_widget(result_time)

        self.change_screen("bookappt")


    def pick_appt_time(self):
        time_picker = MDTimePicker()
        time_picker.bind(time=self.time_chosen)
        time_picker.open()

    def time_chosen(self, picker_widget, time):
        #print(time)
        self.change_screen("bookappt")

        ###### THIS IS NEW ######

    def add_video(self, path, selection):
        try:
            name = selection[0]
            display_new_img = self.root.ids['uploadpage'].ids['imgsource']
            display_new_img.unload()
            files = glob.glob('./images/' + self.user_localId + '*')
            for i in files:
                os.remove(i)
            copyfile(os.path.join(path, name), "./images/" + self.user_localId + '.' + (name.split('.', 1)[1]))
            content_path = "./images/" + self.user_localId + '.' + (name.split('.', 1)[1])
            post_data = '{"content": "%s"}' % (content_path)
            requests.patch("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + ".json", data=post_data)
            # when user deletes video, change to default video
            imgdata = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + ".json")
            img_data_decode = json.loads(imgdata.content.decode())
            display_new_img.source = img_data_decode['content']
            display_new_img.state = "play"


        except:
            print("Upload Error")
            pass

    def load_uploadPage(self, *args):
        display_new_img = self.root.ids['uploadpage'].ids['imgsource']
        imgdata = requests.get("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + ".json")
        img_data_decode = json.loads(imgdata.content.decode())
        display_new_img.source = img_data_decode['content']
        self.change_screen("uploadpage")

    def delete_video(self):
        display_new_img = self.root.ids['uploadpage'].ids['imgsource']
        display_new_img.unload()
        display_new_img.source = "./images/BabyYoda.png"
        post_data = '{"content": "./images/BabyYoda.png"}'
        requests.patch("https://nappyhour-6eb5d.firebaseio.com/" + self.user_localId + ".json", data=post_data)



    #therealnappyhour@gmail.com
    #Coffee123!

    def booking_email(self):
        server = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
        server.login("therealnappyhour@gmail.com", "Coffee123!")

        message = MIMEMultipart()

        msg = "This is my message"

        message['From'] = 'therealnappyhour@gmail.com'
        message['To'] = 'destinholland@gmail.com'
        message['Subject'] = "TEST SUBJECT"

        message.attach(MIMEText(msg,'plain'))

        server.send_message(message)

        del message

        server.quit()


    def reset(self):

        #self.favorites_list = []
        #self.url = 'https://nappyhour-6eb5d.firebaseio.com/.json'
        #self.dialog = None
        #self.user_localId = None
        #self.user_idToken = None
        #self.user_info = {}
        self.root.ids['firebase_login_screen'].refresh_token = ""
        self.root.ids['firebase_login_screen'].localId = ""
        self.root.ids['firebase_login_screen'].idToken = ""
        self.root.ids['firebase_login_screen'].login_success = BooleanProperty(False)
        self.root.ids['fscreen'].ids['favorites_grid'].clear_widgets()
        self.root.ids['srscreen'].ids['search_results_grid'].clear_widgets()
        self.root.ids['userpage'].ids['favorites_carousel'].clear_widgets()
        self.root.ids['editaccount'].ids['addmedia'].opacity = 0
        self.root.ids['editaccount'].ids['addmedia'].disabled = True





    def search_by_dist(self, user_zip):
        shops = [(0, 1000000)] * 10

        results = requests.get("https://nappyhour-6eb5d.firebaseio.com/.json")
        user_info = json.loads(results.content.decode())
        user_info_keys = user_info.keys()

        for key in user_info_keys:
            try:
                if user_info[key]['admin']:
                    shop_zip = user_info[key]['zipcode']
                    loc = GeoDistance('us')
                    dist = int(loc.query_postal_code(shop_zip, user_zip) * 0.621371)
                    count = 0

                    for i in range(10):
                        if shops[i][0] == 0:
                            shops[i] = (key, dist)
                            shops = sorted(shops, key=lambda shop: shop[1])
                            break
                        else:
                            count += 1

                    if count >= 10:
                        for j in range(10):
                            if dist < shops[j][1]:
                                del shops[9]
                                shops.insert(j, (key, dist))

            except:
                print(key)

        print(shops)
        search_results_grid = self.root.ids['srscreen'].ids['search_results_grid']
        for i in range(10):
            if shops[i][0] is not 0:
                print(shops[i])
                result_item = SearchResultsBanner(shop_result=shops[i][0])
                search_results_grid.add_widget(result_item)

        self.change_screen("srscreen")

    def load_confirmation_page(self, time, date, *args):
        global shopid
        confirmtext = self.root.ids['confirmation'].ids['confirmtext']
        confirmtext.text = date
        confirmtext.secondary_text = time
        self.change_screen("confirmation")

    def update_timeslot(self, date, time):
        global shopid
        apt = '{"%s": false}' % (str(time))
        requests.patch("https://nappyhour-6eb5d.firebaseio.com/" + shopid + "/availability/" + date + ".json", data=apt)
        self.change_screen("userpage")




   # notify_users("TESTTTTT", "IT WORKS!")



# Press the green button in the gutter to run the script.
MainApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
