import hid
import random
from enum import Enum


class EyeMovement(Enum):
    EYES_CLOSED = 1
    EYES_ONE_THIRD_OPEN = 2
    EYES_TWO_THIRDS_OPEN = 3
    EYES_OPEN = 4
    NO_MOVEMENT = 0xFF


class HandMovement(Enum):
    HANDS_DOWN = 1
    HANDS_ONE_THIRD_UP = 2
    HANDS_TWO_THIRDS_UP = 3
    HANDS_UP = 4
    NO_MOVEMENT = 0xFF


class AntennaMovement(Enum):
    ANTENNAS_IN = 1
    ANTENNAS_CENTER = 2
    ANTENNAS_OUT = 3
    NO_MOVEMENT = 0xFF


class ChatmanController:
    VENDOR_ID = 0x04D9
    PRODUCT_ID = 0xA050
    REPORT_ID = 3

    def __init__(self, index=0, reset=True):
        self.device = None
        self.index = index
        self._initialize_device(reset)

    def _send_data(self, data):
        if not self.device:
            raise RuntimeError("Device not initialized")

        command = [self.REPORT_ID] + data + [0] * (7 - len(data))
        print(f"Sending: {bytes(command).hex()}")
        self.device.write(command)

    def _initialize_device(self, reset):
        devices = hid.enumerate(self.VENDOR_ID, self.PRODUCT_ID)
        target_index = self.index * 2 + 1

        if target_index >= len(devices):
            raise RuntimeError(f"No device found at index {self.index}")

        device_path = devices[target_index]["path"]
        self.device = hid.device()
        self.device.open_path(device_path)
        self.device.set_nonblocking(0)
        if not reset:
            return

        xx = random.randint(0, 255)
        self._send_data([0x5A, 0x92, xx])

        response = self.device.read(8)
        if response:
            print(f"Received: {bytes(response).hex()}")
            yy = response[4]
            if (xx + yy) & 0xFF == 0xFF:
                print("Handshake successful!")
                self._configure_all()
                self.reset()
            else:
                print("Invalid handshake response")

    def reset(self):
        try:
            self._send_data([0x5A, 0x90])
            response = self.device.read(8, 1000)
            if response:
                print(f"Received: {bytes(response).hex()}")
                error_code = response[2]
                errors = []
                if (error_code & 1) == 1:
                    errors.append("Eyes")
                if (error_code & 2) == 2:
                    errors.append("Hands")
                if (error_code & 4) == 4:
                    errors.append("Antennas")
                if errors:
                    print(f"Reset failed: {', '.join(errors)}")
                else:
                    print("Reset successful")
        except Exception as e:
            print(f"Reset error: {e}")

    def _send_config(self, config_id, byte_data):
        array = [0] * 5
        i = 0
        while i < len(byte_data) - 1:
            array[0] = i
            j = 1
            while j < 5 and i < len(byte_data) - 1:
                array[j] = byte_data[i]
                i += 1
                j += 1
            while j < 5:
                array[j] = 0
                j += 1
            self._send_data([0x5A, config_id] + array)

    def _configure_all(self):
        self._send_config(0x93, [3, 2, 5, 3, 5, 8, 3, 4, 8, 2, 6, 3])  # Eyes
        self._send_config(0x94, [2, 2, 4, 1, 2, 3, 1, 2, 3, 1, 2, 1])  # Hands
        self._send_config(0x95, [0, 2, 4, 4, 4, 4, 2])                # Antennas

    def move(self, eye: EyeMovement, hand: HandMovement, antenna: AntennaMovement, face_led: list[int]):
        command = [0x80, eye.value, hand.value, antenna.value] + face_led[:3]
        self._send_data(command)
