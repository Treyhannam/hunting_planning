FROM python:3.12

WORKDIR /hunting_planning

RUN pip install --upgrade pip 

RUN pip install pip-tools

COPY pyproject.toml /hunting_planning/pyproject.toml

RUN pip-compile -o requirements.txt pyproject.toml

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/hunting_planning/src

COPY src/ ./src

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "src/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]

# CMD ["ls", "-l", "/hunting_planning/src/app/st_pages"]