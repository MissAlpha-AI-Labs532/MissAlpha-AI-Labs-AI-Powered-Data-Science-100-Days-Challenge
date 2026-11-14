# ShopIntel 360 – Flipkart E-commerce Analytics Dashboard

## Project Overview
ShopIntel 360 is a Tableau project focused on analyzing e-commerce orders, customers, products, and regional performance. The dashboard provides a consolidated view of sales activity and helps stakeholders understand what is selling, where orders are coming from, and how customer and product segments contribute to business results.

**Project type:** E-commerce / Sales Analytics  
**Tool:** Tableau  
**Status:** Tableau dashboard completed

## Business Problem
E-commerce businesses generate large volumes of order data. When order, customer, product, and regional information is reviewed separately, it becomes harder to monitor sales performance, compare product groups, identify valuable customer segments, and spot regional differences.

## Project Objectives
- Analyze overall order and sales performance.
- Compare product and category performance.
- Understand customer purchasing patterns.
- Compare sales and orders across regions.
- Track performance over time and identify trends.

## Dataset Files
| File | Purpose |
|---|---|
| `Orders_Fact.csv` | Main order and transaction records |
| `Customers_Dim.csv` | Customer attributes |
| `Products_Dim.csv` | Product attributes and classifications |
| `Regions_Dim.csv` | Regional lookup |
| `Date_Dim.csv` | Calendar attributes for trend analysis |

## Tools and Concepts
- Tableau Desktop: data connections, data model, calculated fields, charts, dashboard actions, filters, and formatting.
- Analytics concepts: sales KPIs, order counts, customer analysis, product mix, geographic comparison, and time-series analysis.
- Example KPIs to validate against available fields: total sales/revenue, total orders, average order value, customer count, and product/category contribution.

## Dashboard Analysis
1. **Executive overview** – headline sales and order indicators.
2. **Product analysis** – compare products or product categories.
3. **Customer analysis** – explore customer-level or customer-segment patterns where supported by the data.
4. **Regional analysis** – compare performance across available regions.
5. **Time analysis** – review sales and order trends over calendar periods.

## Tableau Workflow
1. Open the `.twb` workbook in Tableau Desktop.
2. Reconnect the CSV files if the original file paths are no longer valid.
3. Check the relationship between `Orders_Fact` and the customer, product, region, and date dimensions.
4. Confirm that transaction dates and numeric fields have the correct data types.
5. Validate calculated measures and aggregation levels.
6. Review worksheets, sorting, labels, and filter behavior.
7. Test dashboard filters and actions across all views.
8. Compare headline KPI totals with the underlying CSV data and save the workbook.

## Key Deliverables
- Tableau workbook: `ShopIntel 360 Flipkart Ecommerce.twb`
- Order, customer, product, region, and date CSV datasets
- Interactive Flipkart e-commerce analytics dashboard

## Insights and Recommendations
Use product and category comparisons to identify sales contributors and areas that may need attention. Compare regions before making location-specific decisions. Review customer patterns alongside order trends to inform retention and merchandising strategies.

## Project Outcome
The dashboard transforms transaction and dimension data into an interactive view of e-commerce performance, supporting sales monitoring and business decision-making.

## Author
Add your name, course/internship details, and project date here.
