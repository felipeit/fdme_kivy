"""
# (list) Permissions
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
"""
from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty
from address import address
from plyer import gps
import requests
from websocket import WebSocket
import ssl
import time


class Painel(Screen):
    def callback(self, instance, value):
        print('O switch', instance, 'is', value)
        app = App.get_running_app()
        client = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

        try:           
            app.start(1000, 0)
            client.connect(address.ADDRESS_WEBSOCKET)
            time.sleep(5)
            
            client.send(app.gps_location + 
                "\n" + app.username)
            
        except Exception as e:
            print(e)
        finally:
            app.stop()
            client.close()
            value = False
    
    def request_user(self):
        app = App.get_running_app() 
        #response = requests.get(ADDRESS_API_SEARCH)
        return response.content

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()



