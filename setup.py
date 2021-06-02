from setuptools import setup, find_packages as find
import os, pathlib, sys
from src import downloader_4anime

setup(
		name='downloader_4anime',
		version=downloader_4anime.__version__,
		author=downloader_4anime.__author__,
		author_email=downloader_4anime.__email__,
		url='https://github.com/fabriciopashaj/downloader_4anime',
		description='A python library for downloading anime from the 4anime.to website',
		long_description=open(pathlib.Path('.').resolve()/'README.md').read(),
		long_description_content_type='text/markdown',
		project_urls={
			'Documentation': 'https://github.com/fabriciopashaj/downloader-4anime#readme',
			'Source Code': 'https://github.com/fabriciopashaj/downloader-4anime',
			'Bug Tracker': 'https://github.com/fabriciopashaj/downloader-4anime/issues',
		},
		license='MIT',
		license_files=['LICENSE'],
		platform=["any"],
		classifiers=[
			"Development Status :: 3 - Development/Stable",
			"Target Audience :: Anime Watchers/Weebs",
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent"
		],
		install_requires=[
			"click"
		],
		package_dir={'': 'src'},
		packages=find(where="src"),
		setup_requires=[
			"setuptools >=46.4.0"
		] if sys.version_info >= (3,) else [],
		python_requires=">=3.7"
)
