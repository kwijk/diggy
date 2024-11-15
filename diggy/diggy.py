import logging
import pydicom
from pynetdicom import (
    AE,
    evt,
    _config,
    ALL_TRANSFER_SYNTAXES,
    AllStoragePresentationContexts,
)
from pynetdicom.sop_class import Verification
from pynetdicom.events import Event

# Accept unknown or private SOP classes from any SCU
_config.UNRESTRICTED_STORAGE_SERVICE = True


class Diggy:

    def __init__(
        self,
        ae_title: str = "DIGGY",
        address: tuple[str, int] = ("127.0.0.1", 4242),
        storage_folder: str = "/tmp",
        block: bool = True,
    ):
        self.ae = AE(ae_title=ae_title)
        self.ae.add_supported_context(Verification, ALL_TRANSFER_SYNTAXES)
        for cx in AllStoragePresentationContexts:
            self.ae.add_supported_context(cx.abstract_syntax, ALL_TRANSFER_SYNTAXES)
        self.storage_folder = storage_folder

        self.logger = logging.getLogger("diggy")

        handlers = [
            (evt.EVT_C_ECHO, self.handle_echo),
            (evt.EVT_C_STORE, self.handle_store),
        ]

        self.ae.start_server(address, evt_handlers=handlers, block=block)

    def handle_echo(self, event: Event):
        ae = event.assoc.requestor.ae_title
        ip = event.assoc.requestor.address
        port = event.assoc.requestor.port

        self.logger.info(f"C-Echo request from {ae} at ({ip}:{port})")

        return 0x0000

    def handle_store(self, event: Event):
        ae = event.assoc.requestor.ae_title
        ip = event.assoc.requestor.address
        port = event.assoc.requestor.port

        self.logger.info(f"C-Store request from {ae} at ({ip}:{port})")

        return 0x0000

    def send_c_echo(self, aet: str, address: str, port: int):
        ae = AE(ae_title=aet)
        ae.add_requested_context(Verification)
        assoc = ae.associate(address, port)
        if assoc.is_established:
            status = assoc.send_c_echo()
            if status:
                # If the verification request succeeded this will be 0x0000
                self.logger.info(
                    "C-ECHO request status: 0x{0:04x}".format(status.Status)
                )
            else:
                self.logger.info(
                    "Connection timed out, was aborted or received invalid response"
                )

            # Release the association
            assoc.release()

        else:
            self.logger.info("Association rejected, aborted or never connected")

    def send_c_store(
        self, aet: str, address: str, port: int, instances: list[pydicom.Dataset]
    ):

        ae = AE(ae_title=aet)

        sop_classes = {str(ds.SOPClassUID) for ds in instances if "SOPClassUID" in ds}
        for sop_class_uid in sop_classes:
            ae.add_requested_context(sop_class_uid)

        assoc = ae.associate(address, port)
        if assoc.is_established:
            for ds in instances:
                status = assoc.send_c_store(ds)
                if status:
                    # If the verification request succeeded this will be 0x0000
                    self.logger.info(
                        "C-Store request status: 0x{0:04x}".format(status.Status)
                    )
                else:
                    self.logger.info(
                        "Connection timed out, was aborted or received invalid response"
                    )

            # Release the association
            assoc.release()

        else:
            self.logger.info("Association rejected, aborted or never connected")

    # def start(
    #     self,
    #     address: str = "127.0.0.1",
    #     port: int = 4242,
    #     block: bool = True,
    # ):
    #
    #     handlers = [(evt.EVT_C_ECHO, self.handle_echo)]
    #
    #     self.ae.start_server(
    #         (address, port), evt_handlers=handlers, block=block
    #     )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.ae.shutdown()
