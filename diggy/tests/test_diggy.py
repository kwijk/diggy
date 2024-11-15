import pydicom
from pydicom.data import get_testdata_file
from diggy.diggy import Diggy
from diggy.tests.utils import find_free_port


class TestDiggy:

    def test_diggy_c_echo_scp_scu(self, caplog):

        port = find_free_port()

        with Diggy(address=("127.0.0.1", port), block=False) as diggy:
            diggy.send_c_echo("DIGGY", "127.0.0.1", port)

        assert "C-Echo request from DIGGY at" in caplog.text

    def test_diggy_c_store_scp(self, caplog):

        port = find_free_port()

        ds = pydicom.data.get_testdata_file("MR_small.dcm", read=True)

        with Diggy(address=("127.0.0.1", port), block=False) as diggy:
            diggy.send_c_store("DIGGY", "127.0.0.1", port, instances=[ds])

        assert "C-Store request from DIGGY at" in caplog.text
