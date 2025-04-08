from setuptools import setup, find_packages

try:
    with open('readme.md', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    packages = find_packages(),
    name = 'vpnconf',
    version = '0.0.1',
    author = "Stanislav Doronin",
    author_email = "mugisbrows@gmail.com",
    url = 'https://github.com/mugiseyebrows/vpnconf.git',
    description = 'Script for creating vpn client configuration',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    entry_points = {
        'console_scripts': [
            'vpnconf = vpnconf:main'
        ]
    }
)