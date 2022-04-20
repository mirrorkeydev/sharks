# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['ui.py'],
    pathex=[],
    binaries=[],
    datas=[('trained_model.json', '.'), ('shark.ico', '.'), ('SettingsIcon2.png', '.')],
    hiddenimports=['skimage.filters.edges', 'skimage.filters.thresholding', 'sklearn.utils._typedefs'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
