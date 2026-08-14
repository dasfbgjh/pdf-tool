# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = [
    'pyexpat',
    '_elementtree',
    'xml.parsers.expat',
    'xml.etree.ElementTree',
    'xml.dom',
    'xml.sax',
    'xml',
    'xml.parsers',
    'xml.etree',
    'Crypto',
    'Crypto.Cipher',
    'Crypto.Cipher.AES',
    'Crypto.Protocol.KDF',
    'Crypto.Hash',
    'Crypto.Hash.SHA256',
    'Crypto.Random',
    'Crypto.Util.Padding',
]

tmp_ret = collect_all('pyexpat')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

tmp_ret = collect_all('xml')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

tmp_ret = collect_all('Crypto')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

python_dlls_dir = os.path.join(sys.base_prefix, 'DLLs')
if os.path.exists(python_dlls_dir):
    dll_files = [
        'pyexpat.pyd',
        '_elementtree.pyd',
        '_ctypes.pyd',
        '_hashlib.pyd',
        '_ssl.pyd',
    ]
    
    for dll_file in dll_files:
        dll_path = os.path.join(python_dlls_dir, dll_file)
        if os.path.exists(dll_path):
            binaries.append((dll_path, 'DLLs'))

conda_dlls_dir = os.path.join(sys.base_prefix, 'Library', 'bin')
if os.path.exists(conda_dlls_dir):
    conda_dlls = [
        'libexpat.dll',
        'libffi.dll',
        'libcrypto.dll',
        'libssl.dll',
        'zlib.dll',
        'ffi.dll',
    ]
    
    for dll in conda_dlls:
        dll_path = os.path.join(conda_dlls_dir, dll)
        if os.path.exists(dll_path):
            binaries.append((dll_path, '.'))

a = Analysis(
    ['pdf.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['bz2', 'lzma', 'sqlite3', '_bz2', '_lzma', '_sqlite3'],
    noarchive=True,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pdf_tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)