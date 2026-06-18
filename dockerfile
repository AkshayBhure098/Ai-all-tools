FROM nvidia/cuda:11.8.0-base-ubuntu22.04

WORKDIR /app

# ---------- Install Python ----------
# RUN apt-get update && apt-get install -y \
#     python3 \
#     python3-pip \
#     python3-dev \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
    
# ---------- Upgrade pip ----------
RUN pip install --upgrade pip

# ---------- Install PyTorch CUDA 12.1 ----------
RUN pip3 install --no-cache-dir \
    torch>=2.6.0+cu118 \
    torchvision>=0.15.0+cu118 \
    torchaudio>=2.6.0+cu118 \
    --index-url https://download.pytorch.org/whl/cu118
    
# ---------- Copy & install requirements ----------
COPY req.txt /app/
RUN pip install --no-cache-dir -r req.txt

# ---------- Copy application ----------
COPY . /app

# CMD ["python", "app.py"]

# Streamlit environment variables (bind all IPv4 & IPv6)
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_ADDRESS="::"
ENV STREAMLIT_SERVER_PORT="8501"
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

EXPOSE 8501

# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=::"]

CMD ["streamlit", "run", "app.py", "--server.address", "::", "--server.port", "8501"]
