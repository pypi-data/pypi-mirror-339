# T2PY

Python interface for Titan 2. Simple and easy to use.

## Install
```bash
pip install t2py
```

## Example
```python
import t2py

# Find Titan Two devices
devices = t2py.Titan2.getdisc()
for port, vid, pid in devices:
    print(f"Found Titan Two: {port}")

# Connect and send data
t2 = t2py.Titan2()  # Uses default VID/PID
if t2.connect():
    # Send GVC values (will be converted to fixed point)
    t2.sendgvc([1, 100])  # First value is flag, second is signal
    
    # Stop signaling
    t2.sendgvc([1, 0])
    t2.disconnect()
```

## Dev
```bash
git clone https://github.com/yourusername/t2py.git
cd t2py
pip install -e ".[dev]"
```

MIT License 