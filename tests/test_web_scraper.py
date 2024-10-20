import os
import unittest
import sys
print("Python Path:", sys.path)
#Getting the path for the src package
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)
from src.web_scraper import *

### TESTING that our webscraper can get a valid job url and returns none for an invalid one ###

class TestWebScraper(unittest.TestCase):
    
    def test_valid_url(self):
        """Testing that a valid URL returns title, time, and about the job info. """
        #our valid url
        valid_url = ""
        title, time, about_job = ln_job_scraper(valid_url)
        self.assertIsNotNone(title)
        self.assertIsNotNone(time)
        self.assertIsNotNone(about_job)
    
    def test_invalid_url(self):
        """Testing that an invalid URL returns None."""
        invalid_url = "https://www.linkedin.com/jobs/view/"
        self.assertIsNone(ln_job_scraper(invalid_url))
        
        
if __name__ == "__main__":
    unittest.main()