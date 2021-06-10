from six.moves import urllib
import json
import os

class OctoPartAPI:
    def __init__(self):
        self.endpoint = 'https://octopart.com/api/v4/endpoint'
        self.token = os.getenv('OCTOPART_TOKEN')
        self.headername = 'token'

    def execute(self, query, variables=None):
        return self._send(query, variables)


    def _send(self, query, variables):
        data = {'query': query,
                'variables': variables}
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        if self.token is not None:
            headers[self.headername] = '{}'.format(self.token)

        req = urllib.request.Request(self.endpoint, json.dumps(data).encode('utf-8'), headers)

        try:
            response = urllib.request.urlopen(req)
            return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            print((e.read()))
            print('')
            raise e
            
    def search_by_mfnr(self, mfnr):
        query = '''
        query Search_MfNr($mfnr: String!) {
            search_mpn(q: $mfnr, limit: 1) {
                results {
                    part {
                        mpn
                        manufacturer 
                        {
                            name
                        }
                        best_datasheet 
                        {
                            name
                            url
                            credit_string
                            credit_url
                            page_count
                            mime_type
                        }
                        specs 
                        {
                            attribute 
                            {
                                name
                                group
                            }
                          display_value
                        }                    
                    }
                }
            }
        }
        '''
        resp = self.execute(query, {'mfnr': mfnr})
        raw = json.loads(resp)['data']['search_mpn']['results'][0]['part']
        data = {}
        data['MfNr'] = raw['mpn']
        data['Manufacturer'] = raw['manufacturer']['name']
        data['Datasheet'] = raw['best_datasheet']['url']
        for spec in raw['specs']:
            data[spec['attribute']['name']] = spec['display_value']
        return data
