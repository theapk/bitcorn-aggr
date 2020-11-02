#################################
# Author: Ian Schwartz
# Aggr v2
# Compile Command: pyinstaller --onefile aggr.py --add-data "T:/Crypto/probit-bot/venv/Lib/site-packages/pyfiglet";./pyfiglet --add-data "T:/Crypto/probit-bot/b
# itcorn-aggr/high.mp3";. --icon=rocket_corn.ico.
#################################

import requests, sys, os, locale, click
from datetime import datetime, date
from playsound import playsound
from pyfiglet import Figlet
from colorama import init, Fore

init()  # This starts the color engine

locale.setlocale(locale.LC_ALL, '')  # Set either commas or periods to separate numbers by thousands

f = Figlet(font='big')
print(Fore.YELLOW + f.renderText('CORN AGGR v2'))

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


@click.command()
@click.option('--sound', prompt='Audio "beep" for each buys or sells over X CORN amount', default=100000, help='Set the size in $ to play audio beep')
@click.option('--filter', prompt='Only show buys or sells over X CORN amount (0 = Show all)', default=0, help='Set the filter size in $ to show trades')
def aggr(sound, filter):
    market = 'CORN-BTC'
    audio_file = resource_path('high.mp3')
    playsound(audio_file)
    print('Set filter to: ' + str(filter))
    print('Set beep to: ' + str(sound))
    print('Started, waiting for orders...')
    start = datetime.utcnow().replace(microsecond=0).isoformat()
    feed = []
    count = 0
    data = ''

    while True:
        now = datetime.now()
        # stamp = str(now.year) + '/' + str(now.month) + '/' + str(now.day), str(now.hour) + ':' + str(now.minute)
        stamp = now.strftime("%Y/%m/%d %H:%M:%S")
        # print(stamp)
        try:
            if count == 120:  # This sets a refresh of start time so the list stays pruned and doesnt slow the app down
                start = datetime.utcnow().replace(microsecond=0).isoformat()
            count += 1
            dup = 0
            now = datetime.utcnow().replace(microsecond=0).isoformat()
            end = now + '.000Z'

            url = "https://api.probit.com/api/exchange/v1/trade"
            querystring = {"market_id": market, "start_time": str(start) + '.000Z', "end_time": str(end),
                           "limit": "100"}

            response = requests.request("GET", url, params=querystring)
            rjson = response.json()
            # print(rjson)
            # count = 01

            for i in rjson['data']:
                side = i['side']
                if side == 'sell':
                    action = 'Buy '
                    color = Fore.GREEN  # Sets Text color to GREEN
                elif side == 'buy':
                    action = 'Sell'
                    color = Fore.RED  # Sets Text color to RED
                price = i['price']
                quantity = i['quantity']
                timestamp = i['time']
                id = i['id']
                dollar = float(price) * float(quantity)
                for item in feed:
                    if item == id:
                        dup += 1
                if dup == 0:
                    if int(quantity) > sound:
                        playsound(audio_file)

                    if int(filter) <= int(quantity):
                        # Prints formatted string to console window
                        print(color + stamp + ' -> ' + "{0:.9f}".format(float(price)) + ' - ' + action.upper() + ': ' +
                              f'{int(quantity):n}' + ' CORN' + ' Total: ' + str(dollar) + ' BTC')
                        # data = (color + timestamp + ' -> ' + "{0:.6f}".format(float(price)) + ' - ' + action + ': ' +
                        #         f'{int(quantity):n}' + ' CORN' + ' Total: ' + '${:,.2f}'.format(
                        #                         dollar) + ' USDT')

                    feed.append(id)  # Added order ID to a list so that we can see if it has already been displayed
        except Exception as e:
            print(e)  # If any errors/exceptions arise then they will print to console
            # pass


if __name__ == '__main__':
    aggr()
