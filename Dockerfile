FROM python:3.11

COPY requerements.txt ./
RUN pip install --no-cache-dir -r requerements.txt
RUN pip install -U g4f 

RUN mkdir -p /usr/src/app/
COPY . /usr/src/app/
WORKDIR /usr/src/app/

CMD [ "python", "main.py"]