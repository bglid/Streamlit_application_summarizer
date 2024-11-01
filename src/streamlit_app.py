import streamlit as st
from web_scraper import ln_job_scraper
from text_processing import keyword_rank, compare_resume
from docx import Document #For reading microsoft word files

def main():
    #Set title and box input for entering resume
    st.title('Resume & Job comparison')
    st.write('To help with catching any key phrases you may have missed on your resume')
    st.divider()

    resume = st.file_uploader('Upload Word Doc. resume:', accept_multiple_files=False, type=['docx'])
    #Reading in and converting word document to a string
    if resume is not None:
            try:
                resume_doc = Document(resume)
                #Writing out resume text
                resume_text = ""
                for paragraph in resume_doc.paragraphs:
                    resume_text += paragraph.text + "\n"
            except Exception as e:
                st.error(f'An error occured while reading the resume:\n{e}')

    #Selecting what the user is interested in checking 
    select = st.selectbox('What would you like to check in this job description:', 
                    options=('Check for Keywords', 'Compare Resume Similarity'),
                    index=None,
                    placeholder='Please select an option...')

    #Getting the URL to the job posting
    job_url = st.text_input('Job Posting url', help='Make sure you link the url to the exact page of the job posting. I.e. not a related link to the posting',
                            key='url')
    #Setting button to not react until clicked:
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False
    url_input = st.button('Submit Url', on_click=click_button)
    

    # If there is no clear "About the Job" section, post text in manually for time being:
    # job_text = st.text_input('Job Description', help="NOTE: Use this when the job url isn't from LinkedIn, or the posting isn't based on an online source.")
    #Creating columnns for results
    col_1, col_2 = st.columns(2)


    #Making sure that a url or resume is posted
    if url_input and resume == None:
        st.write('No resume uploaded')


    #keyword comparison
    if url_input and (job_url != ''):
        if select == 'Check for Keywords':
            #once the button is clicked on "Submit Url"
                with st.spinner(text='Processing Text...'):
                    with col_1:
                        posting_title, posting_time, about_the_job = ln_job_scraper(job_url)
                        #Getting the text from the "About the job section"
                        keywords = keyword_rank(about_the_job)
                        st.subheader('Job Posting Key Phrases:')
                        st.table(keywords)
                        st.subheader(posting_title)
                        st.write(f'Posted {posting_time}')
                
                    with col_2:
                        #Getting the text from the resume    
                        resume_keywords = keyword_rank(resume_text)
                        st.subheader('Resume Key Phrases:')
                        st.table(resume_keywords)

        #Document similarities
        if select == 'Compare Resume Similarity':
            if url_input:
                with st.spinner(text='Processing Text...', ):
                    posting_title, posting_time, about_the_job = ln_job_scraper(job_url)
                    st.header(posting_title)
                    st.write(f'Posted {posting_time}')
                    with col_1:
                        similarity_score = compare_resume(resume_text, about_the_job)
    #Posting a message saying the url is blank
    if job_url == '':
        st.write('No job posting url is linked')
                    
    #Creating a button to clear all the data caches
    if st.button("Clear All"):
        st.cache_data.clear()
        # st.session_state['url'] = "" 

#Defining a function to handle the button not reacting until clicked:
def click_button():
    st.session_state.clicked = True
                
                
if __name__ == "__main__":
    main()