import json
import threading
from typing import Union

import requests
import websocket

import gtnapi


class Streaming:
    class MarketData:

        __active: bool

        @classmethod
        def __open_connection(cls, endpoint):
            """
            open the websocket connection
            :param endpoint: websocket endpoint
            :param on_open: method reference
            :param on_message: method reference
            :param on_error: method reference
            :param on_close: method reference
            :return:
            """
            # cls.__on_open = on_open
            # cls.__on_message = on_message
            # cls.__on_error = on_error
            # cls.__on_close = on_close

            if not endpoint[0] == '/':
                endpoint = '/' + endpoint

            websocket.enableTrace(False)
            cls.__ws = websocket.WebSocketApp(
                'wss' + gtnapi.get_api_url()[5:] + endpoint + "?throttle-key=" + gtnapi.get_app_key(),
                on_open=cls.on_open,
                on_message=cls.on_message,
                on_error=cls.on_error,
                on_close=cls.on_close)

            cls.__active = True
            cls.__ws.run_forever()
            cls.__active = False

        @classmethod
        def connect(cls, endpoint,
                    on_open: callable = None,
                    on_message: callable = None,
                    on_error: callable = None,
                    on_close: callable = None
                    ):
            """
            Start the websocket thred
            :param endpoint: websocket endpoint
            :param on_open: method reference
            :param on_message: method reference
            :param on_error: method reference
            :param on_close: method reference
            :return:
            """

            if on_open:
                cls.__on_open = on_open
            else:
                cls.__on_open = cls.__sink
            if on_message:
                cls.__on_message = on_message
            else:
                cls.__on_message = cls.__sink
            if on_error:
                cls._on_error = on_error
            else:
                cls.__on_error = cls.__sink
            if on_close:
                cls.__on_close = on_close
            else:
                cls.__on_close = cls.__sink

            t = threading.Thread(target=cls.__open_connection, args=(endpoint,))
            t.start()

        @classmethod
        def disconnect(cls):
            """
            disconnect the socket on demand
            :return:
            """
            cls.__active = False
            cls.__ws.close()

        @classmethod
        def on_open(cls, ws):
            """
            on open event handler
            :param ws: web socket reference
            """
            ws.send(f'{{ "token": {gtnapi.get_token()["accessToken"]} }}')
            cls.__on_open()

        @classmethod
        def on_message(cls, ws, message):
            """
            on message event handler
            :param ws: web socket reference
            :param message: message received
            """
            cls.__on_message(message)

        @classmethod
        def on_error(cls, ws, error):
            """
            on open error handler
            :param ws: web socket reference
            :param error: error message
            """
            cls.__on_error(error)

        @classmethod
        def on_close(cls, ws, close_status_code, close_msg):
            """
            on close event handler
            :param ws: web socket reference
            :param close_status_code: code
            :param close_msg: closing message
            """
            cls.__active = False
            cls.__on_close(close_status_code, close_msg)

        @classmethod
        def subscribe(cls, message: Union[dict, str]):
            """
            sends a message via the web socket
            :param message: to be sent
            """
            if type(message) is dict:
                cls.__ws.send_text(json.dumps(message))
            else:
                cls.__ws.send_text(message)

        @classmethod
        def active(cls):
            """
            :return: True if market data streaming is active
            """
            try:
                return cls.__active
            except Exception as e:
                return False

        @classmethod
        def __sink(cls, message=None):
            pass

    class TradeData:

        @classmethod
        def connect(cls,
                    endpoint: str,
                    events: Union[list[str], str],
                    on_message: callable = None,
                    on_error: callable = None,
                    on_close: callable = None):

            """
            Connect the HTTP streaming endpoint
            :param endpoint: streaming server endpoint
            :param events: event to be send to streaming server
            :param on_message: method reference to pass incoming messages
            :param on_error: method reference to pass error messages
            :param on_close: method reference to pass close message
            """

            cls.response = None
            cls.__active = True

            if on_message:
                cls.__on_message = on_message
            else:
                cls.__on_message = cls.__sink
            if on_error:
                cls._on_error = on_error
            else:
                cls.__on_error = cls.__sink
            if on_close:
                cls.__on_close = on_close
            else:
                cls.__on_close = cls.__sink

            kwargs = {
                'headers': {
                    'Authorization': 'Bearer ' + gtnapi.get_token()['accessToken'],
                    'Throttle-Key': gtnapi.get_app_key()
                }
            }
            if type(events) is str:
                event_str = events
            else:
                event_str = ','.join(events)

            if not endpoint[0] == '/':
                endpoint = '/' + endpoint

            url = gtnapi.get_api_url() + endpoint + '?events=' + event_str
            cls.connected = True

            cls.t = threading.Thread(target=cls.__reader, args=(url, kwargs))
            cls.t.start()

        @classmethod
        def __reader(cls, url: str, kwargs):
            headers = {
                'Authorization': 'Bearer ' + gtnapi.get_token()['accessToken'],
                'Throttle-Key': gtnapi.get_app_key()
            }
            cls.response = requests.get(url, headers=headers, stream=True, timeout=30)
            try:
                for raw_line in cls.response.iter_lines():
                    line = str(raw_line, encoding='utf-8')
                    if not cls.__active:
                        return
                    if line[0:5] == 'data:':
                        message = json.loads(line[5:])
                        if message['event'] == 'ERROR':
                            cls.__on_error(message)
                        else:
                            cls.__on_message(message)
                cls.__on_close()
            except Exception as e:
                if not cls.__active:
                    return
                try:
                    cls.response.close()
                except:
                    pass
                cls.__on_error({'event': 'ERROR', 'operation': 'ERROR', 'payload': {'reason': e}})

        @classmethod
        def disconnect(cls):
            cls.__active = False
            try:
                cls.response.close()
            except:
                pass

        @classmethod
        def subscribe(cls, events: Union[list[str], str]):
            """
            subscribe to new events
            :param events: to be subscribe to
            """
            # todo

        @classmethod
        def unsubscribe(cls, events: Union[list[str], str]):
            """
            unsubscribe existing events
            :param events: to be unsubscribe from
            """
            # todo

        @classmethod
        def __sink(cls, message=None):
            pass

        @classmethod
        def active(cls):
            try:
                return cls.__active
            except:
                return False
