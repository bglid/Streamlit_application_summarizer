import unittest
from src.web_scraper import ln_job_scraper

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
        self.assertIsNone(invalid_url)
        
        
if __name__ == "__main__":
    unittest.main()