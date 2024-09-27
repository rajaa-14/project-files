from fuzzywuzzy import fuzz, process

def best_match (row, df):
    
    prenom = row['prenom']
    Nom = row['Nom']
    jour_naissance = row['jour_naissance']
    mois_naissance = row['mois_naissance']
    annee_naissance = row['annee_naissance']
        
    
    sexe = row['sexe']
        
        # Define conditions
    matches = []
    conditions = []
    matched_nom = []
    matched_nom1 = []
    matched_prenom = []
    matches_list=[]
    matches_df= pd.DataFrame() 
        
    prenom_list = df['prenom'].unique()
    Nom_list = df['Nom'].unique()
    
        
    if ((row['prenom'] == None) |  (pd.isnull(row['prenom'])) | (row['prenom'] == '')) :
         return matches_list
    if ((row['Nom'] == None) | (pd.isnull(row['Nom']))  | (row['Nom'] == '')) :
         return matches_list
        
        # Check prenom
    if (prenom is not None):
        if isinstance(prenom, str):
            matched_prenom = [p for p in prenom_list if fuzz.token_sort_ratio(prenom, p)> 90]
            if matched_prenom:
                conditions.append(df['prenom'].isin(matched_prenom))
                    #print(prenom, "matches first name " , matched_prenom)
            else:
                conditions.append(df['prenom'] == prenom)
                    #print(prenom, " is not matched")
        
        # Check Nom
    if (Nom is not None ):
        if isinstance(Nom, str):
            matched_nom = [n for n in Nom_list if fuzz.token_sort_ratio(Nom, n) > 90]
            if matched_nom:
                conditions.append(df['Nom'].isin(matched_nom))
                    #print(Nom, "matches last name " , matched_nom)
            else:
                conditions.append(df['Nom'] == Nom)
                    #print(Nom, " is not matched")
    
        # Check dates
    if pd.notna(jour_naissance) and jour_naissance != 0:
        conditions.append((df['jour_naissance'] == jour_naissance) | (df['jour_naissance'] == 0))
    if pd.notna(mois_naissance) and mois_naissance != 0:
        conditions.append((df['mois_naissance'] == mois_naissance) | (df['mois_naissance'] == 0))
    if pd.notna(annee_naissance) and annee_naissance!= 0:
        conditions.append(df['annee_naissance'] == annee_naissance)
        conditions.append(annee_naissance <= df['annee de deces'])
        conditions.append((annee_naissance + 120 ) > df['annee de deces'] )
    
    if pd.notna(sexe) :
        conditions.append(df['sexe'] == sexe)
        
        # Combine conditions
    if (len(conditions)) > 0 :
        matches_df= pd.DataFrame() 
        matches_df = df.loc[pd.concat(conditions, axis=1).all(axis=1)]
        for index, row in matches_df.iterrows() :
            match_info = {
                        'id' : row['ID'], 
                        'jour_deces': row['jour de deces'], 
                        'mois_deces': row['mois de deces'],
                        'annee_deces': row['annee de deces'],
                        'situation_familiale': row['situation familiale'] }
            matches.append(match_info)
    else: matches_list = None 
    if len(matches_df) > 1:
        status = 2  # Uncertain
        death_info = json.dumps(matches, ensure_ascii=False)
    elif len(matches_df) == 1 :
        status= 1 # Surely dead
        death_info = json.dumps(matches, ensure_ascii=False)
    else:
        status = 0 # Still Alive(for now)
        death_info = None
    #print("Possible death_IDs for ", row['ID'], "are", len(matches_df) ) 
    return status, death_info
