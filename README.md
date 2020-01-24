# hmkit-python

The HMKit Python SDK makes it easy to work with car data using the HIGH MOBILITY API platform. The SDK implements a strong security layer between your Python app and the platform while giving you straightforward native interface to read and write to connected cars.

The library is designed to give IOT developers simple access to High Mobility's systems, by handling all the communication protocols, authentication flows and other security related components.

Hmkit Python bluetooth SDK has been tested on Raspbian Pi Zero W.

## Getting started

Get started by reading the [Python SDK guide](https://high-mobility.com/learn/tutorials/sdk/python/) in high-mobility.com.

Check out the [code references](https://high-mobility.com/learn/documentation/iot-sdk/python/hmkit/) for more details that is present in code documentation.

Checkout supporting documentations in [Developer Center](https://developers.high-mobility.com/) 

## Requirements

HMKit SDK requires Python 3.7.

Latest Raspbian image for Pi zero comes with Python 3.7 installed. however Python 2.7 may be enabled as default.
Set Python 3.7 as default in alternatives.

```
If Python 3.7 is not default:
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2

#sudo apt-get install python3.7-dev
#sudo apt-get install libglib2.0-dev
#sudo apt-get install libsqlite3-dev
#sudo apt-get install libssl-dev

```

## Integration

Disable system default Bluetooth software elements (run once per reboot)
```
$./sys_bt_off.sh
```

Install SDK ibraries and packages using the script:
```
$ ./install_libs.sh
```

### Examples

There is a sample app available on Github.com to showcase different use-cases for HMKit:

- [Scaffold](https://github.com/highmobility/hm-python-bt-scaffold): Demonstrates the most basic implementation to use HMKit.

### How do I test? ###

Run the commandline example test application by calling:

```
$./test/cmdline.py
```
This command line test app provides test commands to test some autoapi commands.
From Emulator connect to the Device through Bluetooth(symbol at the left bottom corner) 
Pi zero device need internet access to be able to download Access Certificate.

## Contributing

We would love to accept your patches and contributions to this project. Before getting to work, please first discuss the changes that you wish to make with us via [GitHub Issues](https://github.com/highmobility/hmkit-python/issues), [Spectrum](https://spectrum.chat/high-mobility/) or [Slack](https://slack.high-mobility.com/).

See more in [CONTRIBUTING.md](https://github.com/highmobility/hmkit-python/blob/master/CONTRIBUTING.md)

## License ##

This repository is using MIT license. See more in [LICENSE](https://github.com/highmobility/hmkit-python/blob/master/LICENSE)
