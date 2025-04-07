import unittest
from openscan import scan_ports

class TestOpenScan(unittest.TestCase):
    def test_localhost(self):
        # Test scanning localhost (127.0.0.1) for a small range
        open_ports = scan_ports("127.0.0.1", start_port=1, end_port=10)
        self.assertIsInstance(open_ports, list)

if __name__ == "__main__":
    unittest.main()