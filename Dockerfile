FROM python:3.6-alpine

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt && rm -rf /root/.cache

COPY . /app
WORKDIR /app

# Expose the application's port
EXPOSE 5000

CMD ["python", "app.py"]