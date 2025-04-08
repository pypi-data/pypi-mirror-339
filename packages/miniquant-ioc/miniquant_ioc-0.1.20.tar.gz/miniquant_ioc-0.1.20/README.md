EPICS IOC for the PicoQuant HydraHarp 400
=========================================

![release](https://gitlab.com/kmc3-xpp/miniquant-ioc/-/badges/release.svg) 
![pipeline](https://gitlab.com/kmc3-xpp/miniquant-ioc/badges/release/pipeline.svg)
![coverage](https://gitlab.com/kmc3-xpp/miniquant-ioc/badges/release/coverage.svg)

Introduction
------------

The HydraHarp 400 is [advertized as](https://www.picoquant.com/products/category/tcspc-and-time-tagging-modules/hydraharp-400-multichannel-picosecond-event-timer-tcspc-module)
a "multichannel picosecond event timer module" by its manufacturer,
PicoQuant GmbH in Germany.

This is an [EPICS](https://epics-controls.org/) Input-Output Controller (IOC)
application for the HydraHarp. It uses the [EMMI](https://gitlab.com/codedump2/emmi)
API, which in turn uses [Diamond Light Source](https://www.diamond.ac.uk/)'s EPICS
wrapper [pythonSoftIOC](https://github.com/dls-controls/pythonSoftIOC)
(as of September 2023). This means that miniquant-ioc's EPICS CA stack is
essentially the "original" C/C++ implementation, merely interfaced by Python.

The hardware access layer is being published as
[miniquant](https://pypi.org/project/miniquant/) -- a truly Python'esque :)
API layer on top of the [proprietary HydraHarp API](https://github.com/PicoQuant/HH400-v3.x-Demos)
of PicoQuant, but without the EPICS specific code.


Installation
------------

Miniquant-ioc itself is installed fairly easy via PyPI:
```
pip install miniquant-ioc
```

Or via direct clone from Gitlab:
```
git clone https://gitlab.com/codedump2/miniquant-ioc \
    && pip install ./miniquant-ioc
```

If [miniquant](https://pypi.org/project/miniquant/) (the API layer) is not
already installed, it will be automatically pulled from PyPI as a 
dependency of miniquant-ioc. In that case, you will most certainly
have to go through a mildly elaborate set of
[post-install procedures](https://gitlab.com/codedump2/miniquant#installation)
to make sure that miniquant is, in fact, able to find and access your
HydraHarp. (This is owing for one to the proprietary nature of the original
PicoQuant C/C++ API for the HydraHarp, and for another to the fact that
the HydraHarp 400 has a quirky USB controller; it works with any modern upstream
Linux kernel, but requires specialized kernel boot parameter or USB driver module
settings.)

Configuration
-------------

A specific IOC configuration file is necessary to run the Miniquant IOC.
By default, the IOC loads its configuration from
`/etc/miniquant/harp.yaml`, but that behaviour can be overridden using the `-c`
or `--harp-config` command line parameter of `miniquant-ioc`. 

The PyPI installation might have placed a copy of a usable `harp.yaml` in your
`/etc/miniquant/...` directory. If it hasn't, obtain one e.g. from
[here](https://gitlab.com/codedump2/miniquant-ioc/).

The configuration file has two distinct sets of options, organized
in as many top-level YAML sections:

  - `harp`:  general HydraHarp device settings, like measurement mode,
     histogram size and resolution, offsets and zero-crossing levels;
	 contains the following subkeys:
	 
	 - `device`: should have a string as value with one of "first",
	   "any", or a HydraHarp device; the IOC will only connect
	   to the device as specified ("first" and "any" is a good
	   choice if you have only one device attached to a computer's
	   USB ports)
	   
     - `presets`:
	 
	 - `settings`:

  - `epics`: application settings that directly influence the IOC
     behavior; in turn, these are divided in:
	 
	 - `prefix`: single key, contains the EPICS prefix as a string value
	 
	 - `defaults`: default settings to be used for all exported properties,
	   can individually be overridden
	
	 - `harpBase`: contains PV definitions all non channel specific properties
	    of a HydraHarp device to export as PVs (stuffed in a subsection `exports`),
		
     - `harpChannels`: contains PV definitions for all channel specific
       properties. The subkey `interfix` contains a string to use
	   in naming the channel-specific PVs (should contain `{}` format specifier
	   for the channel index), and an `exports` section with actual PV
	   definitions.
	   
  - IOC-specific settings about which properties to export as process
    variables (PVs).

Running
-------



