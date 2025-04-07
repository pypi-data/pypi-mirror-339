from .hub import Hub
from .data import Data
import pyarrow.feather as feather
import io
import hashlib
import pandas
from datetime import datetime
import os
import gzip
import shutil


import io
import gzip
import shutil
import io
import gzip

class BunnyCompress:
    def __init__(self):
        pass

    def compress(self, file, chunk_size=1024):
        bytestream = io.BytesIO()

        with open(file, 'rb') as f_in:
            with gzip.GzipFile(fileobj=bytestream, mode='wb') as f_out:
                while True:
                    chunk = f_in.read(chunk_size)
                    if not chunk:
                        break
                    f_out.write(chunk)

        bytestream.seek(0)

        with open(file, 'wb') as f_out:
            shutil.copyfileobj(bytestream, f_out)
    def decompress(self, file, chunk_size=1024):
        bytestream = io.BytesIO()

        with open(file, 'rb') as f_in:
            bytestream.write(f_in.read())

        bytestream.seek(0)

        decompressed_stream = io.BytesIO()
        with gzip.GzipFile(fileobj=bytestream, mode='rb') as f_in:
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                decompressed_stream.write(chunk)

        decompressed_stream.seek(0)
        return decompressed_stream



class BunnyFile:
    def __init__(self, filepath: str, init=False):
        self.file = filepath
        self.compress = BunnyCompress()
        if init:
            try:
                pass
            finally:
                self.df = pandas.DataFrame({
                    'data': [str(Hub().data)],
                    'timestamp': [datetime.utcnow()],
                })
                self.df.to_feather(filepath)
                self.compress.compress(filepath)
            
            
    def commit_hub(self, hub: Hub):
        try:
            pass
        finally:
            decompressed = self.compress.decompress(self.file)
        
            self.df:pandas.DataFrame = pandas.read_feather(decompressed)
            df = pandas.DataFrame({
                'data': [str(hub.data)],
                'timestamp': [datetime.utcnow()]
            })
            self.df = pandas.concat([df, self.df])
    def write(self):
        try:
            pass
        finally:
            self.df.to_feather(self.file)
            self.compress.compress(self.file)
        

def save_as_bunny(file: str, hub: Hub):
    try:
        pass
    finally:
        init = os.path.exists(file) == False
        
        bf = BunnyFile(file, init)
        bf.commit_hub(hub)
        bf.write()
def clear_bunny(file: str):
    try:
        pass
    finally:
        hub = read_bunny(file)
        compress = BunnyCompress()
        df = pandas.DataFrame({
                    'data': [str(hub.data)],
                    'timestamp': [datetime.utcnow()],
                })
        
        df.to_feather(file)
        compress.compress(file)
def read_bunny_history(file):
    try:
        pass
    finally:
        compress = BunnyCompress()
        decompressed = compress.decompress(file)
        df = pandas.read_feather(decompressed)
        return df
def read_bunny(file: str, index=0) -> Hub:
    try:
        pass
    finally:
        compress = BunnyCompress()
        decompressed = compress.decompress(file)
        df = pandas.read_feather(decompressed)
        hub = df.iloc[[index]]
        h = list(hub['data'])[0]
        p=compile(h, '_', 'eval')
        data=eval(p, {"Data": Data})
        hub = Hub()
        hub.data = data
        return hub