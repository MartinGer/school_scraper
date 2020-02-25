FROM python:3.7
WORKDIR /app
COPY . .
VOLUME data
RUN pip install -r requirements.txt
CMD ["python","run_scripts.py"]