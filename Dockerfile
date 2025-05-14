FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN echo "[DEBUG] Listing files in /app:" && ls -la /app
RUN echo "[DEBUG] Printing contents of requirements.txt:" && cat requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "[DEBUG] Verifying openai install:" && python -c "import openai; print(openai.__version__)"

CMD ["python", "app.py"]