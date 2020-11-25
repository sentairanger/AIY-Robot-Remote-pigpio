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
#include IP Address when controlling remotely
linus = pigpio.pi()
torvalds = pigpio.pi()

#Setup the pins
linus.set_mode(13, pigpio.OUTPUT)
linus.set_mode(21, pigpio.OUTPUT)
linus.set_mode(27, pigpio.OUTPUT)
linus.set_mode(22, pigpio.OUTPUT)

torvalds.set_mode(7, pigpio.OUTPUT) #motorB2
torvalds.set_mode(8, pigpio.OUTPUT) #motorB1
torvalds.set_mode(9, pigpio.OUTPUT) #motorA2
torvalds.set_mode(10, pigpio.OUTPUT) #motorA1

#create a function that creates hints to what to say to the box
def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('up',
                'down',
                'left',
                'right',
                'north',
                'south',
                'east',
                'west',
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
        if 'up' in text:
            aiy.voice.tts.say('Okay I will go forward')
            linus.write(13, 1)
            linus.write(21, 0)
            linus.write(27, 1)
            linus.write(22, 0)
            sleep(2)
            linus.write(13, 0)
            linus.write(21, 0)
            linus.write(27, 0)
            linus.write(22, 0)
        elif 'down' in text:
            aiy.voice.tts.say('Okay I will go backward')
            linus.write(13, 0)
            linus.write(21, 1)
            linus.write(27, 0)
            linus.write(22, 1)
            sleep(2)
            linus.write(13, 0)
            linus.write(21, 0)
            linus.write(27, 0)
            linus.write(22, 0)
        elif 'left' in text:
            aiy.voice.tts.say('Okay I will go left')
            linus.write(13, 1)
            linus.write(21, 0)
            linus.write(27, 0)
            linus.write(22, 1)
            sleep(0.3)
            linus.write(13, 0)
            linus.write(21, 0)
            linus.write(27, 0)
            linus.write(22, 0)
        elif 'right' in text:
            aiy.voice.tts.say('Okay I will go right')
            linus.write(13, 0)
            linus.write(21, 1)
            linus.write(27, 1)
            linus.write(22, 0)
            sleep(0.3)
            linus.write(13, 0)
            linus.write(21, 0)
            linus.write(27, 0)
            linus.write(22, 0)
        elif 'north' in text:
            aiy.voice.tts.say('Okay I will go forward')
            torvalds.write(10, 1)
            torvalds.write(9, 0)
            torvalds.write(8, 1)
            torvalds.write(7, 0)
            sleep(2)
            torvalds.write(10, 0)
            torvalds.write(9, 0)
            torvalds.write(8, 0)
            torvalds.write(7, 0)
        elif 'south' in text:
            aiy.voice.tts.say('Okay I will go backward')
            torvalds.write(10, 0)
            torvalds.write(9, 1)
            torvalds.write(8, 0)
            torvalds.write(7, 1)
            sleep(2)
            torvalds.write(10, 0)
            torvalds.write(9, 0)
            torvalds.write(8, 0)
            torvalds.write(7, 0)
        elif 'east' in text:
            aiy.voice.tts.say('Okay I will go left')
            torvalds.write(10, 0)
            torvalds.write(9, 1)
            torvalds.write(8, 1)
            torvalds.write(7, 0)
            sleep(0.3)
            torvalds.write(10, 0)
            torvalds.write(9, 0)
            torvalds.write(8, 0)
            torvalds.write(7, 0)
        elif 'west' in text:
            aiy.voice.tts.say('Okay I will go right')
            torvalds.write(10, 1)
            torvalds.write(9, 0)
            torvalds.write(8, 0)
            torvalds.write(7, 1)
            sleep(0.3)
            torvalds.write(10, 0)
            torvalds.write(9, 0)
            torvalds.write(8, 0)
            torvalds.write(7, 0)
        elif 'goodbye' in text:
            aiy.voice.tts.say('Goodbye')
            break

if __name__ == '__main__':
    main()

linus.stop()
torvalds.stop()
