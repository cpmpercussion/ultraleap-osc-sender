# Ultraleap OSC Sender

Experimental project to send data from a Leap Motion Controller as OSC messages.

The `leapc-python-api` code comes from <https://github.com/ultraleap/leapc-python-bindings/>.

The project is derived from the above repository's examples.

## Install

This repo contains the code and pre-compiled module from [leapc-python-bindings](https://github.com/ultraleap/leapc-python-bindings/) but the module is only built for Arm (i.e., M1, M2, M3) macOS. If you don't have one of those, you'll have to follow the instructions for `leapc-cffi` [here](https://github.com/ultraleap/leapc-python-bindings/).

If you do, just run:
```
poetry install
```

## Run

To run the OSC sender, run:

```
poetry run python ultraleap_osc_sender
```
