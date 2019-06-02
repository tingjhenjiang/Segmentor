from distutils.core import setup

setup(
	name='Segmentor (forked)',
	description="NAER Segmentor",
	version='1.0',
	author='J.C. Wu, M.H. Bai(original); T.J. Jiang(forked)',
	url='https://github.com/tingjhenjiang/Segmentor',
	packages={'Segmentor'},
	package_dir={'Segmentor':'Segmentor'},
	package_data={'Segmentor':['Data/*']},
	scripts=['scripts/naer_seg']
)
