import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

# Set seaborn style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

# Load data
df = pd.read_csv('data/main_dataset.csv')

# 1. CORRELATION SCATTER PLOT
clean_data = df[['birth_rate_per_1000', 'Monthlyavgpm2.5']].dropna()
r, p = pearsonr(clean_data['birth_rate_per_1000'], clean_data['Monthlyavgpm2.5'])

plt.figure(figsize=(10, 8))
sns.regplot(data=clean_data, x='Monthlyavgpm2.5', y='birth_rate_per_1000', 
            scatter_kws={'alpha': 0.6, 's': 30, 'color': '#3498db'},
            line_kws={'color': '#e74c3c', 'linewidth': 2.5})
plt.xlabel('PM2.5 (μg/m³)', fontsize=12, fontweight='bold')
plt.ylabel('Birth Rate per 1,000', fontsize=12, fontweight='bold')
plt.title(f'Pollution vs Birth Rate\nCorrelation: r = {r:.3f}, p < 0.001', 
          fontsize=14, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)
plt.savefig('outputs/correlation_scatter.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 2. PRETERM BIRTH COMPARISON: HIGH POLLUTION vs COASTAL COUNTIES
# Load preterm birth data
preterm = pd.read_csv('data/Data-Preterm-Birth.csv')
preterm.columns = ['indicator', 'geography', 'year', 'category', 'subcategory', 
                   'numerator', 'denominator', 'percent', 'lower_ci', 'upper_ci']

# Clean and filter preterm data
preterm_ca = preterm[(preterm['geography'] != 'United States') & 
                     (preterm['geography'] != 'California') &
                     (preterm['category'] == 'Total Population') &
                     (~preterm['year'].astype(str).str.contains('-'))].copy()

preterm_ca['Year'] = preterm_ca['year'].astype(int)
preterm_ca['County'] = preterm_ca['geography']

# Merge with main data
county_year = df.groupby(['County', 'Year']).agg({
    'Monthlyavgpm2.5': 'mean',
    'birth_rate_per_1000': 'mean',
    'Population': 'mean'
}).reset_index()

merged_preterm = county_year.merge(
    preterm_ca[['County', 'Year', 'percent']], 
    on=['County', 'Year'], 
    how='inner'
).rename(columns={'percent': 'preterm_percent'})

# Remove zeros and get county averages
merged_preterm = merged_preterm[merged_preterm['preterm_percent'] > 0]
county_preterm_avg = merged_preterm.groupby('County').agg({
    'Monthlyavgpm2.5': 'mean',
    'preterm_percent': 'mean',
    'Population': 'mean'
}).reset_index()

# Define high pollution and coastal counties
high_pollution_counties = ['Los Angeles', 'Fresno', 'Kern', 'San Bernardino', 'Riverside', 'Madera', 'Tulare']
coastal_counties = ['Monterey', 'Santa Cruz', 'Santa Barbara', 'Ventura', 'San Francisco', 'Marin', 'San Mateo']

# Filter data
high_poll_data = county_preterm_avg[county_preterm_avg['County'].isin(high_pollution_counties)]
coastal_data = county_preterm_avg[county_preterm_avg['County'].isin(coastal_counties)]

# Create the comparison visualization
fig, ax = plt.subplots(1, 1, figsize=(14, 10))

# High pollution counties (red)
ax.scatter(high_poll_data['Monthlyavgpm2.5'], high_poll_data['preterm_percent'], 
          s=400, c='#e74c3c', edgecolor='black', linewidth=2, 
          label='High Pollution Counties', alpha=0.8, zorder=3)

# Coastal counties (blue)
ax.scatter(coastal_data['Monthlyavgpm2.5'], coastal_data['preterm_percent'], 
          s=400, c='#3498db', edgecolor='black', linewidth=2, 
          label='Coastal Counties', alpha=0.8, zorder=3)

# Add county labels with better positioning to avoid overlap
# High pollution counties - position labels to avoid overlap
high_poll_positions = {
    'Fresno': (15, 5), 'Kern': (15, -5), 'San Bernardino': (15, 5), 
    'Tulare': (15, 5), 'Los Angeles': (15, -5), 'Riverside': (15, 5), 'Madera': (15, -5)
}

for _, row in high_poll_data.iterrows():
    offset = high_poll_positions.get(row['County'], (8, 8))
    ax.annotate(row['County'], (row['Monthlyavgpm2.5'], row['preterm_percent']), 
                xytext=offset, textcoords='offset points', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9, edgecolor='#e74c3c'))

# Coastal counties - position labels to avoid overlap
coastal_positions = {
    'San Francisco': (15, 5), 'San Mateo': (15, -5), 'Santa Barbara': (15, 5),
    'Ventura': (15, -5), 'Monterey': (15, 5), 'Santa Cruz': (15, -5), 'Marin': (15, 5)
}

# Special positioning for overlapping coastal counties
coastal_special_positions = {
    'Santa Barbara': (-35, 12), # Move much further to the left and up
    'San Mateo': (25, -12),     # Move much further right and down  
    'San Francisco': (20, 8)    # Move further right and up
}

for _, row in coastal_data.iterrows():
    # Use special positioning for overlapping counties, otherwise use regular positioning
    offset = coastal_special_positions.get(row['County'], coastal_positions.get(row['County'], (8, 8)))
    ax.annotate(row['County'], (row['Monthlyavgpm2.5'], row['preterm_percent']), 
                xytext=offset, textcoords='offset points', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9, edgecolor='#3498db'))

# Calculate and display statistics
high_poll_avg_pm25 = high_poll_data['Monthlyavgpm2.5'].mean()
high_poll_avg_preterm = high_poll_data['preterm_percent'].mean()
coastal_avg_pm25 = coastal_data['Monthlyavgpm2.5'].mean()
coastal_avg_preterm = coastal_data['preterm_percent'].mean()

# Add statistics text box
stats_text = f"""HIGH POLLUTION COUNTIES:
PM2.5: {high_poll_avg_pm25:.1f} μg/m³
Preterm: {high_poll_avg_preterm:.2f}%

COASTAL COUNTIES:
PM2.5: {coastal_avg_pm25:.1f} μg/m³
Preterm: {coastal_avg_preterm:.2f}%

DIFFERENCE:
+{high_poll_avg_pm25 - coastal_avg_pm25:.1f} μg/m³ PM2.5
+{high_poll_avg_preterm - coastal_avg_preterm:.2f}% preterm births"""

ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=11, fontweight='bold',
        verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='black'))

# Styling
ax.set_xlabel('PM2.5 (μg/m³)', fontsize=14, fontweight='bold')
ax.set_ylabel('Preterm Birth %', fontsize=14, fontweight='bold')
ax.set_title('Air Pollution vs Preterm Births: High Pollution vs Coastal Counties\nCalifornia Counties (2007-2023)', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='lower right', frameon=True, fancybox=True, shadow=True, 
          borderpad=1, labelspacing=1.5, handletextpad=0.8)
ax.grid(True, alpha=0.3)

# Set better scaling to show both groups clearly
ax.set_xlim(5, 17)  # Show full range from coastal to high pollution
ax.set_ylim(7, 10)  # Show preterm range clearly

plt.tight_layout()
plt.savefig('outputs/preterm_air_quality_by_county.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()