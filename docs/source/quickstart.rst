.. _getting-started:

###################
Getting Started
###################

.. image:: https://i.imgur.com/7zdSpyQ.png

Mu is a beginners-oriented python code editor that has been built with lots of feedback from teachers and learners throughout the time.
A supported board on the `Mu editor`_ is the `BBC microbit`_ board for which we have created a tailored firmware *(based on the MicroPython project)* that includes the modules 
documented here. The `BBC microbit`_ in turn, gets plugged into the `GiggleBot`_.

The following sections will direct you to setting up the GiggleBot firmware on the `BBC microbit`_ and thus be able to program it with the `Mu editor`_.
At the end of these short instructions, you will be able to run the following snippet of code that lights up the eye LEDs on the `GiggleBot`_.

.. code-block:: python

    from microbit import *
    from gigglebot import *

    # initialize the neopixels on the GiggleBot
    init()

    while True:
        set_eyes() # set GiggleBot eyes to blue (by default)
        sleep(250) # wait 250 msec
        pixels_off() # turn off the GiggleBot eyes
        sleep(250) # wait 250 msec
      

************************
Downloading the Firmware
************************

The 1st option in downloading the firmware is to visit the direct link placed in here and download the afferent file. Make sure you download it as a ``hex`` file.

.. ifconfig:: icbranch != 'master'

    The latest version (which is |fwversion|) of the firmware can also be directly downloaded from |firmware|.

.. ifconfig:: icbranch == 'master'

    .. ifconfig:: iclen_tag_version == 0

        The latest version (which is |fwversion|) of the firmware can also be directly downloaded from |firmware|.

    .. ifconfig:: iclen_tag_version > 0

        To download the current version |fwversion| corresponding to this documentation, click |firmware|.


.. figure:: https://i.imgur.com/h7xhS2n.gif
   :align: center
   :alt: download the firmware directly

The 2nd option is head over to this project's `release page <https://github.com/RobertLucian/micropython-gigglebot/releases>`_ and download the appropriate firmware for the appropriate documentation.
As of this moment, this is the `latest release <https://github.com/RobertLucian/micropython-gigglebot/releases/latest>`_.

.. figure::  _static/gifs/download_firmware.gif
   :align:   center
   :alt: downloading the gigglebot firmware


************************
Downloading the Modules
************************

Apart from being able to download the firmware, the ``.py`` and ``.mpy`` modules can also be downloaded. And just like with the firmware,
you can either download the modules from the `release page <https://github.com/RobertLucian/micropython-gigglebot/releases>`_ or by accessing the following direct links for version |fwversion|:
:s3-storage-module:`gigglebot.py <gigglebot.py>`, :s3-storage-module:`distance_sensor.py <distance_sensor.py>`, :s3-storage-module:`thp.py <thp.py>`, :s3-storage-module:`lightcolor.py <lightcolor.py>`,
:s3-storage-module:`gb_diag.py <gb_diag.py>`.

You can also check this artifact explorer `here <https://dexind.s3.amazonaws.com/index.html#micropython-gigglebot/firmware/>`__.

.. important:: 

    Downloading the modules when the *GiggleBot MicroPython Firmware* is used is redundant. Use the modules (the ``py`` modules) when you are using the basic
    version of micropython. And in that case, not all ``py`` modules will work - for that check this :ref:`section <firmware-how>` and see how you can pair the modules to fit on a basic firmware.

*************************
Flashing the Firmware
*************************

Flashing the firmware is a breeze. Connect the `BBC microbit`_ to your laptop, wait until the *MICROBIT* filesystem appears and then copy-paste the GiggleBot firmware you just
downloaded to the microbit.

.. figure::  _static/gifs/flash_firmware.gif
   :align:   center
   :alt: flashing the gigglebot firmware

After flashing the firmware, you will be able to import all modules listed in this documentation.

********************************
Custom Firmware in the Mu Editor
********************************

The `Mu Editor`_ comes with a default firmware for the microbit that can be overridden with the GiggleBot firmware instead.
All that has to be done is to press on the *gear wheel* on the right hand side of the editor, then go to *BBC micro:bit Settings* and lastly,
copy paste the path to the custom firmware (or runtime as the Mu editor likes to call).

.. figure::  _static/gifs/override_firmware.gif
   :align:   center
   :alt: overriding the mu editor's firmware with the gigglebot one


**************************
Upgrading DAPLink Firmware
**************************

There may be cases when `BBC microbit`_ fails to flash the firmware when the binary is dragged and dropped. This is generally caused by an old version of the DAPLink firmware.
This DAPLink firmware provides the USB interface that allows you to drag-and-drop binaries onto the target microcontroller (the microbit).

This DAPLink firmware can be easily upgraded. Just go over `this short tutorial <https://www.mbed.com/en/platform/hardware/prototyping-production/daplink/daplink-on-kl26z/>`_ to upgrade it.

.. _gigglebot: https://www.gigglebot.io/
.. _distance sensor:  https://www.gigglebot.io/collections/frontpage/products/distance-sensor
.. _mu editor: https://codewith.mu/en/
.. _bbc microbit: https://microbit.org/
