import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from fpdf import FPDF

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

# Generate PDF Report
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, "Crocodile Dataset Report", ln=True, align="C")

pdf.ln(10)

# Narrative text
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, f"This report analyzes {len(df)} crocodile observations from {df['Country/Region'].nunique()} regions and {df['Common Name'].nunique()} species.")
pdf.ln(5)
pdf.multi_cell(0, 10, f"The most observed species is {species_counts.idxmax()} with {species_counts.max()} records.")
pdf.multi_cell(0, 10, f"The largest crocodile recorded is a {longest['Common Name']} measuring {longest['Observed Length (m)']} m.")
pdf.multi_cell(0, 10, f"The heaviest crocodile recorded is a {heaviest['Common Name']} weighing {heaviest['Observed Weight (kg)']} kg.")
pdf.multi_cell(0, 10, f"The most common habitat is {common_habitat}, while the country with the most observations is {common_country}.")
pdf.multi_cell(0, 10, f"Conservation status shows {conservation_counts.idxmax()} is the most frequent category in the dataset.")

# Add Summary Table
pdf.ln(10)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, "Summary Table: Length & Weight (per Species)", ln=True)

pdf.set_font("Arial", size=10)
col_names = ["Species", "Mean L (m)", "Max L (m)", "Min L (m)", "Mean W (kg)", "Max W (kg)", "Min W (kg)"]
col_widths = [50, 20, 20, 20, 25, 25, 25]

# Header
for col_name, width in zip(col_names, col_widths):
    pdf.cell(width, 10, col_name, border=1, align="C")
pdf.ln()

# Rows
for species, row in summary.iterrows():
    pdf.cell(col_widths[0], 10, str(species)[:30], border=1)  # truncate if too long
    pdf.cell(col_widths[1], 10, f"{row[('Observed Length (m)','mean')]:.2f}", border=1, align="C")
    pdf.cell(col_widths[2], 10, f"{row[('Observed Length (m)','max')]:.2f}", border=1, align="C")
    pdf.cell(col_widths[3], 10, f"{row[('Observed Length (m)','min')]:.2f}", border=1, align="C")
    pdf.cell(col_widths[4], 10, f"{row[('Observed Weight (kg)','mean')]:.2f}", border=1, align="C")
    pdf.cell(col_widths[5], 10, f"{row[('Observed Weight (kg)','max')]:.2f}", border=1, align="C")
    pdf.cell(col_widths[6], 10, f"{row[('Observed Weight (kg)','min')]:.2f}", border=1, align="C")
    pdf.ln()


# Insert Charts
pdf.ln(10)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, "Charts & Visualizations", ln=True)

charts = [
    "species_count.png",
    "length_distribution.png",
    "weight_by_age.png",
    "conservation_status.png",
    "length_vs_weight.png",
    "observations_over_time.png"
]

for chart in charts:
    pdf.image(f"{CHART_DIR}/{chart}", w=170)
    pdf.ln(10)

# Save PDF
pdf.output("crocodile_report.pdf")

print("✅ Report generated: crocodile_report.pdf (with text, tables, and charts)")
print(f"📂 Charts saved in: {CHART_DIR}/")