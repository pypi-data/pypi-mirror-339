import setuptools
# with open('README.md') as f:
#     readme = f.read()

setuptools.setup(
    name="LMK05318",
    version="0.1.1",
    author="Oleksandr Shevchenko",
    author_email="shevchenko.adb@gmail.com",
    description="A pure Python 3 library for LMK05318 device.",
    #readme="README.md",
    # long_description="""Linux pure Python library for LMK05318 Ultra-Low Jitter Network Synchronizer Clock With Two Frequency Domains.""",
    long_description=open("README.md", 'r').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/oshevchenko/LMK05318.git",
    packages=setuptools.find_packages(where="src"),  # Look for packages inside "src"
    package_dir={"": "src"},  # Map packages to "src"
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: System :: Hardware',
        'Topic :: System :: Hardware :: Hardware Drivers'
    ],
    # entry_points = {
    #     'console_scripts': [
    #         'lmk05318c=lmk05318.console:main',
    #     ],
    # },
    python_requires='~=3.7',
    license='MIT',
    keywords='LMK05318 pll embedded linux',
)
