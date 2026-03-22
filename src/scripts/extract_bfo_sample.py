import pandas as pd
import requests
import time

df = pd.read_csv("data/sample_with_org_ids.csv")
df = df[df["org_id"].notna()].copy()

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*"
})

records = []

for _, row in df.head(30).iterrows():
    org_id = int(row["org_id"])
    inn = str(row["ИНН"])
    company_name = row["Наименование / ФИО"]

    print(f"Обрабатывается org_id={org_id}, ИНН={inn}")

    url = f"https://bo.nalog.gov.ru/nbo/organizations/{org_id}/bfo"
    response = session.get(url, timeout=(10, 60))
    data = response.json()

    for item in data:
        period = item.get("period")
        correction = item.get("typeCorrections", [{}])[0].get("correction", {})
        fin = correction.get("financialResult", {})
        bal = correction.get("balance", {})

        records.append({
            "inn": inn,
            "org_id": org_id,
            "company_name": company_name,
            "year": period,
            "revenue_2110": fin.get("current2110"),
            "cost_2120": fin.get("current2120"),
            "other_income_2340": fin.get("current2340"),
            "other_expenses_2350": fin.get("current2350"),
            "net_profit_2400": fin.get("current2400"),
            "tax_2410": fin.get("current2410"),
            "assets_1600": bal.get("current1600"),
            "balance_total_1700": bal.get("current1700"),
        })

    time.sleep(1)

flat_df = pd.DataFrame(records)

print(flat_df.head(20))
print("\nРазмер таблицы:", flat_df.shape)
print("\nПропуски:")
print(flat_df.isna().sum())

flat_df.to_csv("data/flat_sample_30_companies.csv", index=False, encoding="utf-8-sig")
print("\nФайл сохранен: data/flat_sample_30_companies.csv")