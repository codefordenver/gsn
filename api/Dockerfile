#Pull base image
FROM python:3

# Set environment variables
ENV PTYHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Create work directory
RUN mkdir /code

# Set work directory
WORKDIR /code

# Move Project to to the working directory
COPY . /code/

EXPOSE 8000

# Install dependencies
RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install --deploy --system --skip-lock --dev
