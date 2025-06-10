# your_app/sse.py
import json
import threading
import time
from queue import Queue, Empty

# Globalna lista wszystkich połączeń
clients = []

def broadcast(event: str, data: dict):
    """Wrzuca zdarzenie do kolejki każdego klienta."""
    payload = f"event: {event}\n" \
              f"data: {json.dumps(data)}\n\n"
    for q in list(clients):
        q.put(payload)

def event_stream(client_queue: Queue, keepalive: float = 15.0):
    """
    Generator dla StreamingHttpResponse:
    - wysyła komentarz keep-alive co `keepalive` sekund
    - wypuszcza wszystkie zdarzenia z kolejki
    """
    try:
        last_keep = time.time()
        while True:
            # wysyłamy zdarzenia, jeśli są
            try:
                msg = client_queue.get(timeout=1)
                yield msg
            except Empty:
                pass

            # keep-alive co `keepalive` sekund
            now = time.time()
            if now - last_keep >= keepalive:
                yield ": keep-alive\n\n"
                last_keep = now
    finally:
        # usuwamy klienta przy zamknięciu generatora
        clients.remove(client_queue)
