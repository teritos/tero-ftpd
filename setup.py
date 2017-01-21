"""Setup file."""
#!/usr/bin/env python

import re
from setuptools import setup


with open('README.rst') as readme_file:
    README = readme_file.read()

with open('HISTORY.rst') as history_file:
    HISTORY = history_file.read()

def get_version():
    """Retrieves package version from the file."""
    with open('teroftpd/_version.py') as fh:
        # pylint: disable=c0103
        m = re.search(r"\(([^']*)\)", fh.read())
    if m is None:
        raise ValueError("Unrecognized version in 'fades/_version.py'")
    return m.groups()[0].replace(', ', '.')


REQUIREMENTS = {
    'pyftpdlib':'pyftpdlib',
    'libtero':'libtero',
    'channels':'channels',
}


setup(
    name='teroftpd',
    version='0.1.0',
    description="Tero FTP Server",
    long_description=README + '\n\n' + HISTORY,
    author=" ",
    author_email=" ",
    url='https://github.com/teritos/tero-ftpd',
    packages=[
        'teroftpd',
    ],
    package_dir={'libtero':
                 'libtero'},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='teroftpd',
    install_required=['setuptools'],
    extras_require=REQUIREMENTS,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3.5',
    ],
)
