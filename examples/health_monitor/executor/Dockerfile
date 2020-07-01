FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY csv_executor.py ./

ENTRYPOINT ["python", "csv_executor.py"]