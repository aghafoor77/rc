"""
Celery application configuration for EU AI Act Compliance System.
Handles background tasks for document processing, classification, and report generation.
"""

import os
from celery import Celery
from kombu import Exchange, Queue

# Get configuration from environment
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "0")

# Celery broker and backend URLs
BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# Create Celery application
app = Celery(
    "eu_ai_act_compliance",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=[
        "backend.tasks.classification",
        "backend.tasks.document_processing",
        "backend.tasks.report_generation",
    ]
)

# Celery configuration
app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task execution settings
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3300,  # 55 minutes
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    
    # Result backend settings
    result_expires=86400,  # 24 hours
    result_persistent=True,
    
    # Queue settings
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
    
    # Define queues
    task_queues=(
        Queue("default", Exchange("default"), routing_key="default"),
        Queue("classification", Exchange("classification"), routing_key="classification"),
        Queue("documents", Exchange("documents"), routing_key="documents"),
        Queue("reports", Exchange("reports"), routing_key="reports"),
    ),
    
    # Task routes
    task_routes={
        "backend.tasks.classification.*": {"queue": "classification"},
        "backend.tasks.document_processing.*": {"queue": "documents"},
        "backend.tasks.report_generation.*": {"queue": "reports"},
    },
    
    # Worker settings
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=False,
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# Task base class configuration
app.conf.task_default_retry_delay = 60  # 1 minute
app.conf.task_max_retries = 3


if __name__ == "__main__":
    app.start()

# Made with Bob
