from importlib import resources

def get_ref():
    ''' Make reference file available for users'''
    return resources.files("h5ad_validate.reference") / "CL_codes_human.tsv"

def get_example():
    ''' Make example file available for users'''
    return resources.files("h5ad_validate.example") / "HTAN_h5ad_exemplar_2025_03_03.h5ad"