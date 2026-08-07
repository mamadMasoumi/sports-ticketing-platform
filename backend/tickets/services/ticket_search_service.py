import json
import hashlib
import redis
from django.conf import settings
from tickets.repositories.ticket_repository import TicketRepository
from decimal import Decimal
from datetime import datetime, date

# Reuse the same Redis connection pattern as otp_service.py
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

CACHE_TTL_SECONDS = 120   # 2 minutes

def _serialize_value(val):
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    if isinstance(val, Decimal):
        return float(val)   # or str(val) if you want consistent strings
    return val

def _serialize_ticket(ticket: dict) -> dict:
    return {k: _serialize_value(v) for k, v in ticket.items()}


class TicketSearchService:
    @staticmethod
    def _build_cache_key(filters: dict) -> str:
        """Create a deterministic cache key from sorted filters."""
        sorted_json = json.dumps(filters, sort_keys=True, default=str)
        hash_hex = hashlib.md5(sorted_json.encode()).hexdigest()
        return f"ticket_search:{hash_hex}"

    @classmethod
    def search(cls, filters: dict) -> list:
        cache_key = cls._build_cache_key(filters)
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        # cache miss
        raw_result = TicketRepository.search_tickets(filters)
        result = [_serialize_ticket(ticket) for ticket in raw_result]
        redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(result))
        return result