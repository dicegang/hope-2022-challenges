import zipfile
import zlib

with zipfile.ZipFile('orphan.zip') as zf:
  deet = zf.read('orphan/.git/objects/d9/27ddf1a74659171e4755a6d407c79ac381c3a5')

print(zlib.decompress(deet).split(b'\0')[1].decode())
