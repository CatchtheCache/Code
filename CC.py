import glob
import urllib.parse
import os
import brotli
import gzip
import zlib
import simplecache

#C:\Users\kkimk\AppData\Local\Google\Chrome\User Data\Default\Cache\Cache_Data
#cache_dir = os.path.expanduser('~/.cache/google-chrome/Default/Cache/*_0') 이거는 리눅스랑 안드로이드용 
cache_dir = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache\Cache_Data')
out_dir = 'cache'

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

for entry_file in glob.glob(cache_dir):
    e = simplecache.Entry(entry_file)
    url = e.get_key()
    print(url)

    filename = urllib.parse.quote(url, safe='')[:255]
    encoding = e.get_header().headers.get('content-encoding', '').strip().lower()
    out_path = os.path.join(out_dir, filename)

    if encoding:
        # decompress with python
        data = e.get_data()
        if encoding == 'gzip':
            data = gzip.decompress(data)
        elif encoding == 'br':
            data = brotli.decompress(data)
        elif encoding == 'deflate':
            data = zlib.decompress(data)

        with open(out_path, 'wb') as f:
            f.write(data)
    else:
        # faster for binary
        e.save(out_path)

        print("commit")