from libs.dnszoneMetAdd import DnsZone

class DNSService():
    def __init__(self):
        self.zone = DnsZone(
            'eindopdracht.test',
            '104.211.15.6'
        )

    def add(self, fqdn, ipv4):
        response = self.zone.add_address(fqdn, ipv4)
        print('ADD DNS RES...', response)
        return response

    def update(self, fqdn, ipv4):
        response = self.zone.update_address(fqdn, ipv4)
        print('UPDATE DNS RES...', response)
        return response

    def delete(self, fqdn):
        response = self.zone.clear_address(fqdn)
        print('DELETE DNS RES...', response)
        return response