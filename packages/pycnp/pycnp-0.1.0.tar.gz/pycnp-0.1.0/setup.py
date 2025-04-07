from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os
import subprocess

# 定义pybind11扩展
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        try:
            subprocess.check_call(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake必须安装才能构建扩展")
            
        for ext in self.extensions:
            self.build_extension(ext)
            
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]
        
        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]
        
        cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
        
        # 确保build_temp目录存在
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
            
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

# 读取README文件作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pycnp",
    version="0.1.0",
    description="Python绑定的CNP求解器包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Bo Xue",
    author_email="xuebo100@outlook.com",
    url="https://github.com/xuebo100/PyCNP",
    packages=["pycnp", "pycnp.stop"],
    ext_modules=[CMakeExtension('PyCNP')],
    cmdclass=dict(build_ext=CMakeBuild),
    install_requires=[
        "numpy>=1.19.0",
        "pybind11>=2.6.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    keywords="critical node problem, graph theory, optimization",
    project_urls={
        "Bug Reports": "https://github.com/xuebo100/PyCNP/issues",
        "Source": "https://github.com/xuebo100/PyCNP",
    },
) 