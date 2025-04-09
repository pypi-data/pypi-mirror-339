import sys
import click
import requests
import tempfile
import os


@click.command()
@click.argument('url')
@click.option('--debug', is_flag=True, help='Show debug information and display code before execution')
def main(url, debug):
    """Run a Python script from a URL."""
    if debug:
        click.echo(f"Fetching Python code from URL: {url}")
    
    try:
        # Get the code from URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        code = response.text
        
        # In debug mode, show the code and ask for confirmation
        if debug:
            click.echo("\n" + "=" * 40)
            click.echo("Code to be executed:")
            click.echo("=" * 40)
            click.echo(code)
            click.echo("=" * 40)
            
            if not click.confirm("Do you want to execute this code?"):
                click.echo("Execution cancelled.")
                return
        
        # Execute the code
        if debug:
            click.echo("Executing code...")
        
        # Create a temporary file to get proper line numbers in tracebacks
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
            temp.write(code.encode('utf-8'))
            temp_path = temp.name
        
        try:
            # Execute the code using the compiled code object
            with open(temp_path) as f:
                exec(compile(f.read(), url, 'exec'), globals())
            if debug:
                click.echo("Execution completed.")
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_path)
            except:
                pass
            
    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching code: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error during execution: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()