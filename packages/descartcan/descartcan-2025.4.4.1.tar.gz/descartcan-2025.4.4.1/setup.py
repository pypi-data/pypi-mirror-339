import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='descartcan',
    version='2025.4.4.1',
    description='A Python toolkit for advanced data processing and API interactions',
    author='DescartCan',
    author_email='louishwh@gmail.com',
    url='',
    #packages=['descartcan.connection'],
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.10',
    install_requires=[
        'aiohttp>=3.11.10',
        'aiofiles~=24.1.0',
        'loguru==0.6.0',
        'openai~=1.58.1',
        'anthropic~=0.42.0',
        'boto3~=1.34.79',
        'httpx==0.25.2',
        'tiktoken==0.8.0',
        'pyyaml~=6.0.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

