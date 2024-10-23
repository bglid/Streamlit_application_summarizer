import streamlit as st
from web_scraper import ln_job_scraper
from text_processing import keyword_rank, compare_resume
from io import StringIO
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
    url_input = st.button('Submit Url')    

    # If there is no clear "About the Job" section, post text in manually for time being:
    # job_text = st.text_input('Job Description', help="NOTE: Use this when the job url isn't from LinkedIn, or the posting isn't based on an online source.")
    #Creating columnns for results
    col_1, col_2 = st.columns(2)



    #keyword comparison
    if select == 'Check for Keywords':
        if url_input: #once the button is clicked on "Submit Url"
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
                    
    #Creating a button to clear all the data caches
    if st.button("Clear All"):
        st.cache_data.clear()
        # st.session_state['url'] = "" 

        
                
                
if __name__ == "__main__":
    main()