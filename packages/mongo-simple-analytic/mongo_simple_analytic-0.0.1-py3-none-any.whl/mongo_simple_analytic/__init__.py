# SPDX-FileCopyrightText: 2025-present Hao Wu <haowu@dataset.sh>
#
# SPDX-License-Identifier: MIT
from datetime import datetime, UTC, timedelta

from pymongo import MongoClient


def get_timeduration(duration_str: str) -> timedelta:
    """
    Parse duration string to a timedelta object.
    Supported formats: 1m (minute), 2h (hour), 3d (day), 4w (week), 5y (year)
    :param duration_str: Duration string (e.g. "1m", "2h", "3d", "4w", "5y")
    :return: A timedelta object representing the parsed duration
    :raises ValueError: If the input string format is invalid
    """
    if not duration_str or not isinstance(duration_str, str):
        raise ValueError("Invalid duration string provided.")

    # Define multipliers for each unit
    multipliers = {
        "m": timedelta(minutes=1),
        "h": timedelta(hours=1),
        "d": timedelta(days=1),
        "w": timedelta(weeks=1),
        "y": timedelta(days=365)  # Approximate a year as 365 days
    }

    # Extract the numeric value and unit
    try:
        value = int(duration_str[:-1])  # Strip the last character (unit) and convert to integer
        unit = duration_str[-1]  # Extract the unit
    except (ValueError, IndexError):
        raise ValueError("Duration string must be in the format '<number><unit>' (e.g., '1m', '2h', '3d').")

    # Calculate timedelta based on unit
    if unit in multipliers:
        return value * multipliers[unit]
    else:
        raise ValueError(
            f"Unsupported duration unit '{unit}'. Supported units: 'm' (minute), 'h' (hour), 'd' (day), 'w' (week), 'y' (year).")


class ActivityLogger:
    def __init__(
            self,
            client: MongoClient,
            database_name: str,
            collection_name: str = 'activity_logs'
    ):
        self.client = client
        self.db = client[database_name]
        self.collection_name = collection_name
        self.coll = self.db[collection_name]

    def create_collection(
            self,
            size=1024 * 1024 * 1024,  # 1GB
            max_records=1000
    ):
        self.db.create_collection(
            self.collection_name,
            capped=True,
            size=size,  # 1MB max size
            max=max_records  # optional: max number of documents
        )
        self.coll = self.db[self.collection_name]
        self.coll.create_index(
            "createdAt",
            expireAfterSeconds=60 * 60 * 24 * 10  # we keep 10 days record.
        )

    def log_activity(self, user: str, target: str, meta):
        self.coll.insert_one({
            "user": user,
            "target": target,
            "meta": meta,
            "createdAt": datetime.now(UTC)
        })

    def fetch_logs(self, end=None, period='10d'):
        if end is None:
            end = datetime.now(UTC)
        start = end - get_timeduration(period)
        return self.coll.find({"createdAt": {"$gte": start, "$lte": end}})
