from setuptools import setup

setup(name='Ansify',
	entry_points={
		'console_scripts' :[
			'Ansify = Ansify.__main__:main']
	}
	)