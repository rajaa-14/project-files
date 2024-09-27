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
    
     # Combine conditions if any are provided
    if conditions:
        result_df = combined_df.loc[pd.concat(conditions, axis=1).all(axis=1)]
    else:
        result_df = combined_df # If no conditions, return the entire DataFrame
    return result_df

#another_one
def get_children_from_mother (combined_df, prenom_Nom_mere=None, nom_mere=None,
       jour_naissance_mere=None, mois_naissance_mere=None, annee_naissance_mere=None,
       profession_mere=None, code_nationalite_mere=None):
    conditions = []
    prenom_meres_list=combined_df.prenom_Nom_mere.unique()
    Nom_meres_list=combined_df.nom_mere.unique()
    if prenom_Nom_mere is not None:
        for p in prenom_meres_list:
            if type(p)==str :
                if (fuzz.token_sort_ratio(prenom_Nom_mere,p)) > 80: prenom_Nom_mere=p 
        conditions.append(combined_df['prenom_Nom_mere'] == prenom_Nom_mere)
    if nom_mere is not None:
        for n in Nom_meres_list:
            if type(n)==str :
                if (fuzz.token_sort_ratio(nom_mere,n)) == 100: nom_mere=n 
        conditions.append(combined_df['nom_mere'] == nom_mere)
    if jour_naissance_mere is not None:
        conditions.append(combined_df['jour_naissance_mere'] == jour_naissance_mere)
    if mois_naissance_mere is not None:
        conditions.append(combined_df['mois_naissance_mere'] == mois_naissance_mere)
    if annee_naissance_mere is not None:
        conditions.append(combined_df['annee_naissance_mere'] == annee_naissance_mere)
    
     # Combine conditions if any are provided
    if conditions:
        result_df = combined_df.loc[pd.concat(conditions, axis=1).all(axis=1)]
    else:
        result_df = combined_df # If no conditions, return the entire DataFrame
    return result_df
