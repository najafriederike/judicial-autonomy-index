
### Define function to clean raw dataset

def cleaning_judicial_autonomy_data(qx_df):

    # Step 1: Create copy of dataframe
    df = qx_df.copy()
    
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


### Define function to recode all fuzzy values as binary values (conservative coding, i.e. value <= 0.5 as 0.0)

def recoding_fuzzy_to_binary(qx_df):

    df_fuzzy_values_recoded = qx_df.copy()
    float_columns = df_fuzzy_values_recoded.select_dtypes(include=float).columns

    for col in float_columns:
        df_fuzzy_values_recoded[col] = df_fuzzy_values_recoded[col].apply(lambda value: 0.0 if value <= 0.5 else 1.0)

    return df_fuzzy_values_recoded



def create_micro_indicators_dict(qx_cleaned):

    subsets = {

    # 1 -- Actors involved in appointment procedures of judges
        'q1_micro_appointment_judges': qx_cleaned[[
                                        'country',
                                        'year',
                                        'q1c1_apjufc',
                                        'q1c1_apjuac',
                                        'q1c1_apjuhc']],
        
    # 2 -- Actors involved in appointment procedures of court presidents
 
        'q1_micro_appointment_court_presidents': qx_cleaned[[
                                        'country',
                                        'year',
                                        'q1c1_appresidfc',
                                        'q1c1_appresidac',
                                        'q1c1_appresidhc']],
    
    # 3 -- Veto powers during appointment procedures
        'q1_micro_appointment_veto': qx_cleaned[[
                                        'country',
                                        'year',
                                        'q1c1_exvetofc',
                                        'q1c1_exvetoac',
                                        'q1c1_exvetohc']],
    
    # 4 -- Selection and appointment criteria for judges - predetermined by law
        'q1_micro_selection_predetermined_law': qx_cleaned[[
                                        'country',
                                        'year',
                                        'q1c1_critfclaw', 
                                        'q1c1_critaclaw',
                                        'q1c1_crithclaw']],

    # 5 -- Selection and appointment criteria for judges - in accordance to international standards
        'q1_micro_selection_intl_standards': qx_cleaned[[
                                        'country',
                                        'year', 
                                        'q1c1_critfcints',
                                        'q1c1_critacints', 
                                        'q1c1_crithcints',
                                        'q1c1_probju']],

    # 6 -- Transparency and mechanisms for appeal in appointment procedures of judges
    'q1_micro_transparency_appeal': qx_cleaned[['country',
                                              'year',
                                              'q1c1_transplaw', 
                                              'q1c1_appealfc',
                                              'q1c1_appealac',
                                              'q1c1_appealhc']],
    # 7 -- Tenure and term in office of judges
    'q1_micro_judge_tenure': qx_cleaned[['country',
                                  'year',
                                  'q1c2_termfcju', 
                                  'q1c2_termacju',
                                  'q1c2_termpresid', 
                                  'q1c2_termhcju']],
    
    # 8 -- Immunity and non-transferability of judges
    'q1_micro_judge_immunity': qx_cleaned[['country',
                                    'year',
                                    'q1c2_juabsimmun', 
                                    'q1c2_jufuncimmun',
                                    'q1c2_juremove', 
                                    'q1c2_jutransf']],

    # 9 -- Salaries and bonuses of judges
    'q1_micro_judge_salary': qx_cleaned[['country',
                                  'year',
                                  'q1c2_jusalary',
                                  'q1c2_jupension']],
        
    # 10 -- Disciplinary proceedings against judges - predetermined by law
    'q1_micro_disciplinary_proceedings_law': qx_cleaned[['country',
                                              'year',
                                              'q1c3_fairtrial', 
                                              'q1c3_disciplaw',
                                              'q1c3_discipints',
                                              'q1c3_sanctscale']],
        
    # 11 -- Disciplinary proceedings against judges - actors involved
    'q1_micro_disciplinary_proceedings_actors': qx_cleaned[['country',
                                              'year',
                                              'q1c3_discipbody',
                                              'q1c3_initdiscip', 
                                              'q1c3_decdiscip',
                                              'q1c3_appealdiscip']],
        
    # 12 -- Conflict of interest, recusal from cases and evaluation of judges
    'q1_micro_conflict_recusal_evaluation': qx_cleaned[['country',
                                          'year',
                                          'q1c3_judisclos', 
                                          'q1c3_jurestrict',
                                          'q1c3_jurecuse']],
                                          
    # 13 -- Composition of the judicial self-governing bodies
    'q1_micro_judicial_self_governance_bodies': qx_cleaned[['country',
                                             'year',
                                             'q1c4_whocharge', 
                                             'q1c4_whoselect',
                                             'q1c4_whochair']], 
        
    # 14 -- Competences and functioning of the judicial self-governing bodies
    'q1_micro_judicial_self_governance_competences': qx_cleaned[['country',
                                             'year',
                                             'q1c4_competence',
                                             'q1c4_sameright', 
                                             'q1c4_reasondecis']], 
    
    # 15 -- Administration, functioning and budget of courts                                         
    'q1_micro_courts_administration': qx_cleaned[['country',
                                           'year',
                                           'q1c4_casealloc', 
                                           'q1c4_regbudget',
                                           'q1c4_manbudget']]
    }

    return subsets


# Function to fill in missing values in each micro-indicator by row mode

def get_row_mode(row):
    """
    Step 1: Calculate the mode for the row. If multiple modes, take the first one
    Step 2: Replace NaN values in the row with the mode
    """
    row_numeric = row[2:]
    numeric_modes = row_numeric.mode()
    mode_value = numeric_modes.iloc[0] if not numeric_modes.empty else np.nan

    return row.fillna(mode_value) 


# Apply function to all micro-indicator subsets

def fill_na_per_micro_indicators(subsets):
    filled_subsets = {}
    for key, subset in subsets.items():
        filled_subset = subset.apply(get_row_mode, axis=1)
        filled_subsets[key] = filled_subset
    return filled_subsets


# Create micro-indicator measurement (by mean)

def calculate_micro_indicators_mean(subsets):
    
    calc_means_subsets = {}
    
    for key, subset in subsets.items():
        calc_means_subsets[key] = subset.copy()
        column_name = f"{key}_ind_measure"
        calc_means_subsets[key][column_name] = subset.select_dtypes(include=float).mean(axis=1).round(2)
        
    return calc_means_subsets


# Create macro-indicator measurement (by mean)

def create_macro_indicators_dict(subset):

    # 1 -- Merge micro-indicators for macro-indicator 'appointment_procedures'
        temporary_merge_app = pd.merge(subset['q1_micro_appointment_judges'], 
                                       subset['q1_micro_appointment_court_presidents'], 
                                       how='outer', on=['country', 'year'])
        temporary_merge_app2 = pd.merge(temporary_merge_app, 
                                        subset['q1_micro_appointment_veto'], 
                                        how='outer', on=['country', 'year'])

    # 2 -- Merge micro-indicators for macro-indicator 'selection_criteria'
        temporary_merge_sel = pd.merge(subset['q1_micro_selection_predetermined_law'],
                                       subset['q1_micro_selection_intl_standards'],
                                        how='outer', on=['country', 'year'])
        temporary_merge_sel2 = pd.merge(temporary_merge_sel, 
                                        subset['q1_micro_transparency_appeal'],                                        
                                        how='outer', on=['country', 'year'])
   
    # 3 -- Merge micro-indicators for macro-indicator 'professional_rights'
        temp_merge_rights = pd.merge(subset['q1_micro_judge_tenure'], 
                                     subset['q1_micro_judge_immunity'], 
                                     how='outer', on=['country', 'year'])
        temp_merge_rights2 = pd.merge(temp_merge_rights, 
                                      subset['q1_micro_judge_salary'],
                                      how='outer', on=['country', 'year'])

    # 4 -- Merge micro-indicators for macro-indicator 'professional_obligations'
        temp_merge_obl = pd.merge(subset['q1_micro_disciplinary_proceedings_law'], 
                                  subset['q1_micro_disciplinary_proceedings_actors'], 
                                  how='outer', on=['country', 'year'])
        temp_merge_obl2 = pd.merge(temp_merge_obl, 
                                   subset['q1_micro_conflict_recusal_evaluation'], 
                                   how='outer', on=['country', 'year'])
        
    # 5 -- Merge micro-indicators for macro-indicator 'judicial_administration'
        temp_merge_adm = pd.merge(subset['q1_micro_judicial_self_governance_bodies'], 
                                  subset['q1_micro_judicial_self_governance_competences'], 
                                  how='outer', on=['country', 'year'])
        temp_merge_adm2 = pd.merge(temp_merge_adm,
                                   subset['q1_micro_courts_administration'],
                                   how='outer', on=['country', 'year'])
    
        macro_indicators = {'q1_macro_appointment_procedures': temporary_merge_app2, 
                            'q1_macro_selection_criteria': temporary_merge_sel2, 
                            'q1_macro_professional_rights': temp_merge_rights2,
                            'q1_macro_professional_obligations': temp_merge_obl2,
                            'q1_macro_judicial_administration': temp_merge_adm2}

        return macro_indicators
    


def aggregate_to_macro_indicators(subsets):
    calc_micro_ind_measure = {}
    for key, subset in subsets.items():
        calc_micro_ind_measure[key] = subset.copy()
        column_name = f"{key}_ind_measure" # macro indicator measure
        ind_measure_columns = [col for col in subset.columns if col.endswith('_ind_measure')]
        calc_micro_ind_measure[key][column_name] = subset[ind_measure_columns].mean(axis=1).round(2)

    return calc_micro_ind_measure


def create_index_dataset(subset):

    temporary_merge_index = pd.merge(subset['q1_macro_appointment_procedures'], 
                                     subset['q1_macro_selection_criteria'], 
                                     how='outer', on=['country', 'year'])
    temporary_merge_index2 = pd.merge(temporary_merge_index, 
                                     subset['q1_macro_professional_rights'], 
                                     how='outer', on=['country', 'year'])
    temporary_merge_index3 = pd.merge(temporary_merge_index2, 
                                     subset['q1_macro_professional_obligations'], 
                                     how='outer', on=['country', 'year'])
    index_merged = pd.merge(temporary_merge_index3, 
                            subset['q1_macro_judicial_administration'], 
                            how='outer', on=['country', 'year'])
    
    return index_merged

#

def aggregate_overall_index(subset):

    # calculate the mean of all macro-indicator measures
    calc_overall_index = subset.copy()
    ind_measure_columns = [col for col in subset.columns if col.startswith('q1_macro')]
    calc_overall_index['index_measure'] = subset[ind_measure_columns].mean(axis=1).round(2)

    # add a new column 'country_year' as UID
    calc_overall_index['country_year'] = calc_overall_index['country'] + "_" + calc_overall_index['year'].astype('string')
    
    return calc_overall_index