# EduMetrics AI – Student Success Analytics Dashboard

## Project Overview
EduMetrics AI is a Tableau analytics project designed to explore student enrollment and course-related data. It supports analysis of student participation, course distribution, and trends over time, helping education stakeholders understand patterns in the available records.

**Project type:** Education / Student Analytics  
**Tool:** Tableau  
**Status:** Tableau dashboard completed

## Business Problem
Educational institutions need to understand enrollment patterns across courses and student groups. When student, course, enrollment, and date information is stored in separate datasets, it can be difficult to obtain a consistent overview and identify areas that may require further investigation.

## Project Objectives
- Summarize student and enrollment activity.
- Compare enrollment across courses.
- Explore student-level patterns using available attributes.
- Analyze enrollment trends over time.
- Present findings in an interactive dashboard for education-focused decision-making.

## Dataset Files
| File | Purpose |
|---|---|
| `Enrollments_Fact.csv` | Main enrollment records |
| `Students_Dim.csv` | Student attributes |
| `Courses_Dim.csv` | Course lookup and attributes |
| `Date_Dim.csv` | Calendar attributes for time-based analysis |

## Tools and Concepts
- Tableau Desktop: data connections, relationships, calculated fields, charts, dashboard filters, and interactive exploration.
- Analytics concepts: enrollment KPIs, course comparison, student segmentation where supported, and time-based analysis.
- Example indicators to validate against the available fields: enrollment count, distinct student count, course count, and enrollment trend.

## Dashboard Analysis
1. **Enrollment overview** – high-level view of student and enrollment records.
2. **Course analysis** – compare enrollment across courses.
3. **Student analysis** – explore patterns across available student attributes.
4. **Time trends** – review enrollment changes over dates or periods.
5. **Interactive exploration** – filter views to investigate selected courses, student groups, or periods.

## Tableau Workflow
1. Open `EduMetrics_AI_Student_Success.twb` in Tableau Desktop.
2. Reconnect the CSV files if the workbook cannot locate the original sources.
3. Verify the enrollment fact table's relationships with the student, course, and date dimensions.
4. Confirm identifiers, date fields, and numeric fields have appropriate data types.
5. Check distinct-count calculations to avoid double-counting students.
6. Review worksheets and dashboard-level filters.
7. Test the dashboard using different courses and time periods.
8. Validate totals against the source CSV files and save the workbook.

## Responsible Use and Privacy
Student information should be handled carefully. Do not publish personally identifiable student details. Prefer aggregated results, restrict access to sensitive source data, and avoid interpreting correlations as proof of cause and effect.

## Key Deliverables
- Tableau workbook: `EduMetrics_AI_Student_Success.twb`
- Enrollment, student, course, and date CSV datasets
- Interactive student success analytics dashboard

## Insights and Recommendations
Use course and time comparisons to identify enrollment patterns that may warrant follow-up. Treat dashboard findings as signals for further investigation rather than definitive explanations of student outcomes. Protect student privacy when sharing results.

## Project Outcome
The dashboard brings enrollment and related education data into one interactive analytical experience, supporting clearer reporting and evidence-informed planning.

## Author
Add your name, course/internship details, and project date here.
