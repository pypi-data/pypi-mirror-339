import re
import subprocess
import click
import pandas as pd
from h5ad_validate.get_data import get_ref

class Validator:
    """HTAN h5ad Validator."""

    def __init__(self, adata, h5ad_path, output_file):
        """Constructor with anndata data structure."""
        self.adata = adata
        self.h5ad_path = h5ad_path
        self.output_file = output_file
        self.error_list = []
        # pass code initially set to pass. update to [1, 0] if fail cellxgene,
        # [0, 1] if fail HTAN. [1, 1] if fail both.
        self.pass_code = [0, 0]
        self.check_cell_x_gene(h5ad_path, output_file)
        self.check_donor_ids(adata.obs)
        self.check_sample_ids(adata.obs)
        self.check_cell_enrichment(adata.obs)
        self.check_intron_inclusion(adata.obs)

    def check_cell_x_gene(self, h5ad_path, output_file):
        """run cell x gene validation"""
        click.echo(click.style("Running cellxgene-schema", fg="green"))

        def run_cellxgene(h5ad_path, output_file):
            try:
                process = subprocess.run(
                    ["cellxgene-schema", "validate", h5ad_path],
                    capture_output=True,
                    text=True,
                    check=False  # Don't raise exception on non-zero exit code
                )
                with open(output_file, "w") as f:
                    f.write("cellxgene-schema output: ")
                    f.write(process.stderr)
                return process.returncode
            except Exception as e:
                print(f"An error occurred: {e}")
                return -1  # Return -1 to indicate an error during execution

        cellxgene = run_cellxgene(h5ad_path, output_file)

        if cellxgene != 0:
            self.pass_code[0] = 1
            click.echo(click.style("Cellxgene run has errors. Please note "
                                   "errors or warnings in the output file.",
                                   fg="red"))
        else:
            click.echo(click.style("Cellxgene run successful. Please check "
                                   "the output file to see if warnings exist.",
                                   fg="green"))

    def check_donor_ids(self, obs):
        """Check Donor IDs."""
        click.echo(click.style("Running HTAN-specific validation", fg="green"))
        pattern = r"^(HTA20[0-9])(?:_0000)?(?:_\d+)?(?:_EXT\d+)?"
        if "donor_id" in obs:
            donor_list = list(obs.donor_id.unique())
            for donor_id in donor_list:
                # TODO:  Add RegEx Matching
                if re.match(pattern, donor_id):
                    pass
                else:
                    self.error_list.append("Invalid donor_id: " + donor_id)
                    self.pass_code[1] = 1
        else:
            self.error_list.append("donor_id was not found in obs")
            self.pass_code[1] = 1

    def check_sample_ids(self, obs):
        """Check Sample IDs."""
        pattern = (
            r"^(HTA20[0-9])(?:_0000)?(?:_\d+)?(?:_EXT\d+)?_(B|D)\d{1,50}$")
        if "sample_id" in obs:
            sample_list = list(obs.sample_id.unique())
            for sample_id in sample_list:
                # TODO:  Add RegEx Matching
                if re.match(pattern, sample_id):
                    pass
                else:
                    self.error_list.append("Invalid sample_id: " + sample_id)
                    self.pass_code[1] = 1
        else:
            self.error_list.append("sample_id was not found in obs")
            self.pass_code[1] = 1

    def check_cell_enrichment(self, obs):
        """Check Cell Enrichment."""
        # POSSIBLE TO DO: add step to check for valid CL term
        pattern = (
            r"^CL:(00000000|[0-9]{7}[+-])$")
        ref_file = get_ref()
        CL_ontology = pd.read_csv(ref_file, sep='\t')
        CL_valid_terms = list(CL_ontology['Permissible Value'])
        CL_valid_terms.append("CL:00000000")
        if "cell_enrichment" in obs:
            cell_enrichment_list = list(obs.cell_enrichment.unique())
            for cell_enrich_term in cell_enrichment_list:
                CL_term = re.sub('[+-]', '', cell_enrich_term)
                if re.match(pattern, cell_enrich_term):
                    if CL_term in CL_valid_terms:
                        pass
                    else:
                        self.error_list.append("Invalid cell_enrichment term "
                                               + cell_enrich_term +
                                               ". CL_term is not in "
                                               "CL_codes_human.tsv")
                        self.pass_code[1] = 1
                else:
                    self.error_list.append("Invalid cell_enrichment term "
                                           + cell_enrich_term +
                                           ". obs.cell_enrichment must be "
                                           "CL term followed by a '+' or '-' "
                                           "sign or CL:00000000 if no "
                                           "enrichment.")
                    self.pass_code[1] = 1
        else:
            self.error_list.append("cell_enrichment was not found in obs")
            self.pass_code[1] = 1

    def check_intron_inclusion(self, obs):
        """Check intron inclusion"""
        valid_values = ['yes', 'no']
        if "intron_inclusion" in obs:
            intron_inclusion_list = (
                list(obs.intron_inclusion.unique().astype(str)))
            for intron_include_term in intron_inclusion_list:
                if intron_include_term in valid_values:
                    pass
                else:
                    self.error_list.append("Invalid intron_inclusion term: " +
                                           intron_include_term
                                           + ". Must be 'yes' or 'no'.")
                    self.pass_code[1] = 1
        else:
            self.error_list.append("intron_inclusion was not found in obs")
            self.pass_code[1] = 1
