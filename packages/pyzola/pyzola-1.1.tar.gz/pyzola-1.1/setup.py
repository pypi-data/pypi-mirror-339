from setuptools import setup,find_packages

d='''

install library

``pip instal pyzola``

usage

``Python

import pyzola

data=pyzola.dumps('Hello, World')

print(data)


original_data=pyzola.loads(data)

print(original_data)

``

``Python

import pyzola

code="""
for i in range(10):
	print(i)
	

"""

encrption_code=pyzola.dump_code(code)

print(encrption_code)


pyzola.run_code(encrption_code)

``


'''






setup(
	version='1.1',
	name='pyzola',
	author='ALI KAZM',
	description='Good library to start with code encryption',
	long_description_content_type='text/markdown',
	packages=find_packages(),
	long_description=d,
	

)




