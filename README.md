# coffee-sales-analysis-ml
End-to-end analysis of coffee shop sales including data cleaning, automated preprocessing pipeline, exploratory analysis, and a baseline machine learning model.

## Project motivation
Real-World datasets are rarely clean.
That's why this project focuses on preprocessing and cleaning a dataset by handling missing values, inconsistencies, and wrong formats before trying to do any statistic analysis or any modeling. 
The goal is not only prediction, but to think and take decisions in a business thinking context to understand and do what the company would actually really need.

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
   - Reusable, customizable y scalable cleaning and preprocessing logic

3. **Exploratory statistical Analysis**
   - Sales patterns by location, time, product, weekday and station of the year (Winter, Spring, Summer and Fall)
   - Most requested product

4. **ML Model**
   - Transformed the data that we already obtained by cleaning it into data that is useful to build, train and test a ML model
   - Evaluation of the model by seeing metrics like R² and RMSE

## Results
- Dataset cleaned and useful to work with
- Functional, scalable and customizable preprocessing and cleaning data pipeline
- Understandable exploratory statistical analysis by using dashboards in Power BI
- ML model

## Limitations
- The pipeline works if the dataset has a very similar structure of the dataset that this project is working with, otherwise the pipeline code must be customized
- The predictive ML model showed limited performance
- R² score was close to 0% and RMSE was close to the baseline mean, indicating underfitting
- This suggests that sales behavior is influenced by external factors not present in the dataset

Rather than forcing a complex model, the project highlights the importance of:
- Feature relevance
- Data limitations
- Honest model evaluation

## Future Improvements
- Incorporate external data (weather, promotions, holidays)
- Test non-linear and probabilistic models

## Tools & Technologies used
- Python (Pandas, Seaborn, Matplotlib, Scikit-learn, pyedautils, holidays, number_parser)
- Jupyter Notebooks
- Power BI

## Conclusion
The main value of this project is not the model performance or the automated data cleaning pipeline, but the data thinking process: working with messy real-world data, automating preprocessing, being honest about model limitations caused by missing external factors, and demonstrating critical thinking by approaching the problem from a business perspective.

Rather than building a generic solution, this project focuses on creating an analysis and workflow that reflects what a company would actually need when dealing with imperfect data and complex real-world problems.
