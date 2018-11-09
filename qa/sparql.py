from qa import utils


class SparqlOnline(object):
    """
    Query knowledge graph using zhishi.me API
    """
    def __init__(self):
        self.api_base = 'http://zhishi.me/api/entity/'

    def get_abstract(self, entity_label, baike='baidubaike'):
        url = self.api_base + entity_label + '?property=abstracts&baike=' + baike
        data = utils.api_get(url)
        if data:
            return data['abstracts']
        else:
            return None

    def get_property(self, entity_label, property_name, baike='baidubaike'):
        url = self.api_base + entity_label + '?property=infobox&baike=' + baike
        data = utils.api_get(url)
        if data:
            infobox = data['infobox']
            if property_name in infobox.keys():
                return ','.join(infobox[property_name])
        return None


class SparqlLocal(object):
    """
    Query knowledge graph using local host Apache Fuseki API.
    """
    def __init__(self):
        self.api_base = 'http://localhost:3030/wiki/sparql'

    def get_abstract(self, entity_label):
        sparql = '''
            select ?o 
                where { 
                    ?s <http://www.w3.org/2000/01/rdf-schema#label> "%s"@zh.
                    ?s <http://zhishi.me/ontology/abstract> ?o
                }
            ''' % entity_label
        data = utils.api_post(self.api_base, {'query': sparql})
        bindings = data['results']['bindings']
        if bindings:
            return bindings[0]['o']['value']
        else:
            return None

    def get_property(self, entity_label, property_name):
        pass


if __name__ == '__main__':
    # sl = SparqlLocal()
    # print(sl.get_abstract('朱军'))
    so = SparqlOnline()
    print(so.get_property('珠穆朗玛峰', '海拔'))







