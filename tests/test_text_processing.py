import os
import unittest
import sys
print("Python Path:", sys.path)
#Getting the path for the src package
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)
from src.web_scraper import *