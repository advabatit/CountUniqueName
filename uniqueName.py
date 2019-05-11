from difflib import SequenceMatcher # To check typo

FIRST_NAME = 0
MIDDLE_NAME = 1
LAST_NAME = 2

def main():
    print(str(count_unique_names("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli")))
    print(str(count_unique_names("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli")))
    print(str(count_unique_names("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli")))
    print(str(count_unique_names("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah")))
    print(str(count_unique_names("Michele", "Egli", "Deborah", "Egli", "Michele Egli")))

    print(str(count_unique_names("Tim", "Brown", "Tiffany", "Egli", "Tiffany Egli")))
    print(str(count_unique_names("Tiff", "Brown", "Tiffany", "Egli", "Tiffany Egli")))
    print(str(count_unique_names("Tiff", "Egli", "Tiffany", "Egli", "Tiffany Egli")))
    print(str(count_unique_names("Tiff", "Egli", "Tiffany", "Egli", "Egli Tiffany")))
    print(str(count_unique_names("Tiff", "Brown", "Tiffany", "Egli", "Egli Tiffany")))


def split_name(name : str) -> str:
    '''
        - Input: string that represent the whole name.
        - Output: 3 strings (first, middle and last name)
        - Function that splits the name to first, middle and last name.
    '''

    if(not type(name) is str):
        raise TypeError("name must be a string type.")

    first = ""
    middle = ""
    last = ""
    split_name = name.split(" ")
    
    # If after split only 2 strings left, there is no middle name.
    if(len(split_name) == 2):
        middle = ""
        first, last = split_name

    elif(len(split_name) == 3):
        first, middle, last = split_name

    else:
        raise ValueError("The name must contain only first middle and last name or first and last name.")

    if(len(first) < 3 or len(last) < 3):
        raise ValueError("First and last name must contain at least 3 chars.")
    
    return (first, middle, last)


def is_compare(full_name1 : tuple,  full_name2 : tuple) -> bool:
    '''
        - Input: Tow tuples that contains the first, middle and last name
        - Output: if the names are the same
        - Function that checks if the names are the same
    '''

    if(not type(full_name1) is tuple or not type(full_name2) is tuple):
        raise TypeError("full_name1 and full_name2 must be a tuple type.")

    # Check all options
    firstName_firstName = check_similarity(full_name1[FIRST_NAME], full_name2[FIRST_NAME])
    middleName_middleName = check_similarity(full_name1[MIDDLE_NAME], full_name2[MIDDLE_NAME])
    lastName_lastName = check_similarity(full_name1[LAST_NAME], full_name2[LAST_NAME])
    firstName_lastName = check_similarity(full_name1[FIRST_NAME], full_name2[LAST_NAME])
    lastName_firstName = check_similarity(full_name1[LAST_NAME], full_name2[FIRST_NAME])

    return (middleName_middleName and
     ((firstName_firstName and lastName_lastName) or
     (firstName_lastName and lastName_firstName)))


def check_match_name_and_nick(name1 : str, name2 : str) -> bool:
    '''
        - Input: 2 strings that represents names (first and last name)
        - Output: True if the names are equal or if one of the names is a nickname. Otherwise, False.
        - Function that checks if the name is one of the possible nicknames.
    '''

    # Check the types of the variables
    if(not type(name1) is str or not type(name2) is str):
        raise TypeError("name1 and name2 must be a string type")

    if(name1 == name2):
        return True
    
    with open("names.csv", "r") as file:
        rows = file.readlines()

    # Check if the name is one of the possible nicknames from a const file (names.csv)
    for name in rows:
        name_and_nicks = name.replace("\n", "").split(",")

        if((name1.lower() in name_and_nicks) and (name2.lower() in name_and_nicks)):
            return True
    
    return False


def check_similarity(name1 : str, name2 : str, ratio : float = 0.75) -> bool:
    '''
        - Input: 2 strings that represents names (first and last name)
        - Output: True, if the ratio of the two names is equal or bigger than 0.75. Otherwise, False.
        - Function that checks how similar the strings (typo).
    '''

    if(not type(name1) is str or not type(name2) is str):
        raise TypeError("name1 and name2 must be a string type")

    return ((SequenceMatcher(None, name1, name2).ratio() >= ratio) 
    or (check_match_name_and_nick(name1, name2)))


def count_unique_names(bill_first_name : str, bill_last_name : str, ship_first_name : str,
 ship_last_name : str, bill_name_on_card : str) -> int:

    '''
        - Input: 4 Strings that represents the first and last name on the bill
                 and the name that appears on the shipping addr.
                 The lase string represent the name of the credit card owner.
        - Output: amount of unique people
        - Function that return the number of unique people.
    '''

    if(not type(bill_first_name) is str or not type(bill_last_name) is str or
       not type(ship_first_name) is str or not type(ship_last_name) is str or
       not type(bill_name_on_card) is str):
        raise TypeError("The first and last name on the bill and the shipping addr must be a string type.")
  
    unique_names = 1

    first_full_name = split_name(bill_first_name + " " + bill_last_name)
    second_full_name = split_name(ship_first_name + " " + ship_last_name)

    # Check if the bill person and the ship person are different
    if(not is_compare(first_full_name, second_full_name)):
        unique_names += 1

    return unique_names


if __name__ == "__main__":
    main()