def search (combined_df, Nom=None, prenom=None, ID=None, jour_naissance=None, mois_naissance=None, annee_naissance=None, sexe=None):
    conditions = []
    prenom_list=combined_df.prenom.unique()
    Nom_list=combined_df.Nom.unique()
    if prenom is not None:
        for p in prenom_list:
            if type(p)==str :
                if (fuzz.token_sort_ratio(prenom,p)) == 100: prenom=p 
        conditions.append(combined_df['prenom'] == prenom)
    if Nom is not None:
        for n in Nom_list:
            if type(n)==str :
                if (fuzz.token_sort_ratio(Nom,n)) == 100: Nom=n 
        conditions.append(combined_df['Nom'] == Nom)
    if ID is not None:
        conditions.append(combined_df['ID'] == ID)
    if jour_naissance is not None:
        conditions.append(combined_df['jour_naissance'] == jour_naissance)
    if mois_naissance is not None:
        conditions.append(combined_df['mois_naissance'] == mois_naissance)
    if annee_naissance is not None:
        conditions.append(combined_df['annee_naissance'] == annee_naissance)
    if sexe is not None:
        conditions.append(combined_df['sexe'] == sexe)
    if code_delegation is not None:
        conditions.append(combined_df['code_delegation'] == code_delegation)
    if code_municipalite is not None:
        conditions.append(combined_df['code_municipalite'] == code_municipalite) 
    if code_arrondissement is not None:
        conditions.append(combined_df['code_arrondissement'] == code_arrondissement)
    if Code_Imada is not None:
        conditions.append(combined_df['Code_Imada'] == Code_Imada) 
    
     # Combine conditions if any are provided
    if conditions:
        result_df = combined_df.loc[pd.concat(conditions, axis=1).all(axis=1)]
    else:
        result_df = combined_df # If no conditions, return the entire DataFrame
    return result_df
