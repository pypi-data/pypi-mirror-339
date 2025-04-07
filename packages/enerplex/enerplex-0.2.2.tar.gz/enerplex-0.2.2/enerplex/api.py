import requests
import os
import dataclasses

from .utils import logger, download_file
from .interface import *
from datetime import datetime, timedelta
from pathlib import Path

_AUTH_TOKEN: str = None
_AUTH_EXPIRES_IN: datetime = None

class APIError(Exception):
    """
    ### Exception raised for errors returned by the API.

    Attributes:
        res (ErrorResponse): The response object containing error details.
    """
    def __init__(self, res: ErrorResponse):
        logger.critical(res.errorMessage + "\033[1;33m" + f"(api version {res.api_version})")
        super().__init__(res.errorMessage)
        self.res = res

def _interfere_errors(res: ApiResponse) -> ApiResponse:
    """
    ### Checks if the API response contains errors and raises an exception if it does.

    Args:
        res (ApiResponse): The API response object to check.

    Returns:
        ApiResponse: The original response if no errors are found.

    Raises:
        APIError: If the response indicates a failure.
    """
    if not res.successful or len(res.errorMessage) != 0:
        raise APIError(res)

    return res

def _get_auth_token(force_refresh: bool = False) -> str:
    """
    ### Retrieves an authentication token for the API.

    Args:
        force_refresh (bool): If True, forces the retrieval of a new token even if the current token is valid.

    Returns:
        str: A valid authentication token.
    """
    global _AUTH_TOKEN
    global _AUTH_EXPIRES_IN

    if _AUTH_TOKEN and (_AUTH_EXPIRES_IN - datetime.today()).seconds > 0 and not force_refresh:
        return _AUTH_TOKEN

    raw_res = requests.post(f"{os.environ.get('ENERPLEX_API_URL')}/auth/login", data={
        "name": os.environ.get("ENERPLEX_API_USER"),
        "password": os.environ.get("ENERPLEX_API_USER_PASSWORD")
    })

    if not raw_res.ok:
        raise ConnectionError(raw_res.content)

    # Parse to login response
    res: LoginResponse = _interfere_errors(LoginResponse(**raw_res.json()))

    expires_in_days = int(res.expiresIn.split("d")[0])

    _AUTH_TOKEN = res.token
    _AUTH_EXPIRES_IN = datetime.now() + timedelta(days=expires_in_days)

    logger.debug(f"Got new auth token for user {os.environ.get('ENERPLEX_API_USER')}.")

    return res.token

def get_target_proteins() -> list[DBTargetProtein]:
    """
    ### Retrieves all target proteins stored in the database.

    Returns:
        list[DBTargetProtein]: A list of target protein objects.
    """
    headers = {"Authorization": _get_auth_token()}
    res = _interfere_errors(DataResponse(**requests.get(f"{os.environ.get('ENERPLEX_API_URL')}/data/target-proteins", headers=headers).json()))
    return [DBTargetProtein(**o) for o in res.data]

def get_ligands(protein_identifier: Union[DBTargetProtein, int, str] = None) -> list[DBProteinLigandComplex]:
    """
    ### Retrieves all stored ligands in the database. Optionally filters ligands for a specific target protein.

    Args:
        protein_identifier (Union[DBTargetProtein, int, str], optional): Specifies a target protein by object, ID, or unique name.

    Returns:
        list[DBProteinLigandComplex]: A list of ligand complex objects.
    """
    headers = {"Authorization": _get_auth_token()}
    url = f"{os.environ.get('ENERPLEX_API_URL')}/data/ligands"

    if protein_identifier:
        if isinstance(protein_identifier, str):
            url += f"?target_protein_name={protein_identifier}"
        elif isinstance(protein_identifier, int):
            url += f"?target_protein_id={protein_identifier}"
        elif isinstance(protein_identifier, DBTargetProtein):
            url += f"?target_protein_id={protein_identifier.id}"
        else:
            raise TypeError(f"Type of complex must be one of DBTargetProtein, int or string, not '{type(protein_identifier)}'.")

    res = _interfere_errors(DataResponse(**requests.get(url, headers=headers).json()))
    return [DBProteinLigandComplex(**o) for o in res.data]

def get_embeddings() -> list[DBTargetProtein]:
    """
    ### Retrieves all embeddings stored in the database.

    Returns:
        list[DBTargetProtein]: A list of embedding objects.
    """
    headers = {"Authorization": _get_auth_token()}
    res = _interfere_errors(DataResponse(**requests.get(f"{os.environ.get('ENERPLEX_API_URL')}/data/embeddings", headers=headers).json()))
    return [DBProteinLigandComplexEmbedding(**o) for o in res.data]

def get_mmxbsa_calculations() -> list[DBMMXBSACalculation]:
    """
    ### Retrieves all MM/XBSA calculations

    Returns:
        list[DBMMXBSACalculation]: A list of MM/XBSA calculations.
    """
    headers = {"Authorization": _get_auth_token()}
    res = _interfere_errors(DataResponse(**requests.get(f"{os.environ.get('ENERPLEX_API_URL')}/data/mmxbsa", headers=headers).json()))
    return [DBMMXBSACalculation(**o) for o in res.data]

def get_fep_calculations() -> list[DBFEPCalculation]:
    """
    ### Retrieves all FEP calculations

    Returns:
        list[DBFEPCalculation]: A list of FEP calculations.
    """
    headers = {"Authorization": _get_auth_token()}
    res = _interfere_errors(DataResponse(**requests.get(f"{os.environ.get('ENERPLEX_API_URL')}/data/fep", headers=headers).json()))
    return [DBFEPCalculation(**o) for o in res.data]

def get_random_energy_calculation_targets(n: int = 5) -> list[DBProteinLigandComplex]:
    """
    ### Retrieves a random amount of targets that dont have energie calculations yet.

    Returns:
        list[DBProteinLigandComplex]: A list of targets.
    """
    headers = {"Authorization": _get_auth_token()}
    res = _interfere_errors(DataResponse(**requests.get(f"{os.environ.get('ENERPLEX_API_URL')}/data/energy-targets?n={n}", headers=headers).json()))
    return [DBProteinLigandComplex(**o) for o in res.data]


def download_target_protein_file(target: DBTargetProtein, path: Path, exists_ok: bool = True) -> None:
    """
    ### Downloads the file for a specific target protein.

    Args:
        target (DBTargetProtein): The target protein object.
        path (Path): The file path to save the downloaded file.
        exists_ok (bool): If False, raises an error if the file already exists.
    """
    headers = {"Authorization": _get_auth_token()}
    download_file(
        f"{os.environ.get('ENERPLEX_API_URL')}/data/target-protein/{target.id}/file",
        headers,
        path=path,
        exist_ok=exists_ok
    )

def download_ligand_file(target: DBProteinLigandComplex, path: Path, exists_ok: bool = True) -> None:
    """
    ### Downloads the file for a specific ligand complex.

    Args:
        target (DBProteinLigandComplex): The ligand complex object.
        path (Path): The file path to save the downloaded file.
        exists_ok (bool): If False, raises an error if the file already exists.
    """
    headers = {"Authorization": _get_auth_token()}
    download_file(
        f"{os.environ.get('ENERPLEX_API_URL')}/data/ligand/{target.id}/file",
        headers,
        path=path,
        exist_ok=exists_ok
    )

def download_embedding_file(target: DBProteinLigandComplexEmbedding, path: Path, exists_ok: bool = True) -> None:
    """
    ### Downloads the file for a specific embedding.

    Args:
        target (DBProteinLigandComplexEmbedding): The embedding object.
        path (Path): The file path to save the downloaded file.
        exists_ok (bool): If False, raises an error if the file already exists.
    """
    headers = {"Authorization": _get_auth_token()}
    download_file(
        f"{os.environ.get('ENERPLEX_API_URL')}/data/embedding/{target.id}/file",
        headers,
        path=path,
        exist_ok=exists_ok
    )



def upload_ligand(
    target_name: str,
    score: float,
    scoring_function: str,
    ligand_structure_file_path: Path,
    smiles: str,
    sa_score: float = 0,
    vina_score: float = 0,
    qed_score: float = 0
) -> DBProteinLigandComplex:
    """
    ### Uploads a ligand structure file to the database.

    Args:
        target_name (str): The name of the target protein.
        score (float): The docking score of the ligand.
        scoring_function (str): The scoring function used.
        ligand_structure_file_path (Path): The file path of the ligand structure file.
        smiles (str): The smiles string of the ligand.
        sa_score (float): The sa score of the ligand.
        vina_score (float): The vina docking score of the ligand.
        qed_score (float): The qed score of the ligand.
    Returns:
        DBProteinLigandComplex: The uploaded ligand complex object.

    Raises:
        FileNotFoundError: If the specified ligand structure file does not exist.
    """
    headers = {"Authorization": _get_auth_token()}
    data = {
        "target_name": target_name,
        "score": score,
        "scoring_function": scoring_function,
        "smiles": smiles,
        "sa_score": sa_score,
        "vina_score": vina_score,
        "qed_score": qed_score,
    }
    files = {"ligand": open(ligand_structure_file_path, "rb")}

    if not os.path.exists(ligand_structure_file_path):
        raise FileNotFoundError(f"Ligand file {ligand_structure_file_path} not found!")

    res = _interfere_errors(DataResponse(**requests.post(f"{os.environ.get('ENERPLEX_API_URL')}/data/ligand", data=data, files=files, headers=headers).json()))
    return DBProteinLigandComplex(**res.data)

def upload_embedding(
    complex_id: int,
    embedding_shape: str,
    embedding_source: str,
    embedding_source_version: str,
    embedding_file_path: Union[str, Path],
    embedding_metadata: str = None,
    overwrite: bool = False,
) -> DBProteinLigandComplexEmbedding:
    """
    ### Uploads an embedding for a protein ligand complex.

    Args:
        complex_id (int): Complex id the embedding is for
        embedding_shape (str): Numpy shape of the embedding
        embedding_source (str): Source of the embedding, i.e. "TopoFormer"
        embedding_source_version (str): Version of the embedding source
        embedding_file_path (Union[str, Path]): Path to the embedding file in numpy format.
        embedding_metadata (str): Optional metadata for the embedding
        overwrite (bool): If true, overwrite the existing embedding for that complex.

    Raises:
        FileNotFoundError

    Returns:
        DBProteinLigandComplexEmbedding: The newly created embedding.
    """

    headers = {"Authorization": _get_auth_token()}
    data = {
        "complex_id": complex_id,
        "embedding_shape": embedding_shape,
        "embedding_source": embedding_source,
        "embedding_source_version": embedding_source_version,
        "embedding_metadata": embedding_metadata,
        "overwrite": overwrite
    }
    files = {"embedding": open(embedding_file_path, "rb")}

    if not os.path.exists(embedding_file_path):
        raise FileNotFoundError(f"Embedding file {embedding_file_path} not found!")

    res = _interfere_errors(DataResponse(**requests.post(f"{os.environ.get('ENERPLEX_API_URL')}/data/embedding", data=data, files=files, headers=headers).json()))
    return DBProteinLigandComplexEmbedding(**res.data)

def upload_mmxbsa_calculation(
    mmxbsa_calculation: DBMMXBSACalculation,
    override: bool = False
):
    """
    # Upload MM/XBSA Calculation

    Args:
        mmxbsa_calculation (DBMMXBSACalculation): The calculation.
        overwrite (bool): If true, overwrite the existing embedding for that complex.

    Returns:
        DBMMXBSACalculation: The newly created MM/XBSA calculation.
    """
    
    headers = {"Authorization": _get_auth_token()}
    data = {**dataclasses.asdict(mmxbsa_calculation), "override": override}

    res = _interfere_errors(DataResponse(**requests.post(f"{os.environ.get('ENERPLEX_API_URL')}/data/mmxbsa", data=data, headers=headers).json()))
    return DBMMXBSACalculation(**res.data)

def upload_fep_calculation(
    fep_calculation: DBFEPCalculation,
    override: bool = False
):
    """
    # Upload FEP Calculation

    Args:
        fep_calculation (DBFEPCalculation): The calculation.
        overwrite (bool): If true, overwrite the existing embedding for that complex.

    Returns:
        DBFEPCalculation: The newly created FEP calculation.
    """
    
    headers = {"Authorization": _get_auth_token()}
    data = {**dataclasses.asdict(fep_calculation), "override": override}

    res = _interfere_errors(DataResponse(**requests.post(f"{os.environ.get('ENERPLEX_API_URL')}/data/fep", data=data, headers=headers).json()))
    return DBFEPCalculation(**res.data)



def delete_target_protein(target_protein: DBTargetProtein):
    """
    ### Delete a Target Protein
    """
    headers = {"Authorization": _get_auth_token()}
    res = _interfere_errors(DataResponse(**requests.delete(f"{os.environ.get('ENERPLEX_API_URL')}/data/target-protein/{target_protein.id}", headers=headers).json()))


def delete_ligand(ligand: DBProteinLigandComplex):
    """
    ### Delete a protein-ligand-complex
    """
    headers = {"Authorization": _get_auth_token()}
    res = _interfere_errors(DataResponse(**requests.delete(f"{os.environ.get('ENERPLEX_API_URL')}/data/ligand/{ligand.id}", headers=headers).json()))


def delete_embedding(embedding: DBProteinLigandComplexEmbedding):
    """
    ### Delete a protein-ligand-complex embedding
    """
    headers = {"Authorization": _get_auth_token()}
    res = _interfere_errors(DataResponse(**requests.delete(f"{os.environ.get('ENERPLEX_API_URL')}/data/embedding/{embedding.id}", headers=headers).json()))

def delete_mmxbsa_calculation(calculation: DBMMXBSACalculation):
    """
    ### Delete a MM/XBSA calculation
    """
    headers = {"Authorization": _get_auth_token()}
    res = _interfere_errors(DataResponse(**requests.delete(f"{os.environ.get('ENERPLEX_API_URL')}/data/mmxbsa/{calculation.id}", headers=headers).json()))

def delete_fep_calculation(calculation: DBFEPCalculation):
    """
    ### Delete a fep calculation
    """
    headers = {"Authorization": _get_auth_token()}
    res = _interfere_errors(DataResponse(**requests.delete(f"{os.environ.get('ENERPLEX_API_URL')}/data/fep/{calculation.id}", headers=headers).json()))
