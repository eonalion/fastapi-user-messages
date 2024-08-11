FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .
COPY scripts/format_check.sh .
COPY scripts/lint.sh .
COPY scripts/test.sh .
COPY pytest.ini .
COPY .coveragerc .


RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app /code/app

# Run Black, Ruff and pytest during the build
RUN bash format_check.sh
RUN bash lint.sh
RUN bash test.sh

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]