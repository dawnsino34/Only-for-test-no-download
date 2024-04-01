from ckan_api import get_dataset_list, get_csv_resources

def serial_crawler(limit=None):
    datasets = get_dataset_list(limit=limit)
    for dataset in datasets:
        csv_urls = get_csv_resources(dataset)