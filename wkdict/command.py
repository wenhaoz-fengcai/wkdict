import click
import wkdict

from wkdict.wkdict import requestAPI
from wkdict.wkdict import parseJSON


@click.command()
@click.argument('word')
def main(word="test"):
    print("(* This application is powered by Wiktionary's API. *)")
    word, resjson = requestAPI(word)
    parseJSON(word, resjson)
