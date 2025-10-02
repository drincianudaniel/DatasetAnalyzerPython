import pandas as pd

# Load Dataset
df = pd.read_csv("crocodile_dataset.csv")
df['Date of Observation'] = pd.to_datetime(df['Date of Observation'], dayfirst=True)

# Generate Insights
species_counts = df['Common Name'].value_counts()
avg_stats = df.groupby('Common Name')[['Observed Length (m)', 'Observed Weight (kg)']].mean()
conservation_counts = df['Conservation Status'].value_counts()

heaviest = df.loc[df['Observed Weight (kg)'].idxmax()]
longest = df.loc[df['Observed Length (m)'].idxmax()]
common_habitat = df['Habitat Type'].value_counts().idxmax()
common_country = df['Country/Region'].value_counts().idxmax()

# Save numeric summary to CSV
summary = df.groupby('Common Name')[['Observed Length (m)', 'Observed Weight (kg)']].agg(['mean','max','min'])
summary.to_csv("crocodile_summary.csv")

