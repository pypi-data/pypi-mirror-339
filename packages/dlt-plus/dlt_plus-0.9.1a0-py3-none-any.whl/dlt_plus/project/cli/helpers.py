from importlib import resources
from typing import Dict, Any, List, Tuple
import os
import tomlkit
import importlib

import argparse

from ruamel.yaml import YAML

from dlt.cli import echo as fmt, CliCommandException
from dlt.common.destination.reference import DestinationReference
from dlt.cli.config_toml_writer import WritableConfigValue
from dlt.extract.reference import SourceReference

from dlt_plus.project.run_context import (
    ProjectRunContext,
    project_from_args,
    ProjectRunContextNotAvailable,
    create_empty_project_context,
)
from dlt_plus.common.constants import DEFAULT_PROJECT_CONFIG_FILE
from dlt_plus.project._templates.project import GIT_IGNORE
from dlt_plus.project.cli.write_state import ProjectWriteState

BASE_TEMPLATES_PATH = "dlt_plus.project._templates"
SOURCES_TEMPLATES_PATH = BASE_TEMPLATES_PATH + ".sources"
DESTINATIONS_TEMPLATES_PATH = BASE_TEMPLATES_PATH + ".destinations"
PROJECT_TEMPLATES_PATH = BASE_TEMPLATES_PATH + ".project"
REQUIREMENTS_FILE_NAME = "requirements.txt"
PYPROJECT_FILE_NAME = "pyproject.toml"
PACKAGE_INIT_FILE_NAME = "package_init.py"
CONFIG_TEMPLATES = {
    "rest_api": """
[sources.{source_name}]
resources = ["pokemon", "berry"] # please set me up!
[sources.{source_name}.client] # please set me up!
base_url= "https://pokeapi.co/api/v2/"
""",
    "sql_database": """
[sources.{source_name}]
table_names = ["family", "clan"]
""",
}

SECRETS_TEMPLATES = {
    "sql_database": """
[sources.{source_name}.credentials]
drivername = "mysql+pymysql"
database = "Rfam"
username = "rfamro"
host = "mysql-rfam-public.ebi.ac.uk"
port = 4497
""",
}


def project_from_args_with_cli_output(
    args: argparse.Namespace, allow_no_project: bool = False
) -> ProjectRunContext:
    try:
        return project_from_args(args)
        # fmt.note(
        #     "Project Context: %s @ %s. Active profile: %s."
        #     % (run_context.name, run_context.run_dir, run_context.profile)
        # )
    except ProjectRunContextNotAvailable:
        if not allow_no_project:
            fmt.error(
                "No project context found. This cli command requires a project context, "
                "get started with `dlt project init` to create a new project."
            )
            raise
    return None


def _read_project_yaml(project_run_context: ProjectRunContext) -> Any:
    """Read the project yaml file."""

    yaml = YAML()
    project_yaml_path = os.path.join(project_run_context.run_dir, DEFAULT_PROJECT_CONFIG_FILE)
    with open(project_yaml_path, "r", encoding="utf-8") as file:
        return yaml.load(file)


def _write_project_yaml(project_dir: str, project_yaml: Any) -> None:
    """Write the project yaml file."""

    yaml = YAML()
    project_yaml_path = os.path.join(project_dir, DEFAULT_PROJECT_CONFIG_FILE)
    with open(project_yaml_path, "w", encoding="utf-8") as file:
        yaml.dump(project_yaml, file)


def _ensure_unique_name(given_name: str, existing_keys: List[str]) -> None:
    """Create a unique name by appending a number to the given name if it already exists."""
    if given_name in existing_keys:
        fmt.error(f"Name {given_name} already exists in project. Please use a different name.")
        raise CliCommandException()


def ensure_project_dirs(project_run_context: ProjectRunContext) -> None:
    """Ensure the project directories exist."""
    os.makedirs(project_run_context.settings_dir, exist_ok=True)


def init_project(
    root_dir: str, name: str = None, package_name: str = None
) -> Tuple[ProjectRunContext, ProjectWriteState]:
    """
    Prepares a new dlt+ project in the given directory by preparing the project state.
    If package_name is provided, the project will be initialized as a pip package.

    To actually create the project, call `project_state.commit()`.
    NOTE: this will overwrite any existing dlt.yml file in the project directory, but will preserve
            the values in .dlt/secrets.toml and .dlt/config.toml files if they exist.

    Returns:
        Tuple[ProjectRunContext, ProjectState]: The project run context and a project_state, holding
            all changes that the project-creation entails.
    """

    yaml = YAML()

    # Load default project YAML template
    with resources.open_text(PROJECT_TEMPLATES_PATH, DEFAULT_PROJECT_CONFIG_FILE) as file:
        project_yaml = yaml.load(file)

    if name:
        project_yaml["project"] = project_yaml.get("project") or {}
        project_yaml["project"]["name"] = name

    # Determine package directory
    package_dir = os.path.join(root_dir, package_name) if package_name else root_dir

    # create new empty context and state
    project_run_context = create_empty_project_context(project_dir=package_dir)
    project_state = ProjectWriteState(project_run_context, read_project_yaml=False)
    project_state.dirs_to_create.append(package_dir)

    # Add project YAML to state
    project_state.dlt_yaml = project_yaml
    # polish-todo: handle existing pin-file. delete pin file if exists (after confirmation?)

    # Get install dependencies
    from dlt_plus.version import __version__ as dlt_plus_version
    from dlt.version import __version__ as dlt_version

    dependencies = [f"dlt=={dlt_version}", f"dlt-plus=={dlt_plus_version}"]

    # Prepare pyproject.toml and package init file if package
    if package_name:
        pptoml = tomlkit.load(resources.open_text(PROJECT_TEMPLATES_PATH, PYPROJECT_FILE_NAME))
        pptoml["project"]["name"] = package_name  # type: ignore
        pptoml["project"]["dependencies"] = dependencies  # type: ignore
        pptoml["project"]["entry-points"]["dlt_package"]["dlt-project"] = package_name  # type: ignore

        project_state.add_new_file(
            os.path.join(root_dir, "pyproject.toml"),
            tomlkit.dumps(pptoml),
        )

        with resources.open_text(PROJECT_TEMPLATES_PATH, PACKAGE_INIT_FILE_NAME) as file:
            project_state.add_new_file(
                os.path.join(package_dir, "__init__.py"),
                file.read(),
            )

    # Prepare requirements.txt if not a package
    else:
        project_state.add_new_file(
            os.path.join(root_dir, REQUIREMENTS_FILE_NAME),
            "\n".join(dependencies),
        )

    # Ensure project directories
    project_state.dirs_to_create.append(project_run_context.settings_dir)

    # Add default toml files to state
    for fname in ["secrets.toml", "config.toml"]:
        project_state.add_new_file(
            os.path.join(project_run_context.settings_dir, fname),
            f"# default {fname} file",
            accept_existing=True,
        )

    # Add .gitignore file to state
    project_state.add_new_file(
        os.path.join(root_dir, ".gitignore"),
        GIT_IGNORE,
    )

    return project_run_context, project_state


def add_profile(project_state: ProjectWriteState, profile_name: str) -> None:
    """Add a profile to the project."""

    project_state.dlt_yaml["profiles"] = project_state.dlt_yaml.get("profiles") or {}
    project_state.dlt_yaml["profiles"][profile_name] = {}

    # create profile secrets file as new file to be created
    project_state.add_new_file(
        os.path.join(project_state.settings_dir, f"{profile_name}.secrets.toml"),
        f"# secrets for profile {profile_name}\n",
    )


def add_source(
    project_state: ProjectWriteState,
    source_name: str,
    source_type: str = None,
) -> str:
    """Add a source to the project, returns the name."""
    project_state.dirs_to_create.append(project_state.settings_dir)

    project_yaml = project_state.dlt_yaml
    project_yaml["sources"] = project_yaml.get("sources") or {}

    # ensure unique name
    source_type = source_type or source_name
    _ensure_unique_name(source_name, project_yaml["sources"].keys())

    # get config and secrets values from source-registry
    source_ref = source_type

    #  check if source is a template in the sources folder
    # if so, copy file to sources dir (and adjust source type to module path)
    source_is_template = resources.is_resource(SOURCES_TEMPLATES_PATH, f"{source_type}.py")
    template_ref = ""
    if source_is_template:
        template_ref = f"{SOURCES_TEMPLATES_PATH}.{source_type}.source"
        sources_dir = project_state.sources_dir
        project_state.dirs_to_create.append(sources_dir)
        new_file_path = os.path.join(sources_dir, f"{source_name}.py")
        with resources.open_text(SOURCES_TEMPLATES_PATH, f"{source_type}.py") as file:
            project_state.add_new_file(new_file_path, file.read())

        # after being written it will be imported from here:
        source_type = f"sources.{source_name}.source"

    # look up source and update configs SourceConfiguration
    source_ref = template_ref or source_type
    source_spec = SourceReference.find(
        source_ref, raise_exec_errors=True, import_missing_modules=True
    ).ref.SPEC

    # inject examples for specific source types
    if source_type in ["rest_api", "sql_database"]:
        if source_type in CONFIG_TEMPLATES.keys():
            project_state.update_config_toml(get_config_template(source_type, source_name))
        if source_type in SECRETS_TEMPLATES.keys():
            project_state.update_secrets_toml(get_secrets_template(source_type, source_name))
    else:
        source_secrets = WritableConfigValue(source_name, source_spec, None, ("sources",))
        project_state.add_secrets_value(source_secrets)

    # update project yaml
    project_yaml["sources"][source_name] = {"type": source_type}

    return source_name


def add_dataset(project_state: ProjectWriteState, dataset_name: str, destination_name: str) -> str:
    """Add a dataset to the project, returns the name."""
    project_yaml = project_state.dlt_yaml
    project_yaml["datasets"] = project_yaml.get("datasets") or {}

    # create name
    _ensure_unique_name(dataset_name, project_yaml["datasets"].keys())

    # add dataset to yaml
    project_yaml["datasets"][dataset_name] = {
        "destination": [destination_name],
    }

    return dataset_name


def add_destination(
    project_state: ProjectWriteState,
    destination_name: str,
    destination_type: str = None,
    dataset_name: str = None,
) -> Tuple[str, str]:
    """Add a destination to the project, returns the name."""
    project_state.dirs_to_create.append(project_state.settings_dir)

    # look up destination
    destination_type = destination_type or destination_name
    destination_ref = DestinationReference.find(
        destination_type,
        raise_exec_errors=True,
        import_missing_modules=True,
    )
    # extract factory if we resolve custom destination (decorator)
    destination_ref = DestinationReference.ensure_factory(destination_ref)

    # ensure unique name
    project_yaml = project_state.dlt_yaml
    project_yaml["destinations"] = project_yaml.get("destinations") or {}
    _ensure_unique_name(destination_name, project_yaml["destinations"].keys())

    # update project yaml
    project_yaml["destinations"][destination_name] = {
        "type": destination_type,
    }

    # extract secrets to toml file
    destination_secrets = WritableConfigValue(
        destination_name, destination_ref.spec, None, ("destination",)
    )
    project_state.add_secrets_value(destination_secrets)

    # add a dataset for this destination
    if dataset_name:
        dataset_name = dataset_name or destination_name + "_dataset"
        dataset_name = add_dataset(project_state, dataset_name, destination_name)
    else:
        dataset_name = None

    return destination_name, dataset_name


def add_pipeline(
    project_state: ProjectWriteState,
    pipeline_name: str,
    source_name: str,
    destination_name: str,
    dataset_name: str = None,
) -> None:
    """Add a pipeline to the project, returns the name."""
    project_yaml = project_state.dlt_yaml
    project_yaml["pipelines"] = project_yaml.get("pipelines") or {}

    # create name
    _ensure_unique_name(pipeline_name, project_yaml["pipelines"].keys())

    # add pipeline to yaml
    project_yaml["pipelines"][pipeline_name] = {
        "source": source_name,
        "destination": destination_name,
    }

    # add dataset name if provided
    if dataset_name:
        project_yaml["pipelines"][pipeline_name]["dataset_name"] = dataset_name
    else:
        project_yaml["pipelines"][pipeline_name]["dataset_name"] = pipeline_name + "_dataset"


def get_available_destinations() -> List[str]:
    """Get all available destinations."""
    return [
        d.replace("dlt_plus.destinations.", "").replace("dlt.destinations.", "")
        for d in DestinationReference.DESTINATIONS.keys()
    ]


def get_available_source() -> Dict[str, str]:
    """Get all available destinations."""
    # TODO: for some reason not all sources are in SourceReference.SOURCES
    # so for now we fake it here
    # TODO: reuse OSS logic that lists verified sources (it imports module from known location)
    #  and then find SOURCES in that location. we will not import sources automatically
    #  because that slows down the startup
    return {
        "sql_database": "SQL Database Source",
        "rest_api": "REST API Source",
        "filesystem": "Source for files and folders, csv, json, parquet, etc.",
    }


def get_available_source_templates() -> Dict[str, str]:
    """Get all available source templates."""
    # if resources.is_resource(SOURCES_TEMPLATES_PATH, f"{source_type}.py"):

    templates: Dict[str, str] = {}
    for source_template in resources.contents(package=SOURCES_TEMPLATES_PATH):
        if source_template.startswith("_"):
            continue
        module_name = source_template.replace(".py", "")
        source = importlib.import_module(SOURCES_TEMPLATES_PATH + "." + module_name)
        templates[module_name] = source.__doc__

    return templates


def get_config_template(source_type: str, source_name: str) -> str:
    """Retrieve the configuration template for a given source type."""
    # return CONFIG_TEMPLATES.get(source_type, "")
    template = CONFIG_TEMPLATES.get(source_type, "")
    return template.replace("{source_name}", source_name)


def get_secrets_template(source_type: str, source_name: str) -> str:
    """Retrieve the secrets template for a given source type."""
    template = SECRETS_TEMPLATES.get(source_type, "")
    return template.replace("{source_name}", source_name)
