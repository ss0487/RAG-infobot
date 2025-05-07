# RAG-infobot

An **end-to-end Retrieval-Augmented Generation (RAG) application** leveraging **Llama 3.1 7b** for text generation and **Stable Diffusion 3.5** for image generation. This project is fully containerized and deployed using **Docker**.

## Features

- **Text Generation**: Harnesses the power of Llama 3.1 7b for accurate and contextual text generation.
- **Image Generation**: Utilizes Stable Diffusion 3.5 for high-quality image generation.
- **End-to-End Workflow**: Combines retrieval, generation, and deployment seamlessly.
- **Dockerized Deployment**: Fully containerized for easy setup and deployment.

## Repository Structure

```
RAG-infobot/
├── src/                # Source code for text and image generation
├── data/               # Data files and datasets
├── models/             # Pre-trained models and checkpoints
├── docker/             # Docker-related configuration files
├── tests/              # Test scripts for ensuring functionality
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration for containerization
└── README.md           # Project documentation
```

## Getting Started

### Prerequisites

- **Docker**: Ensure Docker is installed on your machine.
- **Python 3.8+**: Required for running the application locally.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ss0487/RAG-infobot.git
   cd RAG-infobot
   ```

2. Build the Docker container:
   ```bash
   docker build -t rag-infobot .
   ```

3. Run the Docker container:
   ```bash
   docker run -p 8080:8080 rag-infobot
   ```

### Local Setup (Without Docker)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. **Text Generation**:
   - Input your query through the web interface or API endpoint.
   - The RAG system retrieves relevant context and generates a response using the Llama 3.1 model.

2. **Image Generation**:
   - Provide a textual description for the desired image.
   - Stable Diffusion generates a high-quality image based on the description.

## Acknowledgments

- [Llama 3.1](https://example.com) for advanced text generation.
- [Stable Diffusion](https://example.com) for image generation.
- Docker for containerization and deployment.
