# Welcome to the pal_py_elements wiki!

These are the standard python Pal services used to initiate actions and/or report status. Elements essentially listen as a consumer to a topic on Kafka and then initiate the requested action.  If required it will then submit a request to other topics as a producer to initiate other activity or report status/errors.

## Requirements

- A running Kafka cluser or server.
- [kafka-python](https://github.com/dpkp/kafka-python) - Kafka connection library
- [hue-py](https://github.com/mattboran/hue_py) - Philips HUE Lights
- [python-magichue](https://github.com/namacha/python-magichue) - Magichome, FluxLED, etc... lights
- [Tiny Tuya](https://github.com/jasonacox/tinytuya) - Tuya lights support

### Optional

- [crc32c](https://github.com/ICRAR/crc32c) - enables better performance for kafka-python.  Suspect it will not make a major difference for most uses, however I still recommend using it.

## Supported Elements (Services)

### Devices

#### Lights

- Philips
- Magic HUE
- Tiny Tuya

### Services

#### Audio

- VLC - Controls a VLC audio player running on a server
- Local - (Planned) Enable a local play stored on a server to play local

#### Calendar

- Days Since/Till - Either a running count of days since an event or the number of days till
- Google Calendar - (Planned) Integration with google calendars.

#### Weather

- [National Weather Service](https://www.weather.gov/documentation/services-web-api)
- [Ambient Weather](https://help.ambientweather.net/help/api/)
