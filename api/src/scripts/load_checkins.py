from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from dateutil import parser
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models.checkin import Checkin

# Russian month names mapping
RUSSIAN_MONTHS = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12",
}


def parse_timestamp(ts_str: str) -> datetime:
    """Parse timestamp string to datetime object."""
    try:
        # First try default parsing
        return parser.parse(ts_str)
    except parser.ParserError:
        try:
            # Handle Russian date format
            day, month, year, time = ts_str.split()
            month_num = RUSSIAN_MONTHS.get(month.lower())
            if not month_num:
                raise ValueError(f"Unknown month: {month}")

            date_str = f"{year}-{month_num}-{day.zfill(2)} {time}"
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except Exception as e:
            raise ValueError(f"Could not parse timestamp: {ts_str}") from e


def round_datetime_to_nearest_second(dt: datetime) -> datetime:
    if dt.microsecond >= 500_000:
        dt += timedelta(seconds=1)
    return dt.replace(microsecond=0)


def load_checkins(csv_path: str, db: Session):
    """Load checkins from CSV file into database."""
    print(f"Loading checkins from {csv_path}")
    df = pd.read_csv(csv_path)

    # Convert timestamps
    df["timestamp"] = df["timestamp"].apply(parse_timestamp)
    # Create Checkin objects
    checkins = []
    for _, row in df.iterrows():
        rounded_timestamp = round_datetime_to_nearest_second(row["timestamp"])

        checkin = Checkin(
            user=row["user"],
            timestamp=rounded_timestamp,
            hours=float(row["hours"]),
            project=row["project"],
        )
        print(checkin.hours)
        checkins.append(checkin)

    # Bulk insert records
    try:
        db.bulk_save_objects(checkins)
        db.commit()
        print(f"Successfully loaded {len(checkins)} checkins")
    except Exception as e:
        db.rollback()
        print(f"Error loading checkins: {e}")
        raise


if __name__ == "__main__":
    """Main function to run the script."""
    # Get the project root directory (two levels up from script)
    project_root = Path(__file__).parent.parent.parent.parent
    # Construct path to CSV in project root
    csv_path = project_root / ".temp/dailycheckins_minimal.csv"
    print(f"Looking for CSV at: {csv_path}")
    db = SessionLocal()
    try:
        load_checkins(str(csv_path), db)
    finally:
        db.close()
