from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='github-skyline',
    version='0.0.1',
    author='doctorixx',
    author_email='genius@doctorixx.com',
    description='Package for generate 3d contribution map on github',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/doctorixx/github-skyline',
    packages=find_packages(),
    keywords='github generator skyline github-skyline',
    install_requires=[
        'numpy-stl',
        'requests',
        'colorama',
        'art',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
