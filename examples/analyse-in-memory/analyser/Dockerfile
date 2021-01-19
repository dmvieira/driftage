FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY adwin_analyser.py ./

ENTRYPOINT ["python", "adwin_analyser.py"]