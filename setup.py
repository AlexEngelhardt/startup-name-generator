# https://packaging.python.org/tutorials/packaging-projects/

# Run `python3 setup.py --help-commands`

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='sng',
      version=__import__('sng').__version__,
      description='Generate name proposals for companies, software, etc.',
      long_description=readme(),
      classifiers=[
          # https://pypi.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Text Processing :: Linguistic',
          'Topic :: Utilities'
      ],
      url='http://github.com/AlexEngelhardt/startup-name-generator',
      author='Alexander Engelhardt',
      author_email='alexander.w.engelhardt@gmail.com',
      license='MIT',
      packages=['sng'],
      include_package_data=True,
      install_requires=[
          'pyyaml',
          'keras',
          'tensorflow',
          'numpy'
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      zip_safe=False)
