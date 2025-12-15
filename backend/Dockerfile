# Yengil Python versiyasini olamiz
FROM python:3.10-slim

# Muhit o'zgaruvchilari (Python tezroq ishlashi uchun)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ishchi papkani belgilash
WORKDIR /app

# Kutubxonalarni o'rnatish
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Loyiha kodini ko'chirish
COPY . /app/

# Portni ochish (Hozircha shartli ravishda, aslida Compose hal qiladi)
EXPOSE 8000