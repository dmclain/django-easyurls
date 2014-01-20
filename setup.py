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

setup(
    name='django-easyurls',
    description=easyurls.__doc__.strip().splitlines()[0],
    author='Ollie Rutherfurd',
    author_email='oliver@rutherfurd.net',
    version=easyurls.__version__,
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
