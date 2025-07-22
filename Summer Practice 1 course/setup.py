from setuptools import setup, Extension

tetris_module = Extension(
    'TetrisAPI',
    sources=['TetrisAPI.cpp'],
    extra_compile_args=['-std=c++17'],
    language='c++'
)

setup(
    name='TetrisAPI',
    version='1.0',
    ext_modules=[tetris_module]
)