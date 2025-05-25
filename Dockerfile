FROM python:3.13-slim
WORKDIR /app
COPY . /app/
RUN pip install django dotenv google.generativeai gunicorn
EXPOSE 80
RUN python manage.py migrate
CMD ["gunicorn", "--bind", "0.0.0.0:80", "chatbot_project.wsgi:application"]
