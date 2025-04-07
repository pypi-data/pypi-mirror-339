from setuptools import setup, find_packages

setup(
    name='nordvpn-switch',
    version='0.1.0',
    author='mrnasil',
    author_email='mail@farukarigun.com',
    description='A Python package to switch NordVPN servers easily.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/NordVPN-switcher',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
)