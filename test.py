import sys,os
from steamworks import STEAMWORKS # Import main STEAMWORKS class
if sys.version_info >= (3, 8):
  os.add_dll_directory(os.getcwd()) # Required since Python 3.8
# 初始化steamwork类
steamworks = STEAMWORKS()
steamworks.initialize() 