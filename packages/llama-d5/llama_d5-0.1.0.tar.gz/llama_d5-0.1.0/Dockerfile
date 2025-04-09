FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies using uv
RUN uv pip install --system -r requirements.txt

# Copy the application code
COPY . .

# Run any database migrations
RUN if [ -f "alembic.ini" ]; then alembic upgrade head; fi

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "your_package_name.main:app", "--host", "0.0.0.0", "--port", "8000"] 