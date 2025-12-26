# 1. Start with a lightweight version of Python (like buying a basic empty box)
FROM python:3.11-slim

# 2. Create a folder inside the box called "code" to work in
WORKDIR /code

# 3. Copy your "requirements.txt" list from your laptop into the box
COPY ./requirements.txt /code/requirements.txt

# 4. Install those requirements inside the box (pip install ...)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copy your "app" folder into the box
COPY ./app /code/app

# 6. The final instruction: "When this box opens, run the server!"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]