import time
import sys
import ujson

# Get Das Labor Status from:
# https://wiki.das-labor.org/w/Status-Bot#HTTP
import urequests as requests

# Use LEDs
from machine import Pin
from machine import Timer

# Get settings from CSV file
def get_settings_from_csv():
    global update_interval
    global ping_server
    global red_pin
    global yellow_pin
    global green_pin
    with open('settings.dat', 'r') as file:
        parsed_data = file.read().strip().split(',')
        #print("CSV raw values: " + str(parsed_data[0]) + str(parsed_data[1]) + str(parsed_data[2]) + str(parsed_data[3]) + str(parsed_data[4] + '\n'))
        update_interval = int(parsed_data[0])
        ping_server = parsed_data[1]
        red_pin = int(parsed_data[2])
        yellow_pin = int(parsed_data[3])
        green_pin = int(parsed_data[4])

def show_settings():
    print('Settings:')
    print('Update interval (seconds): ' + str(update_interval))
    print('Ping server: ' + ping_server)
    print('Red pin: ' + str(red_pin))
    print('Yellow pin: ' + str(yellow_pin))
    print('Green pin: ' +  str(green_pin))
    print('')

# Set LEDs
def set_led(red=False, yellow=False, green=False):
    red_pin_state = Pin(red_pin, Pin.OUT).value(red)
    yellow_pin_state = Pin(yellow_pin, Pin.OUT).value(yellow)
    green_pin_state = Pin(green_pin, Pin.OUT).value(green)

# Test LEDs
def test_leds():
    set_led(1,0,0)
    time.sleep(1)
    set_led(0,1,0)
    time.sleep(1)
    set_led(0,0,1)

# Blink red led
def blink_red(timer):
    set_led(1,0,0)
    time.sleep(1)
    set_led(0,0,0)
    time.sleep(1)

# Blink yellow led
def blink_yellow(timer):
    set_led(0,1,0)
    time.sleep(1)
    set_led(0,0,0)
    time.sleep(1)

# Get settings from JSON file
def get_settings_from_json():
  
    try:
        f = open("wlan_conf.json",'r')
        settings_str=f.read()
        f.close()
        settings_dict = ujson.loads(settings_str)
        print("SSID: " + settings_dict["ssid"])
        ssid = settings_dict["ssid"]
        print("Password: " + settings_dict["passwd"])
        passwd = settings_dict["passwd"]
        print("Update Interval: " + settings_dict["update_interval"])
        update_interval = int(settings_dict["update_interval"])
    except:
      print('Loading Settings wlan_conf.json Failed. Exiting ...')
      sys.exit()

# Status Update

def status_update():
    iter=1
    while True:
        #print('')
        print("Trying to request status: (" + str(iter) + ")")
        #print('')
        iter = iter + 1 
        
        try: 
            timer_red_led.deinit()
        except:
            pass
        try:
            timer_yellow_led.deinit()
        except:
            pass

        try:
            f = requests.get("https://das-labor.org/status/status.php?status")
            print("\nRequest result: " + f.text + "\n")
            if f.text == "OPEN":
                print("Das Labor is -> open <-\n")
                set_led(0,0,1)
            elif f.text == "CLOSED":
                print("Das Labor is -> closed <-\n")
                set_led(1,0,0)
            elif f.text == "UNKNOWN":
                print("Das Labor is -> status unknown <-\n")
                set_led(0,1,0)
            else:
                print("Das Labor has -> status error <-\n")
                set_led(0,1,0)
            f.close()
            
        except OSError:
            print("Das Labor is -> server is unreachable <- ")       
            try:
                r = requests.get("https://www.google.de")
                #print('Ping server status code: ' + str(r.status_code))
                if r.status_code == 200:
                    #print('-> Ping server is reachable <- (You have Internet!)')
                    pass
                r.close()
                timer_yellow_led = Timer(-1)
                timer_yellow_led.init(period=1, mode=Timer.PERIODIC, callback=blink_yellow)
            except:             
                print('')
                print("-> No Internet at all :-/ <-")
                timer_red_led = Timer(-1)
                timer_red_led.init(period=1, mode=Timer.PERIODIC, callback=blink_red)
        time.sleep(update_interval)
