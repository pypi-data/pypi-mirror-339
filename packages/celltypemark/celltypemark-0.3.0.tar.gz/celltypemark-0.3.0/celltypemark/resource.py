from collections import defaultdict
import pathlib

def download_resource(resource_url: str, save_path: str):
    ## download from given url and save to given path
    import requests
    response = requests.get(resource_url)
    with open(save_path, 'w') as hubmap:
        hubmap.write(response.text)

def load_resource(resource_path: pathlib.Path=pathlib.Path(__file__).parent.joinpath("HuBMAP_ASCT_plus_B_augmented_w_RNAseq_Coexpression.txt"), resource_url: str='https://maayanlab.cloud/Enrichr/geneSetLibrary?mode=text&libraryName=HuBMAP_ASCT_plus_B_augmented_w_RNAseq_Coexpression') -> defaultdict:
    ## if resource_path is not exist, download it
    if not resource_path.exists():
        download_resource(resource_url, resource_path)
    marker_genes = defaultdict(list)
    with open(resource_path, 'r') as resdata:
        for line in resdata:
            marker_genes[line.strip().split('\t\t')[0]] = line.strip().split('\t\t')[1].split('\t')
    return marker_genes

