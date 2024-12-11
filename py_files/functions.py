# Cleaning function

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
    
    # Step 4: Remove subjective questions
    # Drop columns that contain '_subj'
    df_cleaned = df_countries_cleaned.drop(list(df_countries_cleaned.filter(regex='_subj')), axis=1)

    return df_cleaned



def subset_dataset_into_indicators(qx_cleaned):

    subsets = {

    # Actors involved in appointment procedures of judges
    'q1_appointment_actors': qx_cleaned[['country',
                                        'year',
                                        'q1c1_apjufc',
                                        'q1c1_apjuac',
                                        'q1c1_apjuhc',
                                        'q1c1_appresidfc',
                                        'q1c1_appresidac',
                                        'q1c1_appresidhc',
                                        'q1c1_exvetofc',
                                        'q1c1_exvetoac',
                                        'q1c1_exvetohc']],
    
    # Selection and appointment criteria for judges
    'q1_appointment_criteria': qx_cleaned[['country',
                                          'year',
                                          'q1c1_critfclaw', 
                                          'q1c1_critaclaw',
                                          'q1c1_crithclaw', 
                                          'q1c1_critfcints',
                                          'q1c1_critacints', 
                                          'q1c1_crithcints',
                                          'q1c1_probju']],

    # Transparency and mechanisms for appeal in appointment procedures of judges
    'q1_appointment_transparency': qx_cleaned[['country',
                                              'year',
                                              'q1c1_transplaw', 
                                              'q1c1_appealfc',
                                              'q1c1_appealac',
                                              'q1c1_appealhc']],
    # Tenure and term in office of judges
    'q1_judge_tenure': qx_cleaned[['country',
                                  'year',
                                  'q1c2_termfcju', 
                                  'q1c2_termacju',
                                  'q1c2_termpresid', 
                                  'q1c2_termhcju',
                                  'q1c2_retireage']],
    
    # Immunity and non-transferability of judges
    'q1_judge_immunity': qx_cleaned[['country',
                                    'year',
                                    'q1c2_juabsimmun', 
                                    'q1c2_jufuncimmun',
                                    'q1c2_juremove', 
                                    'q1c2_jutransf']],

    # Salaries and bonuses of judges
    'q1_judge_salary': qx_cleaned[['country',
                                  'year',
                                  'q1c2_jusalary', 
                                  'q1c2_jubonus',
                                  'q1c2_jupension']],
        
    # Disciplinary proceedings against judges
    'q1_disciplinary_proceedings': qx_cleaned[['country',
                                              'year',
                                              'q1c3_fairtrial', 
                                              'q1c3_disciplaw',
                                              'q1c3_discipints', 
                                              'q1c3_discipbody',
                                              'q1c3_initdiscip', 
                                              'q1c3_decdiscip',
                                              'q1c3_immunlift', 
                                              'q1c3_sanctscale',
                                              'q1c3_appealdiscip']],
        
    # Conflict of interest, recusal from cases and evaluation of judges
    'q1_conflict_recusal_evaluation': qx_cleaned[['country',
                                          'year',
                                          'q1c3_judisclos', 
                                          'q1c3_jurestrict',
                                          'q1c3_jurecuse']],
                                          
    # Composition and functioning of the judicial self-governing bodies
    'q1_judicial_self_governance': qx_cleaned[['country',
                                             'year',
                                             'q1c4_whocharge', 
                                             'q1c4_whoselect',
                                             'q1c4_whochair', 
                                             'q1c4_competence',
                                             'q1c4_sameright', 
                                             'q1c4_reasondecis']], 
    
    # Administration, functioning and budget of courts                                         
    'q1_courts_administration': qx_cleaned[['country',
                                           'year',
                                           'q1c4_casealloc', 
                                           'q1c4_regbudget',
                                           'q1c4_manbudget']]
    }

    return subsets
    