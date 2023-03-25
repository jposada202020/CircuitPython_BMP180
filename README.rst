Introduction
============
CircuitPython driver from BMP180 Temperature and Barometic Pressure sensor adapted from `CircuitPython driver for BMP280 <https://github.com/adafruit/Adafruit_CircuitPython_BMP280/>`
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
    pip3 install circuitpython-qmc5883l

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install bmp180

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

Take a look a the ``bmp180_simpletest.py`` in the examples directory

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-qmc5883l.readthedocs.io/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/jposada202020/CircuitPython_bmp180/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

