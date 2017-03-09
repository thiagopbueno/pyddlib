import pydd

from setuptools import setup
import os

def read(filename):
	return open(os.path.join(os.path.dirname(__file__), filename), 'r').read()

setup(
	name = 'pydd',
	version = pydd.__version__,
	author = 'Thiago P. Bueno',
	author_email = 'thiago.pbueno@gmail.com',
	description = 'pydd is a Python3 library for manipulating decision diagrams (DD).',
	long_description = read('README.rst'),
	license = 'GNU General Public License v3.0',
	keywords = ['decision diagrams', 'BDD', 'ADD', 'symbolic', 'boolean', 'data structure'],
	url = 'https://github.com/thiagopbueno/pydd',
	packages = ['pydd', 'tests'],
	zip_safe = False,
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Artificial Intelligence',
		'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],
)
