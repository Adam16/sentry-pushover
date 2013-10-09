"""
sentry_pushover
~~~~~~~~~~~~~~~~~~

"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-pushover').version
except Exception, e:
    VERSION = 'unknown'
