# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import logging
import pkg_resources
import requests
import socket
import zc.buildout.easy_install

from buildout.sendpickedversions.wrappers import DistributionWrapper
from zc.buildout.buildout import MissingOption

try:
    import json
except ImportError:
    import simplejson as json


logger = zc.buildout.easy_install.logger
buildout_version = pkg_resources.get_distribution('zc.buildout').version


def install(buildout):
    """Monkeypatch buildout to collect and send buildout data"""
    info = BuildoutInfo(buildout)

    pick_package_info = info.pick_package_info
    _get_dist = info.enable_sending_picked_versions(zc.buildout.easy_install.Installer._get_dist)  # noqa
    shutdown = info.send_picked_versions(logging.shutdown)

    zc.buildout.easy_install.Installer.pick_package_info = pick_package_info
    zc.buildout.easy_install.Installer._get_dist = _get_dist
    logging.shutdown = shutdown


class BuildoutInfo(object):
    """Main class containing methods for handling buildout data."""

    def __init__(self, buildout):
        self.packages = []
        self.processed = set()
        self.versionmap = {}

        self.buildout = buildout.get('buildout', None)
        self.hostname = socket.gethostname()
        self.ipv4 = socket.gethostbyname(socket.getfqdn())
        self.pinned_versions = dict(buildout.get('versions', None))
        self.started = datetime.datetime.now().isoformat()

    def enable_sending_picked_versions(self, original_get_dist):
        """
        Enables our custom code to run before zc.buildouts get_dist
        method is being called.
        """
        # Check if we have zc.buildout < 2.x
        if int(buildout_version[0]) < 2:
            def get_dist_1(self_, requirement, ws, always_unzip):
                dists = original_get_dist(self_, requirement, ws, always_unzip)
                self_.pick_package_info(dists, ws)
                return dists
            get_dist = get_dist_1
        elif (int(buildout_version[0]) < 3
              and (int(buildout_version[2]) < 3
                   and int(buildout_version[4]) < 5)
              or int(buildout_version[2]) >= 9):
            def get_dist_2(self_, requirement, ws):
                dists = original_get_dist(self_, requirement, ws)
                self_.pick_package_info(dists, ws)
                return dists
            get_dist = get_dist_2
        else:
            def get_dist_225(self_, requirement, ws, for_buildout_run=False):
                dists = original_get_dist(self_, requirement, ws,
                                          for_buildout_run)
                self_.pick_package_info(dists, ws)
                return dists
            get_dist = get_dist_225

        return get_dist

    def pick_package_info(self, dists, ws):
        """Parses through package requirements and picks data."""
        dists = list(dists)
        dists.sort()

        # Pick data from packages fetched via buildout.
        for dist in dists:
            if dist.project_name not in self.processed:
                package = DistributionWrapper(dist)
                # Add package to list of processed packages
                self.processed.update([package.name])
                # Add data to packages list
                self.packages.append(package.get_dict())
                self.update_versionmap(package)

        # Loop through ws to pick packages which have satisfied
        # requirements and aren't in the dists list.
        # (this happens if buildout is ran with -N switch)
        for dist in ws:
            if dist.project_name not in self.processed:
                package = DistributionWrapper(dist)
                # Add package to list of processed packages
                self.processed.update([package.name])
                # Add data to packages list
                self.packages.append(package.get_dict())
                self.update_versionmap(package)

    def update_versionmap(self, package):
        """Updates version map information."""
        if package.version:
            self.versionmap[package.name] = package.version

    def send_picked_versions(self, old_logging_shutdown):

        def logging_shutdown():
            data = {'packages': {}}
            for package in self.packages:
                data['packages'][package['name']] = {
                    'requirements': package['requirements'],
                    'version': package['version']}

            data['buildout_config'] = dict(self.buildout)
            data['versionmap'] = self.versionmap
            data['started'] = self.started
            data['finished'] = datetime.datetime.now().isoformat()
            data['hostname'] = self.hostname
            data['ipv4'] = self.ipv4
            data['pinned_versions'] = self.pinned_versions

            if self.data_url:
                if self.data_url.startswith('file://'):
                    res = self.write_data(data)
                else:
                    res = self.send_data(data)
            else:
                res = json.dumps(data)

            if res:
                print(res)
            else:
                print('Got error sending the data to %s' % self.data_url)

            old_logging_shutdown()
        return logging_shutdown

    @property
    def data_url(self):
        """Return URL where data should be sent."""
        url = None
        try:
            url = self.buildout['send-data-url']
        except MissingOption:
            # Maybe we have old configuration which uses whiskers-url
            try:
                url = self.buildout['whiskers-url']
            except MissingOption:
                logging.info('No send-data-url specified.')
                pass

        if url and not url.startswith('file://') and url[-1] != '/':
            url += '/'

        return url

    def send_data(self, data):
        """Send buildout data to remote URL."""

        logging.info('Sending data to remote url (%s)' % self.data_url)

        try:
            res = requests.post(self.data_url, json=data, timeout=60)
        except Exception as e:
            print(str(e))
            return None

        return res.content or None

    def write_data(self, data):
        """Write buildout data to local file."""

        logging.info('Writing data to file (%s)' % self.data_url)

        try:
            with open(self.data_url[len('file://'):], 'w') as fp:
                fp.write(json.dumps(data, indent=4))
        except IOError as e:
            print(str(e))
            return None

        return self.data_url[len('file://')]
