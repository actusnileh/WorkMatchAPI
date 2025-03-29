from elasticsearch import AsyncElasticsearch

from core.config import config


es_client = AsyncElasticsearch(hosts=[config.ELASTICSEARCH_URL])
