from setuptools import setup, find_packages

setup(
   name='ncc_meu_investimento',
   version='0.1',
   packages=find_packages(),
   install_requires=[],
   author='Robson Nicácio',
   author_email='robson.nicacio@gmail.com',
   description='Uma biblioteca para cálculos de investimentos.',
   url='https://github.com/tadrianonet/meu_investimento',
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   python_requires='>=3.6',
)
