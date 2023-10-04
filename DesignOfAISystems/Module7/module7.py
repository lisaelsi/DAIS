import pandas as pd
import random as rand
from abc import ABC

def init_keywords():
    keywords = {}
    keywords['greeting'] = ['hello', 'hi', 'howdy']

    keywords['weather'] = ['sunny', 'sun', 'weather', 'rain', 'snow', 'clouds', 'cloudy']
    keywords['day'] = ['tomorrow', 'today',  'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    keywords['place'] = ['gothenburg', 'stockholm',  'oslo', 'berlin']

    keywords['restaurant'] = ['restaurant', 'eat', 'food']
    keywords['cuisine'] = ['swedish', 'italian', 'french', 'asian']
    keywords['dish'] = ['pizza', 'steak', 'lasagne']
    keywords['price_class'] = ['expensive', 'cheap']


    keywords['location'] = ['chalmers', 'lindholmen', 'järntorget']
    keywords['travel'] = ['tram', 'go',  'ticket', 'travel', 'go to', 'get', 'travel']
    
    return keywords

def init_greetings():
    greetings = ['Hello!', 'Hi!', 'Good day!']
    return greetings

class DataManager:

    def get_weather(self, day, place):
        csv_path = 'Module7/data/' + place + '_weather.csv'
        df = pd.read_csv(csv_path, sep=';',  index_col=0)

        weather = df.loc['weather', 'today']
        temp = df.loc['temperature', 'today']

        return weather, temp
    
    def recomend_cuisine_restaurant(self, cuisine):
        csv_path = 'Module7/data/gothenburg_restaurant.csv'
        df = pd.read_csv(csv_path, sep=';', index_col=0)
        filtered_df = df.loc[df['cuisine'] == cuisine]
        restaurants = filtered_df.index.tolist()
        recommendation = rand.choice(restaurants)
        return recommendation

    def recomend_dish_restaurant(self, dish):
        csv_path = 'Module7/data/gothenburg_restaurant.csv'
        df = pd.read_csv(csv_path, sep=';',  index_col=0)
        filtered_df = df.loc[df['best dish'] == dish]
        restaurants = filtered_df.index.tolist()
        recommendation = rand.choice(restaurants)
        return recommendation

    def recomend_restaurant(self, cuisine, dish):
        csv_path = 'Module7/data/gothenburg_restaurant.csv'
        df = pd.read_csv(csv_path, sep=';',  index_col=0)
        filtered_df = df.loc[df['best dish'] == dish]
        filtered_df = filtered_df.loc[filtered_df['cuisine'] == cuisine]
        restaurants = filtered_df.index.tolist()
        if restaurants == []:
            return None
        recommendation = rand.choice(restaurants)
        return recommendation

    def get_departure(self, start, destination):
        csv_path = 'Module7/data/gothenburg_travel.csv'
        df = pd.read_csv(csv_path, sep=';')

        fil_df = df.loc[df['destination'] == destination]
        fil_df = fil_df.loc[fil_df['start'] == start]

        number = fil_df['number'].item()
        number_str = str(number)
        dep_time = fil_df['time'].item()

        return number_str, dep_time

class TopicHandler(ABC):

    def __init__(self, inp, keywords):
        super().__init__()
        self.inp = inp
        self.keywords = keywords
        self.datamanager = DataManager()
    
    def fill_blank(self, question, keywords):
        blank = None
        while blank == None:
            print(question)
            inp2 = input()
            inp2 = [word.lower() for word in inp2.split()] 
            if set(inp2) & set(keywords):
                blank = ''.join(set(inp2) & set(keywords))
            else: print('I did not quite understand you.')
        return blank
    
class WeatherHandler(TopicHandler):

    def __init__(self, inp, keywords):
        super().__init__(inp, keywords)
        self.day = None
        self.place = None
        
    def handle(self):
        weather_words = self.keywords['weather']
        if set(self.inp) & set(weather_words):
            day = None
            place = None

            # Check if contains day keyword
            if set(self.inp) & set(self.keywords['day']):
                day = ''.join((set(self.inp) & set(self.keywords['day'])))
                
            else: 
                # If no day in first sentence, ask user for a day until it gives us one
                day = self.fill_blank('What day do you want the weather for?', self.keywords['day'])
            
            # Check if contains place keyword
            if set(self.inp) & set(self.keywords['place']):
                place = ''.join((set(self.inp) & set(self.keywords['place'])))
            else: 
                # If no place in first sentence, ask user for a place until it gives us one
                place = self.fill_blank('What place do you want the weather for?', self.keywords['place'])
            
            weather, temp = self.datamanager.get_weather(day, place)

            print(f'In {place.capitalize()} it will be {weather} and the temperature will be {temp} °C.')

            print("Can I help you with anything else?")
            day = None
            place = None

class RestaurantHandler(TopicHandler):

    def __init__(self, inp, keywords):
        super().__init__(inp, keywords)
        self.cuisine = None
        self.dish = None
            
    def handle(self):
            restaurant_words = self.keywords['restaurant']

            # Check if contains restaurant keywords
            if set(self.inp) & set(restaurant_words):

                if set(self.inp) & set(self.keywords['cuisine']):
                    self.cuisine = ''.join((set(self.inp) & set(self.keywords['cuisine'])))

                if set(self.inp) & set(self.keywords['dish']):
                    self.dish = ''.join((set(self.inp) & set(self.keywords['dish'])))
                
                if self.cuisine == None and self.dish == None:
                    self.cuisine = self.fill_blank("There are many nice restaurants available. What kind of food are you looking for?", self.keywords['cuisine'])
                if self.dish == None:
                    recommendation = self.datamanager.recomend_cuisine_restaurant(self.cuisine)
                    print(f'You should visit {recommendation.capitalize()}, they have nice {self.cuisine} food!')
                    print("Can I help you with anything else?")
                if self.cuisine == None:
                    recommendation = self.datamanager.recomend_dish_restaurant(self.dish)
                    print(f'You should visit {recommendation.capitalize()}, they are famous for their {self.dish}!')
                    print("Can I help you with anything else?")
                if self.cuisine != None and self.dish != None:
                    recommendation = self.datamanager.recomend_restaurant(self.cuisine, self.dish)
                    if recommendation is None:
                        print('Sadly, there is no such restaurant.')
                        print("Can I help you with anything else?")
                    else:
                        print(f'You should visit {recommendation.capitalize()}!')
                        print("Can I help you with anything else?")

class TravelHandler(TopicHandler):
    def __init__(self, inp, keywords):
        super().__init__(inp, keywords)
        self.start = None
        self.destination = None
    
    def get_location_from_input(self, inp, from_location):
        if from_location is True:
            search_for = 'from'
        else:
            search_for = 'to'

        start_ind = inp.index(search_for) + 1
        start = inp[start_ind]
        
        possible_starts = self.keywords['location']

        if start not in possible_starts:
            return None

        return start

    def ask_for_location(self, from_location):
        start = None

        if from_location is True:
            print("Where do you want to travel from?")
        else:
            print("Where do you want to travel to?")

        while start == None:
            inp = input()
            inp = [word.lower() for word in inp.split()] 
            
            if set(inp) & set(self.keywords['location']):
                start = set(inp) & set(self.keywords['location'])
            else:
                print("I couldn't find any departures from that place.")
        return "".join(start)
        
    def handle(self):
        travel_words = self.keywords['travel']
        if set(self.inp) & set(travel_words):
            while self.start == None:
                if 'from' in self.inp:
                    self.start = self.get_location_from_input(self.inp, from_location=True)

                    if self.start is None:
                        print('There are no departures from this place.')
                        self.start = self.ask_for_location(True)
                else:
                    self.start = self.ask_for_location(True)
            
            while self.destination == None:
                if 'to' in self.inp:
                    self.destination = self.get_location_from_input(self.inp, from_location=False)

                    if self.destination is None:
                        print('There are no trams to this place.')
                        self.destination = self.ask_for_location(False)
                else:
                    self.destination = self.ask_for_location(False)
            number, dep_time = self.datamanager.get_departure(self.start, self.destination)
            print(f'The next departure from {self.start.capitalize()} to { self.destination.capitalize()} is tram number {number} at {dep_time}.')
            print("Can I help you with anything else?")

class ChatBot:

    def __init__(self, keywords, greetings):
        self.keywords = keywords
        self.greetings = greetings
    
    def chat(self):
        
        print('Write something to start chatting:')
                        
        while(True):
            # Ask for user input
            inp = input()

            # Clean input, remove special characters and make lowercase
            inp = inp.replace(',', '').replace('?', '').replace('.', '').replace('!', '')
            inp = [word.lower() for word in inp.split()] 

            # Check if input contains greeting keywords
            greeting_words = self.keywords['greeting']
            if set(inp) & set(greeting_words):
                print(rand.choice(greetings))
            
            # Handle weather topic
            WeatherHandler(inp, keywords).handle()

            # Handle restaurant topic
            RestaurantHandler(inp, keywords).handle()
            
            # Handle travel topic
            TravelHandler(inp, keywords).handle()

            # Check if user rrwants to end the conversation
            if inp[0] == 'no' or inp[0] == 'exit':
                print('Good bye!')
                break
            
            # Check if user says bye
            if 'bye' in inp:
                print('If you want to stop chatting, you can type exit. Otherwise, you can ask another question.')

keywords = init_keywords()
greetings = init_greetings()

chatbot = ChatBot(keywords, greetings)
chatbot.chat()




                    

                    


