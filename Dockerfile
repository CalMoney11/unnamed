# Use slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all local files to the container
COPY . .

# Add dummy ENV to force rebuild of next layers
ENV FORCE_REINSTALL=1

# Log files in app dir
RUN echo "[DEBUG] Listing files in /app:" && ls -la /app

# Print the contents of requirements.txt
RUN echo "[DEBUG] Printing contents of requirements.txt:" && cat requirements.txt

# Install Python dependencies
RUN echo "[DEBUG] Installing dependencies from requirements.txt..." && \
    pip install --no-cache-dir -r requirements.txt

# Check that openai is installed correctly
RUN echo "[DEBUG] Verifying openai install:" && \
    python -c "import openai; print('[DEBUG] openai version:', openai.__version__)"

# Run the Flask app
CMD ["python", "app.py"]


ENV OPENAI_API_KEY=$_OPENAI_API_KEY
ENV OPENAI_PROJECT_ID=$_OPENAI_PROJECT_ID
ENV OPENAI_ORG_ID=$_OPENAI_ORG_ID
