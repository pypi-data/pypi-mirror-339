import csv
import json
from pathlib import Path

class DataExporter:
    def __init__(self, export_path="output", filename="scraped_data"):
        """
        Initialize exporter with output directory and base filename.
        """
        self.export_path = Path(export_path)
        self.filename = filename

        # Create export folder if it doesn't exist
        self.export_path.mkdir(parents=True, exist_ok=True)

    def CSVExporter(self, data):
        """
        Export list of dictionaries to a CSV file.
        """
        if not data:
            print("No data to export to CSV.")
            return

        keys = data[0].keys()  # Assume all dicts have the same keys
        file_path = self.export_path / f"{self.filename}.csv"

        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

        print(f"[✓] Data exported to CSV: {file_path}")

    def JSONExporter(self, data):
        """
        Export data (list of dicts) to a JSON file.
        """
        file_path = self.export_path / f"{self.filename}.json"

        with open(file_path, mode='w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[✓] Data exported to JSON: {file_path}")
