from difflib import SequenceMatcher # To check typo


def main():
    print(str(count_unique_names("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli")))
    print(str(count_unique_names("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli")))
    print(str(count_unique_names("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli")))
    print(str(count_unique_names("Deborah", "Egli", "Deborah", "Egli", "Egli Deborah")))
    print(str(count_unique_names("Michele", "Egli", "Deborah", "Egli", "Michele Egli")))


def split_name(name : str) -> str:
    '''
        - Input: string that represent the whole name.
        - Output: 3 strings (first, middle and last name)
        - Function that splits the name to first, middle and last name.
    '''

    first = ""
    middle = ""
    last = ""
    splited_name = name.split(" ")
    
    # If after split only 2 strings left, there is no middle name.
    if(len(splited_name) == 2):
        middle = ''
        first, last = splited_name

    elif(len(splited_name) == 3):
        first, middle, last = splited_name

    else:
        ValueError("The name must contain only first middle and last name or first and last name.")

    if(len(first) < 3 or len(last) < 3):
        ValueError("First and last name must contain at least 3 chars.")
    
    return (first, middle, last)


def is_compare(first : tuple,  second : tuple) -> bool:
    '''
        - Input: Tow tuples that contains the first, middle and last name
        - Output: if the names are the same
        - Function that checks if the names are the same
    '''

    # Check all options
    firstName_firstName = check_similarity(first[0], second[0])
    middleName_middleName = check_similarity(first[1], second[1])
    lastName_lastName = check_similarity(first[2], second[2])
    firstName_lastName = check_similarity(first[0], second[2])
    lastName_firstName = check_similarity(first[2], second[0])

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
    if(not isinstance(name1, str) or not isinstance(name2, str)):
        TypeError("name1 and name2 must be a string type")

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

    if(not isinstance(name1, str) or not isinstance(name2, str)):
        TypeError("name1 and name2 must be a string type")

    return ((SequenceMatcher(None, name1, name2).ratio() >= ratio) 
    or (check_match_name_and_nick(name1, name2)))


def count_unique_names(bill_first_name : str, bill_last_name : str, ship_first_name : str,
 ship_last_name : str, bill_name_on_card : str) -> int:

    '''
        - Input: 4 Strings that represents the first and last name of the name on the bill
                 and the name of the shipping addr. The lase string represent the name of the
                 credit card owner.
        - Output: amount of unique people
        - Function that return the number of unique people.
    '''
    unique_names = 1

    first = split_name(bill_first_name + " " + bill_last_name)
    second = split_name(ship_first_name + " " + ship_last_name)

    # Check if the bill person and the ship person are differents
    if(not is_compare(first, second)):
        unique_names += 1

    return unique_names


if __name__ == "__main__":
    main()