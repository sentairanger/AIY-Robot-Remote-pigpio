# AIY-Robot-Remote-pigpio


## Introduction

This project is based on the previous project I had done using my robot Linus. If you want more information, click [this](https://github.com/sentairanger/Linus-Google-AIY-Robot) link. However, unlike that project I used pigpio due to the limitations of gpiozero. I also used my robot Torvalds that I used from [this](https://github.com/sentairanger/Torvalds-Computer-Vision) project. 

## Getting started

To get started I removed the Voice Kit from my robot Linus and added another Raspberry Pi Zero instead. I decided to use the Voice Kit to control Linus remotely. I tried to control Linus using gpiozero but could not get the motors to run. So instead I used pigpio and it worked. Pigpio is similar to RPi.GPIO and gpiozero but is used to control GPIO pins directly and remotely. For this project I had to get the following materials:

1. My robot Linus
2. My robot Torvalds
3. Google AIY Voice Kit v2
4. 5v 3A Micro USB power supply for the Voice Kit
5. My Linux Desktop to control all three devices via SSH

In order to get things running I had to install pigpio on the Pi Zero W that controls my robot Linus because I installed Raspberry Pi OS Lite which does not have pigpio. Once I got that installed, I had to enable pigpio using raspi-config and the command `sudo pigpiod` to enable the pigpio daemon. Once I had it running everything worked just fine.

Note: to control a Raspberry pi remotely, you must use the following syntax: `pigpio.pi('ip-address')`. Make sure you use different names for each definition to avoid confusion.

## Explanation of Code

`linus_robot.py`: Controls my robot Linus using the Voice Kit. 

`torvalds_robot.py`: Controls my robot Torvalds also using the Voice kit.

`dual_robot.py`: Controls both robots also using the Voice kit.

## Updates

Any future updates will be posted here.
