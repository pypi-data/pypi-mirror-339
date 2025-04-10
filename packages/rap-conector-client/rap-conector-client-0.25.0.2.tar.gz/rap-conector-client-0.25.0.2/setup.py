import os
import sys

import setuptools

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    assert os.system('python3 setup.py sdist bdist_wheel') == 0
    assert os.system('python3 -m twine upload dist/*') == 0
    sys.exit()
elif sys.argv[-1] == 'publish-test':
    assert os.system('python3 setup.py sdist bdist_wheel') == 0
    assert os.system(
        'python3 -m twine upload --repository testpypi dist/*') == 0
    sys.exit()

with open('README-PYPI.md', 'r') as f:
    readme = f.read()

ver = {}
with open(os.path.join(HERE, 'rapconector', 'version.py')) as f:
    exec(f.read(), ver)  # pylint: disable=exec-used

setuptools.setup(
    name='rap-conector-client',
    version=ver['VERSION_STR'],
    author='Samuel de Moura',
    author_email='samueldemouramoreira@gmail.com',
    description='Client for interacting with a RAP Conector API instance',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='LGPLv3',
    install_requires=[
        'requests',
        'requests-toolbelt',
    ],
    extras_require={
        'dev': [
            'yapf',
            'pylint',
        ],
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
        ],
        'test': [
            # Tox 4 breaks tox-pyenv, so we're limiting the version here until
            # that gets fixed.
            # See: https://github.com/tox-dev/tox-pyenv/issues/21
            'tox<4',
            'pytest',
            'pytest-cov',
            'responses',
        ],
        'publish': [
            'twine',
        ]
    },
    packages=setuptools.find_packages(
        exclude=['tests', 'tests_without_mocks']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: Portuguese (Brazilian)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
