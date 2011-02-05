from setuptools import setup, find_packages
import sys, os

version = '0.1.1'

setup(name='CompleteGenomicsTools',
      version=version,
      description="Tools for manipulating and visualizing data from Complete Genomics",
      long_description="""\
""",
      classifiers=["Operating System :: OS Independent",
                   "Topic :: Scientific/Engineering :: Bio-Informatics"], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='genomics biology bioinformatics sequencing',
      author='Sean Davis',
      author_email='seandavi@gmail.com',
      url='https://github.com/seandavi/CompleteGenomicsTools',
      license='GPL-2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      scripts=['scripts/cgent'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
