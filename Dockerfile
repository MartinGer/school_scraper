FROM python:3.7
WORKDIR /app
COPY . .
VOLUME /data
RUN pip install -r requirements.txt
CMD ["python","docker/run_scripts.py"]