#!/usr/bin/env python3
import re
import json
import click
import requests
import textwrap

from wkdict.constants import color
from wiktionaryparser import WiktionaryParser

def requestAPI(word="test"):
    """ Query wiktionary API for json results using WiktionaryParser
    Args:
      word: queried word; default value, "test".
    Returns:
      word queried, and JSON table of queried word
    """    
    parser = WiktionaryParser()
    word_json = parser.fetch(word)

    return word, word_json

def parseJSON(word, table):
    """ Parse the json table based on 
        https://github.com/Suyash458/WiktionaryParser
    Args:
      table: returned json results on queried word from merriam-webster API.
    Raises:
      TypeError: If table is not a string type.
      ValueError: If returned table is empty.
    Returns:
      Print the definitions, pronunciations, partOfSpeech, use examples, related words, and etymology. (v 0.0.3)
    """
    res = list()
    if len(table[0]["definitions"]) < 1:
        print(color.RED + 'Empty look-up result returned' + color.END)
    else:
        for e_idx, entry in enumerate(table):
            # Print out prons
            pron_dict = entry.get("pronunciations", None)
            if pron_dict is None:
                print(str(e_idx+1) + ") " + color.BOLD + word + color.END)
            else:
                # get prons list
                prons = pron_dict.get("text", [""])
                pron = ""
                if len(prons) != 0:
                    pron = prons[0]
                print(str(e_idx+1) + ") " + color.BOLD + word + color.END + '\t' + color.PURPLE + pron + color.END)

            # Print out defitions
            definitions = entry.get("definitions", [])
            for def_idx, def_text in enumerate(definitions):
                print('\t' + color.YELLOW + str(def_idx+1) + " " + def_text.get("partOfSpeech", "") + color.END)
                print('\t' + color.UNDERLINE + 'Definitions' + color.END)
                for text_id, text in enumerate(def_text.get("text", [])):
                    print('\t' +  color.GREEN + "-. "   + str_in_list(textwrap.wrap(text, width=80)) + color.END)

                if def_text.get("examples") != []:
                  print('\t' + color.UNDERLINE + 'Examples' + color.END)
                  for text_id, text in enumerate(def_text.get("examples", [])):
                      print('\t'  +  color.BLUE + "// "   + str_in_list(textwrap.wrap(text, width=80)) + color.END)


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
    ret = "(* This application is powered by Wiktionary Inc.'s API. *)\n"
    word, resjson = requestAPI(word)
    parseJSON(word, resjson)

if __name__ == '__main__':
    main()

