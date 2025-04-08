import click
from datetime import datetime
from rich.console import Console
from elog_cli.auth_manager import AuthManager  # Import the AuthManager type
from elog_cli.hl_api import ElogAPIError, ElogApi

console = Console()

@click.command()
@click.argument("event_at_start", nargs=1)
@click.argument("event_at_end", nargs=1)
@click.pass_context
def update_ngram(ctx, event_at_start:str, event_at_end:str):
    """
    Update the entries ngram vector.

    This command updates the ngram vector for entries in the Elog system.
    
  Parameters:
        event_at_start (str): Represents the evetAt to start including entries (YYYY-MM-DDTHH:MM:SS+00.00).
        event_at_end (str): Represents the event at that contains the end of the entries (YYYY-MM-DDTHH:MM:SS+00.00).

    Raises:
        click.ClickException: If the update fails due to an API error.
    """
    elog_api:ElogApi = ctx.obj["elog_api"] # Retrieve shared ElogApi
    auth_manager:AuthManager = ctx.obj["auth_manager"]  # Retrieve shared AuthManager
    elog_api.set_authentication_token(auth_manager.get_access_token())  # Set the authentication token
    try:
        jobId:str = None
        #check if event_at_start if after event_at_end
        if datetime.fromisoformat(event_at_start) > datetime.fromisoformat(event_at_end):
            jobId = elog_api.update_ngram_for_entries(event_at_end, event_at_start)
            console.print(f"NGram vector update started with id: {jobId}")
        else:
            jobId = elog_api.update_ngram_for_entries(event_at_start, event_at_end)
            console.print(f"NGram vector update started with id: {jobId}")
       
    except ElogAPIError as e:
        raise click.ClickException(e)
