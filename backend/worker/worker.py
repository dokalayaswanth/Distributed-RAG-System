from worker.ingestion_worker import run_ingestion_worker_once

def main() -> None:
    run_ingestion_worker_once()

if __name__ == "__main__":
    main()