from setuptools import setup

setup(name='gym_minichess',
      version='0.0.1',
      install_requires=[
            'gym',
            'minichess @ git+https://github.com/mdhiebert/minichess#egg=minichess'
            ]
)