from lango.matcher import match_rules
from lango.parser import StanfordServerParser
from collections import OrderedDict
from qa.sparql import SparqlOnline, SparqlLocal
from qa.synonyms import PropertySynonyms
import logging


class QueryHandler(object):
    """
    Processing natural language query and return answer.
    """

    def __init__(self, data_source='online', host='localhost', port=9000, properties={}):
        """
        Initialize query handler.

        Args:
            data_source (str): using 'online' zhishi.me API or 'local' sparql endpoint.
            host (str): host of Stanford CoreNLP service
            port (int): port of Stanford CoreNLP service
            properties (dict): properties for Stanfoord CoreNLP service

        """

        # Initialize Stanford CoreNLP Parser
        self.parser = StanfordServerParser(host, port, properties)

        # Define rules.
        # query single entity
        self.entity_rules = OrderedDict([
            # 命名实体，如 周杰伦，微软
            ('( FRAG ( NR:subject-r ) )', {}),
            # 普通名词，如 水果
            ('( NP ( NN:subject-r ) )', {}),
            # 谁是周杰伦，什么是桃子
            ('( IP ( NP ( PN ) ) ( VP ( VC ) ( NP ( NN/NR:subject-r ) ) ) )', {}),
            # 周杰伦是谁，桃子是什么
            ('( IP ( NP ( NN/NR:subject-r ) ) ( VP ( VC ) ( NP ( PN ) ) ) )', {}),
        ])

        # query entity property
        self.entity_property_rules = OrderedDict([
            # 姚明身高
            ('( NP ( NP ( NP/NR:subject-o ) ) ( NP ( NN:property-r ) ) )', {}),
            # 姚明的身高
            ('( NP ( DNP ( NP ( NN/NR:subject-r ) ) ( DEG ) ) ( NP ( NN:property-r ) ) )', {}),
            # 珠穆朗玛峰的海拔是多少
            ('( IP ( NP ( DNP ( NP ( NR:subject-r ) ) ( DEG ) ) ( NP ( NN:property-r ) ) ) ( VP ) )', {}),
            # 珠穆朗玛峰海拔是多少
            ('( IP ( NP ( NP/NR:s_type ) ( NN/NP:p_type ) ) ( VP ( VC ) ( QP/NP:q_type ) ) )', {
                's_type': OrderedDict([
                    ('( NR:subject-r )', {}),
                    ('( NP ( NR:subject-r ) )', {}),
                ]),
                'p_type': OrderedDict([
                    ('( NN:property-r )', {}),
                    ('( NP ( NN:property-r ) )', {}),
                ]),
                'q_type': OrderedDict([
                    ('( QP ( CD ) )', {}),
                    ('( NP ( PN ) )', {}),
                ])
            }),
        ])

        # Initialize Knowledge Graph query client
        self.data_source = data_source
        if self.data_source == 'online':
            self.sparql = SparqlOnline()
        else:
            self.local_sparql = SparqlLocal()

        # Initialize logger
        self.logger = logging.getLogger(self.__class__.__module__)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

        # Initialize synonyms handler
        self.property_synonyms = PropertySynonyms()

    def _entity_query(self, entity_name):
        """
        Handle entity query.

        Args:
            entity_name (str): entity name

        Returns:
            text (str): abstract of entity
        """
        if self.data_source == 'local':
            return self.sparql.get_abstract(entity_name)
        else:
            baidu_result = self.sparql.get_abstract(entity_name, baike='baidubaike')
            if not baidu_result:
                return self.sparql.get_abstract(entity_name, baike='zhwiki')
            return baidu_result

    def _eneity_property_query(self, entity_name, property_name):
        """
        Handle entity property query.

        Args:
            entity_name (str)
            property_name (str)

        Returns:
            text (str): entity property value
        """
        if self.data_source == 'local':
            return self.sparql.get_property(entity_name, property_name)
        else:
            corrected_property = self.property_synonyms.get_synonyms(property_name)
            self.logger.debug('Corrected property:\n%s' % corrected_property)
            baidu_result = self.sparql.get_property(entity_name, property_name, baike='baidubaike')
            if not baidu_result:
                return self.sparql.get_property(entity_name, property_name, baike='zhwiki')
            return baidu_result

    def query(self, sentence):
        """
        Answers a query

        Args:
            sentence (str): query sentence

        Returns:
            ans(str): answer text
        """
        tree = self.parser.parse(sentence)
        self.logger.debug('Dependence parse tree: \n%s' % tree)
        info = match_rules(tree, self.entity_rules)
        if info:
            # entity query
            self.logger.debug('Entity match:\n%s' % info)
            ans = self._entity_query(info['subject'])
            return ans
        info = match_rules(tree, self.entity_property_rules)
        if info:
            # entity proprety query
            self.logger.debug('Entity property match:\n%s' % info)
            ans = self._eneity_property_query(info['subject'], info['property'])
            return ans
        return 'rule not match'




















