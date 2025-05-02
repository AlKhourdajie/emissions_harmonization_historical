# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] editable=true slideshow={"slide_type": ""}
# # Harmonisation - get default aneris methods
#
# Here we get the default method used by aneris for each timeseries.
# This makes it much easier to see what is being used
# and override as needed.

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Imports

# %%
import pandas_indexing as pix
import pandas_openscm
import tqdm.auto
from pandas_openscm.db import (
    FeatherDataBackend,
    FeatherIndexBackend,
    OpenSCMDB,
)
from pandas_openscm.io import load_timeseries_csv

from emissions_harmonization_historical.constants import (
    CMIP7_SCENARIOMIP_PRE_PROCESSING_ID,
    COMBINED_HISTORY_ID,
    DATA_ROOT,
    IAMC_REGION_PROCESSING_ID,
    SCENARIO_TIME_ID,
)
from emissions_harmonization_historical.harmonisation import HARMONISATION_YEAR

# %% [markdown]
# ## Set up

# %%
pandas_openscm.register_pandas_accessor()

# %% editable=true slideshow={"slide_type": ""}
HISTORICAL_GRIDDING_FILE = (
    DATA_ROOT
    / "cmip7-scenariomip-workflow"
    / "harmonisation"
    / f"gridding-historical-emissions_{COMBINED_HISTORY_ID}_{IAMC_REGION_PROCESSING_ID}.csv"
)
HISTORICAL_GRIDDING_FILE

# %%
# TODO: load historical non-gridding data
# TODO: split out io function to just load all default historical data
#       so we can use it here and in the actual harmonisation

# %%
IN_DIR = DATA_ROOT / "cmip7-scenariomip-workflow" / "pre-processing" / CMIP7_SCENARIOMIP_PRE_PROCESSING_ID
in_db = OpenSCMDB(
    db_dir=IN_DIR,
    backend_data=FeatherDataBackend(),
    backend_index=FeatherIndexBackend(),
)

in_db.load_metadata().shape

# %%
OUT_FILE = (
    DATA_ROOT
    / "cmip7-scenariomip-workflow"
    / "harmonisation"
    / f"harmonisation-default-methods_{COMBINED_HISTORY_ID}_{IAMC_REGION_PROCESSING_ID}_{SCENARIO_TIME_ID}_{CMIP7_SCENARIOMIP_PRE_PROCESSING_ID}.csv"
)
OUT_FILE.parent.mkdir(exist_ok=True, parents=True)
# OUT_FILE

# %% [markdown]
# ## Load data

# %%
historical_emissions_gridding = load_timeseries_csv(
    HISTORICAL_GRIDDING_FILE,
    index_columns=["model", "scenario", "region", "variable", "unit"],
    out_column_type=int,
)
if historical_emissions_gridding.empty:
    raise AssertionError

historical_emissions_gridding

# %%
pre_processed = in_db.load(pix.isin(stage="gridding_emissions"), progress=True).reset_index("stage", drop=True)
if pre_processed.empty:
    raise AssertionError

pre_processed

# %%
from aneris.methods import default_methods
from gcages.aneris_helpers import _convert_units_to_match

# %%
model_harm_overrides_default_l = []
for (model, scenario), msdf in tqdm.auto.tqdm(pre_processed.groupby(["model", "scenario"])):
    msdf_relevant_aneris = msdf.reset_index(["model", "scenario"], drop=True)

    history_model_relevant_aneris = _convert_units_to_match(
        start=historical_emissions_gridding.loc[
            pix.isin(region=msdf_relevant_aneris.index.get_level_values("region").unique())
        ]
        .reset_index(["model", "scenario"], drop=True)
        .reorder_levels(msdf_relevant_aneris.index.names),
        match=msdf_relevant_aneris,
    )

    msdf_default_overrides = default_methods(
        hist=history_model_relevant_aneris, model=msdf_relevant_aneris, base_year=HARMONISATION_YEAR
    )

    model_harm_overrides_default_l.append(msdf_default_overrides[0].pix.assign(model=model, scenario=scenario))
    # break

model_harm_overrides_default = pix.concat(model_harm_overrides_default_l)

# %%
pre_processed.shape

# %%
res = model_harm_overrides_default.to_frame()
# res

# %%
res.to_csv(OUT_FILE)
OUT_FILE
