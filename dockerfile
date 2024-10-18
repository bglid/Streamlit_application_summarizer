FROM python:3.10.13

COPY . . 

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENV NAME JobApplicationSummarizer

CMD [ "streamlit", "run", "src/streamlit_app.py"]