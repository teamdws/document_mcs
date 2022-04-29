FROM python:python-3.8.10
COPY .  /flask_project
WORKDIR /flask_project
RUN pip install -r requirements.txt
EXPOSE  8000
CMD ["python3", "main.py"]
