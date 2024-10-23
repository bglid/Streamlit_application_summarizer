import spacy
import pytextrank
import streamlit as st
from spacy_streamlit import visualize_similarity

#Grabbing the keywords from the description
def keyword_rank(text):
    #Setting up the spacy model 
    nlp = spacy.load('en_core_web_md')
    nlp.add_pipe('textrank') #Adding the keyword ranking
    
    #Error handling if the doc is blank:
    try:
        doc = nlp(text)
        key_phrases = []
        #Getting the most relevent keyphrases
        for phrase in doc._.phrases[:10]:
            key_phrases.append(phrase.text.lower())
        return key_phrases
    except Exception as e:
        st.exception(f'{e} \nTry running the URL again!') # For streamlit front-end

#Summarizing the text
def compare_resume(resume, job_description):
    #Setting up the spacy model 
    #Excluding pipes not needed for similarity comparison to improve computing time
    try:
        nlp = spacy.load('en_core_web_md')
        resume_doc = nlp(resume)
        jd_doc = nlp(job_description)
        print(f'Resume Simlarity to job posting: {resume_doc.similarity(jd_doc)}')
        visualize_similarity(nlp, (resume_doc, jd_doc)) #Displaying on Streamlit Front-end
    except Exception as e:
        st.exception(f'{e} \nTry running the URL again!') # For streamlit front-end
        
    return resume_doc.similarity(jd_doc)
    
if __name__ == "__main__":
    sample_resume = "Designed custom Matplotlib data visualization reports with Python for teams without access to Tableau. Cleaned csv data utilizing Python to ingest with Workbench to create actionable data visualization reports in Tableau."
    sample_text = "Dice is the leading career destination for tech experts at every stage of their careers. Our client, TEKsystems c/o Allegis Group, is seeking the following. Apply via Dice today! Description: Participate in the data analysis and design of analytics products within a focused area of the business value stream to enable data driven business decisions that will drive performance and lead to the accomplishment of annual goals. Serve as a domain specialist on data and business processes within area of focus. Translate complex business requirements into data requirements and work with internal customers to define data requirement details based on expressed partner needs.Participate in structured, end-to-end analysis to inform product strategy, data architecture and reporting decisions."
    keyword_rank(sample_text)
    compare_resume(sample_resume, sample_text)