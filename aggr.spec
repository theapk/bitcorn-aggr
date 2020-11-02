# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['aggr.py'],
             pathex=['T:\\Crypto\\probit-bot\\bitcorn-aggr'],
             binaries=[],
             datas=[('T:/Crypto/probit-bot/venv/Lib/site-packages/pyfiglet', './pyfiglet'), ('T:/Crypto/probit-bot/bitcorn-aggr/high.mp3', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='aggr',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='rocket_corn.ico')
