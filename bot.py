import requests
from bs4 import BeautifulSoup


BOT_TOKEN = '953346507:AAEC5oV6j0YfNb7Rrb5zvJTeAATnYkF0Mks'
API_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'


def get_menu(selector):
    MENU_URL = 'http://www.kaist.edu/_prog/fodlst/index.php?site_dvs_cd=en&menu_dvs_cd=050303&stt_dt=2019-12-01'

    response = requests.get(MENU_URL)
    markup = response.content

    soup = BeautifulSoup(markup, "html.parser")
    element = soup.select(selector)[0]

    return element.get_text()


def main():
    offset = -1000_000_000
    breakfast_selector = '#txt > table > tbody > tr > td:nth-child(1)'
    lunch_selector = '#txt > table > tbody > tr > td:nth-child(2)'
    dinner_selector = '#txt > table > tbody > tr > td.t_end'

    while True:
        data = {
            'offset': offset,
            'timeout': 30
        }
        resp = requests.get(API_URL + 'getUpdates', data=data).json()

        updates = resp['result']

        for update in updates:
            offset = max(offset, update['update_id'] + 1)

            message = update.get('message')

            if message:
                text = message.get('text', '')

                if text.startswith('/breakfast'):
                    answer = get_menu(breakfast_selector)
                elif text.startswith('/lunch'):
                    answer = get_menu(lunch_selector)
                elif text.startswith('/dinner'):
                    answer = get_menu(dinner_selector)
                else:
                    answer = 'I don\'t get it 😔'
                
                data = {
                    'chat_id': message['chat']['id'],
                    'text': answer
                }

                requests.post(API_URL + 'sendMessage', data=data)

                print('offset', offset)


if __name__ == '__main__':
    main()
