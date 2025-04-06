from nomad_media_cli.commands.cli_commands.login import login

import click
import json
import os

@click.command()
@click.option("--service-api-url", required=True, help="API URL for the service")
@click.option("--api-type", default="admin", type=click.Choice(['admin', 'portal']), help="API type [admin|portal]. Default is admin")
@click.option("--debug", default=False, type=click.BOOL, help="Enable debug mode. Default is false")
@click.option("--username", help="Username credential")
@click.option("--password", help="Password credential")
@click.pass_context
def init(ctx, service_api_url, api_type, debug, username, password):
    """Initialize the SDK and save configuration"""
    
    config_path = ctx.obj["config_path"]
    config_dir = os.path.dirname(config_path)
    os.makedirs(config_dir, exist_ok=True)
    
    if not service_api_url.startswith("https://"):
        service_api_url = f"https://{service_api_url}"
        
    debug = debug or False
    
    config = {
        "serviceApiUrl": service_api_url,
        "apiType": api_type,
        "debugMode": debug,
        "disableLogging": not debug
    }
    
    if (username or password) and not (username and password):
        click.echo("Please provide both username and password if you are providing credentials.")
        return
    
    try:
        with open(config_path, "w") as file:
            json.dump(config, file, indent=4)
            
        if not username and not password:
            click.echo(json.dumps({ "message": "Successfully initialized the CLI" }))
            
        if username and password:
            ctx.invoke(login, username=username, password=password)
            
    except Exception as e:
        click.echo(json.dumps({ "error": f"Error saving configuration: {e}" }))