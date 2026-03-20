"""PyWorker config for the Legion translation model server.

Configures the Vast serverless PyWorker to proxy requests to the
translation model server running on the same instance.

NOTE: This file is NOT included in the Docker image. The canonical copy
lives at https://github.com/buddhiwick/translate-worker and is cloned
by the Vast platform's start_server.sh via the PYWORKER_REPO env var.
This copy is kept here for reference; edits must be pushed to that repo.
"""
from vastai import (
    Worker,
    WorkerConfig,
    HandlerConfig,
    BenchmarkConfig,
    LogActionConfig,
)

MODEL_SERVER_URL  = "http://127.0.0.1"
MODEL_SERVER_PORT = 18080
MODEL_LOG_FILE    = "/var/log/translate.log"

worker_config = WorkerConfig(
    model_server_url=MODEL_SERVER_URL,
    model_server_port=MODEL_SERVER_PORT,
    model_log_file=MODEL_LOG_FILE,
    model_healthcheck_url=f"{MODEL_SERVER_URL}:{MODEL_SERVER_PORT}/health",
    handlers=[
        HandlerConfig(
            route="/parse",
            allow_parallel_requests=False,
            max_queue_time=30.0,
            workload_calculator=lambda payload: 100.0 * len(payload.get("sentences", [payload.get("sentence", "")])),
            benchmark_config=BenchmarkConfig(
                dataset=[
                    {"sentence": "Add a fallback for client task id when constructing branch names", "parser": "benepar"},
                    {"sentence": "Add a fallback for client task id when constructing branch names", "parser": "stanza"},
                    {"sentence": "Add a fallback for client task id when constructing branch names", "parser": "supar"},
                    {"sentence": "Add a fallback for client task id when constructing branch names", "parser": "roberta"},
                    {"sentence": "Add a fallback for client task id when constructing branch names", "parser": "dep"},
                ],
                runs=1,
                concurrency=1,
            ),
        ),
    ],
    log_action_config=LogActionConfig(
        on_load=["Translation server ready"],
        on_error=["Traceback (most recent call last):", "RuntimeError:"],
    ),
)

Worker(worker_config).run()
