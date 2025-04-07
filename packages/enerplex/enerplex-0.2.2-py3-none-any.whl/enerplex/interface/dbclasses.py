from dataclasses import dataclass

"""
Class interfaces for enerplex-api/src/models/*.ts
Version: 0.0.2
"""

@dataclass
class DBObject:
    id: int

@dataclass
class DBTargetProtein(DBObject):
    unique_name: str
    target_filename: str
    target_filetype: str
    created_at: str

@dataclass
class DBProteinLigandComplex(DBObject):
    target_name: str
    ligand_filename: str
    ligand_filetype: str
    file_hash: str
    scoring_function: str
    score: float
    smiles: str
    qed_score: float
    sa_score: float
    vina_score: float
    created_at: str


@dataclass
class DBProteinLigandComplexEmbedding(DBObject):
    complex_id: int
    embedding_filename: str
    embedding_filetype: str
    embedding_shape: str
    embedding_source: str
    embedding_metadata: str
    embedding_source_version: str
    created_at: str


@dataclass
class DBMMXBSACalculation(DBObject):
    complex_id: int
    source: str
    force_field: str
    dg_c2_pb_mean: float
    dg_c2_gb_mean: float
    dg_ie_pb_mean: float
    dg_ie_gb_mean: float
    dg_qh_pb_mean: float
    dg_qh_gb_mean: float
    dg_en_pb_mean: float
    dg_en_gb_mean: float
    c2_pb_mean: float
    c2_gb_mean: float
    ie_pb_mean: float
    ie_gb_mean: float
    qh_mean: float
    dg_c2_pb_sem: float
    dg_c2_gb_sem: float
    dg_ie_pb_sem: float
    dg_ie_gb_sem: float
    dg_qh_pb_sem: float
    dg_qh_gb_sem: float
    dg_en_pb_sem: float
    dg_en_gb_sem: float
    c2_pb_sem: float
    c2_gb_sem: float
    ie_pb_sem: float
    ie_gb_sem: float
    qh_sem: float
    num_replicas: float
    total_samples: float
    created_at: str

@dataclass
class DBFEPCalculation(DBObject):
    complex_id: int
    source: str
    force_field: str
    mbar: float
    mbar_sem: float
    mbar_uncertainty_propagation: float
    mbar_num_replicas: float
    ti: float
    ti_sem: float
    ti_uncertainty_propagation: float
    ti_num_replicas: float
    created_at: str
