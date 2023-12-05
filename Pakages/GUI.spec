# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['MainGUI.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['googleapiclient.discovery', 'google_auth_oauthlib.flow', 'google.auth.transport.requests', 'pickle', 'os', 'base64', 'Google_API_Credential', 'GmailAPI', 'Note_Retiver', 'json', 'unidecode', 'errno'],
    hookspath=['=.'],
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
    [],
    exclude_binaries=True,
    name='MainGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['LogoApp\\LogoAppimage.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MainGUI',
)
