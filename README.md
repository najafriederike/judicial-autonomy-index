# _Iustitia’s Oracle: Forecasting Political Regime Types by Measuring Judicial Independence_

## Project Overview
This project explores whether the quality of (_de jure_) judicial independence predicts the future of political regime types using machine learning models. The aim of this project is twofold:
1. Create an index: To develop an index to measure the level of judicial independence based on 5 macro and 15 micro indicators.
2. Machine learning model: Build a machine learning model to predict future political regime types and levels of democracy based on levels of judicial independence, with the aim of identifying patterns and correlations that link judicial independence to trends in political regimes.

## Project Structure
**How to explore this repository:**

- _data_: Contains raw and cleaned datasets in csv format 
- _figures_: Contains all created visualizations
- _notebooks_: Contains Jupyter notebooks with python code for:
  - Data cleaning for V-Dem Dataset
  - Data cleaning Judicial Autonomy Dataset
  - Building Judicial Autonomy Index
  - Merging both datasets
  - Exploratory Data Analysis (EDA)
  - Model training K-Nearest Neighbors, incl. visualizations
  - Model training RandomForest, incl. visualizations
- _py-files_: Contains main functions used
- _slides_: Contains presentation slides for project overview
- _yaml file_: Contains references for input and output data
- _toml file_: Contains information about packages and other dependencies used
- _README file_: Project description

## Datasets
1. Varieties of Democracy (V-Dem): [Episodes of Regime Transformation (ERT) dataset](https://github.com/vdeminstitute/ERT/tree/master)
   - Variables used:
     - Electoral democracy index (v2x_polyarchy)
     - Regimes of the World (v2x_regime)
     - Regime type (reg_type)

2. Judicial Autonomy Dataset (unpublished)
   - 40 European countries for the period 2000-2022
   - Coded characteristics of each national judicial system 
   - Approx.. 50 question items covering first instance, appeal and highest courts

## Analysis Approach

**1. Data Cleaning**
   - **Judicial Autonomy Dataset**:
     - Cleaned countries (dropped countries with low data quality and renamed country names where necessary) 
     - Filtered out all columns with >20% of missing values
     - Created two clean datasets:
       - containing fuzzy values
       - containing binary values (recoded values as: 0.0 if value <= 0.5 else 1.0)

   - **Varieties of Democracy (V-Dem) Dataset**:
      - Filtered for defined countries and for years 2000-2022 to match Judicial Autonomy dataset
      - Dropped all columns except from core variables (i.e. v2x_polyarchy, v2x_regime, reg_type)

**2. Index building**

/figures/index_building_treechart.png

   - **Micro Indicators**:
     - Created micro indicator subsets by grouping question items (3 or 4 items per indicator)
     - Filled in missing values at micro indicator level (using group median unless all items were NA, then replaced with 0)
     - Aggregated micro indicator scores by calculating group mean
   - **Macro Indicators**:
     - Macro indicator subsets created by grouping micro indicators (3 per indicator)
     - Aggregated macro indicator scores by calculating group mean
   - **Overall Index**:
     - Aggregated overall index score by calculating group mean

**3. Machine Learning Model Building**
   
   - **K-Nearest Neighbors**
     - Trained several classification and regression models
     - Manual feature selection, feature scaling, oversampling
     - Used to explore best feature-target combinations (accuracy & R2 > 90%)
     - Visualizations: Correlation Heatmap
       
   - **Random Forest**
     - Based on pre-selected feature-target combinations

     - Classification Models:
       - Results: overall accuracy of 93%.
       - Feature importances (top 3):
         - Competences of judicial self-governance bodies
         - Judges' immunity
         - Conflict of interest, obligation of recusal, evaluation procedures

     - Regression Models:
       - Results: R2 score of 96%.
       - Feature importances (top 3):
         - Judges' tenure or term in office
         - Conflict of interest, obligation of recusal, evaluation procedures
         - Actors involved in disciplinary proceedings
         
     - Visualizations created: Confusion Matrix, Scatterplot for True and Predicted Values, and Barplot for Features Importance.

## Conclusion

- **Key Findings**:
  - Weak but recognizable correlation between the quality of judicial independence and the overall quality of democracy.
  - Judicial independence can only be one crucial pillar among many.
  - Challenges in recognizing the subtle erosion of democracy.

- **Implications**: 
  - We cannot predict the (political) future, but we can prepare ourselves by:
    - Identifying critical elements of judicial systems
    - Identifying potential threats to judicial independence and democracy
    - Monitoring incremental change
    - Refining measures and approaches to capture "middle-ground" cases

