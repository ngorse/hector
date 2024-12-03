# Purpose

Chatbot

# Dependencies

Install Ollama 

```
ollama pull llama3.2
```

# Environment

TBD

# Run

## Local

```bash
python app.py
```

## Docker

### Build

```bash
docker build -t hector . 
```

### Run

```bash
docker run -p 5555:5555 hector
```

## Docker compose -- Whole system

### certificates

```bash
docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d ulex.servehttp.com
````

### Run

```bash
docker compose up
```
