FROM python:3.10

WORKDIR /app

# تحديث Ghostscript للنسخة المصلحة من ثغرة Upload2Shell CVE-2026-125396
RUN apt-get update && apt-get install -y --no-install-recommends ghostscript libgs10 \
    && apt-get upgrade -y ghostscript libgs10 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && gs --version

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
