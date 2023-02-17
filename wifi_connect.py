from wifi_manager import WifiManager
import machine

def wifi_connect():

    # Connecting to wifi ....

    wm = WifiManager()
    wm.connect()

    if not wm.is_connected():
        print('Not connected !?!')
        print('Rebooting ...')
        machine.reset()
    else:
        print('Wifi setup done.')
        print('')
    