FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install --upgrade pip

#set work directory early so remaining paths can be relative
WORKDIR /

# Adding requirements file to current directory
# just this file first to cache the pip install step when code changes
COPY requirements.txt .

#install dependencies
RUN pip install -r requirements.txt

# copy code itself from context to image
COPY . .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]