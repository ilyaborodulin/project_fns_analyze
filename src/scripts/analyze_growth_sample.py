import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

flat_df = pd.read_csv("data/flat_sample_30_companies.csv")

flat_df["year"] = pd.to_numeric(flat_df["year"], errors="coerce")
flat_df = flat_df.sort_values(["inn", "year"]).copy()

flat_df["prev_net_profit_2400"] = flat_df.groupby("inn")["net_profit_2400"].shift(1)

flat_df["net_profit_growth_pct"] = (
    (flat_df["net_profit_2400"] - flat_df["prev_net_profit_2400"])
    / flat_df["prev_net_profit_2400"].abs()
) * 100

print(flat_df[[
    "inn",
    "company_name",
    "year",
    "net_profit_2400",
    "prev_net_profit_2400",
    "net_profit_growth_pct"
]].head(20))

print("\nКоличество непустых growth:")
print(flat_df["net_profit_growth_pct"].notna().sum())

plot_df = flat_df.dropna(subset=["net_profit_growth_pct"]).copy()
plot_df = plot_df[
    (plot_df["net_profit_growth_pct"] >= -500) &
    (plot_df["net_profit_growth_pct"] <= 500)
]

bins = list(range(-500, 550, 50))

plt.figure(figsize=(12, 6))
sns.histplot(plot_df["net_profit_growth_pct"], bins=bins)

plt.title("Распределение роста чистой прибыли")
plt.xlabel("Рост чистой прибыли, %")
plt.ylabel("Количество наблюдений")
plt.xticks(range(-500, 501, 50), rotation=45)
plt.tight_layout()

plt.savefig("outputs/net_profit_growth_hist_sample.png", dpi=300, bbox_inches="tight")
print("График сохранен: outputs/net_profit_growth_hist_sample.png")

plt.show()

print("Количество наблюдений для графика:", len(plot_df))
print("Минимум:", plot_df["net_profit_growth_pct"].min())
print("Максимум:", plot_df["net_profit_growth_pct"].max())

flat_df.to_csv("data/flat_sample_30_companies_with_growth.csv", index=False, encoding="utf-8-sig")
print("Файл сохранен: data/flat_sample_30_companies_with_growth.csv")

print("\nАналитический вывод:")
print(
    "В рамках анализа была рассмотрена выборка из 30 компаний строительной отрасли. "
    "По этим компаниям удалось собрать 118 наблюдений финансовой отчетности по годам. "
    "Темп роста чистой прибыли был рассчитан для 70 наблюдений, где присутствовали данные "
    "как за текущий, так и за предыдущий период."
)

print(
    "После исключения сильных выбросов для построения графика осталось 58 наблюдений. "
    "Минимальное значение темпа роста чистой прибыли составило -207.15%, "
    "а максимальное — 489.30%. Это говорит о высокой вариативности финансовых результатов "
    "между компаниями и периодами."
)

print(
    "Полученные результаты показывают, что внутри исследуемой выборки нет единой устойчивой "
    "динамики: часть компаний демонстрирует рост чистой прибыли, а часть — снижение. "
    "Следовательно, финансовое состояние компаний в рассматриваемом сегменте строительной "
    "отрасли является неоднородным. При этом выводы носят предварительный характер, "
    "поскольку основаны на ограниченной выборке из 30 компаний."
)