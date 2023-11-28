import json
import pandas as pd

data = json.load(open('Woo-Contactpersonen.json'))

df_data = [contact['infobox']['foi_dossiers']['0'] for contact in data]
df = pd.DataFrame(df_data)

for column in df.columns:
    print(column, df[df[column] != ''][column].count() / len(df) * 100)
