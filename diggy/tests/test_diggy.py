from diggy.diggy import Diggy
from diggy.tests.utils import find_free_port


class TestDiggy:

    def test_diggy(self, caplog):

        port = find_free_port()

        with Diggy(address=("127.0.0.1", port), block=False) as diggy:
            diggy.send_c_echo("DIGGY", "127.0.0.1", port)

        assert "C-Echo request from DIGGY at" in caplog.text
