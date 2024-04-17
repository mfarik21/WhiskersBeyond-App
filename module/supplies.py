from enum import Enum
from textwrap import dedent
from typing import Dict

from tabulate import tabulate

from services import supplies
from utils.helper import (
    cast_to_int,
    format_currency,
    get_index,
    get_int_input,
    is_valid_choice,
)
from utils.interface import clear_screen, show_title

basket = list()


class SuppliesChoice(Enum):
    ADD_NEW = 1
    REMOVE = 2
    CLEAR = 3
    PROCEED = 0


def module():
    err_msg = ""

    while True:
        clear_screen()
        show_title("Pet Supplies")

        if err_msg:
            print(err_msg)

        if basket:
            display_basket()

        print(
            dedent(
                """
            Options:
            1. Add new items to basket
            2. Remove an item from basket
            3. Clear basket
            0. Proceed and back to Home 
        """
            )
        )

        choice = input("Enter the number corresponding to your choice: ")
        choice = cast_to_int(choice)

        if is_valid_choice(choice, SuppliesChoice):

            if SuppliesChoice(choice) == SuppliesChoice.ADD_NEW:
                show_catalog()
                choice = get_int_input(
                    "Enter the product number you'd like: ", len(supplies)
                )

                qty = get_int_input("Enter the quantity you'd like: ")

                idx = get_index(choice)

                is_sufficient, avail_stock = check_stock_availability(idx, qty)
                if is_sufficient:
                    item = dict(supplies[idx], qty=qty)
                    add_to_basket(item)
                else:
                    err_msg = f"Insufficient stock for item {idx}. Available quantity: {avail_stock}"

            elif SuppliesChoice(choice) == SuppliesChoice.REMOVE:
                num = get_int_input(
                    "Enter the basket number of the item you want to remove: ",
                    len(basket),
                )
                idx = get_index(num)
                remove_from_basket(idx)

            elif SuppliesChoice(choice) == SuppliesChoice.CLEAR:
                option = input("Are you sure you want to clear your basket: (Y/N)?")
                if option.upper() == "Y":
                    clear_basket()

            elif SuppliesChoice(choice) == SuppliesChoice.PROCEED:
                break

        else:
            print("Invalid choice! Please select a valid option.")


def show_catalog():
    headers = [
        "#",
        "Product Name",
        "Category",
        "Subcategory",
        "Type",
        "Size",
        "Price",
    ]
    formatted_data = [
        [
            idx,
            item["name"],
            item["category"],
            item["sub_category"],
            item["type"],
            item["size"],
            format_currency(item["price"]),
        ]
        for idx, item in enumerate(supplies, start=1)
    ]

    print(tabulate(formatted_data, headers=headers, tablefmt="simple_outline"))


def display_basket():
    headers = ["#", "Product Name", "Qty", "Unit Price", "Subtotal"]
    formatted_data = [
        [idx, item["name"], item["qty"], item["price"], item["qty"] * item["price"]]
        for idx, item in enumerate(basket, start=1)
    ]

    print()
    print(tabulate(formatted_data, headers=headers, tablefmt="simple_outline"))


def check_stock_availability(idx, qty):
    if idx >= 0 and idx <= len(supplies):
        available_stock = supplies[idx].get("stock")
        return (available_stock >= qty, available_stock)


def get_basket():
    return basket


def add_to_basket(item: Dict):
    # Handling adding item that already exists
    list_item = [item["name"] for item in basket]
    if item["name"] in list_item:
        for cart_item in basket:
            if cart_item["name"] == item["name"]:
                cart_item["qty"] += item["qty"]
                return

    basket.append(item)


def remove_from_basket(idx: int):
    del basket[idx]


def clear_basket():
    basket.clear()