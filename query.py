from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Write a query that retrieves movies where the description includes the phrase: "timeless classic"
query = {
    "query": {
        "match_phrase": {
            "description": {
                "query": "timeless classic",
                "slop": 5  # Allow for some flexibility in word order
            }
        }
    }
}

res = es.search(index="movies", body=query)
print("Movies with 'timeless classic' in description: \n\n")
for hit in res["hits"]["hits"]:
    print(hit["_source"]["title"])

# Write a query to search for movies that meet the following conditions:
#   - The movie must include the word " romance" in either the title or description fields.
#   - The movie may optionally belong to the Drama genre, which, if present, should influence its relevance in the results.
#   - Only movies with a rating greater than 3.5 should be included in the results.

query = {
    "query": {
        "bool": {
            "must": {
                "multi_match": {
                    "query": "romance",
                    "fields": ["title", "description"]
                }
            },
            "should": {
                "term": {"genres": "Drama"}
            },
            "filter": {
                "range": {
                    "rating": {"gt": 3.5}
                }
            }
        }
    }
}

res = es.search(index="movies", body=query)
print("\nMovies with 'romance' in title or description, optional Drama genre, and rating > 3.5:\n\n")
for hit in res["hits"]["hits"]:
    print(f"{hit['_source']['title']} (score={hit['_score']})")

# Write a query to find movies that satisfy the following criteria:
#   - At least one tag in the tags field has a tag value of "classic”.
#   - The tag must have been created after the January of  2007
#   - Ensure that your query specifically targets the tags field and correctly matches the relationship between the tag and timestamp_ fields.
#   - Test your query to verify it retrieves only those movies where the above conditions are met. Provide the query and the results in your submission.

query = {
    "query": {
        "nested": {
            "path": "tags",
            "query": {
                "bool": {
                    "must": [
                        {"term": {"tags.tag": "classic"}},
                        {
                            "range": {
                                "tags.timestamp": {
                                    "gt": 1167609600  # 2007-01-01 epoch
                                }
                            }
                        }
                    ]
                }
            }
        }
    }
}

res = es.search(index="movies", body=query)

print("\nMovies with 'classic' tag created after January 2007:\n\n")
for hit in res["hits"]["hits"]:
    print(f"{hit['_source']['title']}")

# Create a query that computes the following
#   - Statistical data for movie ratings:
#   - The average value of the ratings.
#   - The highest and lowest ratings recorded in the index.

query = {
    "size": 0,  # No hits needed, only aggregations
    "aggs": {
        "rating_stats": {
            "stats": {
                "field": "rating"
            }
        }
    }
}

res = es.search(index="movies", body=query)

stats = res["aggregations"]["rating_stats"]
print("\nStatistical data for movie ratings:\n")
print(f"Average: {stats['avg']}")
print(f"Min: {stats['min']}")
print(f"Max: {stats['max']}")

# For genres:
#   - Group movies by their genres and calculate how many movies fall into each genre.
#   - Ensure the results are sorted to display the most common genres first.

query = {
    "size": 0,  # No hits needed, only aggregations
    "aggs": {
        "genre_counts": {
            "terms": {
                "field": "genres",
                "size": 20,  # Top 20 genres
                "order": {"_count": "desc"}
            }
        }
    }
}

res = es.search(index="movies", body=query)

print("\nNumber of movies by genre:\n")
for bucket in res["aggregations"]["genre_counts"]["buckets"]:
    print(f"{bucket['key']}: {bucket['doc_count']}")
