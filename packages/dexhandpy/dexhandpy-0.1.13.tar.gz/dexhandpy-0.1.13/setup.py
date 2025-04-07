import os
import sys
import subprocess
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install

__version__ = "0.1.13"

# 初始化路径
BASE_DIR = Path(__file__).parent.resolve()
os.chdir(BASE_DIR)

# 自动安装 pybind11
try:
    from pybind11.setup_helpers import Pybind11Extension, ParallelCompile, naive_recompile
except ImportError:
    print("Installing pybind11...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pybind11>=2.6.0"])
    from pybind11.setup_helpers import Pybind11Extension, ParallelCompile, naive_recompile

# 用户主目录安装路径
HOME = Path.home()
LOCAL_DIR = HOME / ".local"
LIB_INSTALL_DIR = str(LOCAL_DIR / "lib")
INCLUDE_INSTALL_DIR = str(LOCAL_DIR / "include" / "fdexhand")

class CustomInstall(install):
    def run(self):
        # 创建目标目录
        (LOCAL_DIR / "lib").mkdir(parents=True, exist_ok=True)
        (LOCAL_DIR / "include" / "fdexhand").mkdir(parents=True, exist_ok=True)
        
        super().run()

        # 安装头文件
        include_src = BASE_DIR / "fdexhand" / "include"
        if include_src.exists():
            from distutils.dir_util import copy_tree
            copy_tree(str(include_src), INCLUDE_INSTALL_DIR)

        # 安装库文件
        lib_src = BASE_DIR / "_ext" / "libFourierDexHand.so"
        if lib_src.exists():
            import shutil
            shutil.copy2(str(lib_src), LIB_INSTALL_DIR)

# 构建扩展模块
ext_modules = []
source_files = [str(p) for p in BASE_DIR.glob("*.cpp")]

include_dirs = [
    str(BASE_DIR / "fdexhand" / "include"),
    str(BASE_DIR / "fdexhand" / "include" / "hand"),
    str(BASE_DIR / "fdexhand" / "include" / "hand" / "commsocket"),
    str(BASE_DIR / "fdexhand" / "include" / "hand" / "fourierdexhand"),
    str(BASE_DIR / "fdexhand" / "include" / "hand" / "rapidjson"),
    INCLUDE_INSTALL_DIR  # 添加用户目录头文件路径
]

ParallelCompile("NPY_NUM_BUILD_JOBS", needs_recompile=naive_recompile, default=4).install()

ext_modules = [
    Pybind11Extension(
        "dexhandpy.fdexhand",
        sources=source_files,
        include_dirs=include_dirs,
        library_dirs=[
            str(BASE_DIR / "_ext"),
            LIB_INSTALL_DIR
        ],
        runtime_library_dirs=[LIB_INSTALL_DIR],
        libraries=["FourierDexHand"],
        cxx_std=14,
        language='c++',
        extra_compile_args=["-fPIC"]
    )
]

setup(
    name='dexhandpy',
    version=__version__,
    author="Afer Liu",
    author_email="fei.liu@fftai.com",
    description="Fourier dexhand general SDK",
    long_description=(BASE_DIR / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dexhandpy",
    
    # 包配置
    packages=find_packages(include=["dexhandpy*"]),
    package_data={
        "dexhandpy": ["_ext/libFourierDexHand.so"],
    },
    include_package_data=True,
    
    # 扩展模块
    ext_modules=ext_modules,
    
    # 自定义安装命令
    cmdclass={
        'install': CustomInstall,
    },
    
    # 依赖
    setup_requires=["pybind11>=2.6.0"],
    install_requires=["pybind11>=2.6.0"],
    python_requires='>=3.10',
    
    # PyPI 分类
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
    ],
    zip_safe=False,
)