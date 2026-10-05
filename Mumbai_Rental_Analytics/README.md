# Mumbai Rental Market Analytics 🏙️

## 📌 Problem Statement
The Mumbai real estate market is notoriously complex, expensive, and opaque. Renters struggle to find fair-priced homes, while property owners and brokers find it difficult to accurately price their listings. 

This project aims to analyze the Mumbai rental market to discover underlying patterns in rental pricing. By processing raw listing data, exploring key features (BHK, Area, Locality, Furnishing), and building interactive dashboards, this project provides actionable insights for renters looking for the best value and owners wanting to optimize rental yields.

## 🗄️ Dataset
The dataset contains ~5,000 realistic rental listings across major Mumbai localities (Bandra, Juhu, Worli, Powai, etc.). It includes:
* **Locality & Geography**: Area name, Latitude, Longitude.
* **Property Specs**: BHK, Property Type, Area (Sqft), Bathrooms, Parking, Floor, Building Age.
* **Pricing**: Monthly Rent.
* **Other**: Furnishing Status, Listing Date.

## 🧹 Data Cleaning (Python / Pandas)
The raw data contained missing values, outliers, inconsistent formatting, and duplicates. The data cleaning process (`data_cleaning.py`) involved:
* **Missing Value Imputation**: Median imputation for rents based on Locality and BHK; Mode imputation for furnishing.
* **Standardization**: Corrected inconsistent locality names (e.g., `bandra west` -> `Bandra West`).
* **Outlier Removal**: Filtered out erroneous data like negative rents and super-extreme values (> ₹1,000,000 rent or > 10,000 sqft area).
* **Deduplication**: Identified and removed exact duplicate listings.
* **Feature Engineering**: Created a new `rent_per_sqft` column for better spatial comparison.

## 🗃️ Database Schema & SQL Analysis
The cleaned dataset is loaded into a **PostgreSQL** database. The table schema includes appropriate data types (NUMERIC, VARCHAR, INT, DATE).

Advanced SQL queries (`mumbai_rentals_sql_analysis.sql`) were written to extract business intelligence, utilizing:
* **CTEs & Window Functions**: `PERCENTILE_CONT` for medians, `ROW_NUMBER()` for top rankings, and `RANK()` for listing density.
* **CASE Statements**: Custom bucketing for affordability categories (Budget, Mid-Range, Luxury).
* **Aggregations & Joins**: Deep-dives into how property types and furnishing status affect average yields.

## 📊 Exploratory Data Analysis (Python)
Performed using `matplotlib` and `seaborn` (`eda.py`). 
* **Distribution Analysis**: Rent is heavily right-skewed, indicative of the extreme luxury segment in South Mumbai.
* **Correlation**: Strong positive correlation (r > 0.8) between Area (sqft) and Monthly Rent, as well as BHK.
* **Categorical Impacts**: Fully furnished properties command a ~15-20% premium over unfurnished properties holding locality constant.

## 📈 Power BI Dashboard
A professional Power BI dashboard was built to allow non-technical stakeholders to explore the data.
**Key Features of the Dashboard:**
* **KPI Cards**: Total Listings, Median Rent, Average Rent, Avg Rent/Sqft.
* **Map Visualization**: Geographic scatter plot of listings using Latitude/Longitude, bubble size representing Rent.
* **Bar Charts**: Average Rent by Locality & Rent by BHK.
* **Donut Chart**: Listing distribution by Furnishing Status.
* **Line Chart**: Trend of average rental pricing over time (Listing Date).

*(Note: Add screenshot of Power BI Dashboard here: `![Power BI Dashboard](link_to_image)`)*

## 💡 Key Insights
1. **Premium Localities**: Malabar Hill, Juhu, and Worli consistently command the highest median rents, often exceeding ₹100,000 per month for standard configurations.
2. **Value for Space**: Borivali West and Goregaon East offer the lowest rent-per-square-foot, making them ideal for renters prioritizing space over proximity to South Mumbai.
3. **Furnishing Premium**: Landlords can expect a 15-22% increase in rental yield by fully furnishing an apartment compared to leaving it unfurnished.
4. **BHK Scaling**: Rent scales linearly from 1 to 3 BHKs, but exhibits exponential jumps for 4+ BHKs, indicating these cater almost exclusively to the luxury market.
5. **Listing Density**: Andheri West and Bandra West have the highest market liquidity (highest number of active listings), meaning more choices but higher competition among landlords.

## 🚀 Recommendations
**For Renters:**
* If working in Central Mumbai (Lower Parel/Worli), look towards Chembur or Powai for better space-to-rent ratios while maintaining reasonable commute times.
* Negotiate harder on unfurnished properties, as the data shows they sit lower on the price curve than semi-furnished ones.

**For Property Owners & Investors:**
* **Capitalize on Furnishing**: The ROI on furnishing a 2BHK in areas like Bandra or Andheri justifies the upfront interior design costs due to the ~20% rent premium.
* **Target Configurations**: 2BHKs represent the "sweet spot" of high demand (liquidity) and stable rental yield. 
* **Pricing Strategy**: Price listings closer to the median of the specific locality/BHK combo rather than the average, as the average is heavily skewed by ultra-luxury outliers in the same zip code.
