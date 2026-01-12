# Use a lightweight Python image
FROM python:3.13.5

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies (This is cached until requirements.txt changes)
RUN pip install --no-cache-dir -r requirements.txt

COPY SRC/APP/ .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

