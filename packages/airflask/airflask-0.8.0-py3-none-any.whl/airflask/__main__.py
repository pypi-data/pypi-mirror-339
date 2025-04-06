import click
import os
import sys
from airflask.deploy import run_deploy, restartapp, stopapp

@click.group()
def cli():
    """FlaskAir - Deploy Flask apps in production easily."""
    pass

@cli.command()
@click.argument("app_path")
@click.option("--domain", help="Can be used to specify domain name for website.")
@click.option("--ssl", is_flag=True, help="Enable/Get SSL for the website automatically.")
@click.option("--noredirect", is_flag=True, help="Disable automatic HTTP-to-HTTPS redirection.")
def deploy(app_path, domain, ssl, noredirect):
    """Deploy a Flask app."""
    log_file = os.path.join(app_path, "airflask.log")

    if os.path.isfile(log_file):
        click.echo("Error: airflask.log already exists. Did you mean to restart or stop the app?", err=True)
        sys.exit(1)

    if ssl and not domain:
        click.echo("Error: SSL enabled but no domain specified. Use --domain to specify one.", err=True)
        sys.exit(1)

    run_deploy(app_path, domain, ssl, noredirect)

@cli.command()
@click.argument("app_path")
def restart(app_path):
    """Restart a running Flask app."""
    log_file = os.path.join(app_path, "airflask.log")

    if not os.path.isfile(log_file):
        click.echo("Error: airflask.log not found. Did you mean to deploy the app first?", err=True)
        sys.exit(1)

    click.echo("Restarting app...")
    restartapp(app_path)
    click.echo("App restarted successfully.")

@cli.command()
@click.argument("app_path")
def stop(app_path):
    """Stop a running Flask app."""
    log_file = os.path.join(app_path, "airflask.log")

    if not os.path.isfile(log_file):
        click.echo("Error: airflask.log not found. Did you mean to deploy the app first?", err=True)
        sys.exit(1)

    click.echo("Stopping app...")
    stopapp(app_path)
    click.echo("App stopped successfully.")

@cli.command()
def about():
    """Show information about FlaskAir."""
    click.echo("FlaskAir - A simple tool to deploy Flask apps.")
    click.echo("Created by Naitik Mundra.")
    click.echo("More info: https://github.com/naitikmundra/AirFlask")

if __name__ == "__main__":
    cli()
