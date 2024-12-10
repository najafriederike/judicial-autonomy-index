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