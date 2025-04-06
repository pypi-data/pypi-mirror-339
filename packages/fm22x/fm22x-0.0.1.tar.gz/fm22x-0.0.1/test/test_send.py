import sys

from fm22x.response import MidEnroll

sys.path.append(".")

from serial import Serial
from serial.tools import list_ports
from fm22x.connection import Connection
from fm22x.request import GetVersion, Enroll, FaceDir

from unittest import TestCase

s = Serial()
ports = list_ports.comports()
for port in ports:
    print(port.name)

class TestSerial(TestCase):
    def setUp(self):
        self.con = Connection()


    def test_sebd_with_serial(self):
        serial = Serial("COM4")
        data_to_send: bytes = self.con.send(GetVersion())
        print(data_to_send)
        serial.write(data_to_send)
        data = serial.read_all() # fixme
        print(data)
        for ev in self.con.receive(data):
            print(ev)

    def test_sebd_with_serial2(self):
        serial = Serial("COM1")
        data_to_send: bytes = self.con.send(Enroll(True, "a1"*16, FaceDir.UNDEFINE, 0))
        print(data_to_send.hex())
        serial.write(data_to_send)
        data = serial.read_all() # fixme
        print(data)
        for ev in self.con.receive(data):
            print(ev)


if __name__ == "__main__":
    import unittest

    unittest.main()