import pandas as pd
import numpy as np

def clean_data(input_file, output_file):
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # 1. Handle Duplicates
    initial_shape = df.shape
    df.drop_duplicates(inplace=True)
    print(f"Removed {initial_shape[0] - df.shape[0]} duplicate rows.")
    
    # 2. Inconsistent Locality Names
    locality_mapping = {
        'bandra west': 'Bandra West',
        'Andheri W': 'Andheri West',
        'S. Mumbai - Worli': 'Worli'
    }
    df['locality'] = df['locality'].replace(locality_mapping)
    print("Standardized locality names.")
    
    # 3. Handle Missing Values
    # Missing rent: Impute with median rent of the same locality and BHK
    df['monthly_rent'] = df['monthly_rent'].fillna(df.groupby(['locality', 'bhk'])['monthly_rent'].transform('median'))
    
    # Missing furnishing: Impute with mode (most frequent)
    df['furnishing'] = df['furnishing'].fillna(df['furnishing'].mode()[0])
    
    # Missing building age: Impute with median age
    df['building_age'] = df['building_age'].fillna(df['building_age'].median())
    print("Handled missing values.")
    
    # 4. Incorrect Numeric Values (Negatives)
    # Convert negative rents and areas to positive (assuming typo)
    df['monthly_rent'] = df['monthly_rent'].abs()
    df['area_sqft'] = df['area_sqft'].abs()
    
    # 5. Outliers
    # Remove extremely high rents (> 10,00,000) or extremely high areas (> 10,000 sqft)
    outliers_rent = df[df['monthly_rent'] > 1000000]
    outliers_area = df[df['area_sqft'] > 10000]
    df = df[(df['monthly_rent'] <= 1000000) & (df['area_sqft'] <= 10000)]
    print(f"Removed {len(outliers_rent) + len(outliers_area)} outlier rows.")
    
    # 6. Feature Engineering (Optional but good for portfolio)
    df['rent_per_sqft'] = round(df['monthly_rent'] / df['area_sqft'], 2)
    
    # Save the cleaned dataset
    df.to_csv(output_file, index=False)
    print(f"Cleaned dataset saved to {output_file} with shape {df.shape}")

if __name__ == "__main__":
    clean_data("mumbai_rentals_raw.csv", "mumbai_rentals_cleaned.csv")
