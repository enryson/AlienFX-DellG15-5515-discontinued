# AlienFX for Dell G15 5515
## _GTK app for controling the keyboard lights_

![](https://github.com/enryson/AlienFX-DellG15-5515/raw/main/screenshots/Screenshot%20from%202022-05-08%2002-42-36.png)
#### Disclamer
I used the [elc_ng.py](https://gist.github.com/Cheaterman/accd912c6886f4055f45d0594b88553c) LIB made by [Cheaterman](https://gist.github.com/Cheaterman)
(Sorry for my english)

My objective is make a simple clean software for controlling the lights on my laptop (dell G15 5515).
This is my first Python and GTK app, so forgive a few bugs and a messy code.

## Features
- Control the 4 zones of the keyboard
- All changes are stored on a config file and read when the app open

## Upcoming
- Installer
- .desktop file
- better interface
- other effects
- script for restore the pre configure lights (can be used when booting or as a handler for the LID)
- other devices and layouts
- AUR package/ Flatpack?

## Install(kinda)
Isn´t 100%
Depenencies (Arch Linux)
```sh
sudo pacman -S python-pyusb python-setuptools python-gobject python-cairo python-future
```
Clonning the project
```sh
cd ~
mkdir GitHub
git clone https://github.com/enryson/AlienFX-DellG15-5515.git
cd AlienFX-DellG15-5515
```
AlienFX uses USB protocol for the lights
For access without SUDO you need change the access of the USB controller
Just copy the RULES file to the correct directory and reboot OR refresh the UDEV permissions
```sh
sudo cp rules/10-alienfx.rules /etc/udev/rules.d/
```
To run the app just type:
```sh
python alienfx-gui.py
```
I include a .desktop file (isn´t 100%) you need change some stuff.

## Can work on the G7 and other models?
No idea, you can try...
you can run:
- if you get a error of permissions try running as SUDO or appy the RULE fix above
```sh
python functions/test.py
```

If this did´t work you can try modding the file
inside of this file you have this line:
```sh
elc.execute(ColorCommand([8] , 255,255,255))
```
This section of the code is responsable for the ZONE, you can change the number 8, and try a diferent number and see if something happend..
```sh
ColorCommand([8]...
```
oh my case:
- 8 is the left side of the keyboard.
- 9 is the middle left side...
- 10 is the middle right...
- 11 is the right...

if you get lucky, you can modify the color.py with your zones.

This part of the code is responsable for setting the color "red, green, blue" with this exacly sequence
you can mix the values from 0 to 255. the code below is for the white color...
```sh
255,255,255
```


