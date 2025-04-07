import setuptools, re
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

with open('anigamerpy/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(
    name='anigamerpy',
    version=version,
    author='Sakuya0502',
    description='動畫瘋爬蟲工具',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/Sakuya0502/anigamerpy',
    packages=find_packages(),
    classifiers=[
        'Natural Language :: Chinese (Traditional)',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    license='MIT',
    requires=[
        'requests',
        'bs4'
    ]
)