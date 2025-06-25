import click

from .app_layout import app


@click.command()
@click.option("--local", is_flag=True, help="Run in local mode.")
@click.option("--server", is_flag=True, help="Run in server mode.")
@click.option(
    "--host", default="0.0.0.0", help="Host address for server mode."
)
@click.option(
    "--port", default=8050, type=int, help="Port number for server mode."
)
def main(local, server, host, port):
    if local and server:
        click.echo("Error: Cannot use both --local and --server.")
        return

    if local:
        app.run(debug=True)
    elif server:
        app.run(host=host, port=port, debug=False)
    else:
        click.echo("Error: Must specify either --local or --server.")


if __name__ == "__main__":
    main()
