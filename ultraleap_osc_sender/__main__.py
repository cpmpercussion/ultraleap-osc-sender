"""
Connects to one or more leap devices and attempts to send hand tracking events via OSC.
"""

import leap
import time
from timeit import default_timer as timer
from typing import Callable
from leap.events import TrackingEvent
from leap.event_listener import LatestEventListener
from leap.datatypes import FrameData
from pythonosc import udp_client

OSC_IP = "localhost"
OSC_PORT = 5000

osc_client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)


class MultiDeviceListener(leap.Listener):
    def __init__(self, event_type):
        super().__init__()
        self._event_type = event_type
        self.n_events = 0

    def on_event(self, event):
        if isinstance(event, self._event_type):
            self.n_events += 1


def wait_until(condition: Callable[[], bool], timeout: float = 5, poll_delay: float = 0.01):
    start_time = timer()
    while timer() - start_time < timeout:
        if condition():
            return True
        time.sleep(poll_delay)
    if not condition():
        return False


class TrackingEventListener(leap.Listener):
    def __init__(self):
        self.device_latest_tracking_event = {}

    def number_of_devices_tracking(self):
        return len(self.device_latest_tracking_event)

    def on_tracking_event(self, event):
        # print(
        #     f"Frame {event.tracking_frame_id} with {len(event.hands)} hands on device {event.metadata.device_id}"
        # )
        for hand in event.hands:
          hand_type = "left" if str(hand.type) == "HandType.Left" else "right"
          osc_client.send_message(f"/leap/{hand_type}", [hand.palm.position.x, hand.palm.position.y, hand.palm.position.z])
          print(
              f"Hand id {hand.id} is a {hand_type} hand with position ({hand.palm.position.x}, {hand.palm.position.y}, {hand.palm.position.z})."
          )
        source_device = event.metadata.device_id
        self.device_latest_tracking_event[source_device] = event


def get_updated_devices(connection):
    devices = connection.get_devices()

    for device in devices:
        with device.open():
            connection.subscribe_events(device)


def main():
    tracking_listener = TrackingEventListener()
    device_listener = MultiDeviceListener(leap.events.DeviceEvent)

    connection = leap.Connection(multi_device_aware=True)
    connection.add_listener(tracking_listener)
    connection.add_listener(device_listener)

    with connection.open():
        wait_until(lambda: device_listener.n_events > 1)

        current_device_events = device_listener.n_events
        get_updated_devices(connection)

        while True:
            if device_listener.n_events != current_device_events:
                print("device_listener got a new device event")
                current_device_events = device_listener.n_events
                get_updated_devices(connection)

            time.sleep(0.5)


if __name__ == "__main__":
    main()