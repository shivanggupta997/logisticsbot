FROM python:3.13-slim
WORKDIR /app
COPY . /app/
RUN pip install django dotenv google.generativeai gunicorn
EXPOSE 8000
RUN python manage.py migrate
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "chatbot_project.wsgi:application"]