from setuptools import setup, find_packages


setup(
  name='pyfile_lib',
  version='0.0.1',
  author='the_space_prowler',
  author_email='sokolovgames42@gmail.com',
  description='This is the simplest module for quick work with files.',
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  keywords='pyfile file pyfile_lib',
  python_requires='>=3.6'
)