import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for plots
sns.set_theme(style="whitegrid")

def run_eda(file_path):
    print("Loading cleaned dataset...")
    df = pd.read_csv(file_path)
    
    # Ensure date column is datetime
    df['listing_date'] = pd.to_datetime(df['listing_date'])
    
    # 1. Distribution of Monthly Rent
    plt.figure(figsize=(10, 6))
    sns.histplot(df['monthly_rent'], bins=50, kde=True, color='blue')
    plt.title("Distribution of Monthly Rent in Mumbai")
    plt.xlabel("Monthly Rent (INR)")
    plt.ylabel("Frequency")
    plt.savefig("rent_distribution.png")
    plt.close()
    
    # 2. Average Rent by Locality
    plt.figure(figsize=(12, 6))
    avg_rent = df.groupby('locality')['monthly_rent'].mean().sort_values(ascending=False)
    sns.barplot(x=avg_rent.index, y=avg_rent.values, palette='viridis')
    plt.title("Average Monthly Rent by Locality")
    plt.xticks(rotation=45)
    plt.ylabel("Average Rent (INR)")
    plt.tight_layout()
    plt.savefig("avg_rent_locality.png")
    plt.close()
    
    # 3. Rent vs. Area (Scatter Plot)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='area_sqft', y='monthly_rent', hue='bhk', palette='deep', alpha=0.6)
    plt.title("Rent vs. Area (sqft) by BHK")
    plt.xlabel("Area (sqft)")
    plt.ylabel("Monthly Rent (INR)")
    plt.savefig("rent_vs_area.png")
    plt.close()
    
    # 4. Boxplot of Rent by Furnishing Status
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x='furnishing', y='monthly_rent', palette='Set2')
    plt.title("Rent Distribution by Furnishing Status")
    plt.xlabel("Furnishing Status")
    plt.ylabel("Monthly Rent (INR)")
    plt.savefig("rent_by_furnishing.png")
    plt.close()
    
    # 5. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    # Select only numeric columns
    numeric_cols = df.select_dtypes(include=['number'])
    corr = numeric_cols.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title("Correlation Heatmap of Numeric Variables")
    plt.tight_layout()
    plt.savefig("correlation_heatmap.png")
    plt.close()

    print("EDA completed successfully. Visualizations saved as PNG files.")

if __name__ == "__main__":
    run_eda("mumbai_rentals_cleaned.csv")
