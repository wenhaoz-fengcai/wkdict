#!/usr/bin/env python3
import re
import json
import click
import requests

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

def parseJSON(word, table, n):
    """ Parse the json table using library 
        https://github.com/Suyash458/WiktionaryParser
    Args:
        word: string; target word we are looking up
        table: json; returned json results on queried word from Wikitionary API.
        n: int; Maximum number of definition entries/examples shown.

    Raises:
        TypeError: If table is not a string type.
        ValueError: If returned table is empty.

    Returns:
        Returns the formated string
    """
    res = ""
    if len(table[0]["definitions"]) < 1:
        res += click.style("🚨Sorry, wkdict can't find this word in the dictionary...🚨\n", 
                        fg='red', bold=True)
        res += '\n'
        res += click.style('The word you typed is {}\n'.format(word), 
                        fg='bright_red', bold=True)
    else:
        for e_idx, entry in enumerate(table):
            # word + prons (optional)
            pron_dict = entry.get("pronunciations", None)
            word_idx = str(e_idx+1) + ") "
            pron = ""

            if pron_dict is not None:
                prons = pron_dict.get("text", [""])
                if len(prons) != 0:
                    pron = prons[0]

            res += click.style(word_idx + word, bold=True)
            res += click.style('\t' + pron + '\n', fg='bright_magenta')

            # defitions
            definitions = entry.get("definitions", [])
            for def_idx, def_text in enumerate(definitions):
                # part of speech
                part_of_speech = def_text.get("partOfSpeech", "")
                res += click.style('   🏷  ' + part_of_speech + '\n', fg='yellow')
                # underlined heading "definition"
                res += '\n'
                res += click.style('\t📗 ' + click.style('Definitions\n', 
                                                            underline=True))

                for text_id, text in enumerate(def_text.get("text", [])):
                    # definition entries
                    if text_id < n:
                        formated_def = click.wrap_text(text, width=65,
                                        initial_indent='\t☞ ', 
                                        subsequent_indent='\t  ',
                                        preserve_paragraphs=True)
                        res += click.style(formated_def+'\n', fg='green')

                res += '\n'
                if def_text.get("examples") != []:
                    res += click.style('\t📘 ' + click.style('Examples', 
                                                        underline=True) + '\n')
                    for text_id, text in enumerate(def_text.get("examples", [])):
                        if text_id < n:
                            text = click.style(text, fg='blue')
                            formated_eg = click.wrap_text(text, width=65,
                                        initial_indent='\t➡ ', 
                                        subsequent_indent='\t  ',
                                        preserve_paragraphs=True)
                            res += formated_eg + '\n'
    return res