import os
import sys

from setuptools                 import setup, find_packages
from setuptools.command.test    import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        result = pytest.main(self.test_args)
        sys.exit(result)

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid'
    , 'babel'
    , 'pystache'
]

setup(
    name='pyramid_mustache'
    , version='0.3.1'
    , description='pyramid_mustache'
    , long_description=README + '\n\n' +  CHANGES
    , classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ] 
    , author='John Anderson'
    , author_email='sontek@gmail.com'
    , url='http://github.com/eventray/pyramid_mustache'
    , keywords='web pyramid pylons'
    , packages=find_packages()
    , include_package_data=True
    , zip_safe=False
    , install_requires=requires
    , tests_require=requires + ['pytest', 'mock', 'webtest']
    , test_suite='pyramid_mustache'
    , cmdclass = {'test': PyTest}
    , entry_points="""\
      [paste.app_factory]
      main = pyramid_mustache:main
      """
)

