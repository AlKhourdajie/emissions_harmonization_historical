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

# %% [markdown]
# # Run a simple climate model
#
# Here we run a simple climate model.

# %% [markdown]
# ## Imports

# %%
import multiprocessing
import os
import platform
from functools import partial

import openscm_units
import pandas_indexing as pix
import pandas_openscm
import seaborn as sns
from gcages.renaming import SupportedNamingConventions, convert_variable_name
from gcages.scm_running import run_scms
from pandas_openscm.index_manipulation import update_index_levels_func

from emissions_harmonization_historical.constants_5000 import (
    HISTORY_HARMONISATION_DB,
    INFILLED_SCENARIOS_DB,
    RCMIP_PROCESSED_DB,
    REPO_ROOT,
    SCM_OUT_DIR,
    SCM_OUTPUT_DB,
)
from emissions_harmonization_historical.scm_running import get_complete_scenarios_for_magicc, load_magicc_cfgs

# %% [markdown]
# ## Set up

# %%
pandas_openscm.register_pandas_accessor()

# %%
UR = openscm_units.unit_registry
Q = UR.Quantity

# %% editable=true slideshow={"slide_type": ""} tags=["parameters"]
model: str = "AIM"
scm: str = "MAGICCv7.6.0a3"

# %%
output_dir_model = SCM_OUT_DIR / model
output_dir_model.mkdir(exist_ok=True, parents=True)
output_dir_model

# %% [markdown]
# ## Load data

# %% [markdown]
# ### Complete scenarios

# %%
complete_scenarios = INFILLED_SCENARIOS_DB.load(
    pix.isin(stage="complete") & pix.ismatch(model=f"*{model}*")
).reset_index("stage", drop=True)
# complete_scenarios

# %% [markdown]
# ### History
#
# Just in case we need it for MAGICC

# %%
history = HISTORY_HARMONISATION_DB.load(pix.ismatch(purpose="global_workflow_emissions")).reset_index(
    "purpose", drop=True
)

# history

# %% [markdown]
# ## Configure SCM

# %%
output_variables = (
    # GSAT
    "Surface Air Temperature Change",
    # # GMST
    # "Surface Air Ocean Blended Temperature Change",
    # # ERFs
    # "Effective Radiative Forcing",
    # "Effective Radiative Forcing|Anthropogenic",
    # "Effective Radiative Forcing|Aerosols",
    # "Effective Radiative Forcing|Aerosols|Direct Effect",
    # "Effective Radiative Forcing|Aerosols|Direct Effect|BC",
    # "Effective Radiative Forcing|Aerosols|Direct Effect|OC",
    # "Effective Radiative Forcing|Aerosols|Direct Effect|SOx",
    # "Effective Radiative Forcing|Aerosols|Indirect Effect",
    # "Effective Radiative Forcing|Greenhouse Gases",
    # "Effective Radiative Forcing|CO2",
    # "Effective Radiative Forcing|CH4",
    # "Effective Radiative Forcing|N2O",
    # "Effective Radiative Forcing|F-Gases",
    # "Effective Radiative Forcing|Montreal Protocol Halogen Gases",
    # "Effective Radiative Forcing|Ozone",
    # # Heat uptake
    # "Heat Uptake",
    # # "Heat Uptake|Ocean",
    # # Atmospheric concentrations
    "Atmospheric Concentrations|CO2",
    "Atmospheric Concentrations|CH4",
    "Atmospheric Concentrations|N2O",
    # # Carbon cycle
    # "Net Atmosphere to Land Flux|CO2",
    # "Net Atmosphere to Ocean Flux|CO2",
    "CO2_CURRENT_NPP",
    # # Permafrost
    # "Net Land to Atmosphere Flux|CO2|Earth System Feedbacks|Permafrost",
    # "Net Land to Atmosphere Flux|CH4|Earth System Feedbacks|Permafrost",
)

# %%
if scm in ["MAGICCv7.5.3", "MAGICCv7.6.0a3"]:
    if scm == "MAGICCv7.6.0a3":
        magicc_exe_path = REPO_ROOT / "magicc" / "magicc-v7.6.0a3" / "bin" / "magicc-darwin-arm64"
        magicc_expected_version = "v7.6.0a3"
        magicc_prob_distribution_path = (
            REPO_ROOT / "magicc" / "magicc-v7.6.0a3" / "configs" / "magicc-ar7-fast-track-drawnset-v0-3-0.json"
        )

    elif scm == "MAGICCv7.5.3":
        os.environ["DYLD_LIBRARY_PATH"] = "/opt/homebrew/opt/gfortran/lib/gcc/current/"
        if platform.system() == "Darwin":
            if platform.processor() == "arm":
                magicc_exe = "magicc-darwin-arm64"
            else:
                raise NotImplementedError(platform.processor())
        elif platform.system() == "Windows":
            magicc_exe = "magicc.exe"
        else:
            raise NotImplementedError(platform.system())

        magicc_exe_path = REPO_ROOT / "magicc" / "magicc-v7.5.3" / "bin" / magicc_exe
        magicc_expected_version = "v7.5.3"
        magicc_prob_distribution_path = REPO_ROOT / "magicc" / "magicc-v7.5.3" / "configs" / "600-member.json"

    else:
        raise NotImplementedError(scm)

    os.environ["MAGICC_EXECUTABLE_7"] = str(magicc_exe_path)

    climate_models_cfgs = load_magicc_cfgs(
        prob_distribution_path=magicc_prob_distribution_path,
        output_variables=output_variables,
        startyear=1750,
    )

    complete_scm = get_complete_scenarios_for_magicc(
        scenarios=complete_scenarios,
        history=history,
    )

else:
    raise NotImplementedError(scm)

# complete_scm

# %% [markdown]
# ### If MAGICC, check how yuck the jump will be
#
# Answer: not ideal but we're going to have to live with it.


# %%
if scm.startswith("MAGICC"):
    reporting_to_rcmip = partial(
        convert_variable_name,
        to_convention=SupportedNamingConventions.RCMIP,
        from_convention=SupportedNamingConventions.CMIP7_SCENARIOMIP,
    )
    rcmip_to_reporting = partial(
        convert_variable_name,
        from_convention=SupportedNamingConventions.RCMIP,
        to_convention=SupportedNamingConventions.CMIP7_SCENARIOMIP,
    )

    rcmip_hist = RCMIP_PROCESSED_DB.load(
        pix.isin(
            region="World",
            scenario="ssp245",
            variable=complete_scenarios.pix.unique("variable").map(reporting_to_rcmip),
        ),
        progress=True,
    ).loc[:, 1990:2014]
    rcmip_hist = rcmip_hist.openscm.update_index_levels({"variable": rcmip_to_reporting})
    # rcmip_hist

    pdf = pix.concat([rcmip_hist, complete_scm]).loc[:, 1990:2030].openscm.to_long_data().dropna()
    # pdf

    fg = sns.relplot(
        data=pdf,
        x="time",
        y="value",
        hue="scenario",
        col="variable",
        col_order=sorted(pdf["variable"].unique()),
        col_wrap=3,
        kind="line",
        facet_kws=dict(sharey=False),
    )
    for ax in fg.axes.flatten():
        ax.set_ylim(ymin=0.0)

# %% [markdown]
# ## Run SCM

# %%
complete_openscm_runner = update_index_levels_func(
    complete_scm,
    {
        "variable": partial(
            convert_variable_name,
            from_convention=SupportedNamingConventions.CMIP7_SCENARIOMIP,
            to_convention=SupportedNamingConventions.OPENSCM_RUNNER,
        )
    },
)
# complete_openscm_runner

# %%
run_scms(
    scenarios=complete_openscm_runner,
    climate_models_cfgs=climate_models_cfgs,
    output_variables=output_variables,
    scenario_group_levels=["model", "scenario"],
    n_processes=multiprocessing.cpu_count(),
    db=SCM_OUTPUT_DB,
    verbose=True,
    progress=True,
    batch_size_scenarios=15,
    force_rerun=False,
)

# %% [markdown]
# ## Save
#
# The SCM output is already saved in the db.
# Here we also save the emissions that were actually used by the SCM.

# %%
SCM_OUTPUT_DB.save(complete_scm.pix.assign(climate_model=scm), allow_overwrite=True)
