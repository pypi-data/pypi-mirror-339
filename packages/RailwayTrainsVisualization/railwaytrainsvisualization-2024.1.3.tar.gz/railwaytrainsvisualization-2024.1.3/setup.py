import setuptools
import re

package_name = "RailwayTrainsVisualization"

VERSION = "2024.1.3"  # 更新为2024.1.3

def main():
    """Setup package"""
    long_description = """# RailwayTrainsVisualization
为研究人员与工程技术人员提供的可扩展、可交互的铁路可视化工具
"""
    
    required = [
        "numpy>=1.20.0",
        "pandas>=1.0.0",
        "matplotlib>=3.3.0",
        "plotly>=5.0.0"
    ]

    setuptools.setup(
        name=package_name,
        version=VERSION,
        author="ZeyuShen",  # 作者名称
        author_email="sc22zs2@leeds.ac.uk", # 作者邮箱
        description="为研究人员与工程技术人员提供的可扩展、可交互的铁路可视化工具", # 库描述
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/yourusername/RailwayTrainsVisualization", # 库的官方地址
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=required,
    )

if __name__ == '__main__':
    main()
