import pandas as pd
import anthropic
import os

# 1. Load and Analyze Data with Pandas
df = pd.read_csv('sales_data.csv')
total_revenue = df['Revenue'].sum()
top_product = df.loc[df['Units_Sold'].idxmax()]['Product']
top_category = df.groupby('Category')['Revenue'].sum().idxmax()

# 2. Prepare the Summary for Claude
stats_summary = f"""
Total Revenue: ${total_revenue}
Top Selling Product: {top_product}
Highest Revenue Category: {top_category}
"""

# 3. Connect to Anthropic
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    temperature=0,
    system="You are a Senior Retail Analyst. Convert the provided sales data into a professional 3-sentence executive summary for a Store Manager.",
    messages=[
        {"role": "user", "content": f"Here are today's sales stats: {stats_summary}"}
    ]
)

print("\n--- AI GENERATED SALES INSIGHTS ---")
print(message.content[0].text)