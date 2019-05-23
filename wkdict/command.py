import click
import wkdict

from wkdict.wkdict import requestAPI
from wkdict.wkdict import parseJSON


@click.command()
@click.argument('word')
@click.option('--limit', type=int, default=3, show_default=True,
    help="Maximum number of entries/examples shown.")
@click.version_option()
def main(word, limit):
    click.echo()
    click.secho("🔅 This application is powered by Wiktionary's API 🔅", 
                fg='cyan', bold=True, blink=True)
    click.echo()
    word, resjson = requestAPI(word)
    ret = parseJSON(word, resjson, limit)
    click.echo(ret)
