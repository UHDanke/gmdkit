from gmdkit import Level
import time

_start = time.perf_counter()
lvl = Level.from_file("data/gmd/online/ORBIT.gmd",load_content=False)
_end = time.perf_counter()
print(f"File load took {_end - _start:.6f} seconds")
_start = time.perf_counter()
lvl.load()
_end = time.perf_counter()
print(f"Load took {_end - _start:.6f} seconds")
_start = time.perf_counter()
lvl.to_string()
_end = time.perf_counter()
print(f"Save took {_end - _start:.6f} seconds")
