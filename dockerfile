FROM python:3.10.5
RUN pip3 install pandas uvicorn fastapi
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]
