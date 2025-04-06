import json
import sqlite3
from typing import List, Dict, Any
import os
import csv
from datetime import datetime
import gzip
import pickle
from concurrent.futures import ThreadPoolExecutor
import uuid


class StorageManager:
    def save_advanced(
        self,
        data: List[Dict],
        filename: str,
        format: str = "json",
        compress: bool = False,
    ):
        if not data:
            raise ValueError("No data to save")
        base_filename = filename.rsplit(".", 1)[0]
        if format == "json":
            output = {
                "data": data,
                "metadata": {
                    "saved_at": datetime.now().isoformat(),
                    "source": "WebChameleon",
                },
            }
            with ThreadPoolExecutor() as executor:
                executor.submit(self._save_json, base_filename, output, compress)
        elif format == "db":
            with sqlite3.connect(f"{base_filename}.db") as conn:
                self._save_to_db(conn, data)
        elif format == "csv":
            with ThreadPoolExecutor() as executor:
                executor.submit(self._save_csv, base_filename, data)
        else:
            raise ValueError("Unsupported format. Use json, db, or csv")

    def _save_json(self, filename: str, data: Dict, compress: bool):
        if compress:
            with gzip.open(f"{filename}.json.gz", "wt", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            with open(f"{filename}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    def _save_to_db(self, conn: sqlite3.Connection, data: List[Dict]):
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS scraped_data
                          (id TEXT PRIMARY KEY, url TEXT, title TEXT, content TEXT, metadata TEXT, timestamp TEXT)"""
        )
        for item in data:
            cursor.execute(
                "INSERT OR REPLACE INTO scraped_data VALUES (?, ?, ?, ?, ?, ?)",
                (
                    str(uuid.uuid4()),
                    item.get("url"),
                    item.get("title"),
                    item.get("content"),
                    json.dumps(item.get("metadata", {})),
                    datetime.now().isoformat(),
                ),
            )
        conn.commit()

    def _save_csv(self, filename: str, data: List[Dict]):
        with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["url", "title", "content", "metadata", "timestamp"]
            )
            writer.writeheader()
            for item in data:
                writer.writerow(
                    {
                        "url": item.get("url"),
                        "title": item.get("title"),
                        "content": item.get("content"),
                        "metadata": json.dumps(item.get("metadata", {})),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
