import pandas as pd
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


df = pd.read_csv("data/registry_filtered.csv")
sample_df = df.head(100).copy()

session = requests.Session()
retry_strategy = Retry(
    total=3,
    connect=3,
    read=3,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*"
})


def get_org_id_by_inn(inn):
    url = f"https://bo.nalog.gov.ru/advanced-search/organizations/search?query={inn}&page=0"

    try:
        response = session.get(url, timeout=(10, 60))
        response.raise_for_status()
        data = response.json()

        if "content" in data and len(data["content"]) > 0:
            return data["content"][0]["id"]
        return None
    except Exception as e:
        print(f"Ошибка для ИНН {inn}: {e}")
        return None


org_ids = []

for i, inn in enumerate(sample_df["ИНН"], start=1):
    print(f"Обрабатывается {i}/100, ИНН: {inn}")
    org_id = get_org_id_by_inn(inn)
    org_ids.append(org_id)
    time.sleep(1)

sample_df["org_id"] = org_ids

print(sample_df[["Наименование / ФИО", "ИНН", "org_id"]])
print("Найдено org_id:", sample_df["org_id"].notna().sum())

sample_df.to_csv("data/sample_with_org_ids.csv", index=False, encoding="utf-8-sig")
print("Файл сохранен: data/sample_with_org_ids.csv")