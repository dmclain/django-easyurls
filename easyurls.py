#!/usr/bin/env python
#
# Copyright (C) 2009 by Ollie Rutherfurd <oliver@rutherfurd.net>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# * Redistributions of source code must retain the above copyright notice, 
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * The name of the author may not be used to endorse or promote products 
#   derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE. 
#
r"""
Making it easier to read and write Django URL patterns.

By assuming defaults, such as `year` is a 4-digit number and `id` is
one or more digits, `easyurls` removes much of the repetition from
defining URLs in Django.  As a result, URLs are shorter, easier to read,
and easier to write.

Compare the following:

.. sourcecode:: python

    # standard
    urlpatterns += patterns('django.views.generic.date_based',
        url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
            'object_detail', info_dict),
        url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/$',
            'archive_day',   info_dict),
        url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', info_dict),
        url(r'^(?P<year>\d{4})/$', 'archive_year',  info_dict),
    )

    # using easyurls: let it generate the regex
    from easyurls import regex as p
    urlpatterns += patterns('django.views.generic.date_based',
        url(p('<year>/<month:mon>/<day>/<slug>'), 'object_detail', info_dict),
        url(p('<year>/<month:mon>/<day>'),        'archive_day',   info_dict),
        url(p('<year>/<month:mon>'),              'archive_month', info_dict),
        url(p('<year>'),                          'archive_year',  info_dict),
    )

    # using easyurls: calling easyurl is equivalent to url(regex(...), ...)
    from easyurls import easyurl
    urlpatterns += patterns('django.views.generic.date_based',
        easyurl('<year>/<month:mon>/<day>/<slug>', 'object_detail', info_dict),
        easyurl('<year>/<month:mon>/<day>',        'archive_day',   info_dict),
        easyurl('<year>/<month:mon>',              'archive_month', info_dict),
        easyurl('<year>',                          'archive_year',  info_dict),
    )


These three sets of URL patterns are equivalent.  In the second and
third sets, ``easyurl`` generated the same regular expressions as in the
first set.  The difference is the patterns in second and third set are
easier to read, write, and so less likely to contain errors.  Why keep
repeating that `year` is a 4-digit number or that `id` is an integer?
Why not have reasonable defaults, that can be overridden when deviating
from them.  For example, by default `month` is a 1- or 2-digit year, but
above we're overriding the default, expecting instead a 3-letter
abbreviation.  Lastly, continuing the trend of less repetition: by
default, if missing, '^' is prepended to patterns and '/' and '$' are
appended.

`easyurls` works by defining names for patterns and generating
regular expressions for you.  By default, the name of the captured
variable is the name of the pattern.  This can be overridden, as is done
above where the `mon` pattern is used for `month`, instead of the
default ``\d{1,2}``.

Let's dive in and explore easyurls.

.. sourcecode:: pycon

    >>> from easyurls import easyurl, regex

``easyurl`` is an automatically created instance of
``URLPatternGenerator``.

.. sourcecode:: pycon

    >>> type(easyurl)
    <class 'easyurls.URLPatternGenerator'>

``regex`` is just an alias for ``easyurl.regex``, which generates the
regular expressions.

.. sourcecode:: pycon

    >>> easyurl.regex == regex
    True
    >>> print regex('article/<id>/edit')
    ^article/(?P<id>\d+)/edit/$

Here are the default patterns:

.. sourcecode:: pycon

    >>> for name in sorted(easyurl.patterns):
    ...     print '%5s: %s' % (name, easyurl.patterns[name])
      day: \d{1,2}
       id: \d+
      mon: [a-z]{3}
    month: \d{1,2}
        n: \d+
     slug: [\w-]+
      tag: \w+
     year: \d{4}

To use a different name for a pattern, or different pattern for a name,
add the pattern after the name, prefixing the pattern with ":".

.. sourcecode:: pycon

    # default for month is \d{1,2}
    >>> print easyurl.regex('<month>')
    ^(?P<month>\d{1,2})/$

    # using [a-z]{3} for month
    >>> print easyurl.regex('<month:mon>')
    ^(?P<month>[a-z]{3})/$

    # using [a-z]{3} for mmm
    >>> print easyurl.regex('<mmm:mon>')
    ^(?P<mmm>[a-z]{3})/$

It's easy to add new or override existing patterns:

.. sourcecode:: pycon

    >>> easyurl['yy'] = r'\d{2}'
    >>> easyurl['mm'] = r'\d{2}'
    >>> easyurl['dd'] = r'\d{2}'

    >>> print easyurl.regex('<year:yy>/<month:mm>/<day:dd>')
    ^(?P<year>\d{2})/(?P<month>\d{2})/(?P<day>\d{2})/$

By default, if no pattern is found, ``\d+`` is assumed.

.. sourcecode:: pycon

    >>> print easyurl.regex('releases/<project_id>')
    ^releases/(?P<project_id>\d+)/$

For flexibility, you can always use a regular expression.

.. sourcecode:: pycon

    # regex for unknown "zip_code"
    >>> print easyurl.regex('zip/<zip_code:\d{5}>')
    ^zip/(?P<zip_code>\d{5})/$

    # override slug, allowing "."
    >>> print easyurl.regex('<slug:[\w-.]+>')
    ^(?P<slug>[\w-.]+)/$

For demonstration and testing purposes, here's how prepending and
appending or '^', '/', and '$' is handled:

.. sourcecode:: pycon

    >>> print easyurl.regex('')
    ^$
    >>> print easyurl.regex('foo$')
    ^foo$
    >>> print easyurl.regex('foo/')
    ^foo/$
    >>> print easyurl.regex('/')
    ^/$

Prepending of '^' and appending of '/' and '$' can be disabled.

.. sourcecode:: pycon

    >>> easyurl.regex('foo', anchor=False, terminate=False, append_slash=False)
    'foo'
"""
__version__ = '0.2'
__all__ = ['easyurl', 'regex', 'URLPatternGenerator']

import functools,re

# name: pattern
PATTERNS = {
    'day':   r'\d{1,2}',
    'id':    r'\d+',
    'month': r'\d{1,2}',
    'slug':  r'[\w-]+',
    'tag':   r'\w+',
    'year':  r'\d{4}',
    # these defined for the pattern, not name
    # ex: <month:mon>
    'mon':   r'[a-z]{3}', # jan, feb, etc...
    'n':     r'\d+',      # n=number
}

# <name[:pattern]>
VARIABLE = re.compile(r'<(?P<name>\w+)(?::?(?P<pattern>[^>]+))?>')


class URLPatternGenerator(object):
    def __init__(self, patterns=None, default=r'\d+',
                 append_slash=True, anchor=True, terminate=True):
        self.patterns = patterns or dict(PATTERNS.items())
        self.default = default              # default pattern
        self.append_slash = append_slash    # trailing /
        self.anchor = anchor                # prepend ^
        self.terminate = terminate          # append $
    
    def add(self, name, pattern):
        self.patterns[name] = pattern
    __setitem__ = add
    
    def _replace(self, match, url):
        regexp = None
        name = match.group('name')
        pattern = match.group('pattern')
        # pattern may be a name or regexp
        if pattern:
            regexp = self.patterns.get(pattern, pattern)
        # use pattern for name, or default
        else:
            regexp = self.patterns.get(name, self.default)
        segment = '(?P<%s>%s)' % (name, regexp)
        return segment
    
    def url(self, path, *args, **kw):
        # replacement for django.conf.urls.defaults.url
        from django.conf.urls.defaults import url as _url
        return _url(self.regex(path), *args, **kw)
    __call__ = url
    
    def regex(self, url, **kw):
        r = VARIABLE.sub(functools.partial(self._replace, url=url), url)
        if kw.get('anchor', self.anchor) and r[:1] != '^':
            r = '^' + r
        # special-case so '^$' doesn't end up with a '/' in it
        if url and kw.get('append_slash', self.append_slash) and r[-1:] not in ('$','/'):
            r += '/'
        if kw.get('terminate', self.terminate) and r[-1:] != '$':
            r += '$'
        return r


# don't require creating an instance of the class
easyurl = URLPatternGenerator()
regex = easyurl.regex


if __name__ == '__main__':
    import doctest; doctest.testmod()
