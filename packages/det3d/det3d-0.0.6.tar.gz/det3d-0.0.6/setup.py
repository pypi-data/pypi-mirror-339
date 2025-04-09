import os
from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

# 获取当前目录路径
here = os.path.abspath(os.path.dirname(__file__))

# 读取 readme.md
try:
    with open(os.path.join(here, "readme.md"), "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Det3D: 3D Object Detection Library"

def make_cuda_ext(name, module, sources):
    return CUDAExtension(
        name=f"{module}.{name}",
        sources=[os.path.join(*module.split("."), "src", src) for src in sources],
    )

setup(
    name="det3d",
    version="0.0.6",
    author="Tao Xiang",
    author_email="xiang.tao@outlook.de",
    description="A package of 3D object detection models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leoxiang66/3D-Detection",
    packages=find_packages(),
    include_package_data=True,  # 确保 MANIFEST.in 文件生效
    package_data={
        "det3d.ops.iou3d_nms": ["src/*.cpp", "src/*.cu", "src/*.h"],
    },
    install_requires=[
        "torch>=1.8.0",
        "numpy>=1.19.2",
    ],
    cmdclass={
        "build_ext": BuildExtension,
    },
    ext_modules=[
        make_cuda_ext(
            name="iou3d_nms_cuda",
            module="det3d.ops.iou3d_nms",
            sources=[
                "iou3d_cpu.cpp",
                "iou3d_nms_api.cpp",
                "iou3d_nms.cpp",
                "iou3d_nms_kernel.cu",
            ],
        ),
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)