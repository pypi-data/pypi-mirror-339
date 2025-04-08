import os
import sys
import subprocess
import shutil
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
from os.path import expanduser
home = expanduser("~")
__version__ = "0.0.38"
BASE_DIR = Path(__file__).parent.resolve()
# print(BASE_DIR)
# 自动安装 pybind11
try:
    from pybind11.setup_helpers import Pybind11Extension, ParallelCompile, naive_recompile
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pybind11>=2.6.0"])
    from pybind11.setup_helpers import Pybind11Extension, ParallelCompile, naive_recompile

# Read long description from README
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Fourier dexhand general SDK"

# class CustomInstall(install):
#     def run(self):
#         # 标准安装流程
#         super().run()
        
#         # 用户本地目录路径
#         local_lib = Path.home() / ".local/lib"
#         local_include = Path.home() / ".local/include/fdexhand"
        
#         # 确保目录存在
#         local_lib.mkdir(parents=True, exist_ok=True)
#         local_include.mkdir(parents=True, exist_ok=True)
        
#         # 复制库文件
#         lib_src = BASE_DIR / "./_ext/libFourierDexHand.so"
#         if lib_src.exists():
#             shutil.copy2(lib_src, str(local_lib))
#             print(f"Installed library to {local_lib}")
        
#         # 复制头文件
#         include_src = BASE_DIR / "./fdexhand/include"
#         if include_src.exists():
#             shutil.copytree(
#                 include_src,
#                 str(local_include),
#                 dirs_exist_ok=True
#             )
#             print(f"Installed headers to {local_include}")

class CustomInstall(install):
    def run(self):
        # 标准安装流程
        super().run()
        
        # 用户本地目录路径
        local_lib = Path.home() / ".local/lib"
        local_include = Path.home() / ".local/include/fdexhand"
        
        # 确保目录存在
        local_lib.mkdir(parents=True, exist_ok=True)
        local_include.mkdir(parents=True, exist_ok=True)
        print(f"Installed library to {local_lib}")
        print(f"Installed headers to {local_include}")
        
        # 处理库文件
        lib_src = BASE_DIR / "_ext/libFourierDexHand.so"
        lib_dest = local_lib / "libFourierDexHand.so"
        
        if lib_src.exists():
            # 检查目标是否存在（无论是文件还是链接）
            if lib_dest.exists() or lib_dest.is_symlink():
                print(f"Removing existing file/link: {lib_dest}")
                lib_dest.unlink()  # 删除文件或链接
                
            shutil.copy2(lib_src, lib_dest)
            print(f"Installed library to {lib_dest}")
        else:
            print(f"Warning: Source library not found at {lib_src}")
        
        # 处理头文件目录
        include_src = BASE_DIR / "fdexhand/include"
        if include_src.exists():
            # 删除已存在的目标目录
            if local_include.exists():
                print(f"Removing existing directory: {local_include}")
                shutil.rmtree(local_include)
                
            shutil.copytree(
                include_src,
                local_include,
                dirs_exist_ok=False  # 我们已经确保目录不存在
            )
            print(f"Installed headers to {local_include}")
        else:
            print(f"Warning: Header directory not found at {include_src}")

# class CustomInstall(install):
#     def run(self):
#         # 标准安装流程
#         super().run()
        
#         # 用户本地目录路径
#         local_lib = Path.home() / ".local/lib"
#         local_include = Path.home() / ".local/include/fdexhand"
        
#         try:
#             # 确保库目录存在（递归创建）
#             local_lib.mkdir(parents=True, exist_ok=True)
            
#             # 处理库文件
#             lib_src = BASE_DIR / "_ext/libFourierDexHand.so"
#             lib_dest = local_lib / "libFourierDexHand.so"
            
#             if lib_src.exists():
#                 # 检查并清理目标文件/链接
#                 if lib_dest.exists() or lib_dest.is_symlink():
#                     print(f"Removing existing file/link: {lib_dest}")
#                     lib_dest.unlink(missing_ok=True)  # Python 3.8+ 支持
                
#                 # 复制库文件
#                 shutil.copy2(lib_src, lib_dest)
#                 print(f"Installed library to {lib_dest}")
#             else:
#                 print(f"Warning: Source library not found at {lib_src}")

#             # 确保头文件目录存在（先清理再创建）
#             if local_include.exists():
#                 print(f"Removing existing directory: {local_include}")
#                 shutil.rmtree(local_include, ignore_errors=True)
            
#             local_include.mkdir(parents=True, exist_ok=True)
            
#             # 处理头文件
#             include_src = BASE_DIR / "fdexhand/include"
#             if include_src.exists():
#                 shutil.copytree(
#                     include_src,
#                     local_include,
#                     dirs_exist_ok=False  # 已确保目录不存在
#                 )
#                 print(f"Installed headers to {local_include}")
#             else:
#                 print(f"Warning: Header directory not found at {include_src}")

#         except Exception as e:
#             print(f"Error during installation: {str(e)}")
#             raise  # 重新抛出异常，让安装过程失败

# 启用并行编译
ParallelCompile("NPY_NUM_BUILD_JOBS", needs_recompile=naive_recompile, default=4).install()

# 构建扩展模块
ext_modules = []
source_files = list(map(str, Path(".").glob("*.cpp")))

ext_modules = [
    Pybind11Extension(
        "dexhandpy.fdexhand",
        sources=source_files,
        include_dirs=[
            BASE_DIR / "./fdexhand/include",
            str(Path.home() / ".local/include/fdexhand")  # 包含用户本地头文件
        ],
        library_dirs=[
            str(BASE_DIR / "./_ext"),
            str(Path.home() / ".local/lib")  # 包含用户本地库
        ],
        runtime_library_dirs=[
            str(BASE_DIR / "_ext"), 
            str(Path.home() / ".local/lib")
        ],  # 运行时搜索路径
        libraries=["FourierDexHand"],
        cxx_std=14,
        extra_compile_args=["-fPIC"],
        extra_link_args=["-Wl,-rpath,$ORIGIN/../_ext"]  # 显式设置rpath
    )
]


setup(
    name='dexhandpy',
    version=__version__,
    author="Afer Liu",
    author_email="fei.liu@fftai.com",
    description="Fourier dexhand general SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/dexhandpy",
    
    # 包配置
    packages=find_packages(include=["dexhandpy*"]),
    package_data={
        "dexhandpy": ["_ext/libFourierDexHand.so"],
    },
    # data_files=[
    #     ('/usr/local/lib', ['_ext/libFourierDexHand.so']),
    #     ('/usr/local/include/fdexhand', ['fdexhand/include/dexhand.h']),
    #     ('/usr/local/include/fdexhand/hand', ['fdexhand/include/hand/fhand.h']),
    #     ('/usr/local/include/fdexhand/hand/commsockets', ['fdexhand/include/hand/commsockets/commsockets.h']),
    # ],
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
    python_requires='>=3.8',
    
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