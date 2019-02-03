#!/usr/bin/env python3
import re
import json
import click
import requests

from constants import color
from constants import URL
from constants import KEY

from pandas.io.json import json_normalize

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
      short definition, full definition, usage example for each entry. (v 0.0.1)
    """
    res = "" + '\n'
    # first section: idx. head word pron(optional)
    res += str(idx+1) + ". " + get_word(entry) + '\t' + get_pron(entry) \
            + '\t' + get_funlabel(entry) +'\n\n'
    # second section: short definition
    res += get_shortdef(entry) + '\n\n'

    # third section: full definition with use examples
    res += get_sseq(entry) + '\n\n'
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

def get_sseq(entry):
    """
    Args:
      entry: The organizational unit of a dictionary. An entry consists of 
             at minimum a headword, along with content defining or translating 
             the headword.
    Returns:
      Returns a string representation of definitions and example
       sentences: (full_definition_str, list_of_usage_example_strs).
    """
    ret = ""
    defi = entry.get("def", [dict()])
    if len(defi) < 1 or "sseq" not in defi[0] or len(defi[0]["sseq"]) < 1:
      return ret

    sseqlist = defi[0]["sseq"]
    for idx, e in enumerate(sseqlist):
      for sense_or_pseq in e:
        if "sense" == sense_or_pseq[0]:
          ret +=  get_sense(sense_or_pseq[1])
        elif "pseq" == sense_or_pseq[0]:
          ret += get_pseq(sense_or_pseq[1])
    # "sseq is not an empty list"
    return (color.GREEN + "Full definition: \n" + color.END) + ret 

def get_pseq(pseq):
  ret = ""
  for lst in pseq:
    if lst[0] == "bs":
      ret += get_bs(lst[1])
    elif lst[0] == "sense":
      ret += get_sense(lst[1])
  return ret

def get_bs(bs):
  ret = ""
  ret += get_sense(bs["sense"])
  return ret


def get_sense(sense):
    """ parse sense object and return a string representation.
    Args:
      dt_lst: contains "sn" and "dt"
    Returns:
      Returns a string representation of sense object
    """
    ret = ""
    sn = sense.get("sn", "")
    defi = get_def(sense["dt"]).strip()
    if sn == "":
      ret += defi
    elif defi == "":
      ret += defi
    else:
      print(defi)
      ret +=  (color.GREEN + sn + ". " + color.END) + defi
    return ret

def get_def(dt_lst):
    """If size of dt_lst is at least 2, then extract definition with the example
     Otherwise, extract definition text only.
    Args:
      dt_lst: consisting of one or more ['text'] or ['vis']
    Returns:
      Returns a string representation of definitions and example
    """
    ret = ""
    for e in dt_lst:
      if e[0] == "text":
        ret += (color.GREEN + e[1] + '\n' + color.END)
      elif e[0] == "vis":
        for case in e[1]:
          ret += color.DARKCYAN + "//e.g. " + case["t"] + '\n' + color.END

    return re.sub('{.*?}', '', ret)

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
    
@click.command()
@click.argument('word')
def main(word):
    ret = "(* This application is powered by Merriam-Webster Inc.'s API. *)\n"
    ret += "(* Commercial use of this app is NOT allowed! *) \n"
    resjson = requestAPI(word)
    ret += parseJSON(resjson)
    print(ret)
    


if __name__ == '__main__':
    main()

