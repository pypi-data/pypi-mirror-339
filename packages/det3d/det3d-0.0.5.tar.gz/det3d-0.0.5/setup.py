from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import os

def make_cuda_ext(name, module, sources):
    cuda_ext = CUDAExtension(
        name='%s.%s' % (module, name),
        sources=[os.path.join(*module.split('.'), src) for src in sources]
    )
    return cuda_ext

with open("readme.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "torch==1.8.0",
    'numpy==1.19.2',
] 

setup(
    name="det3d",
    version="0.0.5",
    author="Tao Xiang",
    author_email="xiang.tao@outlook.de",
    description="A package of 3D object detection models",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/leoxiang66/3D-Detection",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "det3d.ops.iou3d_nms": ["src/*.cpp", "src/*.cu", "src/*.h"],
    },
    install_requires=requirements,
    cmdclass={
        'build_ext': BuildExtension,  # 用于编译 CUDA 扩展
    },
    ext_modules=[
        make_cuda_ext(
            name='iou3d_nms_cuda',
            module='det3d.ops.iou3d_nms',
            sources=[
                'src/iou3d_cpu.cpp',
                'src/iou3d_nms_api.cpp',
                'src/iou3d_nms.cpp',
                'src/iou3d_nms_kernel.cu',
            ],
        ),
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)