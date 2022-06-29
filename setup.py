
from setuptools import setup

with open("README.rst", "r") as fh:
	long_description = fh.read()

setup(
	name = 'tspop',
	version = '0.0.1',
	description = 'Extracts population-based ancestry from simulated tree sequence datasets.',
	py_modules = ["tspop"],
	package_dir = {'' : 'src'},
	classifiers = [
		"Programming Language :: Python :: 3",
		"Topic :: Scientific/Engineering :: Bioinformatics",
		"Development Status :: Planning",
		"License :: OSI Approved :: MIT License",
		"Intended Audience :: Science/Research",
		"Natural Language :: English"
	],
	long_description = long_description,
	long_description_content_type = "text/x-rst",
	install_requires = [
		"tskit>=0.2.3"
	],
	extras_require = {
		"dev" : ["pytest>=3.7",
				"msprime==1.1.1"
				]
	}
	)