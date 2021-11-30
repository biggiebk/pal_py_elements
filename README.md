# Welcome to the Pal Py Elements project

These are the standard python Pal services used to initiate actions and/or report status. Elements essentially listen as a consumer to a topic on Kafka and then initiate the requested action.  If required it will then submit a request to other topics as a producer to initiate other activity or report status/errors.

## Requirements

- A running Kafka cluser or server.
- [kafka-python](https://github.com/dpkp/kafka-python) - Kafka connection library
- [beartype](https://github.com/beartype/beartype) - PEP-compliant constant-time runtime type checker
- [hue-py](https://github.com/mattboran/hue_py) - Philips HUE Lights
- [python-magichue](https://github.com/namacha/python-magichue) - Magichome, FluxLED, etc... lights
- [Tiny Tuya](https://github.com/jasonacox/tinytuya) - Tuya lights support

### Optional

- [crc32c](https://github.com/ICRAR/crc32c) - enables better performance for kafka-python.  Suspect it will not make a major difference for most deployment, however I still recommend using it.

## Supported Elements (Services)

### Devices

#### Lights

- Philips
- Magic HUE
- Tiny Tuya

### Services

#### Audio

- VLC - Controls a VLC audio player running on a server
- Local - (Planned) Enable a local media stored on a server to play locally

#### Calendar

- Days Since/Till - Either a running count of days since an event or the number of days till
- Google Calendar - (Planned) Integration with google calendars.

#### Weather

- [National Weather Service](https://www.weather.gov/documentation/services-web-api)
- [Ambient Weather](https://help.ambientweather.net/help/api/)
