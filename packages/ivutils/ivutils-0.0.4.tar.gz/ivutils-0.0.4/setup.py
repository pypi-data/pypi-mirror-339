from setuptools import setup, find_packages

with open("README.md") as fp:
    desc_text = fp.read()

setup(
    name="ivutils",
    version="0.0.4",
    license="MIT license",
    long_description=desc_text,
    long_description_content_type= "text/markdown",
    packages=find_packages(),
    install_requires=[
        "opencv-python~=4.10.0.84",
        "numpy~=2.1.3",
        "pillow~=11.0.0"
    ],
    entry_points={
        'console_scripts': [
            'ivutils = ivutils.cli:run',
        ],
    },
)
