from setuptools import setup, find_packages

install_requires = ['redis', 'motor', 'jinja2', 'yuicompressor', 'webassets',
                    'cssmin', 'PyYAML']
# 'Routes'

setup(name='scheduler',
      version='0.1',
      author='Oleksandr Sochka',
      author_email='sasha.sochka@gmail.com',
      package_dir={'': 'src'},
      packages=find_packages('src', exclude=["test**"]),
      install_requires=install_requires,
      zip_safe=False)
