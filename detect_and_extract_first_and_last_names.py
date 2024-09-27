#Extract Names 
import pandas as pd  
import re  
keywords = {  
        'daughter': [' بنت ', ' ابنة ', 'إبنة', ' ابنت ', ' إبنت '],  
        'ancestor': [' ابن ', ' إبن ', ' بن ']  
           } 
compound_patterns = [
        re.compile(r'عبد\s+\S+'), 
        re.compile(r'\S+\s+الدين'), 
        re.compile(r'\S+\s+الاسلام'), 
        re.compile(r'\S+\s+الله') 
]
def extract_names_mothers(full_name):
    full_name = full_name.strip()
    
    #Check for compound names
    for pattern in compound_patterns:
        match = pattern.search(full_name)
        if match:
            full_name = full_name.replace(match.group(), match.group().replace(' ', ''))
            
    # Count occurrences of each keyword category bent/ben
    keyword_counts = {category: sum(len(re.findall(keyword, full_name)) for keyword in keywords[category]) for category in keywords}
    
    # print(f"Full Name: {full_name}")
    # print(f"Keyword Counts: {keyword_counts}")

    # Check for the presence of keywords and call appropriate functions 
    if keyword_counts['daughter'] == keyword_counts['ancestor'] == 0: #if 'bent' nor 'ben' exist
        return handle_without_keywords_mere(full_name)
    elif keyword_counts['daughter'] > 0 and keyword_counts['ancestor'] == 0 :  #if 'bent' exists
        #print('going to split_with_daughter ')
        return split_with_daughter_mere(full_name)  
    elif keyword_counts['ancestor'] == 1:  #if one 'ben' exists
        ##print("going to split_with_single_ancestor")
        return split_with_single_ancestor_mere(full_name)  
    elif keyword_counts['ancestor'] > 1:  #if multiple 'ben' exist
        #print("going to split_multiple_ancestor")
        return split_with_multiple_ancestors_mere(full_name)  


def handle_without_keywords_mere(full_name):  
    parts = full_name.split()  # Split the full name into parts  
    if len(parts) > 1:  
        nom_de_famille_mere = parts[-1]  # Last part becomes the family name  
        prenom = ' '.join(parts[:-1])  # Join all parts except the last for the given name  
    else:  
        prenom = full_name  # If there's only one part, that is the given name  
        nom_de_famille_mere = None  # No family name available  
    nom1_mere = None  
    nom2_mere = None 
    return prenom, nom1_mere, nom2_mere, nom_de_famille_mere

def split_with_daughter_mere(full_name):
    parts = full_name.split()
    keywords = { 
        'daughter': ['بنت', 'ابنة', 'إبنة', 'ابنت', 'إبنت'],  
        'ancestor': ['ابن', 'إبن', 'بن']  }
    try:
        # Find the first occurrence of any daughter keyword
        index = next(i for i, part in enumerate(parts) if part in keywords['daughter'])
        # print(f"Daughter keyword found at index: {index}")
    except StopIteration:
        return None, None, None, None

    if len(parts) > index + 1 and len(parts) != 3:
        prenom = ' '.join(parts[:index])
        nom_de_famille_mere = parts[-1]
        nom1_mere = ' '.join(parts[index + 1:-1])
        # print(f"Prenom: {prenom}, Nom1_mere: {nom1_mere}, Nom_de_famille: {nom_de_famille}")
    elif len(parts) > index + 1 and len(parts) == 3 :
        prenom = ' '.join(parts[:index])
        nom_de_famille_mere = None
        nom1_mere = ' '.join(parts[index + 1:])
    else:
        prenom = None
        nom_de_famille_mere= None
        nom1_mere = None
    nom2_mere = None 
    return prenom, nom1_mere, nom2_mere, nom_de_famille_mere


def split_with_single_ancestor_mere(full_name):
    parts = full_name.split()
    
    keywords = {  
        'daughter': ['بنت', 'ابنة', 'إبنة', 'ابنت', 'إبنت'],  
        'ancestor': ['ابن', 'إبن', 'بن']  }

    # Check for ancestor and daughter keywords using the centralized keywords dictionary
    has_ancestor = any(part in keywords['ancestor'] for part in parts)
    has_daughter = any(part in keywords['daughter'] for part in parts)
    #print(f"Has ancestor: {has_ancestor}, Has daughter: {has_daughter}")

    if has_ancestor == None and has_daughter== None :
        return None, None, None, None

    try:
        index_ancestor = next(i for i, part in enumerate(parts) if part in keywords['ancestor'])
        index_daughter = next(i for i, part in enumerate(parts) if part in keywords['daughter'])
        #print(" index_ancestor is ", index_ancestor, "index_daughter is ", index_daughter) 

    except StopIteration:
        return None, None, None, None

    prenom_mere = ' '.join(parts[:index_daughter]).strip()  # Join all parts before the daughter keyword
    if index_ancestor == len(parts) - 2:  # Ancestor is the second to last part
        nom_de_famille_mere = ' '.join(parts[-2:])  # Combine last two parts
    else:
        nom_de_famille_mere = parts[-1]  # Last part is the family name
        
#result = extract_names("فاطمة الزهراء بنت سالم بن عامر المقراني")
    
    # Join parts between ancestor and daughter for nom1_mere
    nom1_mere = ' '.join(parts[index_daughter + 1:index_ancestor ]).strip() 
    nom2_mere = ' '.join(parts[index_ancestor + 1: -1 ]).strip()
    #print(f"Prenom_mere: {prenom_mere}, Nom1_mere: {nom1_mere}, nom2_mere: {nom2_mere} , Nom_de_famille: {nom_de_famille_mere}")
    # print ("prenom : ", prenom_mere )
    # print ("nom1_mere : ", nom1_mere)
    # print ("nom2_mere : ", nom2_mere)
    # print ("nom_de_famille_mere : ", nom_de_famille_mere )

    return prenom_mere, nom1_mere, nom2_mere, nom_de_famille_mere


def split_with_multiple_ancestors_mere(full_name):
    parts = full_name.split()
    keywords = {  
        'daughter': ['بنت', 'ابنة', 'إبنة', 'ابنت', 'إبنت'],  
        'ancestor': ['ابن', 'إبن', 'بن']  }
    # Check for ancestor and daughter keywords using the centralized keywords dictionary
    has_daughter = any(part in keywords['daughter'] for part in parts)
    has_ancestor = any(part in keywords['ancestor'] for part in parts)
    # print(f"Has ancestor: {has_ancestor}, Has daughter: {has_daughter}")

    if not has_daughter or not has_ancestor:
        return None, None, None, None

    try:
        index_daughter = next(i for i, part in enumerate(parts) if part in keywords['daughter'])
        ancestor_indices = [i for i, part in enumerate(parts) if part in keywords['ancestor']]
        # print(f"Daughter keyword found at index: {index_daughter}")
        # print(f"Ancestor indices: {ancestor_indices}")
    except StopIteration:
        return None, None, None, None

    if len(parts) > 1:
        prenom_mere = ' '.join(parts[:index_daughter]).strip()  # Words before 'daughter'
        nom1_mere = ' '.join(parts[index_daughter + 1:ancestor_indices[0]]).strip() if ancestor_indices else None

        if len(ancestor_indices) > 1:
            if ancestor_indices[1] == len(parts) - 2:
                nom_de_famille_mere = ' '.join(parts[-2:])  # Last two parts
            else:
                nom_de_famille_mere = parts[-1]  # Last part is the family name
            nom2_mere = ' '.join(parts[ancestor_indices[0] + 1:ancestor_indices[1]]).strip() if len(ancestor_indices) > 1 else None
        else:
            nom_de_famille_mere = parts[-1]  # Last part is the family name
            nom2_mere = None

        # print(f"Prenom_mere: {prenom_mere}, Nom1_mere: {nom1_mere}, Nom2_mere: {nom2_mere}, Nom_de_famille: {nom_de_famille}")
        return prenom_mere, nom1_mere, nom2_mere, nom_de_famille_mere
    else:
        return None, None, None, None


