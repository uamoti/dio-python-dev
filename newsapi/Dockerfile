from python:3.10.13-slim
workdir /newsapi
copy . /newsapi
run pip install -r requirements.txt
expose 8000
cmd uvicorn main:app --host 0.0.0.0
