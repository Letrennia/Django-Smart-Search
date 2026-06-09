# Django-Smart-Search
Django Smart Search is a web application that allows users to easily find answers within Django documentation. It provides a link to the article and highlights the answer in the preview. The system estimates the difficulty level of every article.

---
## Features
- Ask questions in natural language.
- Semantic search based on vector embeddings and BM25.
- Find answers withing Django documentation.
- Display headlines with url to relevant documentation articles.
- Results ranked according to relevance.
- Highlighted answers in the preview.
- Analysis of article's difficulty level.
- User friendly interface.

## Technology Used
- Python 3.10.11
- Django (ver. 5.2.14)

## Embedding Model
- Django-Smart-Search uses 'granite-embedding-english-small-r2' from Hugging Face developed by IBM team.

- The model can be found at https://huggingface.co/ibm-granite/granite-embedding-small-english-r2

## Installation
Clone the repository
```bash
git clone https://github.com/Letrennia/Django-Smart-Search.git
cd django-smart-search
```
Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```
Install dependencies
```bash
pip install -r requirements.txt
```
## Configuration
Create a .env file and configure the required environment variables:
```bash
SECRET_KEY_ENV=your_django_secret_key
```

## Running the Application
Start the development server:
```bash
python manage.py runserver
```
The application will be available at: http://127.0.0.1:8000/

## Authors
- Letrennia
- Drogon3

This project was developed as part of the Techniques and Tools of Natural Language Processing course at Bialystok Univerity of Technology.