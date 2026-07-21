from pathlib import Path
import math

base=Path('')
candidates=sorted(base.glob("field*.txt"))
if not candidates:
    raise FileNotFoundError(f"No field*.txt found in {base}")
src=candidates[0]
target=src.with_name(src.stem+"_under20MB.txt")
max_bytes=20*1024*1024-50000
size=src.stat().st_size

with src.open("r",encoding="utf-8",errors="ignore") as f:
    header=f.readline()
    data=f.readlines()

if size<=max_bytes:
    with target.open("w",encoding="utf-8") as out:
        out.write(header)
        out.writelines(data)
else:
    ratio=max_bytes/size
    keep=max(1,int(len(data)*ratio))
    step=max(1,math.ceil(len(data)/keep))
    with target.open("w",encoding="utf-8") as out:
        out.write(header)
        out.writelines(data[::step])

print("Source:",src)
print("Original MB:",round(size/1024/1024,2))
print("New MB:",round(target.stat().st_size/1024/1024,2))
print("Output:",target)
