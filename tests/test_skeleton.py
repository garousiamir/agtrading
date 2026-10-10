"""Phase 0 smoke test: every package from docs/04-architecture.md exists and imports."""

import importlib

import pytest

MODULES = [
    "cp_core",
    "cp_ingest",
    "cp_catalog",
    "cp_features",
    "cp_strategy",
    "cp_sim",
    "cp_validation",
    "cp_stats",
    "cp_risk",
    "cp_oms",
    "cp_llm",
    "cp_signals",
    "cp_api",
    "cp_worker_research",
    "cp_worker_eval",
]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name: str) -> None:
    importlib.import_module(name)


def test_execution_service_not_in_research_distribution() -> None:
    # Rule 11: research code must not be able to import the execution service,
    # which is the only process allowed to hold exchange trading credentials.
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("cp_execution")
