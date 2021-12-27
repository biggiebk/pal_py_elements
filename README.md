# Welcome to the Pal Py Elements Project

These are the standard python Pal services used to initiate actions and/or report status. Elements essentially listen as a consumer to a topic on Kafka and then initiate the requested action.  If required it will then submit a request to other topics as a producer to initiate other activity or report status/errors.

## Requirements

- [kafka-python](https://github.com/dpkp/kafka-python) - Kafka connection library
- [hue-py](https://github.com/mattboran/hue_py) - Philips HUE Lights
- [python-magichue](https://github.com/namacha/python-magichue) - Magic Hue, FluxLED, etc... lights
- [Tiny Tuya](https://github.com/jasonacox/tinytuya) - Tuya (MagicHome) lights support
- [VLC Media Player](https://www.videolan.org/vlc/) - Used to play audio
- [python-vlc](https://wiki.videolan.org/Python_bindings/) - Python bindings for VLC Media player
- [pymongo](https://github.com/mongodb/mongo-python-driver) - Connect and query mongo from python

### Optional

- [crc32c](https://github.com/ICRAR/crc32c) - enables better performance for kafka-python.  Suspect it will not make a major difference for most deployments, however I still recommend using it.

## Supported Elements (Services)

### Devices

#### Lights

- Philips
- Magic HUE
- Tiny Tuya (MagicHome)

### Services

#### Audio

- Player - Controls a VLC audio player running on a server
