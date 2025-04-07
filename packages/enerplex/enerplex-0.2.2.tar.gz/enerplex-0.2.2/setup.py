import setuptools
from enerplex import __version__ as version

setuptools.setup(
    name='enerplex',
    version=version,
    description='Enerplex API Client',
    long_description=open('README.md').read().strip(),
    long_description_content_type='text/markdown',  # Ensures markdown is rendered correctly on PyPI
    author='Noel Schwabenland',
    author_email='noel@lusi.uni-sb.de',
    url='https://github.com/NoxelS/enerplex-api-client',
    py_modules=[],
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.25.0'
    ],
    license='MIT License',
    zip_safe=True,
    keywords='energen enerplex',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering',
    ],
    python_requires='>=3.9',
)
