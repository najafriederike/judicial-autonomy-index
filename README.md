## Iustitia’s Oracle:\
## Forecasting Political Regime Types by Measuring Judicial Independence

## Project Overview
**Intro:**

**Key Question:**
Can the quality of de jure judicial independence predict the future of political regime types?

**Goal:**
- Create an Index: Develop an index to measure the level of judicial independence, based on 5 macro-indicators and 15 micro-indicators.
- Machine Learning Model: Build a machine learning model to predict future political regime types and levels of democracy based on judicial independence levels, aiming to identify patterns and correlations that link judicial independence to trends in political regimes.

## Project Structure
**How to explore this repository:**

- data: contains raw and cleaned datasets in csv format 
- figures: contains all created visualizations
- notebooks: contains Jupyter notebooks with code for:
  - data cleaning for V-Dem Dataset
  - data cleaning Judicial Autonomy Dataset
  - merging both datasets,
  - building Judicial Autonomy Index, incl. visualizations
  - model training K-Nearest Neighbors, incl. visualizations
  - model training RandomForest, incl. visualizations
- py-files: containing main functions used
- slides: contains presentation slides for project overview

## Datasets
1. Varieties of Democracy (V-Dem): [Episodes of Regime Transformation (ERT) dataset] (https://github.com/vdeminstitute/ERT/tree/master)
   - Variables used:
     - Electoral democracy index (v2x polyarchy)
     - Regimes of the World (v2x regime)
     - Regime type (reg type)

2. Judicial Autonomy Dataset (unpublished)
   - 40 European countries over 23 years (2000-2022)
   - Coded characteristics of national judicial system 
   - Approx.. 50 question items covering first instance, appeal and highest courts (Questionnaire 1)

## Analysis Approach

1. **Data Cleaning**
   - Judicial Autonomy Dataset:
     - Clean countries (drop countries with low data quality) 
     - Rename country names where necessary
     - Filter out all columns with >20% of missing values
     - Create two clean datasets:
       - containing fuzzy values
       - recoding fuzzy values into binary values (if value <= 0.5 then 0 else 1)

    - Data Cleaning Varieties of Democracy (V-Dem) Dataset:
      - Filter for defined countries and for years 2000-2022 to match judicial autonomy dataset
      - Drop all columns except from core variables

2. **Index building**

/figures/index_building_treechart.png

   - Micro Indicators:
     - Created subsets for micro indicators by grouping question items (3 or 4 items per indicator)
     - Filled in missing values on micro indicator level (using group median, unless all items would be NA, then replace all with 0)
     - Aggregated micro indicator scores by calculating group mean
   - Macro Indicators:
     - Created subsets for macro indicators by grouping micro indicators (3 per indicator)
     - Aggregated macro indicator scores by calculating group mean
   - Overall Index:
     - Aggregated overall index score by calculating group mean

3. Machine Learning Model Building:
   - K-Nearest Neighbors
     - Classification and Regression Models
     - Manual feature selection, feature scaling, oversampling
     - Used to explore best feature-target combinations (accuracy & R2 > 90%)
     - Visualizations: Correlation Heatmap
       
   - Random Forest
     - Classification and Regression Models
     - Based on pre-selected feature-target combinations
     - Identify feature importances
     - Visualizations: Confusion Matrix, Scatterplot for True and Predicted Values, and Barplot for Features Importance

## Key Findings & Implications

- Can written law predict the quality of democracy?
  - Weak but recognizable correlation between the quality of judicial independence and the overall quality of democracy.
  - Judicial independence can only be one crucial pillar among many.
  - Challenges in recognizing the subtle erosion of democracy.

- We cannot predict the (political) future, but we can prepare ourselves by:
  - Identifying critical elements of judicial systems
  - Identifying potential threats to judicial independence and democracy
  - Monitoring incremental change
  - Refining measures and approaches to capture "middle-ground" cases

