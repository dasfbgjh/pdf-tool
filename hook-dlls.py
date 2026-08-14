import os
import sys
from PyInstaller.utils.hooks import collect_dynamic_libs

hiddenimports = [
    'pyexpat',
    '_elementtree',
    'xml.parsers.expat',
    'xml.etree.ElementTree',
    'xml.dom',
    'xml.sax',
]

binaries = []

python_dlls_dir = os.path.join(sys.base_prefix, 'DLLs')
if os.path.exists(python_dlls_dir):
    dll_files = [
        'pyexpat.pyd',
        '_elementtree.pyd',
        '_lzma.pyd',
        '_bz2.pyd',
        '_ctypes.pyd',
    ]
    
    for dll_file in dll_files:
        dll_path = os.path.join(python_dlls_dir, dll_file)
        if os.path.exists(dll_path):
            binaries.append((dll_path, 'DLLs'))

conda_dlls_dir = os.path.join(sys.base_prefix, 'Library', 'bin')
if os.path.exists(conda_dlls_dir):
    conda_dlls = [
        'libexpat.dll',
        'liblzma.dll',
        'libbz2.dll',
        'libffi.dll',
    ]
    
    for dll in conda_dlls:
        dll_path = os.path.join(conda_dlls_dir, dll)
        if os.path.exists(dll_path):
            binaries.append((dll_path, '.'))