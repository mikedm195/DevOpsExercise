FROM tensorflow/tensorflow:1.13.2-gpu-py3

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt && rm -rf /root/.cache

COPY . /app
WORKDIR /app

# Expose the application's port
EXPOSE 5000

CMD ["python", "app.py"]