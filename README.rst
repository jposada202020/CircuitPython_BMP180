Introduction
============

.. image:: https://readthedocs.org/projects/circuitpython-bmp180/badge/?version=latest
    :target: https://circuitpython-bmp180.readthedocs.io/
    :alt: Documentation Status

.. image:: https://github.com/jposada202020/CircuitPython_BMP180/workflows/Build%20CI/badge.svg
    :target: https://github.com/jposada202020/CircuitPython_BMP180/actions
    :alt: Build Status

.. image:: https://img.shields.io/pypi/v/circuitpython-bmp180.svg
    :alt: latest version on PyPI
    :target: https://pypi.python.org/pypi/circuitpython-bmp180

.. image:: https://static.pepy.tech/personalized-badge/circuitpython-bmp180?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Pypi%20Downloads
    :alt: Total PyPI downloads
    :target: https://pepy.tech/project/circuitpython-bmp180


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython driver from BMP180 Temperature and Barometric Pressure sensor
Derived from the work of BadTigrou

Installation and Dependencies
=============================

This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_


On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-bmp180/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-bmp180

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-bmp180

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install circuitpython-bmp180

Usage Example
=============

Take a look a the ``bmp180_simpletest.py`` in the examples directory

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-bmp180.readthedocs.io/>`_.
