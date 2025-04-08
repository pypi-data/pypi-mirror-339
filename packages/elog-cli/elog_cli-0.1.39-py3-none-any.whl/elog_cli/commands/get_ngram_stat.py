import click
from rich.console import Console
from elog_cli.auth_manager import AuthManager  # Import the AuthManager type
from elog_cli.hl_api import ElogAPIError, ElogApi
from elog_cli.elog_management_backend_client.models import EntryProcessingStats
from elog_cli.elog_management_backend_client.types import UNSET
console = Console()

@click.command()
@click.argument("job_id", nargs=1)
@click.pass_context
def get_ngram_stat(ctx, job_id: str):
    """
    Get the statistics of the entry processing.
    This command retrieves the statistics of the entry processing in the Elog system.
    Parameters:
        job_id (str): Represent the job id for wich we whant the statistic
    Raises:
        click.ClickException: If the retrieval fails due to an API error.
    """
    elog_api:ElogApi = ctx.obj["elog_api"] # Retrieve shared ElogApi
    auth_manager:AuthManager = ctx.obj["auth_manager"]  # Retrieve shared AuthManager
    elog_api.set_authentication_token(auth_manager.get_access_token())  # Set the authentication token
    try:
        stat:EntryProcessingStats = elog_api.get_stat_for_ngram_task(job_id)
        print_stat(stat)
    except ElogAPIError as e:
        raise click.ClickException(e)

def print_stat(stat: EntryProcessingStats):
    """
    Print the statistics of the entry processing.

    Args:
        stat (EntryProcessingStats): The statistics to print.
    """
    console.print(f"Processed entries: {stat.processed_entries}")
    console.print(f"Failed entries: {stat.failed_entries}")
    console.print(f'Completed: {stat.completed}')
    if stat.error_message != UNSET:
        console.print(f"Error message: {stat.error_message}")