# FoodPulse 360 – Zomato-Style Restaurant & Food Delivery Analytics Dashboard

## Project Overview
FoodPulse 360 is a Tableau project that analyzes restaurant and food-order data. It combines order, customer, restaurant, and date information to help explore order activity, restaurant performance, customer patterns, and trends over time.

**Project type:** Food Delivery / Restaurant Analytics  
**Tool:** Tableau  
**Status:** Tableau dashboard completed

## Business Problem
Food delivery platforms handle orders across many restaurants and customers. Without a unified dashboard, it can be difficult to monitor order volume, compare restaurant performance, understand customer activity, and identify changes in demand over time.

## Project Objectives
- Analyze overall food-order activity.
- Compare restaurant performance using available order measures.
- Explore customer ordering patterns.
- Track order trends over time.
- Present the results in an interactive dashboard to support operational and business decisions.

## Dataset Files
| File | Purpose |
|---|---|
| `Food_Orders_Fact.csv` | Main food-order and transaction records |
| `Customers_Dim.csv` | Customer attributes |
| `Restaurants_Dim.csv` | Restaurant attributes |
| `Date_Dim.csv` | Calendar attributes for trend analysis |

## Tools and Concepts
- Tableau Desktop: CSV connections, data relationships, calculated fields, KPI cards, charts, dashboard filters, and actions.
- Analytics concepts: order analysis, restaurant comparison, customer analysis, time-series analysis, and KPI reporting.
- Potential KPIs include total orders, order value/revenue, average order value, customer count, and restaurant contribution where corresponding fields exist in the dataset.

## Dashboard Analysis
1. **Business overview** – summarize key food-order indicators.
2. **Restaurant analysis** – compare restaurants using order and value measures available in the data.
3. **Customer analysis** – explore customer ordering patterns and contributions.
4. **Time analysis** – track order activity across dates and calendar periods.
5. **Interactive filtering** – investigate selected restaurants, customers, and periods.

## Tableau Workflow
1. Open `FoodPulse 360 Zomato Food Delivery.twb` in Tableau Desktop.
2. Reconnect the four CSV files if their original paths are unavailable.
3. Confirm relationships between `Food_Orders_Fact` and the customer, restaurant, and date dimensions.
4. Verify date, identifier, and numeric field types.
5. Review calculations for order counts, revenue/order value, and averages; ensure the aggregation level is appropriate.
6. Inspect worksheets, labels, sorting, and filter settings.
7. Test dashboard interactions and confirm that all views update as expected.
8. Reconcile headline figures with the source data and save the workbook.

## Key Deliverables
- Tableau workbook: `FoodPulse 360 Zomato Food Delivery.twb`
- Food order, customer, restaurant, and date CSV datasets
- Interactive restaurant and food delivery analytics dashboard

## Insights and Recommendations
Use restaurant comparisons to identify strong contributors and areas that may need operational review. Examine order trends to understand demand patterns and compare customer activity across consistent periods. Validate findings with the underlying data before making business decisions.

## Project Outcome
The Tableau dashboard consolidates food delivery data into an interactive view of order, restaurant, customer, and time-based performance.

## Author
Add your name, course/internship details, and project date here.
