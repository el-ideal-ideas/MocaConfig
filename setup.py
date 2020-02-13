from setuptools import setup, find_packages
from codecs import open
from os import path
from moca_config import VERSION

package_name = "moca_config"

root_dir = path.abspath(path.dirname(__file__))


def __requirements():
    require_list = [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]
    print('----------------------------------------------------------------------------')
    print('Requirements List: ' + ','.join(require_list))
    print('----------------------------------------------------------------------------')
    return require_list


with open('README.md', mode='r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=package_name,
    packages=find_packages(),
    version=VERSION,
    license=license,
    install_requires=__requirements(),
    author='el.ideal-ideas',
    author_email='el.idealideas@gmail.com',
    url='https://github.com/el-ideal-ideas/MocaConfig',
    description='An JSON based config manager.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='Moca, MocaConfig, config, json, JSON',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Natural Language :: English',
        'Natural Language :: Japanese',
        'Natural Language :: Chinese (Simplified)',
    ],
)
