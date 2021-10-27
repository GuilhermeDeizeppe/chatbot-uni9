from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
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
        # http://api.openweathermap.org/data/2.5/weather?q=osasco&APPID=xxxxx&units=metric&lang=pt_br

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

        # return the entity LOC with the city provided by the user
        return [SlotSet('LOC', city)]

    class ValidateExchangeForm(FormValidationAction):

        # the name of the custom action which is declared in domain.yml
        def name(self):
            return "validate_simple_exchange_form"

        # list of supported currencies
        @staticmethod
        def currency_list() -> List[Text]:
            return ['USD', 'BRL', 'EUR', 'GBP']

        # validation of the slot currency1
        def validate_currency1(
                self,
                slot_value: Any,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: DomainDict) -> Dict[Text, Any]:

            # checks if the currency1 value is in currency_list()
            # if the result is true, the currency1 slot is set with the value provided by the user
            # if the result is false, the currency1 slot is set to none, which will make the bot ask the user again for
            # the correct value
            if slot_value.upper() in self.currency_list():
                return {"currency1": slot_value}
            else:
                dispatcher.utter_message('Moeda não encontrada. Por favor, digite o código da moeda corretamente.')
                return {"currency1": None}

        # validation of the slot currency2
        def validate_currency2(
                self,
                slot_value: Any,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: DomainDict) -> Dict[Text, Any]:

            # checks if the currency2 value is in currency_list()
            # if the result is true, the currency2 slot is set with the value provided by the user
            # if the result is false, the currency2 slot is set to none, which will make the bot ask the user again for
            # the correct value
            if slot_value.upper() in self.currency_list():
                return {"currency2": slot_value}
            else:
                dispatcher.utter_message('Moeda não encontrada. Por favor, digite o código da moeda corretamente.')
                return {"currency2": None}

    class ActionGetExchange(Action):

        def name(self) -> Text:
            return 'action_get_exchange'

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]):

            url = 'https://economia.awesomeapi.com.br/'  # API's URL
            currency1 = tracker.get_slot('currency1')
            currency2 = tracker.get_slot('currency2')
            currencies = currency1 + '-' + currency2  # Currencies to convert in API

            # the complete URL to get the desired result from the API
            complete_url = url + currencies

            # Example of a complete url
            # https://economia.awesomeapi.com.br/USD-BRL

            # gets the API result in a JSON format and puts into the "data" variable
            data = requests.get(complete_url).json()

            # these variables store the informations that we are going to use
            name = data[0]['name']
            high = data[0]['high']
            low = data[0]['low']
            buy = data[0]['bid']
            sell = data[0]['ask']

            # information provided by the API which will be returned to the user
            exchange_information = \
                f"Cotação entre {name}:\n\nCompra: {buy}\nVenda: {sell}\nBaixa do dia: {low}\nAlta do dia: {high}"

            # the dispatcher.utter_message displays the information to the user as a chatbot message
            dispatcher.utter_message(exchange_information)
