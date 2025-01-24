# _Iustitia’s Oracle: Forecasting Political Regime Types by Measuring Judicial Independence_

## Project Overview
This project explores whether the quality of (_de jure_) judicial independence can predict the future of political regime types using machine learning models. The aim of this project is twofold:
1. Create an index: To develop an index to measure the level of judicial independence based on 5 macro and 15 micro indicators.
2. Machine learning (ML) model: Build a machine learning model to predict future political regime types and levels of democracy based on levels of judicial independence, with the aim of identifying patterns and correlations that link judicial independence to trends in political regimes.

## Project Structure
**How to explore this repository:**

- _data_: Contains raw and cleaned datasets in csv format 
- _figures_: Contains all created visualizations
- _notebooks_: Contains Jupyter notebooks with python code for:
  - Data cleaning for V-Dem Dataset
  - Data cleaning for Judicial Autonomy Dataset
  - Building the Judicial Autonomy Index
  - Merging both datasets
  - Exploratory Data Analysis (EDA), , incl. visualizations
  - ML Model training K-Nearest Neighbors, incl. visualizations
  - ML Model training RandomForest, incl. visualizations
  - Appendix: Exploring missing values in Judicial Autonomy Dataset, incl. visualizations
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

## Appendix (List of full variable names):
 
- **Appointment Procedures** _('q1_macro_appointment_procedures_ind_measure')_
  - Actors involved in appointment procedures of judges<br/> _('q1_micro_appointment_judges_ind_measure')_
  - Actors involved in appointment procedures of court presidents<br/> _('q1_micro_appointment_court_presidents_ind_measure')_
  - Veto powers during appointment procedures<br/> _('q1_micro_appointment_veto_ind_measure')_

- **Selection Criteria** _('q1_macro_selection_criteria_ind_measure')_
  - Selection and appointment criteria for judges - predetermined by law<br/> _('q1_micro_selection_predetermined_law_ind_measure')_
  - Selection and appointment criteria for judges - in accordance to international standards<br/> _('q1_micro_selection_intl_standards_ind_measure')_
  - Transparency and mechanisms for appeal in appointment procedures of judges<br/> _('q1_micro_transparency_appeal_ind_measure')_

- **Professional Rights** _('q1_macro_professional_rights_ind_measure')_
  - Tenure and term in office of judges<br/> _('q1_micro_judge_tenure_ind_measure')_
  - Immunity and non-transferability of judges<br/> _('q1_micro_judge_immunity_ind_measure')_
  - Salaries and bonuses of judges<br/> _('q1_micro_judge_salary_ind_measure')_

- **Professional Obligations** _('q1_macro_professional_obligations_ind_measure')_
  - Disciplinary proceedings against judges - predetermined by law<br/> _('q1_micro_disciplinary_proceedings_law_ind_measure')_
  - Disciplinary proceedings against judges - actors involved<br/> _('q1_micro_disciplinary_proceedings_actors_ind_measure')_
  - Conflict of interest, recusal from cases and evaluation of judges<br/> _('q1_micro_conflict_recusal_evaluation_ind_measure')_

- **Judicial Administration** _('q1_macro_judicial_administration_ind_measure')_
  - Composition of the judicial self-governing bodies<br/> _('q1_micro_judicial_self_governance_bodies_ind_measure')_
  - Competences and functioning of the judicial self-governing bodies<br/> _('q1_micro_judicial_self_governance_competences_ind_measure')_
  - Administration, functioning and budget of courts<br/> _('q1_micro_courts_administration_ind_measure')_