response = opensearch_client.indices.delete(index=index_name, ignore=[400, 404])