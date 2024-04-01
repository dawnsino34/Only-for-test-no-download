import requests
from typing import List, Dict

CKAN_BASE_URL = "https://open.canada.ca/data/en/api/3/action/"
PACKAGE_SEARCH_PATH = "package_search"
FILE_FORMAT = 'csv'

def get_dataset_list(limit=None) -> List[Dict]:
    """
    获取指定数量的数据集列表。

    Parameters:
        limit (int): 请求的数据集最大数量，默认为100。

    Returns:
        List[Dict]: 包含数据集信息的字典列表，请求失败返回空列表。
    """
    try:
        response = requests.get(f"{CKAN_BASE_URL}{PACKAGE_SEARCH_PATH}?rows={limit}")
        response.raise_for_status()
        data = response.json()
        return data['result']['results'] if data['success'] else []
    except requests.RequestException:
        return []

def get_csv_resources(dataset: Dict) -> List[str]:
    """
    从数据集中提取所有CSV文件的URL。

    Parameters:
        dataset (Dict): 包含数据集信息的字典。

    Returns:
        List[str]: 数据集中所有CSV格式资源的URL列表。
    """
    return [resource['url'] for resource in dataset.get('resources', []) if resource.get('format', '').lower() == FILE_FORMAT]