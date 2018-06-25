import time
import json
import os
import psycopg2.extras
from binance.client import Client
from telegram_bot import send_message

def main():

    def get_current_price():
        array_price = {}
        prices = client.get_all_tickers()
        for coin in prices:
            symbol = coin['symbol']
            price = float(coin['price'])
            array_price[symbol] = price
        return array_price


    client = Client(os.environ['BINANCE_APIKEY'], os.environ['BINANCE_SECRET'])

    connect = psycopg2.connect(host=os.environ['DB_HOST'], port=5432, database=os.environ['DB_DATABASE'],
                               user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'])

    previous = get_current_price()
    i = 0
    while i < 10:
        messages = []

        current = get_current_price()

        result = 0.0

        for key, value in current.items():
            if value < previous[key]:
                result = (value - previous[key]) / previous[key]
                if result < -0.005:
                    value = key + ': ' + str(current[key]) + ' ' + str(round(result * 100, 2)) + '%'
                    messages.append(value)

        now = int(time.time())
        sql = ("""insert into binance_bot(time, data) values (%s, %s::json)""")
        cursore = connect.cursor()
        cursore.execute(sql, (now, json.dumps(current)))
        connect.commit()

        print(messages)

        send_message(messages)

        time.sleep(10)

        previous = current
        i += 1

    connect.close()
    print('exit')

if __name__ == '__main__':
    main()