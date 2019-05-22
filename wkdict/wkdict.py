#!/usr/bin/env python3
import re
import json
import click
import requests
import textwrap

from wkdict.constants import color
from wiktionaryparser import WiktionaryParser

def requestAPI(word="love"):
    """ Query wiktionary API for json results using WiktionaryParser
    Args:
        word: queried word; default value, "test".
    Returns:
        word queried, and JSON table of queried word
    """    
    parser = WiktionaryParser()
    word_json = parser.fetch(word)

    return word, word_json

def parseJSON(word, table, defs, egs):
    """ Parse the json table using library 
        https://github.com/Suyash458/WiktionaryParser
    Args:
        word: string; target word we are looking up
        table: json; returned json results on queried word from Wikitionary API.
        defs: int; Maximum number of definition entries to print out.
        egs: int; Maximum number of example entries to print out.

    Raises:
        TypeError: If table is not a string type.
        ValueError: If returned table is empty.

    Returns:
        Print the definitions, pronunciations, partOfSpeech, use examples, related words, and etymology.
    """
    res = list()
    if len(table[0]["definitions"]) < 1:
        click.secho("Sorry, I☹ can't find this word in the dictionary...", 
                        fg='red', bold=True)
        click.secho('🚨Please check the spelling or try a different word🚨', 
                        fg='red', blink=True)
    else:
        for e_idx, entry in enumerate(table):
            # Print out word + prons (optional)
            pron_dict = entry.get("pronunciations", None)
            word_idx = str(e_idx+1) + ") "
            pron = ""

            if pron_dict is not None:
                prons = pron_dict.get("text", [""])
                if len(prons) != 0:
                    pron = prons[0]

            click.secho(word_idx + word, bold=True, nl=False)
            click.secho('\t' + pron, fg='bright_magenta')

            # Print out defitions
            definitions = entry.get("definitions", [])
            for def_idx, def_text in enumerate(definitions):
                # print out part of speech
                part_of_speech = def_text.get("partOfSpeech", "")
                click.secho('   🏷  ' + part_of_speech, fg='yellow')
                # print out underlined heading "definition"
                click.echo()
                click.echo('\t📗 ' + click.style('Definitions', underline=True))

                for text_id, text in enumerate(def_text.get("text", [])):
                    # print out definition entries
                    if text_id < defs:
                        def_entry = str_in_list(textwrap.wrap(text, width=80))
                        click.echo('\t☞ ' + click.style(def_entry, fg="green"))
                click.echo()
                if def_text.get("examples") != []:
                    click.echo('\t📘 ' + click.style('Examples', underline=True))
                    # print('\t' + color.UNDERLINE + 'Examples' + color.END)
                    for text_id, text in enumerate(def_text.get("examples", [])):
                        if text_id < egs:
                            eg_entry = str_in_list(textwrap.wrap(text, width=80))
                            click.echo('\t➡ ' + click.style(eg_entry, fg="blue"))
                click.echo()

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

