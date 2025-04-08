from setuptools import setup, find_packages
try:
    from pathlib2 import Path
except ImportError:
    from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='ezx-pyapi',
    version='1.0.0',
    license='MIT',
    author="EZX Inc.",
    author_email='support@ezxinc.com',
    packages=find_packages('.'),
    package_dir={'': '.'},
    url='http://www.ezxinc.com/',
    keywords='EZX iServer API trading',
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.8, <4",
    project_urls={'Sample API Application' : 'https://github.com/EZXInc/ezx-sample-py' }
)


