import pandas as pd

try:
    df = pd.read_csv(r'e:/RESUME/resume/Resume.csv')
    print("Unique Categories:")
    print(df['Category'].unique())
except Exception as e:
    print(f"Error reading CSV: {e}")
