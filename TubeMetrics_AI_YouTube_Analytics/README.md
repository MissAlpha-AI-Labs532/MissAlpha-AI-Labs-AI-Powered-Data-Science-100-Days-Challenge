# TubeMetrics AI – YouTube Analytics Dashboard

## Project Overview
TubeMetrics AI is a Tableau analytics project for exploring YouTube video performance, traffic sources, formats, categories, and publishing trends. It helps creators and channel teams understand how videos perform and how viewers discover content.

**Project type:** Video / Digital Content Analytics  
**Tool:** Tableau  
**Status:** Tableau dashboard completed

## Business Problem
A channel may publish videos across different categories and formats while receiving views from several traffic sources. Reviewing these measures independently makes it difficult to understand content performance, compare formats, and identify discovery channels that contribute to views.

## Project Objectives
- Monitor video performance using the measures available in the dataset.
- Compare performance across video categories and formats.
- Analyze traffic-source contribution.
- Track video performance over time.
- Identify content patterns that can inform channel strategy.

## Dataset Files
| File | Purpose |
|---|---|
| `Video_Performance_Fact.csv` | Main video performance records |
| `Video_Categories_Dim.csv` | Video category lookup |
| `Video_Formats_Dim.csv` | Video format lookup |
| `Traffic_Sources_Dim.csv` | Traffic source lookup |
| `Date_Dim.csv` | Calendar attributes for time-based analysis |

## Tools and Concepts
- Tableau Desktop: data modeling, calculated fields, KPI cards, trend charts, comparison charts, filters, and dashboard actions.
- Analytics concepts: content performance, traffic-source mix, category comparison, format comparison, and trend analysis.
- Potential measures include views, watch time, engagement, subscribers, and other performance fields when present in the source file. Use the exact field definitions in the supplied dataset.

## Dashboard Analysis
1. **Channel overview** – summary of key video performance measures.
2. **Category performance** – compare results across video categories.
3. **Format performance** – understand differences among available video formats.
4. **Traffic-source analysis** – examine where views originate.
5. **Performance trends** – explore changes over time and identify notable periods.

## Tableau Workflow
1. Open `TubeMetrics_AI_YouTube_Analytics.twb` in Tableau Desktop.
2. Reconnect the CSV sources if Tableau reports missing files.
3. Confirm relationships between `Video_Performance_Fact` and the category, format, traffic-source, and date dimensions.
4. Check data types and confirm date fields are recognized as dates.
5. Review calculated fields and ensure KPI definitions match the dataset.
6. Inspect each worksheet and validate the displayed measures.
7. Test filters and dashboard interactions, including cross-filtering if configured.
8. Save the workbook with updated data-source paths.

## Key Deliverables
- Tableau workbook: `TubeMetrics_AI_YouTube_Analytics.twb`
- Video performance and dimension CSV datasets
- Interactive YouTube analytics dashboard

## Insights and Recommendations
Compare categories and formats using consistent measures and date ranges. Review traffic sources to understand which discovery routes contribute most to video views. Use the results to guide future content experiments, while avoiding conclusions based on a small number of videos.

## Project Outcome
The dashboard provides a consolidated view of YouTube video and discovery performance, helping channel teams explore trends and make informed content decisions.

## Author
Add your name, course/internship details, and project date here.
