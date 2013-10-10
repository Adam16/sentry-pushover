"""
sentry_pushover.plugin
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2011 by the Sentry Team, see AUTHORS for more details.
:license: GNU General Public License, see LICENSE for more details.
"""

import sys
import logging
from pprint import pformat
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from sentry.plugins.bases.issue import IssuePlugin
from sentry_pushover import VERSION

import httplib
import urlparse
import requests
import simplejson as json


class PushoverSettingsForm(forms.Form):
    userkey = forms.CharField(help_text='Your user key. See https://pushover.net/')
    apikey = forms.CharField(help_text='Application API token. See https://pushover.net/apps/')

    choices = ((logging.CRITICAL, 'CRITICAL'), (logging.ERROR, 'ERROR'), (logging.WARNING,
               'WARNING'), (logging.INFO, 'INFO'), (logging.DEBUG, 'DEBUG'))
    severity = forms.ChoiceField(choices=choices,
                                 help_text="Don't send notifications for events below this level.")

    priority = \
        forms.BooleanField(required=False,
                           help_text='High-priority notifications, also bypasses quiet hours.')


class PushoverPlugin(IssuePlugin):
    author = 'Adam Balachowski'
    author_url = 'https://github.com/Adam16'
    version = VERSION
    slug = 'pushover'
    title = 'Pushover'
    conf_title = title
    conf_key = slug
    project_conf_form = PushoverSettingsForm
    resource_links = [
        ('Bug Tracker', 'https://github.com/Adam16/sentry-pushover/issues'),
        ('Source', 'https://github.com/Adam16/sentry-pushover'),
    ]

    def can_enable_for_projects(self):
        return True

    def is_setup(self, project):
        return all(self.get_option(key, project) for key in ('userkey', 'apikey'))

    def post_process(
        self,
        group,
        event,
        is_new,
        is_sample,
        **kwargs
        ):

        if not is_new or not self.is_setup(event.project):
            return

        # https://github.com/getsentry/sentry/blob/master/src/sentry/models.py#L353
        if event.level < int(self.get_option('severity', event.project)):
            return

        title = '%s: %s' % (event.get_level_display().upper(), event.error().split('\n')[0])

        link = '%s/%s/group/%d/' % (settings.URL_PREFIX, group.project.slug, group.id)

        message = 'Server: %s\n' % event.server_name
        message += 'Group: %s\n' % event.group
        message += 'Logger: %s\n' % event.logger
        message += 'Message: %s\n' % event.message

        self.send_notification(title, message, link, event)

    def send_notification(
        self,
        title,
        message,
        link,
        event,
        ):

        # see https://pushover.net/api

        params = {
            'user': self.get_option('userkey', event.project),
            'token': self.get_option('apikey', event.project),
            'message': message,
            'title': title,
            'url': link,
            'url_title': 'More info',
            'priority': self.get_option('priority', event.project),
            }
        requests.post('https://api.pushover.net/1/messages.json', params=params)
