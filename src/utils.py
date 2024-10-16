import random
import requests
import time
import streamlit as st

#Creating a random User agent to avoid being blocked with web scraping
def random_user_agent():
    """Returns a random user agent string."""
    user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
                   ]
    return random.choice(user_agents)

def get_url(url, headers, retries=3, backoff_factor=1.5, status_list = [429, 500, 502, 503, 504]):
    """Used to get url with retries and backoff.

    Args:
        url (str): The URL to fetch.
        headers (dict): HTTP headers for the request.
        retries (int, optional): Maximum number of retries. Defaults to 3.
        backoff_factor (float, optional): Factor for calculating the sleep time between retries. Defaults to 1.5.
        status_list (list, optional): List of status codes to retry. Defaults to [429, 500, 502, 503, 504].

    Returns:
        request.Response: The response object if successful, None otherwise.
    """
    #First checking if we are able to access the site. Terminating if not:
    for index in range(retries):
        try:
            response = requests.get(url, headers) 
            if response.status_code == 200:
                return response #successful response!
                
            if response.status_code in status_list:
                st.warning(f'Attempt {index + 1} failed with status code of {response.status_code}. Retrying...')
                time.sleep(backoff_factor * (2 ** index)) #Exponential backoff
            
        except requests.exceptions.RequestException as e:
            st.error(f'Request failed: {e}')
            time.sleep(backoff_factor * (2 ** index))

    #Error codes for user
    #Creating a dict of errors for the user incase they hit an error
    error_codes = {
        403: "Forbidden: The server understands the request but won't fulfill it because it doesn't have the right permissions or access.",
        429: "Too Many Requests: The server has received too many requests from the same IP within a given time frame, so it's rate-limiting in web scraping.",
        500: "Internal Server Error: A generic server error occurred, indicating that something went wrong on the server while processing the request.",
        502: "Bad Gateway:	The server acting as a gateway or proxy received an invalid response from an upstream server.",
        503: "Service Unavailable: The server is too busy or undergoing maintenance and can't handle the request right now.",
        504: "Gateway Timeout: An upstream server didn't respond quickly enough to the gateway or proxy."
    }

    #If all else fails, return none...
    #Returning the likely status codes the user may have received with some potentially helpful info
    st.error(f'Max retries made. Unable to get job posting due to: {response.status_code}: {error_codes[response.status_code]}...')
    return None
