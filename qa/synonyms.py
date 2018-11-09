

class PropertySynonyms(object):
    """
    Get standardized name of properties.
    """

    def __init__(self, dict_file='./dict/property_synonyms.txt'):

        self._map = {}

        with open(dict_file, 'r', encoding='utf-8') as in_file:
            line = in_file.readline()
            while line:
                data = line.split(' ')
                for i in range(1, len(data)):
                    self._map[data[i]] = data[0]
                line = in_file.readline()

    def get_synonyms(self, word):
        if word in self._map.keys():
            return self._map[word]
        else:
            return word





