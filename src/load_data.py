from datetime import date, timedelta
from pathlib import Path
import json

import meteostat as ms
import pandas as pd


STATION_ID = "15614"
START_DATE = date(1952, 1, 1)
END_DATE = date(2025, 8, 22)

OUTPUT_DIR = Path("data/raw")
DATA_FILE = OUTPUT_DIR / "sofia_daily_temperature.csv"
METADATA_FILE = OUTPUT_DIR / "sofia_data_metadata.json"


def get_data():
    dataframes = []
    time_series = []

    current_start = START_DATE

    while current_start <= END_DATE:
        current_end = min(
            date(current_start.year + 10, current_start.month, current_start.day)
            - timedelta(days=1),
            END_DATE,
        )

        ts = ms.daily(
            station=ms.Station(id=STATION_ID),
            start=current_start,
            end=current_end,
            parameters=[
                ms.Parameter.TEMP,
                ms.Parameter.TMIN,
                ms.Parameter.TMAX,
            ],
            providers=[
                ms.Provider.DAILY,
            ],
        )

        df = ts.fetch(
            fill=False,
            clean=False,
            sources=True,
        )

        if df.empty:
            raise RuntimeError(
                f"No data returned for {current_start} to {current_end}."
            )

        dataframes.append(df)
        time_series.append(ts)

        current_start = current_end + timedelta(days=1)

    combined_df = pd.concat(dataframes)
    combined_df = combined_df[~combined_df.index.duplicated(keep="first")]
    combined_df = combined_df.sort_index()

    return time_series, combined_df

def get_metadata(ts, df):
    providers = set()
    licenses = {}
    attributions = set()
    commercial_use = set()

    source_columns = [
        column
        for column in df.columns
        if column.endswith("_source")
    ]

    sources_by_column = {
        column: sorted(
            df[column]
            .dropna()
            .unique()
            .tolist()
        )
        for column in source_columns
    }

    for current_ts in ts:
        providers.update(
            str(provider)
            for provider in current_ts.providers
        )

        if current_ts.attribution:
            attributions.add(current_ts.attribution)

        commercial_use.add(current_ts.commercial)

        for license_info in current_ts.licenses:
            key = (
                license_info.name,
                license_info.url,
                license_info.commercial,
                license_info.attribution,
            )

            licenses[key] = {
                "name": license_info.name,
                "url": license_info.url,
                "commercial": license_info.commercial,
                "attribution": license_info.attribution,
            }

    return {
        "providers": sorted(providers),
        "licenses": list(licenses.values()),
        "attributions": sorted(attributions),
        "commercial_use": sorted(commercial_use),
        "sources_by_column": sources_by_column,
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading data...")

    time_series, df = get_data()
    metadata = get_metadata(time_series, df)

    df.to_csv(DATA_FILE, index=False)

    metadata_file_content = {
        "station_id": STATION_ID,
        "station_name": "Sofia Observ.",
        "start_date": str(START_DATE),
        "end_date": str(END_DATE),
        "parameters": [
            "mean temperature",
            "minimum temperature",
            "maximum temperature",
        ],
        "request_method": "10-year chunks",
        "metadata": metadata,
    }

    METADATA_FILE.write_text(
        json.dumps(
            metadata_file_content,
            indent=4,
        ),
        encoding="utf-8",
    )

    print(f"Data saved: {DATA_FILE}")
    print(f"Metadata saved: {METADATA_FILE}")
    print(f"Rows: {len(df):,}")
    print("Done.")

if __name__ == "__main__":
    main()