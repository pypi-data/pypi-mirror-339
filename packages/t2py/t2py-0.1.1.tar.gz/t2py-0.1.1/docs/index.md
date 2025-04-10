# T2PY

Python interface for Titan 2. Simple and easy to use.

## Install
```bash
pip install t2py
```

## Basic Usage
```python
import t2py

# List USB devices
for port, vid, pid in t2py.Titan2.getdisc():
    print(f"{port}: {vid:04x}:{pid:04x}")

# Connect to Titan 2
t2 = t2py.Titan2(vid_pid=(0x0483, 0x5740))  # Change to your VID/PID
if t2.connect():
    # Do stuff
    t2.upload("program.gpc")  
    t2.sendgvc([1, 2, 3])  # Send some data
    t2.disconnect()
```

## Functions

### Find USB Devices
```python
# Returns list of (port, vid, pid)
devices = t2py.Titan2.getdisc()
```

### Connect to Device
```python
t2 = t2py.Titan2(vid_pid=(vid, pid))
connected = t2.connect()  # True if connected
```

### Upload GPC File
```python
success = t2.upload("program.gpc")
```

### Send Data
```python
# Can send list or bytes
t2.sendgvc([1, 2, 3])
t2.sendgvc(b'\x01\x02\x03')
```

## API Reference

### Titan2 Class

#### Constructor

```python
Titan2(vid_pid: Tuple[int, int] = None)
```

- `vid_pid`: Optional tuple of (vendor_id, product_id) for USB device

#### Methods

##### connect
```python
connect(vid_pid: Tuple[int, int] = None) -> bool
```
Connects to the device using VID/PID. Returns True if successful.

##### upload
```python
upload(gpc_file: Union[str, Path]) -> bool
```
Uploads a GPC file to the device. Returns True if successful.

##### sendgvc
```python
sendgvc(data: Union[bytes, List[int]]) -> bool
```
Sends GVC data to the device. Returns True if successful.

##### getdisc
```python
@staticmethod
getdisc() -> List[Tuple[str, int, int]]
```
Returns list of connected devices

## Contributing

We welcome contributions! Please see our [Contributing Guide](contributing.md) for details. 