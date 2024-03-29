import os
import io
import datetime

class StaleFile(io.FileIO):
    def __init__(self, filename, mode='r'):
        super().__init__(filename, mode)
        self.filename = filename

    def save(self, contents, keep_len):
        if isinstance(contents, str):
            with open(self.filename, 'w') as f:
                f.write(contents)
        elif isinstance(contents, bytearray):
            with open(self.filename, 'wb') as f:
                f.write(contents)
        now = datetime.datetime()
        stale_time = now + keep_len
        os.setxattr(self.filename, 'user.staletime', stale_time)

    def open(self, typecode):
        now = datetime.datetime()
        stale_time = os.getxattr(self.filename, 'user.staletime')
        if (now > stale_time) or \
                (not os.path.isfile(self.filename)):
            return None
        else:
            with open(self.filename, typecode) as f:
                contents = f.read()
            return contents 
            
    def __enter__(self, filename):
        pass
        
    def __exit__(self, exc_type, exc_value, exc_tb):
        pass