FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip 

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src

COPY ./data /app/data

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "src/1_Overview.py", "--server.port=8501", "--server.address=0.0.0.0"]