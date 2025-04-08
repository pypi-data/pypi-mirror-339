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
    def __init__(self, compression_level=2):
        self.compression_level = compression_level

    def compress(self, buffer: io.BytesIO, file, chunk_size=1024):
        try:pass
        finally:
            bytestream = io.BytesIO()

            
            with gzip.GzipFile(fileobj=bytestream, mode='wb', compresslevel=self.compression_level) as f_out:
                    while True:
                        chunk = buffer.read(chunk_size)
                        if not chunk:
                            break
                        f_out.write(chunk)

            bytestream.seek(0)

        with open(file, 'wb') as f_out:
            shutil.copyfileobj(bytestream, f_out)
    def decompress(self, file, chunk_size=1024):
        try:pass
        finally:
            bytestream = io.BytesIO()

            with open(file, 'rb') as f_in:
                bytestream.write(f_in.read())

            bytestream.seek(0)

            decompressed_stream = io.BytesIO()
            try:
                with gzip.GzipFile(fileobj=bytestream, mode='rb', compresslevel=self.compression_level) as f_in:
                    while True:
                        chunk = f_in.read(chunk_size)
                        if not chunk:
                            break
                        decompressed_stream.write(chunk)
            except gzip.BadGzipFile as e:
                print(e)
            decompressed_stream.seek(0)
            return decompressed_stream



class BunnyFile:
    def __init__(self, filepath: str, init=False):
        self.file = filepath
        buffer = io.BytesIO()
        self.compress = BunnyCompress()
        self.init = init
        if init:
            try:
                pass
            finally:
                self.df = pandas.DataFrame({
                    'data': [],
                    'data_len': [],
                    'timestamp': [],
                })
                self.df.to_feather(buffer)
                buffer.seek(0)
                self.compress.compress(buffer, self.file)
            
            
    def commit_hub(self, hub: Hub):
        try:
            pass
        finally:
            df = pandas.DataFrame({
                    'data': [str(hub.data)],
                    'data_len': [len(hub.filter())],
                    'timestamp': [datetime.utcnow()]
                })
            if self.init:
                self.df = df
            else:
                self.df:pandas.DataFrame = pandas.read_feather(decompressed)
                decompressed = self.compress.decompress(self.file)
                self.df = pandas.concat([df, self.df])
                self.init = False
    def write(self):
        try:
            pass
        finally:
            buffer = io.BytesIO()
            self.df.to_feather(buffer)
            buffer.seek(0)
            self.compress.compress(buffer, self.file)
        

def save_as_bunny(file: str, hub: Hub, clear=False):
    try:
        pass
    finally:
        init = (os.path.exists(file) == False) or clear
        
        bf = BunnyFile(file, init)
        bf.commit_hub(hub)
        bf.write()
def clear_bunny(file: str):
    try:
        pass
    finally:
        hub = read_bunny(file)
        compress = BunnyCompress()
        buffer = io.BytesIO()
        df = pandas.DataFrame({
                    'data': [str(hub.data)],
                    'data_len': [len(hub.filter())],
                    'timestamp': [datetime.utcnow()],
                })
        
        df.to_feather(buffer)
        buffer.seek(0)
        compress.compress(buffer, file)
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
        if not os.path.exists(file):
            hub = Hub()
            save_as_bunny(file, hub)
        else:
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