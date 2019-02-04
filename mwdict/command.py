import mwdict

from mwdict.mwdict import requestAPI
from mwdict.mwdict import parseJSON

import click

@click.command()
@click.argument('word')
def main(word="test"):
    ret = "(* This application is powered by Merriam-Webster Inc.'s API. *)\n"
    ret += "(* Commercial use of this app is NOT allowed! *) \n"
    resjson = requestAPI(word)
    ret += parseJSON(resjson)
    print(ret)
