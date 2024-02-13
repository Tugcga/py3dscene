import sys
import os
from urllib import request

p_prime: int = sys.version_info[0]
p_second: int = sys.version_info[1]

def try_download(bin_name: str) -> None:
    if not os.path.exists("py3dscene\\bin\\" + bin_name):
        url = "https://github.com/Tugcga/py3dscene/releases/download/1.0/" + bin_name
        print(f"The binary {bin_name} is missing, try to download from {url}")
        request.urlretrieve(url, "py3dscene\\bin\\" + bin_name)

if p_prime == 3 and p_second == 12:
    try_download("tiny_gltf_py312.pyd")
    import py3dscene.bin.tiny_gltf_py312 as tiny_gltf  # type: ignore
elif p_prime == 3 and p_second == 11:
    try_download("tiny_gltf_py311.pyd")
    import py3dscene.bin.tiny_gltf_py311 as tiny_gltf  # type: ignore
elif p_prime == 3 and p_second == 10:
    try_download("tiny_gltf_py310.pyd")
    import py3dscene.bin.tiny_gltf_py310 as tiny_gltf  # type: ignore
elif p_prime == 3 and p_second == 9:
    try_download("tiny_gltf_py39.pyd")
    import py3dscene.bin.tiny_gltf_py39 as tiny_gltf  # type: ignore
elif p_prime == 3 and p_second == 8:
    try_download("tiny_gltf_py38.pyd")
    import py3dscene.bin.tiny_gltf_py38 as tiny_gltf  # type: ignore
elif p_prime == 3 and p_second == 7:
    try_download("tiny_gltf_py37.pyd")
    import py3dscene.bin.tiny_gltf_py37 as tiny_gltf  # type: ignore
elif p_prime == 3 and p_second == 6:
    try_download("tiny_gltf_py36.pyd")
    import py3dscene.bin.tiny_gltf_py36 as tiny_gltf  # type: ignore
else:
    raise ValueError(f"Python version {p_prime}.{p_second} is not supported")
