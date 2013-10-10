"""
sentry_pushover
~~~~~~~~~~~~~~~~~~

:copyright: (c) 2011 by the Sentry Team, see AUTHORS for more details.
:license: GNU General Public License, see LICENSE for more details.
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-pushover').version
except Exception, e:
    VERSION = 'unknown'
