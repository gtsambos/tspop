
from setuptools import setup

with open("README.rst", "r") as fh:
	long_description = fh.read()

version = {}
with open("src/_version.py") as fp:
    exec(fp.read(), version)
fp.close()

setup(
	name = 'tspop',
	version = version['__version__'],
	description = 'Extracts population-based ancestry from simulated tree sequence datasets.',
	url = "https://github.com/gtsambos/tspop",
	author = "Georgia Tsambos",
	author_email = "g.tsambos@gmail.com",
	py_modules = ["tspop"],
	package_dir = {'' : 'src'},
	classifiers = [
		"Programming Language :: Python :: 3",
		"Topic :: Scientific/Engineering :: Bio-Informatics",
		"Development Status :: 1 - Planning",
		"License :: OSI Approved :: MIT License",
		"Intended Audience :: Science/Research",
		"Natural Language :: English"
	],
	long_description = long_description,
	long_description_content_type = "text/x-rst",
	install_requires = [
		"tskit>=0.2.3",
		"pandas>=1.2.0",
		"numpy>=1.21.0"
	],
	extras_require = {
		"dev" : ["pytest>=3.7",
				"msprime==1.1.1"
				]
	}
	)