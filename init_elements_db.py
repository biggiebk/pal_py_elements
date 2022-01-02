#!/usr/bin/python3
"""
	Description: Initialize mongod DB for Pal Elements
"""
import sys
from support.initialize import InitializeElementsDB

initialize_element_db = InitializeElementsDB(sys.argv[1])
initialize_element_db.initialize()
