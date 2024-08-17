# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

def _get_abs_path(rel_path):
    return os.path.join(os.getcwd(), rel_path)

APP_NAME = "pyscript-engine"

# Local paths
VERSION_FILE = _get_abs_path("VERSION")
EXIFTOOL_EXE = _get_abs_path(r"dependency\win64\exiftool.exe")
ICON_IMG = _get_abs_path(r"src\icon\logo_high.ico")
ICON_DIR = _get_abs_path(r"src\icon")
SPLASH_IMG = _get_abs_path(r"src\images\splash.png")


# For windows build DLLs
DLL_BIN_DIR = _get_abs_path("dependency\win64\DLL")

datas = [(ICON_DIR, "icon"), (VERSION_FILE, "."), (EXIFTOOL_EXE, ".")]

binaries = []
hiddenimports = []

LIBS_TO_ADD = [
    "cv2",
    "pykml",
    "numpy",
    "shapely",
    "pandas",
    "imageio",
    "customtkinter",
    "requests",
    "boto3",
    "aioboto3",
    "azure",
    "exiftool",
    "httpx",
    "rich",
    "psycopg2",
    "geopy",
    "sqlalchemy",
    "tifffile",
    "matplotlib",
]
for lib in LIBS_TO_ADD:
    tmp_ret = collect_all(lib)
    datas += tmp_ret[0]
    binaries += tmp_ret[1]
    hiddenimports += tmp_ret[2]

# https://github.com/cgohlke/imagecodecs/issues/11
import imagecodecs

hiddenimports += ["imagecodecs." + x for x in imagecodecs._extensions()] + [
    "imagecodecs._shared"
]


# Exclude tests module
exclude_tests = [f"{lib}.tests" for lib in LIBS_TO_ADD]

with open(VERSION_FILE) as file:
    app_version = file.read()

# for pathex: https://stackoverflow.com/questions/72614529/exe-file-made-by-pyinstaller-pops-up-dll-error-tkinter-is-crashing
a = Analysis(
    ["..\src\main.py"],
    pathex=[DLL_BIN_DIR],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=exclude_tests + [],
    noarchive=False,
)
pyz = PYZ(a.pure)
splash = Splash(
    SPLASH_IMG,
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(15, 370),
    text_size=12,
    text_color="#f8f4e3",
    minify_script=True,
    always_on_top=True,
    text_default="Loading",
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    splash,
    splash.binaries,
    [],
    name=f"{APP_NAME}_v{app_version}",
    icon=ICON_IMG,
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
