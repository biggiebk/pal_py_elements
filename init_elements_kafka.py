#!/usr/bin/python3
"""
	Description: Initialize mongod DB for Pal Elements
"""
import sys
from support.initialize import InitializeElementsKafka

initialize_element_kafka = InitializeElementsKafka(sys.argv[2])

if sys.argv[1] == 'init':
	initialize_element_kafka.initialize()
elif sys.argv[1] == 'reset':
	initialize_element_kafka.reset()
elif sys.argv[1] == 'get':
	print(initialize_element_kafka.get_topics())
