from setuptools import setup
import pymapgb

pymapgb.DownloadData()

setup(name='pymapgb',
      packages=[''],
      version='0.1',
      install_requires=["pyshp", "matplotlib", "wget"]
      )
