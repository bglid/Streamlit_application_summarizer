from . import utils
import requests
from bs4 import BeautifulSoup
import streamlit as st


def ln_job_scraper(job_url):
    """Webscraper for LinkedIn that returns the Job title (often including company and location)
    The Time it was posted, and the "About the Job" section of the posting.

    Args:
        job_url (str): URL to LinkedIn Job posting page

    Returns:
        job_posting_title (str):Title which often includes role name, company name, location, misc.      
        
        job_posting_time (str):
                Time since job has been posted.
        about_the_job (str):
                Text document containing the role description in the "About the Job" section of LinkedIn
    """
    #Creating a random User agent to avoid being blocked
    random_headers = {'User-Agent': utils.random_user_agent()}

    #First checking if we are able to access the site. Terminating if not:
    # url = requests.get(job_url, random_headers) 
    url = utils.get_url(url=job_url, headers=random_headers)
        
    try:    
        #Getting request and parsing through HTML 
        soup = BeautifulSoup(url.content, 'html.parser')   
    except Exception as e:            
        print(f'Error: {e}\nBad URL: Try a different URL or consider entering posting manually.')
        st.exception(e) #For streamlit front-end only
        return None, None, None
    
    #Getting the title, location, company
    title = soup.find('title')
    if title:
        posting_title = title.get_text()
    else: 
        print('Title not found')
        st.warning('Title not found') #For streamlit front-end only
        posting_title = None
    
    #Getting the time it was posted
    time = soup.find('span', {'class': "posted-time-ago__text topcard__flavor--metadata"})
    if time:
        posting_time = time.get_text(strip=True) #Removing whitespace from html
    else: 
        print('Time not found')
        st.warning('Time not found') #For streamlit front-end only
        posting_time = None
    
    #The following class below appears to be what LinkedIn uses as the marker for the "About the Job" section
    about = soup.find('div', {'class': "show-more-less-html__markup"})
    #Checking to see if there is an "About the Job" section
    if about:
        about_the_job = about.get_text() #returning just text about the job posting
        print(about_the_job)
    else:
        print('No "About the Job" section, consider entering posting in manually.')
        st.warning('No "About the Job" section, consider entering posting in manually.') #For streamlit front-end only
        about_the_job = None
    
    return posting_title, posting_time, about_the_job
   

if __name__ == "__main__":
    #For testing
    sample_url = ''
    ln_job_scraper(sample_url)
    
