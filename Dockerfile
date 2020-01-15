FROM python:3
LABEL maintainer="17600235827@163.com"
WORKDIR /src
COPY requirements.txt ./
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "./one.py"]