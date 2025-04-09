import unittest
from unittest.mock import Mock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
# from mq4hemc import HemcMessage, HemcMessageDict, HemcTick, getNotifier
import time
from lmk05318 import LMK05318, ConsoleHelper

class TestLMK05318(unittest.TestCase):
    def test_file_parser(self):
        hex_regs_path = os.path.join(os.path.dirname(__file__), 'HexRegisterValuesHemc_2_lines.txt')
        registers = ConsoleHelper.parse(hex_regs_path)
        """
        The file contains 2 lines:
        R0	0x000010
        R411	0x019B08
        """
        expected = [
            (0, 16),
            (411, 8)
        ]
        self.assertEqual(registers, expected)


if __name__ == "__main__":
    unittest.main()
