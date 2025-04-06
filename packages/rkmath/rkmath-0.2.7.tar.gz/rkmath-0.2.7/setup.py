from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='rkmath',
    packages=find_packages(include=['rkmath']),
    version='0.2.7',
    description='Math library for easy math operations',
     long_description=long_description,
    long_description_content_type="text/markdown",
    author='Swifterhtmler',
    install_requires=["numpy>=1.21.0"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)

