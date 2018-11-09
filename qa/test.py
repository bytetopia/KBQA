from lango.parser import StanfordServerParser


class StanfordParserTest(object):

    def __init__(self, host='localhost', port=9000, properties={}):
        self.parser = StanfordServerParser(host, port, properties)

    def query(self, sentence):
        tree = self.parser.parse(sentence)
        return tree


if __name__ == '__main__':
    q = StanfordParserTest()
    query = input('Enter query: ')
    while query != 'exit':
        response = q.query(query)
        print(response)
        query = input('Enter query: ')




















