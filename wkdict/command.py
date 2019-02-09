import click
import wkdict

from wkdict.wkdict import requestAPI
from wkdict.wkdict import parseJSON


@click.command()
@click.argument('word')
def main(word="test"):
    rprint("(* This application is powered by Merriam-Webster Inc.'s API. *)")
    resjson = requestAPI(word)
    parseJSON(word, resjson)
