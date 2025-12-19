import pandas as pd

SHEET_ID = "1zzf4ax_H2WiTBVrJigGjF2Q3Yz-qy2qMCbAMKvl6VEE"
GID = "1438203274"

CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export"
    f"?format=csv&gid={GID}"
)

def load_seo_dataframe() -> pd.DataFrame:
    df = pd.read_csv(CSV_URL)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

# done