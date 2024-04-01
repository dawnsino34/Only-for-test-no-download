from concurrent.futures import ThreadPoolExecutor, as_completed
from ckan_api import get_dataset_list, get_csv_resources

def parallel_crawler(max_workers=None, limit=None):
    datasets = get_dataset_list(limit=limit)
    futures = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for dataset in datasets:
            csv_urls = get_csv_resources(dataset)
            for url in csv_urls:
                future = executor.submit(lambda x: x, url)
                futures.append(future)

        for future in as_completed(futures):
            future.result()