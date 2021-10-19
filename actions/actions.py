from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests


class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"  # the actual name of the custom action which is declared in domain.yml

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'http://api.openweathermap.org/data/2.5/weather'  # API's URL
        app_id = ''  # your own API key
        units = 'metric'  # makes the API return the numbers in metric format
        lang = 'pt_br'  # sets the language for cities names and weather descriptions
        city = tracker.get_slot('LOC')  # uses the Tracker to get the entity LOC, which stands for location

        # the complete URL to get the desired result from the API
        complete_url = url + '?q=' + city + '&APPID=' + app_id + '&units=' + units + '&lang=' + lang + ''

        # Example of a complete url
        #complete_url = 'http://api.openweathermap.org/data/2.5/weather?q=osasco&APPID=xxxxx&units=metric&lang=pt_br'

        # gets the API result in a JSON format and puts into the "data" variable
        data = requests.get(complete_url).json()

        # these variables store the informations that we are going to use
        api_weather_information = data['weather']
        condition = api_weather_information[0]['description']
        api_main_information = data['main']
        temperature = api_main_information['temp']
        place = data['name']

        # information provided by the API which will be returned to the user
        weather_information = f"No momento está {condition} em {place}, com temperatura de {temperature}ºC."

        # the dispatcher.utter_message displays the information to the user as a chatbot message
        dispatcher.utter_message(weather_information)

        # this return the entity LOC with the city provided by the user
        return [SlotSet('LOC', city)]
