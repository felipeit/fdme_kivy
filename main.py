__version__ = "0.1"

from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os
from kivy.properties import NumericProperty
from plyer import gps
import requests
from painel import Painel
from kivy.clock import mainthread, Clock
from address import address


class Login(Screen):
    def check_user(self):
        app = App.get_running_app()
        response = requests.Session()
        response.auth = (app.username, app.password)
        result = response.get(address.ADDRESS_API)
        return result.status_code
    
    def autenticar_login(self, loginText, passwordText):
        app = App.get_running_app()
        app.username = loginText
        app.password  = passwordText
        
        if self.check_user() == 200:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'painel'

            app.config.read(app.get_application_config())
            app.config.write()
        else:
            print(self.check_user())
            exit()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""


class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates.')


    def build(self):
        try:
            gps.configure(on_location=self.on_location,
             on_status=self.on_status)

        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_sattus = "Gps not implemented." 

        manager = ScreenManager()
        manager.add_widget(Login(name='login'))
        manager.add_widget(Painel(name='painel'))

        return manager
    
    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)
     
    def on_pause(self):
        gps.stop()
        
    def on_resume(self):
        gps.start(1000, 0)
        
    def get_application_config(self, **kwargs):
        if not self.username:
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if not os.path.exists(conf_directory):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config('%s/config.cfg' % conf_directory)


if __name__ == '__main__':
    LoginApp().run()
