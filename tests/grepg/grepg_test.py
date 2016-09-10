import unittest
from mock import patch
import argparse
from ..grepg.subcommands.Search import Search
from grepg.grepg import GrepG

class GrepGTest(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(subcommad="search"))
    def test_create_command_clazz(self):
        parsed_args = argparse.ArgumentParser.parse_args()
        expected = GrepG.create_command_clazz(parse_args)
        assert(isinstance(expected, Search))


if __name__ == '__main__':
    unittest.main()

