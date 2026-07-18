FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY bot.py config.py scheduler.py ./
COPY services/ ./services/
COPY utils/ ./utils/

# Create logs directory
RUN mkdir -p logs

# Run the bot
CMD ["python", "bot.py"]
