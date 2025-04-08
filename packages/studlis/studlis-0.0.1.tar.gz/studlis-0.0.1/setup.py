from setuptools import setup,find_packages

setup(name='studlis',
      version='0.0.1',
      description='',
      author='Niklas Rodemund',
      author_email='',
      include_package_data=True, 
      url='https://www.python.org/sigs/distutils-sig/',
      packages=find_packages(),
      install_requires=[
        'fastapi',
        'uvicorn',
        'mako',
        "aiosqlite",
        "aiohttp"
      ]
     )
