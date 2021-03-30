'''
Module containing DnsZone utility class which provides resolving and
    updating functionality.
    For now, only *A* resource records are targeted.

DNS server will have to both accept queries and allow zone-updates
    for the zone from this host.

Depends on [``dnspython``](https://www.dnspython.org/) module (installed through PIP)
'''

import re            # regex functionality from standard library
import dns.message   # from dnspython package
import dns.query     # from dnspython package
import dns.resolver  # from dnspython package
import dns.update    # from dnspython package

class DnsZone:
    '''
    Class that contains DNS zone functionality and works with dnspython
    '''
    def __init__ (self, zone, nameserver, timeout = 5.0):
        '''
        Initialize this DNS zone and corresponding Resolver object.

        Positional arguments:
         - zone -- FQDN of the DNS zone (with or without the trailing dot)
         - nameserver -- IP address for the authoritative nameserver for zone

        Keyword argument:
         - timeout -- timeout for DNS queries (both resolving and updating),
                           otherwise operations could hang indefinitely
        '''
        self.zone = re.sub('[.]$', '', zone)  # strip trailing dot
        self.nameserver = nameserver

        # Create resolver object using not the system resolver settings ...
        self.resolver = dns.resolver.Resolver(configure=False)
        # ... but the provided nameserver
        self.resolver.nameservers = [ self.nameserver ]
        self.timeout = timeout
    #fed __init__

    def _update(self, update_record):
        ''' Internal method to update a DNS resource record for the zone '''
        try:
            dns.query.udp(update_record, self.nameserver, timeout=self.timeout)
        except dns.exception.Timeout:
            raise
    #fed _update

    def can_contain(self, fqdn):
        ''' Check if zone can contain this FQDN '''
        return self.zone in fqdn  # simple text-based check suffices for now

    def check_address(self, fqdn):
        '''
        Check the status of the A record for an FQDN in the DNS zone
        and return dictionary, either
        `` { 'ipv4' : ``*``<IP address>``*``, 'error' : False } ``
        if successful, or
        `` { 'error' : True, 'error_text' : ``*``<error description>``*`` } ``
        otherwise
        '''
        try:
            # We're only interested in the very first answer by resolver
            return { 'ipv4' : self.resolver.resolve(fqdn, lifetime=self.timeout).response.answer[0][0].address , 'error' : False }
        except dns.exception.Timeout:
            return { 'error' : True , 'error_text' : f'connection to nameserver {self.nameserver} timed out' }, 503
        except dns.resolver.NXDOMAIN:
            return { 'error' : True , 'error_text' : f'{fqdn} not found' }, 404

    #fed check_address

    def update_address(self, fqdn, ipv4):
        '''
        Update the A record associated with an FQDN in the DNS zone
        and return dictionary, either
        `` { 'ipv4' : ``*``<IP address>``*``, 'error' : False } ``
        if successful, or
        `` { 'error' : True, 'error_text' : ``*``<error description>``*`` } ``
        otherwise
        '''
        if not self.can_contain(fqdn):
            return { 'error' : True , 'error_text' : f'FQDN "{fqdn}" is not part of zone {self.zone}' }, 400

        # Create the update record
        my_update = dns.update.Update(self.zone)
        my_update.replace(f'{fqdn}.', 300, 'a', ipv4)

        # Try to modify the zone with the update record
        try:
            self._update(my_update)
        except dns.exception.Timeout:
            return { 'error' : True, 'error_text' : f'connection to nameserver {self.nameserver} timed out' }, 503

        # Check for success
        return self.check_address(fqdn)
    #fed update_address

    def clear_address(self, fqdn):
        '''
        Clear the A record associated with an FQDN in the DNS zone
        and return dictionary, either
        if successful, or
        `` { 'ipv4' : 'not found' } ``
        if successful, or
        `` { 'error' : True, 'error_text' : ``*``<error description>``*`` } ``
        otherwise
        '''
        if not self.can_contain(fqdn):
            return { 'error' : True, 'error_text' : f'FQDN "{fqdn}" is not part of zone {self.zone}' }, 400

        # Create the update record
        my_update = dns.update.Update(self.zone)
        my_update.delete(f'{fqdn}.')

        # Try to modify the zone with the update record
        try:
            self._update(my_update)
        except dns.exception.Timeout:
            return { 'error' : True, 'error_text' : f'connection to nameserver {self.nameserver} timed out' }, 503

        # Check for success. check_address() cannot be used as we now desire
        #     a 'not found' result instead of that being an error
        try:
            return { 'error' : True, 'error_text' : f'{fqdn} resolves to {self.resolver.resolve(fqdn).response.answer[0][0].address}' }
        except dns.resolver.NXDOMAIN:
            return { 'ipv4' : 'not found' }
    #fed clear_address
#ssalc DnsZone
