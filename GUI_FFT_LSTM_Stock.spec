# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['APP/GUI_FFT_LSTM_Stock.py'],
    pathex=['Pakages/DataSetgenPacks/Retriver_and_Processor_Dataset.py', 'Pakages/ForcastingPacks/Forcaster_Model_DateFromToForcast.py', 'Pakages/ForcastingPacks/Trainer_Predicting_Esamble.py'],
    binaries=[],
    datas=[('APP/DataSets', 'DataSets'), ('APP/DataStructures', 'DataStructures'), ('APP/ModelForcast', 'ModelForcast'), ('APP/Models', 'Models')],
    hiddenimports=['matplotlib.pyplot', 'os.path', 'os', 'PyQt5', 'sqlite3', 'cmath', 'sys', 'pandas', 'numpy', 'Model_Forcast', 'Model_Trainner', 'Model_Creator', 'DataSet_Creator', 'PyQt5.QtCore', 'tensorflow.keras.layers', 'tensorflow.keras.optimizers', 'tensorflow.keras.models', 'tensorflow.keras.layers', 'tensorflow', 'tensorflow.python.keras.layers.core', 'datetime', 'time', 'Retriver_and_Processor_Dataset', 'matplotlib', 'cProfile', 'seaborn', 'sklearn.preprocessing', 'sklearn.metrics', 'math', 'mplfinance', 'unittest', 'yfinance', 'sklearn.preprocessing', 'yfinance'],
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
    [],
    exclude_binaries=True,
    name='GUI_FFT_LSTM_Stock',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logoApp.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GUI_FFT_LSTM_Stock',
)
