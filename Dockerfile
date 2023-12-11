FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y unzip

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN unzip data/geo.zip -d data
RUN unzip data/hotels.zip -d data
RUN unzip data/inventory.zip -d data

EXPOSE 8080

CMD ["python", "src/main.py"]