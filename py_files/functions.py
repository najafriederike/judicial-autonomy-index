
## JUDICIAL AUTONOMY DATASET ##

#### Function to clean raw dataset

def cleaning_judicial_autonomy_data(q1_df):
    """
    Objective: Basic data cleaning of raw Judicial Autonomy Dataset.
    Input data: Raw Judicial Autonomy Dataset.
    """
    
    # Step 1: Create copy of dataframe
    df = q1_df.copy()
    
    # Step 2: Adjust dataframe shape
    # Pivot long dataframe to wide dataframe
    df_pivoted = df.pivot(index=['username', 'country', 'country_code', 'year'], 
                          columns=['uid'], 
                          values=['value'])
    
    # Reset index and flattening multi-level column names
    df_pivoted.reset_index(inplace=True)
    df_pivoted.columns = [col[1] if col[1] else col[0] for col in df_pivoted.columns]

    # Step 3: Clean country and user names
    # Remove usernames
    remove_usernames = ('ADMIN123', 
                        'ALB22uFF4m',
                        'BEL22cEw8t', 
                        'BIH22q2nOU', 
                        'DNK22KFh1N', 
                        'MNE22N8NJv', 
                        'NLD22Ba53p', 
                        'SRB22L4wbh')
    df_countries_cleaned = df_pivoted[~df_pivoted['username'].isin(remove_usernames)]

    # Replace country names
    df_countries_cleaned.loc[:,'country'] = df_countries_cleaned['country'].replace({
        'Czech Republic': 'Czechia',
        'Republic of Albania': 'Albania',
        'Republic of Serbia': 'Serbia',
        'Bosnia and Herzegovina (BiH)': 'Bosnia and Herzegovina',
        'Montenegro (MON)': 'Montenegro',
        'Kingdom of Belgium': 'Belgium'})
    
    # Step 4: Remove columns
    # Drop columns that contain '_subj'
    # Drop columns with more than 20% values missing values ['q1c2_jubonus', 'q1c2_retireage', 'q1c3_evalints', 'q1c3_immunlift']
    columns_nan_percentage = df_countries_cleaned.isna().mean()*100
    columns_nan_20_percent = columns_nan_percentage[columns_nan_percentage > 20].index
    df_cleaned = df_countries_cleaned.drop(columns=columns_nan_20_percent)

    return df_cleaned


#### Function to recode fuzzy values as binary values

def recoding_fuzzy_to_binary(q1_df):
    """
    Objective: Recode all fuzzy values (i.e. 0.33, 0.5, 0.67) 
    as binary values (conservative coding, i.e. value <= 0.5 as 0.0).
    Input data: Raw judicial autonomy dataset.
    Next step: Clean judicial autonomy dataset.
    """
    
    df_fuzzy_values_recoded = q1_df.copy()
    float_columns = df_fuzzy_values_recoded.select_dtypes(include=float).columns

    for col in float_columns:
        df_fuzzy_values_recoded[col] = df_fuzzy_values_recoded[col].apply(lambda value: 0.0 if value <= 0.5 else 1.0)

    return df_fuzzy_values_recoded


## V-DEM DATASET ##

#### Function to clean raw dataset

def cleaning_vdem_ert_data(vdem_data):
    """
    Objective: Basic data cleaning of raw V-Dem Episodes of Regime Transformation Dataset.
    Input data: Raw V-Dem Episodes of Regime Transformation Dataset.
    """
    
    # Step 1: Create copy of dataframe
    vdem = vdem_data.copy()

    # Step 2: Clean countries
    # Set list of Council of Europe member states (i.e. sample used in the judicial autonomy dataset)
    council_of_europe_countries = ['Albania', 'Armenia', 'Austria', 'Azerbaijan', 'Belgium',
       'Bulgaria', 'Bosnia and Herzegovina', 'Switzerland', 'Cyprus',
       'Czechia', 'Germany', 'Spain', 'Estonia', 'Finland', 'France',
       'United Kingdom', 'Georgia', 'Greece', 'Croatia', 'Hungary',
       'Ireland', 'Iceland', 'Italy', 'Lithuania', 'Latvia', 'Moldova',
       'North Macedonia', 'Malta', 'Montenegro', 'Norway', 'Poland',
       'Portugal', 'Romania', 'Russia', 'Serbia', 'Slovakia', 'Slovenia',
       'Sweden', 'Türkiye', 'Ukraine']

    # Filter dataset for defined countries
    vdem_country = vdem[vdem['country_name'].isin(council_of_europe_countries)]

    # Rename Turkey to match judicial autonomy dataset
    vdem_country.loc[:, 'country_name'] = vdem_country['country_name'].replace({'Türkiye': 'Turkey'})

    # Step 3: Filter for years 2000-2022
    vdem_country_year = vdem_country.loc[(vdem_country['year'] >= 2000) & (vdem_country['year'] <= 2022)]

    # Step 4: Drop columns
    # Define which columns to keep
    columns_to_keep = ['country_name', 'year', 'reg_type', 'v2x_regime', 'v2x_polyarchy']

    # Drop all other columns
    vdem_cleaned = vdem_country_year[columns_to_keep]

    # Rename country column to match judicial autonomy dataset
    vdem_cleaned = vdem_cleaned.rename(columns={'country_name': 'country'})
    
    return vdem_cleaned


## INDEX BUILDING ##

#### Function to merge question items to create micro indicator subsets

def create_micro_indicators_dict(q1_cleaned):
    """ 
    Objective: Create a dictionary with subsets of question items, 
    each including country-year information and the respective question items.
    Input data: Cleaned Judicial Autonomy data (fuzzy or binary).
    """
    
    subsets_micro_indicators = {

    # 1 -- Actors involved in appointment procedures of judges
    'q1_micro_appointment_judges': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c1_apjufc',
                                        'q1c1_apjuac',
                                        'q1c1_apjuhc']],
        
    # 2 -- Actors involved in appointment procedures of court presidents
 
    'q1_micro_appointment_court_presidents': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c1_appresidfc',
                                        'q1c1_appresidac',
                                        'q1c1_appresidhc']],
    
    # 3 -- Veto powers during appointment procedures
    'q1_micro_appointment_veto': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c1_exvetofc',
                                        'q1c1_exvetoac',
                                        'q1c1_exvetohc']],
    
    # 4 -- Selection and appointment criteria for judges - predetermined by law
    'q1_micro_selection_predetermined_law': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c1_critfclaw', 
                                        'q1c1_critaclaw',
                                        'q1c1_crithclaw']],

    # 5 -- Selection and appointment criteria for judges - in accordance to international standards
    'q1_micro_selection_intl_standards': q1_cleaned[[
                                        'country',
                                        'year', 
                                        'q1c1_critfcints',
                                        'q1c1_critacints', 
                                        'q1c1_crithcints',
                                        'q1c1_probju']],

    # 6 -- Transparency and mechanisms for appeal in appointment procedures of judges
    'q1_micro_transparency_appeal': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c1_transplaw', 
                                        'q1c1_appealfc',
                                        'q1c1_appealac',
                                        'q1c1_appealhc']],
        
    # 7 -- Tenure and term in office of judges
    'q1_micro_judge_tenure': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c2_termfcju',
                                        'q1c2_termacju',
                                        'q1c2_termpresid',
                                        'q1c2_termhcju']],
    
    # 8 -- Immunity and non-transferability of judges
    'q1_micro_judge_immunity': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c2_juabsimmun', 
                                        'q1c2_jufuncimmun',
                                        'q1c2_juremove', 
                                        'q1c2_jutransf']],

    # 9 -- Salaries and bonuses of judges
    'q1_micro_judge_salary': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c2_jusalary',
                                        'q1c2_jupension']],
        
    # 10 -- Disciplinary proceedings against judges - predetermined by law
    'q1_micro_disciplinary_proceedings_law': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c3_fairtrial', 
                                        'q1c3_disciplaw',
                                        'q1c3_discipints',
                                        'q1c3_sanctscale']],
        
    # 11 -- Disciplinary proceedings against judges - actors involved
    'q1_micro_disciplinary_proceedings_actors': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c3_discipbody',
                                        'q1c3_initdiscip', 
                                        'q1c3_decdiscip',
                                        'q1c3_appealdiscip']],
        
    # 12 -- Conflict of interest, recusal from cases and evaluation of judges
    'q1_micro_conflict_recusal_evaluation': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c3_judisclos', 
                                        'q1c3_jurestrict',
                                        'q1c3_jurecuse']],
                                          
    # 13 -- Composition of the judicial self-governing bodies
    'q1_micro_judicial_self_governance_bodies': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c4_whocharge', 
                                        'q1c4_whoselect',
                                        'q1c4_whochair']], 
        
    # 14 -- Competences and functioning of the judicial self-governing bodies
    'q1_micro_judicial_self_governance_competences': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c4_competence',
                                        'q1c4_sameright', 
                                        'q1c4_reasondecis']], 
    
    # 15 -- Administration, functioning and budget of courts                                         
    'q1_micro_courts_administration': q1_cleaned[[
                                        'country',
                                        'year',
                                        'q1c4_casealloc', 
                                        'q1c4_regbudget',
                                        'q1c4_manbudget']]
    }

    return subsets_micro_indicators
    

#### Function to fill in missing values per micro indicator with row-wise mode

def fill_na_per_micro_indicators(subsets_micro):
    """ 
    Objective: Identify row mode per micro indicator subset and fill in missing values with it.
    Input data: Dictionary of micro indicator subsets.

    """
    
    def get_row_mode(subsets_micro):
        """        
        Objective: Identify row mode.
        Step 1: Check if row contains only missing values and replace all with 0 if true.
        Step 2: Otherwise, calculate the mode for the row. If multiple modes, take the first one.
        Step 3: Replace missing values in the row with row mode.
        """
        row_numeric = subsets_micro[2:]
        
        if row_numeric.isna().all():
            return subsets_micro.fillna(0)
        else:
            numeric_modes = row_numeric.mode()
            mode_value = numeric_modes.iloc[0] if not numeric_modes.empty else np.nan
            return subsets_micro.fillna(mode_value) 
    
    filled_subsets = {}
    for key, subset in subsets_micro.items():
        filled_subset = subset.apply(get_row_mode, axis=1)
        filled_subsets[key] = filled_subset
    return filled_subsets


#### Function to calculate micro indicator measure (row-wise mean)

def calculate_micro_indicators_mean(subsets_micro):
    """
    Objective: Calculate row mean per micro-indicator subset as an indicator measure.
    Input data: Dictionary of micro-indicator subsets after filling in missing values.
    """
    
    calc_means_subsets = {}
    
    for key, subset in subsets_micro.items():
        subset_copy = subset.copy()
        column_name = f"{key}_ind_measure"
        subset_copy[column_name] = subset_copy.select_dtypes(include=float).mean(axis=1).round(2)
        calc_means_subsets[key] = subset_copy
        
    return calc_means_subsets


#### Function to merge micro indicator subsets to create macro indicators

def create_macro_indicators_dict(subsets_micro_meas):
    """ 
    Objective: Create a new dictionary with subsets of macro indicators, 
    each including country-year information and the respective question items
    and micro indicator measures.
    Input data: Dictionary of micro indicator subsets after calculating micro indicator measures. 
    """
   
    # 1 -- Merge micro-indicators for macro-indicator 'appointment_procedures'
    temp_merge_app = pd.merge(subsets_micro_meas['q1_micro_appointment_judges'],
                              subsets_micro_meas['q1_micro_appointment_court_presidents'],
                              how='outer', on=['country', 'year'])
    temp_merge_app2 = pd.merge(temp_merge_app,
                               subsets_micro_meas['q1_micro_appointment_veto'],
                               how='outer', on=['country', 'year'])

    # 2 -- Merge micro-indicators for macro-indicator 'selection_criteria'
    temp_merge_sel = pd.merge(subsets_micro_meas['q1_micro_selection_predetermined_law'],
                              subsets_micro_meas['q1_micro_selection_intl_standards'],
                              how='outer', on=['country', 'year'])
    temp_merge_sel2 = pd.merge(temp_merge_sel,
                               subsets_micro_meas['q1_micro_transparency_appeal'],
                               how='outer', on=['country', 'year'])
   
    # 3 -- Merge micro-indicators for macro-indicator 'professional_rights'
    temp_merge_rights = pd.merge(subsets_micro_meas['q1_micro_judge_tenure'],
                                 subsets_micro_meas['q1_micro_judge_immunity'],
                                 how='outer', on=['country', 'year'])
    temp_merge_rights2 = pd.merge(temp_merge_rights,
                                  subsets_micro_meas['q1_micro_judge_salary'],
                                  how='outer', on=['country', 'year'])

    # 4 -- Merge micro-indicators for macro-indicator 'professional_obligations'
    temp_merge_obl = pd.merge(subsets_micro_meas['q1_micro_disciplinary_proceedings_law'],
                              subsets_micro_meas['q1_micro_disciplinary_proceedings_actors'],
                              how='outer', on=['country', 'year'])
    temp_merge_obl2 = pd.merge(temp_merge_obl,
                               subsets_micro_meas['q1_micro_conflict_recusal_evaluation'],
                               how='outer', on=['country', 'year'])
        
    # 5 -- Merge micro-indicators for macro-indicator 'judicial_administration'
    temp_merge_adm = pd.merge(subsets_micro_meas['q1_micro_judicial_self_governance_bodies'],
                              subsets_micro_meas['q1_micro_judicial_self_governance_competences'],
                              how='outer', on=['country', 'year'])
    temp_merge_adm2 = pd.merge(temp_merge_adm,
                               subsets_micro_meas['q1_micro_courts_administration'],
                               how='outer', on=['country', 'year'])
    
    subsets_macro_indicators = {'q1_macro_appointment_procedures': temp_merge_app2,
                        'q1_macro_selection_criteria': temp_merge_sel2,
                        'q1_macro_professional_rights': temp_merge_rights2,
                        'q1_macro_professional_obligations': temp_merge_obl2,
                        'q1_macro_judicial_administration': temp_merge_adm2}

    return subsets_macro_indicators
    

#### Function to calculate macro indicator measure based on mean of all micro indicator measures

def aggregate_to_macro_indicators(subsets_macro):
    """
    Objective: Calculate row mean per macro indicator subset as an indicator measure.
    Input data: Dictionary of macro indicator subsets.
    """
    
    calc_macro_ind_measure = {}
    for key, subset in subsets_macro.items():
        calc_micro_ind_measure[key] = subset.copy()
        column_name = f"{key}_ind_measure" # macro indicator measure
        ind_measure_columns = [col for col in subset.columns if col.endswith('_ind_measure')]
        calc_micro_ind_measure[key][column_name] = subset[ind_measure_columns].mean(axis=1).round(2)

    return calc_macro_ind_measure


#### Function to calculate overall index measure based on mean of all macro indicator measures

def create_index_dataset(subsets_macro_meas):
    """
    Objective: Create a new DataFrame with all macro indicator subsets, including 
    country-year information, all micro indicator measures and respective question items.
    Input data: Dictionary of macro indicator subsets after calculating macro indicator measures. 
    """
    
    temp_merge_index = pd.merge(subsets_macro_meas['q1_macro_appointment_procedures'],
                                subsets_macro_meas['q1_macro_selection_criteria'],
                                how='outer', on=['country', 'year'])
    temp_merge_index2 = pd.merge(temp_merge_index,
                                 subsets_macro_meas['q1_macro_professional_rights'],
                                 how='outer', on=['country', 'year'])
    temp_merge_index3 = pd.merge(temp_merge_index2,
                                 subsets_macro_meas['q1_macro_professional_obligations'],
                                 how='outer', on=['country', 'year'])
    index_merged = pd.merge(temp_merge_index3, 
                            subsets_macro_meas['q1_macro_judicial_administration'], 
                            how='outer', on=['country', 'year'])
    
    return index_merged

    
#### Function to calculate index measure based on mean of all macro indicator measures

def aggregate_overall_index(dataframe_index):
    """    
    Objective: 
    1) Calculate mean of all macro indicator measures as an overall index measure.
    2) Move country-year and index measure columns to front positions. 
    Input data: Dictionary of macro indicator subsets after calculating indicator measures.
    """
    
    # Calculate mean of all macro indicator measures
    calc_overall_index = dataframe_index.copy()
    ind_measure_columns = [col for col in dataframe_index.columns if col.startswith('q1_macro')]
    calc_overall_index['index_measure'] = dataframe_index[ind_measure_columns].mean(axis=1).round(2)

    # Add a new column 'country_year' as UID
    calc_overall_index['country_year'] = calc_overall_index['country'] + "_" + calc_overall_index['year'].astype('string')

    # Remove 'country_year' and 'index_measure' columns from DataFrame
    move_column1 = calc_overall_index.pop('country_year')
    move_column2 = calc_overall_index.pop('index_measure')
    
    # Move 'country_year' and 'index_measure' columns to front positions
    calc_overall_index.insert(2, 'country_year', move_column1)
    calc_overall_index.insert(3, 'index_measure', move_column2)
    
    return calc_overall_index
    