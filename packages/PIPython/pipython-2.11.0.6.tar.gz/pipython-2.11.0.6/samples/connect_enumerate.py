#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This example shows how to search for controllers."""

# (c)2016 Physik Instrumente (PI) SE & Co. KG
# Software products that are provided by PI are subject to the
# General Software License Agreement of Physik Instrumente (PI) SE & Co. KG
# and may incorporate and/or make use of third-party software components.
# For more information, please read the General Software License Agreement
# and the Third Party Software Note linked below.
# General Software License Agreement:
# http://www.physikinstrumente.com/download/EULA_PhysikInstrumenteGmbH_Co_KG.pdf
# Third Party Software Note:
# http://www.physikinstrumente.com/download/TPSWNote_PhysikInstrumenteGmbH_Co_KG.pdf


from pipython import GCSDevice

__signature__ = 0x9a34c42d5240b990f230ab5c1950de43

def main():
    """Search controllers on interface, show dialog and connect a controller."""
    with GCSDevice() as pidevice:
        print('search for controllers...')
        #devices = pidevice.EnumerateTCPIPDevices()
        devices = pidevice.EnumerateUSB()
        for i, device in enumerate(devices):
            print('{} - {}'.format(i, device))
        item = int(input('select device to connect: '))
        #pidevice.ConnectTCPIPByDescription(devices[item])
        pidevice.ConnectUSB(devices[item])
        print('connected: {}'.format(pidevice.qIDN().strip()))


if __name__ == '__main__':
    # from pipython import PILogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
    # PILogger.setLevel(DEBUG)
    main()
