from setuptools import setup, find_packages

setup(
    name='aanft',
    version='0.1.10',
    description='Fetching WAX AtomicAssets made easier',
    url='https://github.com/funkaclau',
    author='funkaclau',
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "asyncio",
        "loguru",
        "typing_extensions",
        "typing",
        "aiofiles"
    ],
    include_package_data=True
)
