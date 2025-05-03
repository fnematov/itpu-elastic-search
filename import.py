from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

mapping = {
    "mappings": {
        "properties": {
            "movieId": {"type": "integer"},
            "title": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}}
            },
            "genres": {"type": "keyword"},
            "description": {"type": "text"},
            "tags": {
                "type": "nested",
                "properties": {
                    "userId": {"type": "integer"},
                    "tag": {"type": "keyword"},
                    "timestamp": {"type": "date", "format": "epoch_second"}
                }
            },
            "rating": {"type": "float"}
        }
    }
}

es.indices.create(index="movies", body=mapping)

import json
from elasticsearch.helpers import bulk

with open("data/movies.json") as f:
    movies = json.load(f)

actions = [
    {
        "_index": "movies",
        "_source": movie
    }
    for movie in movies
]

bulk(es, actions)