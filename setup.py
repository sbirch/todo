from setuptools import setup

setup(name='todo',
      version='0.1',
      description='Print TODOs in a codebase',
      url='https://github.com/sbirch/todo',
      author='Sam Birch',
      author_email='sam.m.birch@gmail.com',
      license='MIT',
      packages=['todo'],
      zip_safe=False,
      scripts=['bin/todo'])