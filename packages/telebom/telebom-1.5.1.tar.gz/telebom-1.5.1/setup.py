from setuptools import setup, find_packages
import os

long_description = ''
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='telebom',
    version='1.5.1',
    description='reaction-Telegram-Post By : t.me/goldenxpris.',
    author='Golden',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'requests',
        'rich',
        'colorama',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
