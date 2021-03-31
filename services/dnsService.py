from libs.dnszoneMetAdd import DnsZone

class DNSService():
    def __init__(self):
        self.zone = DnsZone(
            'eindopdracht.test.',
            '192.168.178.10'
            # '104.211.15.6'
        )

    def add(self, fqdn, ipv4):
        print('ADD DAN?!', fqdn, ipv4)
        response = self.zone.add_address('foobar.eindopdracht.test', '123.123.123.123')
        print('RESPONSE...', response)
        # if response['error']:
        #     print('HELEMAAL KAPOT DIE UPDATE', response)
        # else:
        #     print('HEEY, Hij doet het?', response)