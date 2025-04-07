# P2PlantAccess
Access to process variable of a [P2Plant](https://github.com/ASukhanov/P2Plant).

## Demo
Start simulatedADCs plant as discribed in the P2Plant module:<br>
Start the client:<br>
``` python3 -m p2plantaccess.simulatedADCs -k -g```<br>
A dynamic plot should appear with 8 sawtooth curves.

### Example of Python interaction with simulatedADCs
Have the simulatedADCs plant running.
```python
from p2plantaccess import Access as pa
pa.init()
pa.start()

pa.request(["info", ["*"]])
{'*': {'version': 'MCU and software version, system clock', 'debug': 'Show debugging messages', 'run': 'For experts. Start/Stop board peripherals except ADCs', 'sleep': 'Sleep in the program loop', 'perf': 'Performance counters. TrigCount, RPS in main loop', 'adc_offsets': 'Offsets of all ADC channels', 'adc_reclen': 'Record length. Number of samples of each ADC', 'adc_srate': 'Sampling rate of ADCs', 'adc': 'Two-dimentional array[adc#][samples] of ADC samples'}}

pa.request(["get", ["version"]])
{'version': {'v': 'MCU: STM32G431, soft:0.2.0 2025-02-02, clock:170000000,baudrate:7372800', 't': (1738803674, 976149845)}}

# Get info on run and sleep PVs:
pa.request(['info', ['run','sleep']])
{'run': {'desc': 'For experts. Start/Stop board peripherals except ADCs', 'type': 'char*', 'shape': [1], 'fbits': 'WRDsrE', 'legalValues': 'start,stop'}, 'sleep': {'desc': 'Sleep in the program loop', 'type': 'uint32', 'shape': [1], 'fbits': 'R', 'units': 'ms', 'opLow': 0, 'opHigh': 10000}}

pa.request(["get", ["run"]])
{'run': {'v': 'start', 't': (1738803674, 976150227)}}

pa.request(['set', [('run','stop')]])
{}

pa.request(["get", ["run"]])
{'run': {'v': 'stop', 't': (1738803674, 976150227)}}

pa.request(['get', ['adc']])
{'adc': {'shape': [8, 80], 'v': array([[
        10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
        26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
...
         1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16]],
      dtype=uint16), 't': (1738803674, 976151047)}}

