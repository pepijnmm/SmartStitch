# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['SmartStitchGUI.py'],
             pathex=['.'],
             binaries=[],
             datas = [],
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
          [],
          exclude_binaries=True,
          name='SmartStitchGUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='SmartStitchLogo.ico')
coll = COLLECT(exe,
               a.binaries + [('SmartStitchLogo.png', 'SmartStitchLogo.png', 'DATA'), ('SmartStitchLogo.ico', 'SmartStitchLogo.ico', 'DATA')],
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='SmartStitchGUI')
