import json
import click
import requests
import textwrap

from constants import color
from constants import URL
from constants import KEY

def requestAPI(word="test"):
    """ Query merriam-webster dictionary API for json results
    Args:
      word: queried word; default value, "test".
    Raises:
      ApiError: If response status code is not 200.
    Returns:
      JSON table of queried word
    """    
    resp = requests.get(URL + word + '?key=' + KEY)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('Ooops, something went wrong; GET Status {}'.format(resp.status_code))
    return resp.json()

def parseJSON(table):
    """ Parse the json table based on 
        "https://www.dictionaryapi.com/products/json#term-pron" 
    Args:
      table: returned json results on queried word from merriam-webster API.
    Raises:
      TypeError: If table is not a string type.
      ValueError: If returned table is empty.
    Returns:
      String representation of a sequence of returned parse entry. (v 0.0.1)
    """
    assert isinstance(table, list)
    res = ""
    if len(table) < 1:
        raise ValueError('Empty look-up result returned')
    else:
        for idx, entry in enumerate(table):
            res += parse_entry(idx, entry)
    return res  

def parse_entry(idx, entry):
    """
    Args:
      idx: index of the entry in the table
      entry: The organizational unit of a dictionary. An entry consists of 
             at minimum a headword, along with content defining or translating 
             the headword.
    Returns:
      String representation of headword, pronunciation, functional label, 
      short definition, full definition, use cases for each entry. (v 0.0.1)
    """
    res = "" + '\n'
    # first line: idx. head word pron(optional)
    res += str(idx+1) + ". " + get_word(entry) + '\t' + get_pron(entry) \
            + '\t' + get_funlabel(entry) +'\n'
    # second line: short definition
    res += get_shortdef(entry) + '\n'
    return res


def get_word(entry):
    """
    Args:
      entry: The organizational unit of a dictionary. An entry consists of 
             at minimum a headword, along with content defining or translating 
             the headword.
    Returns:
      Headword.
    """
    return color.BOLD + entry["hwi"]["hw"] + color.END

def get_funlabel(entry):
    """Get the grammatical function of a headword or undefined entry word, 
       such as "noun" or "adjective".
    Args:
      entry: The organizational unit of a dictionary. An entry consists of 
             at minimum a headword, along with content defining or translating 
             the headword.
    Returns:
      Function label. Or, return empty string, ""
    """
    fl = entry.get("fl", "")
    if fl == "":
        return ""
    return color.PURPLE + '<' + entry["fl"] + '>' + color.END

def get_pron(entry):
    """Get written pronunciation in Merriam-Webster format of queried headword. If 
       entry doesn't contains this field, return empty string, "".
    Args:
      entry: The organizational unit of a dictionary. An entry consists of 
             at minimum a headword, along with content defining or translating 
             the headword.
    Returns:
      A written pronunciation in Merriam-Webster format. Or, return empty 
      string, ""
    """
    prs = entry["hwi"].get("prs", [dict()])
    mw = prs[0].get("mw", "")
    if mw == "":
        return color.PURPLE +  color.END
    return color.PURPLE + '[' + mw + ']' + color.END

def get_shortdef(entry):
    """Get short definition of queried headword. If entry doesn't contains this field,
       return empty string, "".
    Args:
      entry: The organizational unit of a dictionary. An entry consists of 
             at minimum a headword, along with content defining or translating 
             the headword.
    Returns:
      A short definition provides a highly abridged version of the main definition section, 
      consisting of just the definition text for the first three senses. Or, return empty 
      string, ""
    """
    shortdef = str_in_list(entry.get("shortdef", [""]))
    if shortdef == "":
        return ""
    return (color.RED + "Short definition: \n"
            + '* ' + str_in_list(entry.get("shortdef", [""])) + color.END)

def str_in_list(lst):
    """Concatenate all strings in a list of strings. For example,
       this function returns "Hello World!" from ["Hello", "World!"].
    Args:
      lst: A list contains all strings to be concatenated.
    Raises:
      TypeError: If lst is not a string type.
    Returns:
      The concatenated string.
    """
    assert isinstance(lst, list)

    ret = ""
    for e in lst:
        ret += e
    return ret

def pretty_print(lst):
    """Pretty_print func print each string line by line.
    Args:
      lst: A list contains all strings.
    Raises:
      TypeError: If lst is not a string type.
    """
    assert isinstance(lst, list)
    for e in lst:
        print(e)

def main():
    ret = "(* This application is powered by Merriam-Webster Inc.'s API. *)\n"
    ret += "(* Commercial use of this app is NOT allowed! *) \n"
    resjson = requestAPI("love")
    ret += parseJSON(resjson)
    print(ret)
    # pretty_res = textwrap.wrap(ret)
    # pretty_print(pretty_res)


if __name__ == '__main__':
    main()

