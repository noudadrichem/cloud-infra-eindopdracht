from dnszone import DnsZone

class DNSService():
    def __init__(self):
        self.zone = DnsZone(
            'www.???.com',
            '192.'
        )