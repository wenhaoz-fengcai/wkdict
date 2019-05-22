import click
import wkdict

from wkdict.wkdict import requestAPI
from wkdict.wkdict import parseJSON


@click.command()
@click.argument('word')
@click.option('--defs', is_flag=False, 
    help="Maximum number of definition entries to print out.")
@click.option('--egs', is_flag=False, 
    help="Maximum number of example entries to print out.")
@click.version_option()
def main(word="love", defs="3", egs="3"):
    click.secho("🔅 This application is powered by Wiktionary's API 🔅", fg='yellow')
    click.echo()
    word, resjson = requestAPI(word)
    parseJSON(word, resjson, int(defs), int(egs))
    click.echo()
