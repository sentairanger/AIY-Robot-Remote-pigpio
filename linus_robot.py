#!/usr/bin/env python3
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# robot_precision.py
# Moves a robot based on commands
# Modified by Edgardo Peregrino
# 9/15/2020

"""A demo of the Google CloudSpeech recognizer."""
#import libraries
import pigpio
from time import sleep
import aiy.voice.tts

import argparse
import locale
import logging

from aiy.cloudspeech import CloudSpeechClient

#Define the pigpio daemon
#Include IP address
pi = pigpio.pi()

#Setup the pins
pi.set_mode(13, pigpio.OUTPUT)
pi.set_mode(21, pigpio.OUTPUT)
pi.set_mode(27, pigpio.OUTPUT)
pi.set_mode(22, pigpio.OUTPUT)

#create a function that creates hints to what to say to the box
def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('go forward',
                'go backward',
                'go left',
                'go right',
                'goodbye')
    return None

#create a function that defines the local language based on location
def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    #log any issues and print the commands on the terminal
    logging.basicConfig(level=logging.DEBUG)
    # use this if you aren't using English
    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()
    #initialize the cloudspeech API
    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    while True:
        #here it detects if your statements match with the hints
        if hints:
            logging.info('Say something, e.g. %s.' % ', '.join(hints))
        else:
            logging.info('Say something.')
        text = client.recognize(language_code=args.language, hint_phrases=hints)
        if text is None:
            logging.info('You said nothing.')
            continue
        logging.info('You said: "%s"' % text)
        # Robot moves based on which ever direction it is told
        # Added more precise movement
        text = text.lower()
        if 'go forward' in text:
            aiy.voice.tts.say('Okay I will go forward')
            pi.write(13, 1)
            pi.write(21, 0)
            pi.write(27, 1)
            pi.write(22, 0)
            sleep(2)
            pi.write(13, 0)
            pi.write(21, 0)
            pi.write(27, 0)
            pi.write(22, 0)
        elif 'go backward' in text:
            aiy.voice.tts.say('Okay I will go backward')
            pi.write(13, 0)
            pi.write(21, 1)
            pi.write(27, 0)
            pi.write(22, 1)
            sleep(2)
            pi.write(13, 0)
            pi.write(21, 0)
            pi.write(27, 0)
            pi.write(22, 0)
        elif 'go left' in text:
            aiy.voice.tts.say('Okay I will go left')
            pi.write(13, 0)
            pi.write(21, 1)
            pi.write(27, 1)
            pi.write(22, 0)
            sleep(0.3)
            pi.write(13, 0)
            pi.write(21, 0)
            pi.write(27, 0)
            pi.write(22, 0)
        elif 'go right' in text:
            aiy.voice.tts.say('Okay I will go right')
            pi.write(13, 1)
            pi.write(21, 0)
            pi.write(27, 0)
            pi.write(22, 1)
            sleep(0.3)
            pi.write(13, 0)
            pi.write(21, 0)
            pi.write(27, 0)
            pi.write(22, 0)
        elif 'goodbye' in text:
            aiy.voice.tts.say('Goodbye')
            break

if __name__ == '__main__':
    main()        

pi.stop()
