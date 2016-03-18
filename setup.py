from distutils.core import setup

setup(
	name='Segmentor',
	description="NAER Segmentor",
	version='1.0',
	author='J.C. Wu, M.H. Bai',
	url='https://github.com/naernlp/Segmentor',
	packages={'Segmentor'},
	package_dir={'Segmentor':'Segmentor'},
	package_data={'Segmentor':['Data/*']},
	scripts=['scripts/naer_seg']
)
