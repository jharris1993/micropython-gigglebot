## GiggleBot MicroPython for the BBC Micro:bit 
[![Build Status](https://travis-ci.org/RobertLucian/micropython-gigglebot.svg?branch=master)](https://travis-ci.org/RobertLucian/micropython-gigglebot) [![Documentation Status](https://readthedocs.org/projects/gigglebot-dev/badge/?version=develop)](https://gigglebot-dev.readthedocs.io/en/develop/?badge=develop)

This is the repository for the MicroPython that's running on the BBC micro:bit + GiggleBot robot.

This firmware, when compared to [bbcmicrobit/micropython](https://github.com/bbcmicrobit/micropython), has libraries to support the collection of sensors that go on a GiggleBot. Also, there are a couple of features enabled that allow the use of pre-compiled modules on the microbit and others that permit the better use of the memory.

Check the documentation for more details.

![](docs/source/_static/images/GiggleBot-Line_Follower_900x.png)

Artifacts can be found on the release page or on [this S3 bucket](https://dexind.s3.amazonaws.com/index.html#micropython-gigglebot/firmware/).

## Building It

Running the following commands are enough to build the firmware locally.
```bash
docker image build -t gigglebot-micropython src
docker container run --name gigglebot gigglebot-micropython
docker container cp gigglebot:/src/gupy/build/firmware.hex build/
docker container cp gigglebot:/src/tmp/ build/
```

This can take up to 5-8 minutes to finish so go grab a coffee. 

When it's done, a `firmware.hex` will show up in `build` directory. In the `build` directory there's also going to be a `tmp` directory containing `mpy` and `py` files of the libraries that get compiled into the firmware.

The last thing to do is to copy paste the `firmware.hex` to the microbit. 

## Project Structure

* **docs** - Contains the ReadTheDocs documentation.
* **integration** - Scripts required by the CI system.
* **misc** - Various useful tools. At the moment it only contains the color picker for HSV values.
* **src** - The python libraries for the GiggleBot + DI-Sensors along with the Dockerfile and other custom source/header files.
    * **inc** - Custom header files used to reduce the size of the firmware.
    * **source** - Custom source files used to reduce the size of the firmware.
* **static** - Photo with the GiggleBot.