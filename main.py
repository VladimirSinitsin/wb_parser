import requests
import argparse

import db

from config import DEBUG
from config import ITEMS_AMOUNT
from config import SEARCH_PRODUCT


def main():
    args = parse_args()
    data = collect_data(search_product=args.search_product, items_amount=args.items_amount)
    # Save to database.
    for product_data in data:
        db.insert(product_data)


def parse_args():
    parser = argparse.ArgumentParser(description="Parse products from Wildberries.ru")
    parser.add_argument("--search", dest="search_product", type=str,
                        help="Product name to search for.", default=SEARCH_PRODUCT)
    parser.add_argument("--amount", dest="items_amount", type=int,
                        help="Amount of first products.", default=ITEMS_AMOUNT)
    parser.add_argument("--debug", dest="debug", action="store_true",
                        help='Creating a clean database.', default=DEBUG)
    args = parser.parse_args()
    return args


def collect_data(search_product: str, items_amount: int) -> list:
    """
    Collect data from Wildberries.ru

    :param search_product: product name to search for.
    :param items_amount: amount of first products.
    :return: list with products.
    """
    response = requests.get(
            "https://search.wb.ru/exactmatch/ru/male/v4/search?appType=1&couponsGeo=2,12,7,3,6,18,21&curr=rub&"
            "dest=-1029256,-85617,-389795,123585987&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&"
            f"query={search_product}"
            "&reg=1&regions=68,64,83,4,38,80,33,70,82,86,30,69,22,66,31,40,1,48&resultset=catalog&sort=popular&"
            "spp=22&suppressSpellcheck=false"
    )

    all_products = response.json()["data"]["products"]
    curr_products = all_products[:items_amount]
    data = [{"name": product["name"], "price": f'{product["salePriceU"] / 100:.2f}'} for product in curr_products]
    return data


if __name__ == "__main__":
    main()
