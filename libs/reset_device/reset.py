import RPi.GPIO as GPIO
import os
import time
import subprocess
import reset_lib

<<<<<<< HEAD
import requests
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=90, rotate=0, blocks_arranged_in_reverse_order=True)

# # defining a params dict for the parameters to be sent to the API
# PARAMS = {'address':location}

# # sending get request and saving the response as response object
# r = requests.get(url = URL, params = PARAMS)
# extracting data in json format
# data = r.json()

# api-endpoint
HALT_SCROLLER = "http://pi02-2:3000/halt_scroller"
PLAY_MUSIC = "http://pi02-2:3000/play_music"

WIFI_RESET_PIN = 18
COUNTDOWN = 5
=======
WIFI_RESET_PIN = 18
>>>>>>> 080322450e79d880e753e4dada097679dc8873e8

GPIO.setmode(GPIO.BCM)
GPIO.setup(WIFI_RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = COUNTDOWN
serial_last_four = subprocess.check_output(['cat', '/proc/cpuinfo'])[-5:-1].decode('utf-8')
config_hash = reset_lib.config_file_hash()
ssid_prefix = config_hash['ssid_prefix'] + " "
reboot_required = False

reboot_required = reset_lib.wpa_check_activate(config_hash['wpa_enabled'], config_hash['wpa_key'])

reboot_required = reset_lib.update_ssid(ssid_prefix, serial_last_four)

if reboot_required == True:
    os.system('reboot')

# This is the main logic loop waiting for a button to be pressed on WIFI_RESET_PIN for 5 seconds.
# If that happens the device will reset to its AP Host mode allowing for reconfiguration on a new network.
while True:
    while GPIO.input(WIFI_RESET_PIN) == 1:

        if(counter == COUNTDOWN):
            r = requests.get(url=HALT_SCROLLER)
            print(r)
            Tv = " "
            Tv = Tv.rjust(4, " ")
            with canvas(device) as draw:
                text(draw, (0, 0), "    ", fill="white")

        time.sleep(1)

        print(counter)
        Tv = str(counter)
        Tv = Tv.rjust(4, " ")

        with canvas(device) as draw:
            text(draw, (0, 0), Tv, fill="white")

        counter = counter - 1

        if counter == 0:
            with canvas(device) as draw:
                text(draw, (0, 0), "----", fill="white")
            time.sleep(3)
            with canvas(device) as draw:
                text(draw, (0, 0), "boot", fill="white")
            reset_lib.reset_to_host_mode()
            break

        if GPIO.input(WIFI_RESET_PIN) == 0:
            counter = COUNTDOWN
            Tv = " "
            Tv = Tv.rjust(4, " ")
            with canvas(device) as draw:
                text(draw, (0, 0), "    ", fill="white")
            r = requests.get(url=PLAY_MUSIC)
            print(r)
            break

    time.sleep(1)
