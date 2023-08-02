import csv


def read_csv() -> list[dict]:
    general_data = []
    with open("sales_data.csv", "r", newline="\n") as sales_file:
        reader = csv.DictReader(sales_file)
        for row in reader:
            general_data.append(row)

    return general_data


data = read_csv()

total_transactions = len(data)
total_revenue = sum(int(item["amount"]) for item in data)
avg_transaction_amount = total_revenue / total_transactions

transactions_per_category = {}

for item in data:
    category = item["product_category"]
    transactions_per_category[category] = transactions_per_category.get(category, 0) + 1

if __name__ == "__main__":
    print("Total number of transactions:", total_transactions)
    print("Total revenue:", total_revenue)
    print("Average transaction amount:", avg_transaction_amount)
    print("\nNumber of transactions per product category:")
    for category, num_transactions in transactions_per_category.items():
        print(category, num_transactions)



