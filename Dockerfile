FROM python

WORKDIR /TutorBackend

COPY run.py .
COPY requirements.txt .
COPY tutor /TutorBackend/tutor

RUN pip install -r requirements.txt

RUN pip install gunicorn

# CMD ["python", "run.py"]

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "run:wsgi()"]
