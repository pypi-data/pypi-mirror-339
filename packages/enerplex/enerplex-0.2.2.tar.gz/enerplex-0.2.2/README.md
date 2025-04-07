Enerplex API Client
==========================

The Enerplex API Client is a Python package designed to interact with the Enerplex platform, providing functionality to manage and retrieve data related to target proteins, ligands, and their embeddings. This package facilitates authentication, data retrieval, and file management through a user-friendly interface.

## Features

- **Authentication**: Securely authenticate with the Enerplex API using user credentials.
- **Target Proteins**: Retrieve and manage information about target proteins.
- **Ligands**: Fetch ligands associated with specific proteins and upload new ligands.
- **Embeddings**: Retrieve embeddings for proteins and ligands.
- **File Management**: Download and manage files related to proteins, ligands, and embeddings.

## Installation

Install the package using pip:

```bash
pip install enerplex
```

## Setup

The package uses environment variables for configuration. Either set environment variable or create a `.env` file in your project directory with the following variables:

```env
ENERPLEX_API_URL=<your-api-url>
ENERPLEX_API_USER=<your-username>
ENERPLEX_API_USER_PASSWORD=<your-password>
```

## Usage

### Authentication

The package automatically handles authentication. Tokens are refreshed as needed to ensure seamless interaction with the API.

### Fetch Target Proteins

```python
from enerplex import get_target_proteins

proteins = get_target_proteins()
for protein in proteins:
    print(protein.name)
```

### Fetch Ligands

```python
from enerplex import get_ligands

ligands = get_ligands(protein_identifier=123)
for ligand in ligands:
    print(ligand.id, ligand.name)
```

### Download Files

```python
from enerplex import download_target_protein_file
from pathlib import Path

protein = ...  # A DBTargetProtein object
download_target_protein_file(protein, path=Path("/path/to/save/file"))
```

### Upload Ligands

```python
from enerplex import upload_ligand
from pathlib import Path

ligand = upload_ligand(
    target_name="ProteinX",
    score=92.5,
    scoring_function="Docking",
    ligand_structure_file_path=Path("/path/to/ligand/file")
)
print(ligand.id, ligand.name)
```

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request. Ensure your code adheres to the existing style and is well-documented.

## License

This package is licensed under the MIT License. See the `LICENSE` file for more details.

## Support

For any issues or questions, please open an issue on the GitHub repository or contact the maintainer directly.

---

### Example Workflow

Here's a complete example that retrieves a target protein, downloads its associated file, and uploads a new ligand:

```python
from enerplex import get_target_proteins, download_target_protein_file, upload_ligand, DBProteinLigandComplex, DBTargetProtein
from pathlib import Path

# Retrieve proteins
proteins: list[DBTargetProtein] = get_target_proteins()
selected_protein: DBTargetProtein = proteins[0]

# Download protein file
download_target_protein_file(selected_protein, path=Path("protein_file.pdb"))

# Build a ligand with some workflow
# ...

# Upload the new ligand
new_ligand: DBProteinLigandComplex  = upload_ligand(
    target_name=selected_protein.name,
    score=-9.3,
    scoring_function="Vina",
    ligand_structure_file_path=Path("ligand_structure.pdb")
)
print(f"Uploaded ligand: {new_ligand.id}, {new_ligand.name}")
```

