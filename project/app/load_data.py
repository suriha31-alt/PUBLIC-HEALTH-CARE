import pandas as pd
from mongodb import collection

df = pd.read_csv("healthcare.csv")

data = df.to_dict("records")
collection.insert_many(data)

print("Data inserted!")