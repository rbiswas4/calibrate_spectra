#from ez_setup import use_setuptools
#use_setuptools()
from distutils.core import setup

setup(# package information
      name="transientSources",
      version="0.0.1dev",
      description='',
      long_description=''' ''',
      # What code to include as packages
      packages=['transientSources'],
      packagedir={'transientSources':'transientSources'},
      # What data to include as packages
      include_package_data=True,
      package_data={'transientSources':['example_data/2007uy/cfa_2007uy/*', 
                                        'example_data/2007uy/B/*',
                                        'example_data/2007uy/V/*',
                                        'example_data/2007uy/i/*',
                                        'example_data/2007uy/r/*',
                                        'example_data/filters/*']
                   }
      )
