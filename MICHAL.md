Start Klipper with COAP support:

```sh
LIBCOAP_PATH=/home/mc/gits/libcoap/.libs/libcoap-3-gnutls.so python klippy.py ~/Desktop/klipper/printer.cfg -a /tmp/klippy_uds -l /tmp/klippy.log
```

I have been testing with coap-client example from libcoap. It's important to use `%2F` inside
the socket path but `/` to denote the URI path.

```sh
coap-client -m put -e hej coap://%2Ftmp%2Fklippy_uds/t
```
