# Copyright (c) 2020 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


from argparse import ArgumentParser, Namespace

import qumulo.lib.opts

from qumulo.lib.request import pretty_json
from qumulo.rest_client import RestClient


class AuthoritativeDnsGetSettings(qumulo.lib.opts.Subcommand):
    NAME = 'authoritative_dns_get_settings'
    SYNOPSIS = 'Retrieve settings for Qumulo hosted Authoritative DNS server'

    @staticmethod
    def main(rest_client: RestClient, _args: Namespace) -> None:
        settings = rest_client.authoritative_dns.get_settings()
        print(f"Enabled: {settings['enabled']}")
        print(f"FQDN: {settings['fqdn']}")
        restrictions_msg = ' None' if len(settings['host_restrictions']) == 0 else ''
        print(f'Host Restrictions:{restrictions_msg}')
        for host in settings['host_restrictions']:
            print(f'\t{host}')


class AuthoritativeDnsPatchSettings(qumulo.lib.opts.Subcommand):
    NAME = 'authoritative_dns_patch_settings'
    SYNOPSIS = 'Configure settings for Qumulo hosted Authoritative DNS server'

    @staticmethod
    def options(parser: ArgumentParser) -> None:
        parser.add_argument(
            '--fqdn', type=str, help='Fully Qualified Domain Name for the DNS server'
        )
        parser.add_argument(
            '--enable', action='store_true', help='Enable the Authoritative DNS server'
        )
        parser.add_argument(
            '--disable', action='store_true', help='Disable the Authoritative DNS server'
        )
        parser.add_argument(
            '--host-restrictions',
            type=str,
            nargs='+',
            help='List of host restrictions (IP addresses or CIDR blocks)',
        )

    @staticmethod
    def main(rest_client: RestClient, args: Namespace) -> None:
        settings = {}

        if args.fqdn is not None:
            settings['fqdn'] = args.fqdn

        if args.enable:
            settings['enabled'] = True

        if args.disable:
            settings['enabled'] = False

        if args.disable and args.enable:
            parser = ArgumentParser(description='authoritative_dns_patch_settings')
            parser.error('Cannot enable and disable at the same time')

        if args.host_restrictions is not None:
            settings['host_restrictions'] = args.host_restrictions

        response = rest_client.authoritative_dns.modify_settings(**settings)
        print('Authoritative DNS settings updated successfully')
        print(pretty_json(response))
