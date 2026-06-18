# 🏪 Smart Retail Management System (Project Home Store)

![Project Banner](https://img.shields.io/badge/Status-Active-success)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)

A comprehensive AI-powered system designed for smart retail environments. This project integrates real-time video analytics, facial recognition, product detection, and an intelligent QA system to streamline store management and enhance the customer experience.

## ✨ Key Features

*   **📷 Camera Management & RTSP Processing**: Real-time video stream ingestion (`read_rtsp.py`) from multiple IP cameras with a comprehensive dashboard for camera configuration.
*   **👤 Facial Detection & Recognition**: Real-time facial tracking, alignment, and recognition using high-performance models (ResNet50/CLIP) and optimized vector search (FAISS/HNSW).
*   **🛒 Retail Object Detection (OBB & YOLO)**: Specialized detection and classification of retail products on shelves using YOLOv8/YOLOv11 and Oriented Bounding Boxes (OBB).
*   **🤖 RAG-based Q&A System**: An intelligent Retrieval-Augmented Generation module (`Rag_answear_question`) utilizing ChromaDB to answer queries about product descriptions and store inventory.
*   **📊 Web Dashboard**: A modern web interface (`web_sell`) for administrators to manage cameras, view recognition logs, and monitor system health.
*   **🔄 Scalable Architecture**: Built with a message broker (RabbitMQ) and robust database backend (PostgreSQL) for reliable inter-service communication and data storage.

## 🛠️ Technology Stack

*   **Machine Learning/Computer Vision**: PyTorch, YOLOv8/v11, TensorRT, FAISS, OpenCV
*   **Backend Application**: Python, Django/Flask
*   **Vector Database**: ChromaDB (for RAG), FAISS (for Face/Object embeddings)
*   **Database & Message Queue**: PostgreSQL, RabbitMQ
*   **Deployment**: Docker, Docker Compose

## 📁 Project Structure

```text
project_home/
├── Rag_answear_question/   # Logic for Retrieval-Augmented Generation (Q&A)
├── web_sell/               # Frontend & Backend web dashboard code
├── docker-compose.yaml     # Container orchestration configuration
├── read_rtsp.py            # Service to ingest and process RTSP camera streams
├── process_face.py         # Core logic for face detection and embedding extraction
├── infer_detect_sell_obj.py# Inference script for retail product detection
├── build_index.py          # Script for building/updating FAISS/HNSW indices
├── rabbitmq.py             # Message queue publisher/consumer logic
├── process_postgre_db.py   # Database interaction layer
└── requirements.txt        # Python dependency list
```

## 🚀 Getting Started

### Prerequisites

*   Docker and Docker Compose
*   NVIDIA GPU with CUDA support (recommended for TensorRT/model inference)
*   Python 3.8+ (if running locally without Docker)

### Installation & Execution

1.  **Clone the repository:**
    ```bash
    git clone <your-github-repo-url>
    cd project_home
    ```

2.  **Environment Setup:**
    Ensure you configure your `.env` file with the correct database credentials, RTSP URLs, and API keys.

3.  **Run with Docker Compose:**
    The easiest way to start the entire system is using Docker Compose.
    ```bash
    docker-compose up -d --build
    ```

    *Alternatively, for specific service configurations, you can use `compose_vd.yml`.*

4.  **Access the Dashboard:**
    Open your browser and navigate to the configured port (check your `.env` or compose file) to access the Smart Retail Management Dashboard.

## 🧠 AI Models & Inference

The system uses several pre-trained and fine-tuned models located in the project directory:
*   `resnet50_embedding_model.pt`: Deep learning model for extracting facial embeddings.
*   `yolov8s.pt` / `yolo11n.pt`: Models used for detecting and classifying products.
*   `landmark_model.onnx`: Used for facial alignment before recognition.

*Note: TensorRT optimizations are supported via the included `TensorRT-8.6.1.6` libraries for accelerated inference on NVIDIA hardware.*

## 📈 Future Enhancements
*   [ ] Implement dynamic updates for vector databases without service interruption.
*   [ ] Enhance the RAG system to process real-time inventory changes.
*   [ ] Add advanced analytics and heatmaps for customer movement tracking.


