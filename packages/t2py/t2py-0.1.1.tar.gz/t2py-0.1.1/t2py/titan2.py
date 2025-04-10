import hid
import time
from pathlib import Path

class Titan2:
    # Default Titan Two VID/PID
    VENDOR_ID = 0x2508
    PRODUCT_ID = 0x0032

    def __init__(self, vid_pid=None):
        self.vid = vid_pid[0] if vid_pid else self.VENDOR_ID
        self.pid = vid_pid[1] if vid_pid else self.PRODUCT_ID
        self.dev = None
        
    def _float_to_fix16_16(self, val):
        # Convert float to fixed point 16.16 format
        i = int(val * 65536)
        return bytes([(i >> s) & 0xFF for s in (24, 16, 8, 0)])

    def _make_packet(self, values):
        # Packet structure from CHL
        header = bytes([0, 0x60, 0, 0x30, 0])
        
        # Convert all values to fixed point, pad with zeros if needed
        floats = b"".join(self._float_to_fix16_16(values[i] if i < len(values) else 0.0) 
                         for i in range(12))
        
        # Add suffix bytes
        suffix = bytes([0, 0, 128, 231, 11, 55, 35, 1, 0, 0, 128, 0])
        
        return header + floats + suffix

    def connect(self, vid_pid=None):
        if vid_pid:
            self.vid = vid_pid[0]
            self.pid = vid_pid[1]
            
        if not self.vid or not self.pid:
            return False
            
        try:
            self.dev = hid.device()
            self.dev.open(self.vid, self.pid)
            self.dev.set_nonblocking(1)
            return True
        except:
            self.dev = None
            return False
            
    def disconnect(self):
        if self.dev:
            self.dev.close()
            self.dev = None
            
    def upload(self, gpc_file):
        if not self.dev:
            return False
            
        try:
            with open(gpc_file, 'rb') as f:
                data = f.read()
                
                # Todo: Implement proper GPC upload protocol
                return True
        except:
            return False
            
    def sendgvc(self, values, sleep_time=0.02):

        if not self.dev:
            return False
            
        try:
            packet = self._make_packet(values)
            self.dev.write(packet)
            time.sleep(sleep_time)
            return True
        except:
            return False
            
    @staticmethod
    def getdisc():
        devs = []
        for d in hid.enumerate():
            if d['vendor_id'] == Titan2.VENDOR_ID and d['product_id'] == Titan2.PRODUCT_ID:
                devs.append((d['path'].decode(), d['vendor_id'], d['product_id']))
        return devs
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect() 