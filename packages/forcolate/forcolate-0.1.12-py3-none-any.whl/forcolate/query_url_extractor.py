   
import re


def extract_query_and_folder(query):
    """
    Extracts the query and folder path from the input string. "
    """

    # extract any folder path from the query
    folder_list = re.findall(r'folder:\s*([^\s]+)', query)

    # replace all folder paths in the query with empty string
    query = re.sub(r'folder:\s*[^\s]+', '', query)
        
    # append the source_directory to the list

    # remove any duplicates from the list
    folder_list = list(set(folder_list))
    # remove any empty strings from the list
    folder_list = [folder for folder in folder_list if folder]
    # remove any leading/trailing whitespace from each folder path
    folder_list = [folder.strip() for folder in folder_list]
    
    return query, folder_list