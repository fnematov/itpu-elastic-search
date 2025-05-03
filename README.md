# 🎬 Elasticsearch Movies Search Project

This project demonstrates how to use **Elasticsearch** for full-text search and analytics on a dataset of movies using Python.

---
## 🚀 Components

- `import.py`:  
  Imports movie data from `data/movies.json` into Elasticsearch with a predefined mapping.

- `query.py`:  
  Contains example queries:
  - Phrase match: `"timeless classic"`
  - Boolean filter: rating > 3.5 and optional genre
  - Nested tag filter: `"classic"` tag added after 2007
  - Aggregation: stats and group by genre

---
## ⚙️ Requirements

- Docker
- Python 3.8+
- Elasticsearch 8.11.1
- Kibana (optional)

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## 🐳 Run Elasticsearch and Kibana

Make sure Docker is installed and run:

```bash
docker-compose up --build
```

Access:
- Elasticsearch: [http://localhost:9200](http://localhost:9200)
- Kibana: [http://localhost:5601](http://localhost:5601)

---

## 📥 Import data

```bash
python import.py
```

This will:
- Create the `movies` index with proper mapping
- Load `data/movies.json` into Elasticsearch

---

## 🔎 Run queries

```bash
python query.py
```

---

## 📁 Project structure

```
.
├── data/
│   └── movies.json
├── import.py
├── query.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

Enjoy searching with Elasticsearch! 🚀
