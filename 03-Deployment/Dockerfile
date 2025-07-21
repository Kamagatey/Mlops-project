FROM python:3.10-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

COPY app/ .
RUN mkdir -p /app/model

CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]