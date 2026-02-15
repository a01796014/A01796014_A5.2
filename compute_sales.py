#!/usr/bin/env python3
"""
computeSales.py

Computes total sales cost based on a price catalogue and a sales record.
Outputs results to console and SalesResults.txt.
"""

import json
import sys
import time
from typing import Dict, List, Any


RESULT_FILE = "SalesResults.txt"


def load_json_file(filename: str) -> Any:
    """
    Load a JSON file safely.

    :param filename: Path to JSON file
    :return: Parsed JSON content
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"ERROR: File '{filename}' contains invalid JSON.")
    except OSError as exc:
        print(f"ERROR: Cannot open file '{filename}': {exc}")
    return None


def build_price_dict(price_data: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Convert price catalogue list into dictionary for fast lookup.

    :param price_data: List of product price records
    :return: Dictionary mapping product to price
    """
    price_dict = {}
    for entry in price_data:
        try:
            product = entry["product"]
            price = float(entry["price"])
            price_dict[product] = price
        except (KeyError, ValueError, TypeError):
            print(f"WARNING: Invalid price entry skipped: {entry}")
    return price_dict


def compute_total_sales(
    sales_data: List[Dict[str, Any]],
    price_dict: Dict[str, float]
) -> float:
    """
    Compute total sales value.

    :param sales_data: List of sales records
    :param price_dict: Product-to-price mapping
    :return: Total sales cost
    """
    total = 0.0

    for sale in sales_data:
        items = sale.get("items", [])
        if not isinstance(items, list):
            print(f"WARNING: Invalid items format in sale: {sale}")
            continue

        for item in items:
            try:
                product = item["product"]
                quantity = float(item["quantity"])

                if product not in price_dict:
                    print(f"WARNING: Product '{product}' not in catalogue.")
                    continue

                total += price_dict[product] * quantity

            except (KeyError, ValueError, TypeError):
                print(f"WARNING: Invalid sale item skipped: {item}")

    return total


def write_results(output: str) -> None:
    """
    Write results to output file.

    :param output: Formatted output string
    """
    try:
        with open(RESULT_FILE, "w", encoding="utf-8") as file:
            file.write(output)
    except OSError as exc:
        print(f"ERROR: Could not write results file: {exc}")


def main() -> None:
    """
    Main execution function.
    """
    if len(sys.argv) != 3:
        print(
            "Usage: python computeSales.py priceCatalogue.json "
            "salesRecord.json"
        )
        sys.exit(1)

    start_time = time.time()

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    price_data = load_json_file(price_file)
    sales_data = load_json_file(sales_file)

    if price_data is None or sales_data is None:
        sys.exit(1)

    price_dict = build_price_dict(price_data)
    total_sales = compute_total_sales(sales_data, price_dict)

    elapsed_time = time.time() - start_time

    output = (
        "\n===== SALES SUMMARY =====\n"
        f"Total Sales: ${total_sales:,.2f}\n"
        f"Execution Time: {elapsed_time:.6f} seconds\n"
        "=========================\n"
    )

    print(output)
    write_results(output)


if __name__ == "__main__":
    main()
