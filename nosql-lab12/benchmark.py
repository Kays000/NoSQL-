import csv
import json
import math
import os
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "nosql_lab12")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "books")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client[DB_NAME]
coll = db[COLLECTION_NAME]

QUERY = {"categoryId": 10, "publishedYear": 2015}
INDEX_SPEC = [("categoryId", ASCENDING), ("publishedYear", ASCENDING)]
INDEX_NAME = "idx_category_year"


def get_explain_metrics(mode: str) -> dict:
    exp = coll.find(QUERY).explain()
    stats = db.command("collStats", COLLECTION_NAME)
    exec_stats = exp.get("executionStats", {})
    winning_plan = exp.get("queryPlanner", {}).get("winningPlan", {})

    return {
        "mode": mode,
        "winningPlan": winning_plan.get("stage"),
        "inputStage": winning_plan.get("inputStage", {}).get("stage"),
        "nReturned": exec_stats.get("nReturned"),
        "totalDocsExamined": exec_stats.get("totalDocsExamined"),
        "totalKeysExamined": exec_stats.get("totalKeysExamined"),
        "executionTimeMillis": exec_stats.get("executionTimeMillis"),
        "storageSizeBytes": stats.get("storageSize"),
        "totalIndexSizeBytes": stats.get("totalIndexSize"),
    }


def one() -> tuple[float, bool]:
    start = perf_counter()
    try:
        list(coll.find(QUERY).limit(100))
        return ((perf_counter() - start) * 1000, True)
    except Exception:
        return ((perf_counter() - start) * 1000, False)


def percentile(values: list[float], p: float) -> float:
    sorted_vals = sorted(values)
    if not sorted_vals:
        return float("nan")
    idx = (len(sorted_vals) - 1) * p / 100
    lo, hi = math.floor(idx), math.ceil(idx)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (idx - lo)


def run_benchmark(workers: int, n: int = 400, warmup: int = 40) -> dict:
    # Отдельный warm-up перед замером
    for _ in range(warmup):
        one()

    t0 = perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda _: one(), range(n)))
    seconds = perf_counter() - t0

    latencies = [ms for ms, ok in results if ok]
    success = len(latencies)
    errors = n - success

    return {
        "workers": workers,
        "total_requests": n,
        "success": success,
        "errors": errors,
        "error_rate_pct": round((errors / n) * 100, 2),
        "duration_s": round(seconds, 4),
        "rps": round(success / seconds, 2),
        "p50": round(percentile(latencies, 50), 3),
        "p95": round(percentile(latencies, 95), 3),
        "p99": round(percentile(latencies, 99), 3),
    }


def main():
    all_rows = []
    explain_report = []

    # 1. Тест БЕЗ составного индекса
    if INDEX_NAME in coll.index_information():
        coll.drop_index(INDEX_NAME)

    print("=== Режим: БЕЗ индекса (no_index) ===")
    explain_report.append(get_explain_metrics("no_index"))

    for workers in (1, 4, 8):

        for repeat in range(1, 4):
            res = run_benchmark(workers=workers, n=400)
            res["mode"] = "no_index"
            res["repeat"] = repeat
            all_rows.append(res)
            print(f"[no_index] workers={workers}, repeat={repeat} | RPS={res['rps']} | P95={res['p95']} ms | err={res['errors']}")

    # 2. Создание составного индекса и повтор эксперимента
    coll.create_index(INDEX_SPEC, name=INDEX_NAME)

    print("\n=== Режим: С индексом (with_index) ===")
    explain_report.append(get_explain_metrics("with_index"))

    for workers in (1, 4, 8):

        for repeat in range(1, 4):
            res = run_benchmark(workers=workers, n=400)
            res["mode"] = "with_index"
            res["repeat"] = repeat
            all_rows.append(res)
            print(f"[with_index] workers={workers}, repeat={repeat} | RPS={res['rps']} | P95={res['p95']} ms | err={res['errors']}")

    # Сохранение сырых результатов в CSV
    fieldnames = [
        "mode", "workers", "repeat", "rps", "p50", "p95", "p99",
        "errors", "error_rate_pct", "duration_s", "success", "total_requests"
    ]
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    # Сохранение планов explain до/после
    with open("explain_stats.json", "w", encoding="utf-8") as f:
        json.dump(explain_report, f, indent=2, ensure_ascii=False)

    print("\nГотово! Данные сохранены в results.csv и explain_stats.json")


if __name__ == "__main__":
    main()
