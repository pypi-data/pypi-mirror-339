from setuptools import setup, find_packages

setup(
    name='branchconflicts',
    packages=find_packages(),
    version='0.1.3',
    description='Find conflicted files between two branches.',
    author='39matt',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.3.5'],
    test_suite='tests',
)