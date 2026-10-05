# Power BI Dashboard Creation Guide

To complete the portfolio project, you will build the dashboard in Power BI. Follow these exact steps to create a professional-grade dashboard.

## 1. Import Data
1. Open Power BI Desktop.
2. Click **Get Data** -> **Text/CSV**.
3. Select `mumbai_rentals_cleaned.csv`.
4. Click **Transform Data** to open Power Query. Ensure data types are correct (e.g., `monthly_rent` is Whole Number, `listing_date` is Date, `latitude`/`longitude` are Decimal Numbers).
5. Click **Close & Apply**.

## 2. Create Measures (DAX)
Create a dedicated "Measures" table (Enter Data -> name it `_Measures`). Create the following DAX measures:
* `Total Listings = COUNTROWS('mumbai_rentals')`
* `Average Rent = AVERAGE('mumbai_rentals'[monthly_rent])`
* `Median Rent = MEDIAN('mumbai_rentals'[monthly_rent])`
* `Avg Rent per Sqft = AVERAGE('mumbai_rentals'[rent_per_sqft])`

## 3. Build the Visualizations

### A. Top KPI Ribbon (Cards)
Place 4 **Card** visuals at the top of your canvas for quick insights:
* Total Listings
* Median Rent (Format as Currency: ₹)
* Average Rent (Format as Currency: ₹)
* Avg Rent per Sqft (Format as Currency: ₹)

### B. Map Visualization
* **Visual Type**: Map (or Azure Map)
* **Latitude**: `latitude`
* **Longitude**: `longitude`
* **Bubble Size**: `Average Rent`
* **Tooltip**: `locality`, `Total Listings`
* *Purpose*: Shows the geographical spread and pricing heat across Mumbai.

### C. Bar Charts
1. **Average Rent by Locality**
   * **Visual**: Clustered Bar Chart
   * **Y-Axis**: `locality`
   * **X-Axis**: `Average Rent`
   * Sort by Average Rent descending.

2. **Rent by BHK**
   * **Visual**: Column Chart
   * **X-Axis**: `bhk`
   * **Y-Axis**: `Average Rent`

### D. Donut Chart
* **Visual**: Donut Chart
* **Legend**: `furnishing`
* **Values**: `Total Listings` (or `Average Rent` to show price share)
* *Purpose*: Shows the distribution of furnishing statuses in the market.

### E. Line Chart (Rent Trends)
* **Visual**: Line Chart
* **X-Axis**: `listing_date` (Hierarchy: Year, Month)
* **Y-Axis**: `Average Rent`
* *Purpose*: Track how rental pricing changed over the months in the dataset.

## 4. Add Slicers for Interactivity
Add **Slicer** visuals on the left or top panel so users can filter the dashboard:
* **Locality Slicer**: Dropdown list of localities.
* **BHK Slicer**: Checkboxes for 1, 2, 3, 4, 5 BHK.
* **Property Type Slicer**: Dropdown for Apartment, Villa, etc.

## 5. Formatting & Polish
* **Theme**: Go to *View -> Themes* and select a clean, professional theme (e.g., Executive or Innovate).
* **Titles**: Ensure all charts have clean, readable titles (e.g., "Median Rent by Locality" instead of "Sum of monthly_rent by locality").
* **Background**: Add a subtle light grey background to the page, and make the chart backgrounds white with a slight shadow for a modern web-app look.
