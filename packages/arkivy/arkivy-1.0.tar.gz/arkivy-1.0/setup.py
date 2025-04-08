from setuptools import setup,find_packages

d='''

install library

``pip instal arkivy``


'''






setup(
	version='1.0',
	name='arkivy',
	author='ALI KAZM',
	description='Help library with kivy in Arabic language formatting',
	packages=find_packages(),
	long_description=d,
	install_requires=['arabic_reshaper','python_bidi','kivy'],
	

)



