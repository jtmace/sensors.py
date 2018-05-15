#!/usr/bin/env python
import json, os
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
PINS = [7, 8, 11]
for pin in PINS:
    GPIO.setup(pin,  GPIO.IN, pull_up_down=GPIO.PUD_UP)

time_ = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

zones = {
        '1':{'name':'Back','state':'Closed','curr':0, 'prev': 0, 'pin':7, 'change': time_ },
        '2':{'name':'Front','state':'Closed','curr':0, 'prev': 0, 'pin':8, 'change': time_},
        '3':{'name':'Garage','state':'Closed','curr':0, 'prev': 0, 'pin':11, 'change': time_ }
}

print json.dumps(zones)
with open('/var/www/zones.json', 'w') as outfile:
        json.dump(zones, outfile)

try:
    while True:
        for x in sorted(zones.keys()):
                changed = 0
                zones[x]['curr'] = GPIO.input(zones[x]['pin'])
                time_ = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                if ( zones[x]['curr'] == zones[x]['prev'] and zones[x]['curr'] == 0 ) :
                        zones[x]['state'] = 'Closed'
                if ( zones[x]['curr'] == zones[x]['prev'] and zones[x]['curr'] == 1 ) :
                        zones[x]['state'] = 'Open'

                if ( zones[x]['curr'] != zones[x]['prev'] ) :
                        if ( zones[x]['curr'] == 1 ):
                                zones[x]['state'] = 'Open'
                                zones[x]['change'] = time_
                                output = '%s - The %s door is now open' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),zones[x]['name'])
                                os.system('echo %s >> /root/log.txt' % output)
                                print (output)
                        if ( zones[x]['curr'] == 0 ):
                                zones[x]['state'] = 'Closed'
                                zones[x]['change'] = time_
                                output = '%s - The %s door is now closed' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), zones[x]['name'])
                                os.system('echo %s >> /root/log.txt' % output)
                                print (output)
                        changed = 1

                if ( changed == 1 ) :
                        print json.dumps(zones)
                        with open('/var/www/zones.json', 'w') as outfile:
                                json.dump(zones, outfile)

                zones[x]['prev'] = zones[x]['curr']

        sleep(.75)
except KeyboardInterrupt:
    GPIO.cleanup()
