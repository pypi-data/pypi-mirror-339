from setuptools import setup, find_packages

setup(
    name='cocoa-plant-detector',
    version='0.1.1',
    description='YOLOv8 Cocoa Plant Detection + GIS AI Pipeline with CLI',
    author='Michael Ofeor',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'opencv-python',
        'ultralytics',
        'geopandas',
        'shapely',
        'pyproj',
        'tqdm',
        'streamlit',
    ],
    entry_points={
        'console_scripts': [
            'cocoa-detect=cocoa_detector.cocoa_cli_pipeline.main:cli',
        ],
    },
)
