import click
from vagoncli.helpers import api_generator


@click.command()
def machine_types():
    """List available performance alternatives."""

    response = api_generator(
        "GET", "/app-stream-management/cli/applications/available-machine-types"
    )
    if response.status_code != 200:
        click.echo(f"Failed with status code: {response.status_code}")
        if response.text:
            click.echo(f"Response: {response.text}")
        return

    response_json = response.json()

    click.echo("Performance / ID")
    for machine_type in response_json.get("machine_types"):
        click.echo(f"{machine_type['name']} / {machine_type['machine_type_id']}")
