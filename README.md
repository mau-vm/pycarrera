pycarrera
=========
This project provides python bindings for communicating with a Carrera Digital Slot Car 132/124 Control Unit. I created the project to run on a



* A Race Monitor class for monitoring the state of a race.
* A simple REST API for querying the Race Monitor.


Usage:
Control Unit Client
```python
from pycarrera import ControlUnitClient

# our TTL-Serial cable shows up on port ttyUSB0
serial_port = '/dev/ttyUSB0'
client = ControlUnitClient(serial_port)



```

Credit
====
This library is only possible because Stephan Hess (http://www.slotbaer.de/) did all of the hard work decoding the Control Unit protocol.