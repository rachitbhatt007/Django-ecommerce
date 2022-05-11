FROM python
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirement.txt /app
RUN pip install -r requirement.txt
COPY . /app
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]