from collections import defaultdict
import csv

from constants import BASE_DIR, DATE_TIME, RESULTS


class PepParsePipeline:

    def open_spider(self, spider):
        self.status_counts = defaultdict(int)

    def process_item(self, item, spider):
        self.status_counts[item['status']] += 1
        return item

    def close_spider(self, spider):
        result_dir = BASE_DIR / RESULTS
        result_dir.mkdir(exist_ok=True)
        filename = result_dir / f'status_summary_{DATE_TIME}.csv'

        total = sum(self.status_counts.values())
        self.status_counts['Total'] = total

        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])
            writer.writerows(self.status_counts.items())

        self.status_counts.clear()
