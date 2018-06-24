import urllib.request
import os

class MY_URLError(Exception):
    pass

def send_message(msg):
    if len(msg) > 0:
        for message in msg:
            try:
                urllib.request.urlopen("""
                https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={TEXT}
                """.format(
                API_TOKEN=os.environ['TELEGRAM_API_TOKEN'],
                CHAT_ID=os.environ['TELEGRAM_CHAT_ID'],
                TEXT=message
                ))
            except urllib.HTTPError as err:  # timeout error
                raise MY_URLError("urlopen error", err)
