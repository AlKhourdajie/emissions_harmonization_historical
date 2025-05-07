"""
Constants for use in the 5000 notebooks

These are a way of ensuring that shared ideas are consistent across notebooks
and identifying the processing
that was done to create different data
as we update our processing steps.
If you update the way something is done
and want to avoid overwriting your old data,
just update the ID in here
(because then the data will be written to a different file).
There are much more sophisticated ways this could be done,
but they also require more effort :)
"""

from pathlib import Path

from pandas_openscm.db import (
    CSVDataBackend,
    CSVIndexBackend,
    FeatherDataBackend,
    FeatherIndexBackend,
    OpenSCMDB,
)

# Chosen to match the CMIP experiment ID
HISTORY_SCENARIO_NAME = "historical"

REPO_ROOT = Path(__file__).parents[2]
DATA_ROOT = REPO_ROOT / "data"

CEDS_VERSION_ID = "v_2025_03_18"

# ID for the CEDS processing step
CEDS_PROCESSING_ID = "0001"

CEDS_TOP_LEVEL_RAW_PATH = DATA_ROOT / "raw" / "ceds"
CEDS_RAW_PATH = CEDS_TOP_LEVEL_RAW_PATH / CEDS_VERSION_ID

# Database into which the processed CEDS data is saved
CEDS_PROCESSED_DB = OpenSCMDB(
    db_dir=DATA_ROOT / "processed" / "ceds" / CEDS_PROCESSING_ID / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

# ID for the GFED4 processing step
GFED4_PROCESSING_ID = "0001"

GFED4_TOP_LEVEL_RAW_PATH = DATA_ROOT / "raw" / "gfed4"
GFED4_RAW_PATH = GFED4_TOP_LEVEL_RAW_PATH

# Database into which the processed GFED4 data is saved
GFED4_PROCESSED_DB = OpenSCMDB(
    db_dir=DATA_ROOT / "processed" / "gfed4" / GFED4_PROCESSING_ID / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

GCB_VERSION = "2024v1.0"

# ID for the CEDS processing step
GCB_PROCESSING_ID = "0001"

GCB_RAW_PATH = DATA_ROOT / "raw" / "gcb" / GCB_VERSION

# Database into which the processed GCB data is saved
GCB_PROCESSED_DB = OpenSCMDB(
    db_dir=DATA_ROOT / "processed" / "gcb" / GCB_PROCESSING_ID / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

WMO_2022_RAW_PATH = DATA_ROOT / "raw" / "wmo-2022"

# ID for the WMO 2022 processing step
WMO_2022_PROCESSING_ID = "0001"

WMO_2022_PROCESSED_DB = OpenSCMDB(
    db_dir=DATA_ROOT / "processed" / "wmo-2022" / WMO_2022_PROCESSING_ID / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

VELDERS_ET_AL_2022_RAW_PATH = DATA_ROOT / "raw" / "velders-et-al-2022"

# ID for the Velders et al. 2022 processing step
VELDERS_ET_AL_2022_PROCESSING_ID = "0001"

VELDERS_ET_AL_2022_PROCESSED_DB = OpenSCMDB(
    db_dir=DATA_ROOT / "processed" / "velders-et-al-2022" / VELDERS_ET_AL_2022_PROCESSING_ID / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

ADAM_ET_AL_2024_RAW_PATH = DATA_ROOT / "raw" / "adam-et-al-2024"

# ID for the adam et al. 2024 processing step
ADAM_ET_AL_2024_PROCESSING_ID = "0001"

ADAM_ET_AL_2024_PROCESSED_DB = OpenSCMDB(
    db_dir=DATA_ROOT / "processed" / "adam-et-al-2024" / ADAM_ET_AL_2024_PROCESSING_ID / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

CMIP7_GHG_VERSION_ID = "CR-CMIP-1-0-0"
CMIP7_GHG_PUB_DATE = "v20250228"

CMIP7_GHG_RAW_PATH = DATA_ROOT / "raw" / "cmip7-ghgs" / CMIP7_GHG_VERSION_ID

# ID for the CMIP7 GHG processing step
CMIP7_GHG_PROCESSING_ID = "0001"

CMIP7_GHG_PROCESSED_DIR = DATA_ROOT / "processed" / "cmip7-ghgs" / CMIP7_GHG_PROCESSING_ID
CMIP7_GHG_PROCESSED_DB = OpenSCMDB(
    db_dir=CMIP7_GHG_PROCESSED_DIR / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

RCMIP_VERSION_ID = "v5.1.0"

RCMIP_RAW_PATH = DATA_ROOT / "raw" / "rcmip" / RCMIP_VERSION_ID

# ID for the CMIP7 GHG processing step
RCMIP_PROCESSING_ID = "0001"

RCMIP_PROCESSED_DIR = DATA_ROOT / "processed" / "rcmip" / RCMIP_PROCESSING_ID
RCMIP_PROCESSED_DB = OpenSCMDB(
    db_dir=RCMIP_PROCESSED_DIR / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)


# Commit from https://github.com/IAMconsortium/common-definitions
# to use
COMMON_DEFINITIONS_COMMIT = "95b5f2c9fb62e32a4d08fe2ffc5b4a6ff246ad2d"
COMMON_DEFINITIONS_PATH = REPO_ROOT / "common-definitions"

# ID for the creation of a historical emissions dataset for gridding
CREATE_HISTORY_FOR_GRIDDING_ID = "0001"

# ID for the created history for harmonisation
HISTORY_FOR_HARMONISATION_ID = "_".join(
    [
        CEDS_PROCESSING_ID,
        GFED4_PROCESSING_ID,
        CREATE_HISTORY_FOR_GRIDDING_ID,
    ]
)

# Directory in which the history for harmonisation information lives
HISTORY_HARMONISATION_DIR = DATA_ROOT / "processed" / "history-for-harmonisation" / HISTORY_FOR_HARMONISATION_ID

REGION_MAPPING_FILE = HISTORY_HARMONISATION_DIR / f"region-mapping_{COMMON_DEFINITIONS_COMMIT}.csv"

# Database to hold historical emissions for harmonisation
HISTORY_HARMONISATION_DB = OpenSCMDB(
    db_dir=HISTORY_HARMONISATION_DIR / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)


# ID for the scenario download step
DOWNLOAD_SCENARIOS_ID = "0001"
# Updated May 6 for revised AIM scenarios
DOWNLOAD_SCENARIOS_ID = "0002"

# Database into which raw scenarios are saved
RAW_SCENARIO_DB = OpenSCMDB(
    db_dir=DATA_ROOT / "raw" / "scenarios" / DOWNLOAD_SCENARIOS_ID / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

# ID for the pre-processing step
PRE_PROCESSING_ID = "0001"

# Database into which pre-processed scenarios are saved
PRE_PROCESSED_SCENARIO_DB = OpenSCMDB(
    db_dir=DATA_ROOT / "processed" / "pre-processed" / f"{DOWNLOAD_SCENARIOS_ID}_{PRE_PROCESSING_ID}" / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

# ID for the harmonisation step
HARMONISATION_ID = "0002"

HARMONISED_OUT_DIR = (
    DATA_ROOT
    / "processed"
    / "harmonised"
    / f"{DOWNLOAD_SCENARIOS_ID}_{PRE_PROCESSING_ID}_{HISTORY_FOR_HARMONISATION_ID}_{HARMONISATION_ID}"
)

# Database into which harmonised scenarios are saved
HARMONISED_SCENARIO_DB = OpenSCMDB(
    db_dir=HARMONISED_OUT_DIR / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

# ID for the infilling database creation step
INFILLING_DB_CREATION_ID = "0001"

INFILLING_DB_DIR = (
    DATA_ROOT
    / "processed"
    / "infilling-db"
    / f"{DOWNLOAD_SCENARIOS_ID}_{WMO_2022_PROCESSING_ID}_{HARMONISATION_ID}_{INFILLING_DB_CREATION_ID}"
)

# Database into which pre-processed scenarios are saved
INFILLING_DB = OpenSCMDB(
    db_dir=INFILLING_DB_DIR / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

# ID for the infilling step
# INFILLING_ID = "0001"
# Fixed a bug in how some Montreal gases were infilled
# (some had emissions that were becoming way too low in future).
INFILLING_ID = "0002"

INFILLED_OUT_DIR = (
    DATA_ROOT
    / "processed"
    / "infilled"
    / f"{DOWNLOAD_SCENARIOS_ID}_{PRE_PROCESSING_ID}_{HISTORY_FOR_HARMONISATION_ID}_{HARMONISATION_ID}_{INFILLING_ID}"
)

# Database into which infilled data is saved
INFILLED_SCENARIOS_DB = OpenSCMDB(
    db_dir=INFILLED_OUT_DIR / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

# ID for the simple climate model running step
SCM_RUNNING_ID = "0001"

SCM_OUT_DIR = (
    DATA_ROOT
    / "processed"
    / "scm-output"
    / "_".join(
        [
            DOWNLOAD_SCENARIOS_ID,
            PRE_PROCESSING_ID,
            HISTORY_FOR_HARMONISATION_ID,
            HARMONISATION_ID,
            INFILLING_ID,
            SCM_RUNNING_ID,
        ]
    )
)

# Database into which SCM output is saved
SCM_OUTPUT_DB = OpenSCMDB(
    db_dir=SCM_OUT_DIR / "db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

# ID for the post-processing step
POST_PROCESSING_ID = "0001"

POST_PROCESSING_DIR = (
    DATA_ROOT
    / "processed"
    / "post-processed"
    / "_".join(
        [
            DOWNLOAD_SCENARIOS_ID,
            PRE_PROCESSING_ID,
            HISTORY_FOR_HARMONISATION_ID,
            HARMONISATION_ID,
            INFILLING_ID,
            SCM_RUNNING_ID,
            POST_PROCESSING_ID,
        ]
    )
)

# Databases intwo which post-processed output is saved.
# There are lots of these because each kind of data
# has slightly different axes,
# so we don't want to use the same ones.

POST_PROCESSED_METADATA_CATEGORIES_DB = OpenSCMDB(
    db_dir=POST_PROCESSING_DIR / "db-metadata-categories",
    backend_data=CSVDataBackend(),
    backend_index=CSVIndexBackend(),
)

POST_PROCESSED_METADATA_EXCEEDANCE_PROBABILITIES_DB = OpenSCMDB(
    db_dir=POST_PROCESSING_DIR / "db-metadata-exceedance-probabilities-db",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

POST_PROCESSED_METADATA_QUANTILE_DB = OpenSCMDB(
    db_dir=POST_PROCESSING_DIR / "db-metadata-quantile",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

POST_PROCESSED_METADATA_RUN_ID_DB = OpenSCMDB(
    db_dir=POST_PROCESSING_DIR / "db-metadata-run-id",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

POST_PROCESSED_TIMESERIES_EXCEEDANCE_PROBABILITIES_DB = OpenSCMDB(
    db_dir=POST_PROCESSING_DIR / "db-timeseries-exceedance-probabilities",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

POST_PROCESSED_TIMESERIES_QUANTILE_DB = OpenSCMDB(
    db_dir=POST_PROCESSING_DIR / "db-timeseries-quantile",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

POST_PROCESSED_TIMESERIES_RUN_ID_DB = OpenSCMDB(
    db_dir=POST_PROCESSING_DIR / "db-timeseries-run-id",
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)
