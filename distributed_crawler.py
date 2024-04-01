# distributed_crawler.py
from mpi4py import MPI
from ckan_api import get_dataset_list, get_csv_resources

def distributed_crawler(limit=None):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        limit = int(limit) if limit else None
        datasets = get_dataset_list(limit=limit)
        chunks = [datasets[i::size] for i in range(size)]
    else:
        chunks = None

    chunk = comm.scatter(chunks, root=0)

    for dataset in chunk:
        csv_urls = get_csv_resources(dataset)

# parallel_crawler.py
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

# serial_crawler.py
from ckan_api import get_dataset_list, get_csv_resources

def serial_crawler(limit=None):
    datasets = get_dataset_list(limit=limit)
    for dataset in datasets:
        csv_urls = get_csv_resources(dataset)