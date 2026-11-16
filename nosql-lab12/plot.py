import os
import pandas as pd
import matplotlib.pyplot as plt


def main():
    os.makedirs("charts", exist_ok=True)
    df = pd.read_csv("results.csv")

    # Медиана по 3 повторам для каждой конфигурации
    summary = (
        df.groupby(["mode", "workers"], as_index=False)[["rps", "p50", "p95", "p99", "error_rate_pct"]]
        .median()
        .round(3)
    )
    summary.to_csv("summary_medians.csv", index=False)
    print("=== Сводная таблица (медианы по 3 запускам) ===")
    print(summary.to_string(index=False))

    # Расчёт относительного улучшения P95 (%)
    piv_p95 = summary.pivot(index="workers", columns="mode", values="p95")
    piv_p95["p95_improvement_pct"] = (
        (piv_p95["no_index"] - piv_p95["with_index"]) / piv_p95["no_index"] * 100
    ).round(2)
    print("\n=== Относительное улучшение P95 (%) ===")
    print(piv_p95)

    # График 1: P95 Latency
    plt.figure(figsize=(8, 5))
    for mode, label in [("no_index", "Без индекса (COLLSCAN)"), ("with_index", "С индексом (IXSCAN)")]:
        sub = summary[summary["mode"] == mode].sort_values("workers")
        plt.plot(sub["workers"], sub["p95"], marker="o", linewidth=2, label=label)

    plt.title("Зависимость P95 Latency от числа клиентов (Вариант 3: Библиотека)")
    plt.xlabel("Число параллельных клиентов (workers)")
    plt.ylabel("P95 Latency (мс)")
    plt.xticks([1, 4, 8])
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("charts/p95_latency.png", dpi=150)
    plt.close()

    # График 2: Throughput (RPS)
    plt.figure(figsize=(8, 5))
    for mode, label in [("no_index", "Без индекса (COLLSCAN)"), ("with_index", "С индексом (IXSCAN)")]:
        sub = summary[summary["mode"] == mode].sort_values("workers")
        plt.plot(sub["workers"], sub["rps"], marker="s", linewidth=2, label=label)

    plt.title("Зависимость Throughput (RPS) от числа клиентов (Вариант 3: Библиотека)")
    plt.xlabel("Число параллельных клиентов (workers)")
    plt.ylabel("Пропускная способность (RPS)")
    plt.xticks([1, 4, 8])
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("charts/throughput_rps.png", dpi=150)
    plt.close()

    print("\nГрафики сохранены: charts/p95_latency.png и charts/throughput_rps.png")


if __name__ == "__main__":
    main()
