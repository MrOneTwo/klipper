Start Klipper with COAP support:

```sh
LIBCOAP_PATH=/home/mc/gits/libcoap/.libs/libcoap-3-gnutls.so python klippy.py ~/Desktop/klipper/printer.cfg -a /tmp/klippy_uds -l /tmp/klippy.log
```

I have been testing with coap-client example from libcoap. It's important to use `%2F` inside
the socket path but `/` to denote the URI path.

```sh
coap-client -m put -e hej coap://%2Ftmp%2Fklippy_uds/t
```

Test file for the client.

```python
from libcoapy import *
from threading import Thread
import time

# Usage: simply start coap-server-openssl on the same system and execute this script

coap_set_log_level(coap_log_t.COAP_LOG_DEBUG)

if len(sys.argv) < 2:
	uri_str = "coap://%2Ftmp%2Fklippy_uds"
else:
	uri_str = sys.argv[1]

ctx = CoapContext()

session = ctx.newSession(uri_str)


def response_callback(session, pdu_tx, pdu_rx, mid):
	print("async-subscribe.py:response_callback", pdu_rx.payload)
	pdu_rx.make_persistent()
	#observer.addResponse(rx_msg)

	return coap_response_t.COAP_RESPONSE_OK

t = Thread(target=ctx.loop, daemon=True)
t.start()
session.sendMessage("/list_endpoints", observe=False, query="a&b=3", save_rx_pdu=True, response_callback=response_callback)

while True:
	time.sleep(2)

sys.exit()
```
