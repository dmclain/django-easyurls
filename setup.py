from distutils.core import setup
import os,re,sys

sys.path.insert(0, os.path.dirname(__file__))
try:
    import easyurls
finally:
    del sys.path[0]

def _stripsourcecode(s):
    # replace sourcecode blocks with literal blocks
    return re.sub(r'\.\. sourcecode:: \w+', '::', s.strip())


import sys

if 'sdist' in sys.argv:
    import mmf_release_tools
    version = mmf_release_tools.generate_release_version(easyurls.__version__, __file__)
    mmf_release_tools.write_release_version(version)
else:
    with open("RELEASE-VERSION", "r") as f:
        version = f.readlines()[0].strip()


setup(
    name='django-easyurls',
    description=easyurls.__doc__.strip().splitlines()[0],
    author='Ollie Rutherfurd',
    author_email='oliver@rutherfurd.net',
    version=version,
    license='BSD',
    py_modules=['easyurls'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    long_description=_stripsourcecode(easyurls.__doc__),
    platforms=['any'],
)
