-- ==========================================================
-- PostgreSQL Database Setup & Data Loading
-- ==========================================================

-- 1. Create the table
CREATE TABLE IF NOT EXISTS mumbai_rentals (
    id INT PRIMARY KEY,
    locality VARCHAR(100),
    monthly_rent NUMERIC,
    property_type VARCHAR(50),
    bhk INT,
    area_sqft NUMERIC,
    furnishing VARCHAR(50),
    bathrooms INT,
    parking INT,
    floor INT,
    building_age NUMERIC,
    latitude NUMERIC,
    longitude NUMERIC,
    listing_date DATE,
    rent_per_sqft NUMERIC
);

-- 2. Load the data (Adjust the file path based on your system)
-- COPY mumbai_rentals FROM '/path/to/mumbai_rentals_cleaned.csv' DELIMITER ',' CSV HEADER;


-- ==========================================================
-- Advanced SQL Analysis (Answering Business Questions)
-- ==========================================================

-- Q1. Which Mumbai localities have the highest median rent? (Using CTE and percentile window function)
WITH LocalityRents AS (
    SELECT 
        locality,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monthly_rent) AS median_rent
    FROM mumbai_rentals
    GROUP BY locality
)
SELECT 
    locality,
    ROUND(median_rent::numeric, 2) AS median_rent
FROM LocalityRents
ORDER BY median_rent DESC
LIMIT 5;

-- Q2. Which localities provide the most space for the rent? (Best value for money)
SELECT 
    locality,
    ROUND(AVG(area_sqft), 2) AS avg_area,
    ROUND(AVG(monthly_rent), 2) AS avg_rent,
    ROUND(AVG(monthly_rent)/AVG(area_sqft), 2) AS avg_rent_per_sqft
FROM mumbai_rentals
GROUP BY locality
ORDER BY avg_rent_per_sqft ASC;

-- Q3. How does rent change with BHK?
SELECT 
    bhk,
    COUNT(*) AS total_listings,
    ROUND(AVG(monthly_rent), 2) AS avg_monthly_rent,
    ROUND(MIN(monthly_rent), 2) AS min_rent,
    ROUND(MAX(monthly_rent), 2) AS max_rent
FROM mumbai_rentals
GROUP BY bhk
ORDER BY bhk;

-- Q4. How does furnishing affect rent across different property types? (Using CASE and aggregates)
SELECT 
    property_type,
    ROUND(AVG(CASE WHEN furnishing = 'Fully Furnished' THEN monthly_rent END), 2) AS avg_rent_fully_furnished,
    ROUND(AVG(CASE WHEN furnishing = 'Semi-Furnished' THEN monthly_rent END), 2) AS avg_rent_semi_furnished,
    ROUND(AVG(CASE WHEN furnishing = 'Unfurnished' THEN monthly_rent END), 2) AS avg_rent_unfurnished
FROM mumbai_rentals
GROUP BY property_type
ORDER BY avg_rent_fully_furnished DESC;

-- Q5. Which areas have the highest number of listings and rank them? (Using Window Functions)
SELECT 
    locality,
    COUNT(*) AS listing_count,
    RANK() OVER(ORDER BY COUNT(*) DESC) AS listing_rank
FROM mumbai_rentals
GROUP BY locality;

-- Q6. How has rental pricing changed over time? (Using Date Functions)
SELECT 
    DATE_TRUNC('month', listing_date) AS listing_month,
    COUNT(*) AS new_listings,
    ROUND(AVG(monthly_rent), 2) AS avg_rent
FROM mumbai_rentals
GROUP BY listing_month
ORDER BY listing_month;

-- Q7. What are the top 3 most expensive listings in each locality? (Using ROW_NUMBER)
WITH RankedListings AS (
    SELECT 
        locality,
        property_type,
        bhk,
        monthly_rent,
        ROW_NUMBER() OVER(PARTITION BY locality ORDER BY monthly_rent DESC) as rn
    FROM mumbai_rentals
)
SELECT * 
FROM RankedListings 
WHERE rn <= 3;

-- Q8. Categorize properties by affordability (Using CASE Statement)
SELECT 
    id,
    locality,
    monthly_rent,
    CASE 
        WHEN monthly_rent < 40000 THEN 'Budget'
        WHEN monthly_rent BETWEEN 40000 AND 100000 THEN 'Mid-Range'
        ELSE 'Luxury'
    END AS affordability_category
FROM mumbai_rentals
LIMIT 20;
