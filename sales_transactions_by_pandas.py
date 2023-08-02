import pandas as pd

df = pd.read_csv('sales_data.csv')

total_transactions_number = df['transaction_id'].nunique()
total_revenue = df['amount'].sum()
avg_transaction_amount = df['amount'].mean()
transactions_per_category = df.groupby('product_category')['transaction_id'].nunique().reset_index()

if __name__ == "__main__":
    print("\nTotal number of transactions:", total_transactions_number)
    print("Total revenue:", total_revenue)
    print("Average transaction amount:", avg_transaction_amount)
    print("\nNumber of transactions per product category:")
    print(f"{transactions_per_category}\n")
