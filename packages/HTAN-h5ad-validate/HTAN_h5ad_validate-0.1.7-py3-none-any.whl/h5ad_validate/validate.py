"""
HTAN h5ad Validator.
"""
from h5ad_validate.validator import Validator
from h5ad_validate.get_data import get_example
import anndata
import click
import sys


@click.command()
@click.argument("h5ad_path")
@click.argument("output_file")
def run_validate(h5ad_path, output_file):
    """HTAN h5ad Validator."""
    click.echo(click.style("HTAN h5ad File Validator", bg="blue", fg="white"))
    if h5ad_path == "example":
        h5ad_path = get_example()

    click.echo(click.style("File:  " + str(h5ad_path), fg="green"))

    """Make sure file exists and can be opened"""
    try:
        adata = anndata.read_h5ad(h5ad_path)
    except FileNotFoundError:
        click.echo(click.style("File not found: " + h5ad_path, fg="red"))
        sys.exit()
    except Exception as e:
        click.echo(click.style(
            "An error occurred while trying to open " + h5ad_path, fg="red"))
        click.echo(click.style(e, fg="red"))
        sys.exit()

    """Create Validator object"""
    validator = Validator(adata, h5ad_path, output_file)

    """Get error list (HTAN-specific errors only) and validator pass code"""
    error_list = validator.error_list
    pass_code = validator.pass_code
    if pass_code == [0, 0] and len(error_list) == 0:
        click.echo(click.style("Validation Passed!", fg="green"))
    elif pass_code[1] != 0:
        click.echo(click.style("HTAN Validation Failed.", fg="red"))
        click.echo(click.style(
            "Please check output file for errors.", fg="red"))

        """Append HTAN-specific errors to output file."""
        with open(output_file, "a+") as f:
            f.write("\nHTAN-specific Validation Errors: \n")
            for error in error_list:
                f.write(f"{error} \n")


if __name__ == "__main__":
    run_validate()
