import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Setup
CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)

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

def save_chart(path, plot_func):
    plot_func()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

# Species count
save_chart(f"{CHART_DIR}/species_count.png", lambda: sns.countplot(
    y='Common Name', data=df, order=species_counts.index, palette='viridis').set(title="Number of Observations per Species")
)

# Length distribution
save_chart(f"{CHART_DIR}/length_distribution.png", lambda: sns.histplot(
    df['Observed Length (m)'], bins=15, kde=True, color='skyblue').set(title="Distribution of Observed Length (m)")
)

# Weight by Age Class
save_chart(f"{CHART_DIR}/weight_by_age.png", lambda: sns.boxplot(
    x='Age Class', y='Observed Weight (kg)', data=df, palette='Set2').set(title="Weight Distribution by Age Class")
)

# Conservation status
plt.figure(figsize=(6,6))
plt.pie(conservation_counts, labels=conservation_counts.index, autopct='%1.1f%%', colors=sns.color_palette("Set3"))
plt.title("Conservation Status Distribution")
plt.savefig(f"{CHART_DIR}/conservation_status.png")
plt.close()

# Length vs Weight scatter
save_chart(f"{CHART_DIR}/length_vs_weight.png", lambda: sns.scatterplot(
    x='Observed Length (m)', y='Observed Weight (kg)', hue='Common Name', data=df, palette='tab10').set(title="Length vs Weight by Species")
)

# Observations over time
obs_per_year = df.set_index('Date of Observation').resample('Y')['Observation ID'].count()
plt.figure(figsize=(10,6))
obs_per_year.plot(marker='o')
plt.title("Observations Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Observations")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/observations_over_time.png")
plt.close()