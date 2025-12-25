# coffee-sales-analysis-ml
End-to-end analysis of coffee shop sales including data cleaning, automated preprocessing pipeline, exploratory analysis, and a baseline machine learning model.

## Project motivation
Real-World datasets are rearley clean.
Thats why this project focuses on preprocesing and cleaning a dataset by handling missing values, inconsistencies, and wrong formats before trying to do any statistic analysis or any modeling. 
The goal is not onaly prediction, but to think and take desitions in a bussisnes thinking context to undesrtand and do what the company would really need.

## About the Dataset
- Cafe sales data
- Includes missing values, inconsistent entries and errors
- Data was intentionally kept close to the original quality form to simulate the real-world needs

## Project Structure
cafe-sales-analysis/
├── data/
│ ├── raw/ # Original dataset
│ └── processed/ # Cleaned dataset
│
├── notebooks/
│ ├── 01_data_cleaning.ipynb
│ ├── 02_pipeline.ipynb
│ └── 03_predictive_modeling_sales_analysis.ipynb
│
├── power_bi/
│ └── screenshots/
│
└── README.md

## Methodology

1. **Data Cleaning**
   - Missing values handled by using grouped statistics
   - Missing values from columns like Sales, Price and Total Spent are handled by using the mathematical correlation between this three columns
   - Inconsistencies and invalid entries on a column due to the context of the column are corrected
   - Preserve data integrity over data quantity
     
2. **Automated Pipeline**
   - Reusable, customisable y scalable cleaning and preprocesing logic

3. **Exploratory statistical Analysis**
   - Sales patterns by location, time, product, weekday and station of the year (Winter, Spring, Summer and Fall)
   - Most requested product

4. **ML Model**
   - Transformed the data that we arlready obtained by cleaning it into data that is useful to build, train and test a ML model
   - Evaluation of the model by seeing metrics like R² and RMSE

## Results and Limitations
