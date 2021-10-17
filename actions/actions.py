from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests


class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'http://api.openweathermap.org/data/2.5/weather'
        app_id = ''  # aqui você deve incluir sua própria chave de API
        units = 'metric'
        lang = 'pt_br'
        city = tracker.get_slot('LOC')

        complete_url = url + '?q=' + city + '&APPID=' + app_id + '&units=' + units + '&lang=' + lang + ''
        #complete_url = 'http://api.openweathermap.org/data/2.5/weather?q=osasco&APPID=xxxxx&units=metric&lang=pt_br'

        data = requests.get(complete_url).json()

        api_weather_information = data['weather']
        condition = api_weather_information[0]['description']
        api_main_information = data['main']
        temperature = api_main_information['temp']
        place = data['name']

        weather_information = f"No momento está {condition} em {place}, com temperatura de {temperature}ºC."
        dispatcher.utter_message(weather_information)

        return [SlotSet('LOC', city)]
