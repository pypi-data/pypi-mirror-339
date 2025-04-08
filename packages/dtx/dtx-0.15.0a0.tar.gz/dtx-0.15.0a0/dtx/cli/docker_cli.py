import argparse
import logging
import os
import shutil
import sys
from pathlib import Path

import docker
import yaml
from pydantic import BaseModel, Field

from dtx.core.models.providers.base import ProviderType

from .datasetargs import DatasetArgs
from .evaluatorargs import EvalMethodArgs
from .format import SmartFormatter
from .workspace import (
    WorkspaceManager,
)

# Add this at the top of your `main()` function
dataset_args = DatasetArgs()
evaluator_args = EvalMethodArgs()

DEFAULT_WORKDIR = os.path.join(Path.home(), ".dtx")
TEMPLATES_DIR = os.path.join(DEFAULT_WORKDIR, "templates")
REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "OPENAI_API_BASE_URL",
    "HF_TOKEN",
    "DETOXIO_API_KEY",
    "DETOXIO_BASE_URL",
]

TMP_DIR_HOST = os.path.join(DEFAULT_WORKDIR, "tmp")
TMP_DIR_CONTAINER = "/app/.dtx/tmp"

FILE_ARG_MAPPING = {
    ("redteam", "scope"): {"output": "output"},
    ("redteam", "plan"): {"scope_file": "input", "output": "output"},
    ("redteam", "run"): {"plan_file": "input", "yml": "output"},
}


# --- Config model using Pydantic ---
class DtxConfig(BaseModel):
    docker_image: str = Field(default="detoxio/dtx:latest")
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    base_url: str = Field(
        default_factory=lambda: os.getenv(
            "OPENAI_API_BASE_URL", "https://api.openai.com/v1"
        )
    )
    default_dataset: str = "basic"
    default_output: str = "redteam_scope.yml"

    @classmethod
    def load(cls, path: str):
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            default_config = cls()
            with open(path, "w") as f:
                yaml.dump(default_config.dict(), f)
            return default_config

        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f) or {}
            return cls(**data)
        except Exception as e:
            print(f"\n⚠️  Error loading config from {path}: {e}")
            choice = (
                input(
                    "Config file appears to be corrupted. Recreate a new one? [y/N]: "
                )
                .strip()
                .lower()
            )
            if choice == "y":
                backup_path = path + ".bak"
                shutil.move(path, backup_path)
                print(f"🔁 Old config backed up as: {backup_path}")
                default_config = cls()
                with open(path, "w") as f:
                    yaml.dump(default_config.dict(), f)
                print(f"✅ New config created at: {path}")
                return default_config
            else:
                print("❌ Aborting due to config error.")
                sys.exit(1)


class DockerDtxCli:
    def __init__(self, args):
        self.args = args
        self.verbose = getattr(args, "verbose", False)
        self.logger = logging.getLogger("DockerDtxCli")
        self.docker_client = docker.from_env()
        self.config = DtxConfig.load(os.path.join(DEFAULT_WORKDIR, "docker_dtx.yml"))
        self.output_files = {}

        self._setup_logger()
        self._check_docker_running()
        self._process_file_args()

    def _setup_logger(self):
        log_level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")

    def _check_docker_running(self):
        try:
            self.docker_client.ping()
            self.logger.debug("Docker is running and accessible.")
        except docker.errors.DockerException as e:
            self.logger.error("❌ Docker does not seem to be running or accessible.")
            self.logger.debug(f"Docker error: {e}")
            sys.exit(1)

    def run(self):
        command_map = {
            "redteam": self._run_dynamic_command,
            "datasets": self._run_dynamic_command,
            "plugins": self._run_dynamic_command,
            "tactics": self._run_dynamic_command,
            "version": self._handle_version,
        }

        handler = command_map.get(self.args.command)
        if handler:
            handler()
        else:
            self.logger.error("Unsupported command")
            sys.exit(1)

    def _handle_version(self):
        if self.args.version_command == "upgrade":
            self.logger.info(f"Pulling latest Docker image: {self.config.docker_image}")
            try:
                self.docker_client.images.pull(self.config.docker_image)
                print(f"✅ Upgraded: {self.config.docker_image}")
            except docker.errors.APIError as e:
                self.logger.error(f"Failed to pull image: {e}")
                sys.exit(1)
        else:
            print(f"📦 Current Docker image: {self.config.docker_image}")

    def _run_dynamic_command(self):
        docker_cmd = self._build_docker_command()
        self._run_container(docker_cmd)
        self._copy_back_output_files()

    def _build_docker_command(self):
        cmd = []

        if self.args.command == "redteam":
            sub = self.args.redteam_command
            if sub == "scope":
                cmd = ["redteam", "scope", self.args.description, self.args.output]
            elif sub == "plan":
                cmd = [
                    "redteam",
                    "plan",
                    self.args.scope_file,
                    self.args.output,
                    "--max_prompts",
                    str(self.args.max_prompts),
                    "--prompts_per_risk",
                    str(self.args.prompts_per_risk),
                    "--dataset",
                    self.args.dataset,
                ]
            elif sub == "run":
                cmd = [
                    "redteam",
                    "run",
                    self.args.plan_file,
                    self.args.agent,
                    "--url",
                    self.args.url,
                    "--max_prompts",
                    str(self.args.max_prompts),
                    "--yml",
                    self.args.yml,
                ]
                if self.args.no_rich:
                    cmd.append("--no-rich")
                for tactic in self.args.tactics:
                    cmd += ["--tactics", tactic]

        elif self.args.command in ["datasets", "plugins", "tactics"]:
            # Handle "list" subcommands
            sub_command_attr = f"{self.args.command}_command"
            sub = getattr(self.args, sub_command_attr, None)
            if sub == "list":
                cmd = [self.args.command, "list"]

        return cmd

    def _run_container(self, docker_cmd):
        volumes = {
            os.path.abspath(DEFAULT_WORKDIR): {"bind": "/app/.dtx", "mode": "rw"}
        }
        environment = {
            key: os.environ[key] for key in REQUIRED_ENV_VARS if key in os.environ
        }

        self.logger.info(f"Starting Docker container for: {docker_cmd}")
        self.logger.debug(f"Image: {self.config.docker_image}")
        self.logger.debug(f"Command: {docker_cmd}")
        self.logger.debug(f"Volumes: {volumes}")
        self.logger.debug(f"Environment vars: {environment}")

        try:
            output = self.docker_client.containers.run(
                image=self.config.docker_image,
                command=docker_cmd,
                volumes=volumes,
                tty=True,
                remove=True,
                environment=environment,
            )
            print(output.decode("utf-8") if isinstance(output, bytes) else output)
        except docker.errors.ContainerError as e:
            self.logger.error(f"[Container Error] {e}")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"[Unexpected Error] {e}")
            sys.exit(1)

    def _process_file_args(self):
        cmd = self.args.command
        subcmd = getattr(self.args, f"{cmd}_command", None)
        key = (cmd, subcmd)
        if key not in FILE_ARG_MAPPING:
            return

        for arg_name, io_type in FILE_ARG_MAPPING[key].items():
            original_path = getattr(self.args, arg_name)
            filename = os.path.basename(original_path)
            tmp_host_path = os.path.join(TMP_DIR_HOST, filename)
            container_path = os.path.join(TMP_DIR_CONTAINER, filename)

            if io_type == "input":
                if not os.path.exists(original_path):
                    self.logger.error(f"Input file '{original_path}' not found.")
                    sys.exit(1)
                shutil.copy(original_path, tmp_host_path)
                self.logger.debug(
                    f"Copied input file: {original_path} -> {tmp_host_path}"
                )
                setattr(self.args, arg_name, container_path)
            elif io_type == "output":
                self.output_files[arg_name] = original_path
                setattr(self.args, arg_name, container_path)

    def _copy_back_output_files(self):
        for arg_name, dest in self.output_files.items():
            container_path = getattr(self.args, arg_name)
            filename = os.path.basename(container_path)
            tmp_host_path = os.path.join(TMP_DIR_HOST, filename)

            if os.path.exists(tmp_host_path):
                shutil.copy(tmp_host_path, dest)
                self.logger.info(f"Copied output file: {tmp_host_path} -> {dest}")
            else:
                self.logger.warning(f"Expected output not found: {tmp_host_path}")


# Parse args inside `main()`
def main():
    parser = argparse.ArgumentParser(description="Docker DTX CLI wrapper")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug output"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Enable development mode: mount local code and install in editable mode",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # === templates ===
    templates_parser = subparsers.add_parser(
        "templates", help="Manage redteam templates"
    )
    templates_subparsers = templates_parser.add_subparsers(dest="templates_command")
    templates_subparsers.add_parser("update", help="Pull latest templates")
    templates_subparsers.add_parser("list", help="List available templates")

    # === redteam ===
    redteam_parser = subparsers.add_parser(
        "redteam",
        help="Red teaming operations",
        formatter_class=lambda prog: SmartFormatter(
            prog, max_help_position=40, width=150
        ),
    )
    redteam_subparsers = redteam_parser.add_subparsers(dest="redteam_command")

    scope_parser = redteam_subparsers.add_parser(
        "scope", help="Generate red team scope"
    )
    scope_parser.add_argument("description", type=str)
    scope_parser.add_argument(
        "output", type=str, nargs="?", default="redteam_scope.yml"
    )

    plan_parser = redteam_subparsers.add_parser(
        "plan",
        help="Generate red team plan",
        formatter_class=lambda prog: SmartFormatter(
            prog, max_help_position=40, width=150
        ),
    )
    plan_parser.add_argument("scope_file", type=str)
    plan_parser.add_argument("output", type=str, nargs="?", default="redteam_plan.yml")
    plan_parser.add_argument("--max_prompts", type=int, default=20)
    plan_parser.add_argument("--prompts_per_risk", type=int, default=5)
    dataset_args.augment_args(plan_parser)

    run_parser = redteam_subparsers.add_parser(
        "run",
        help="Run red team tests",
        formatter_class=lambda prog: SmartFormatter(
            prog, max_help_position=40, width=150
        ),
    )
    run_parser.add_argument("agent", type=ProviderType, choices=ProviderType.values())
    run_parser.add_argument("--url", type=str, default="")
    run_parser.add_argument("--plan_file", type=str)
    run_parser.add_argument("--max_prompts", type=int, default=20)
    run_parser.add_argument("--tactics", type=str, action="append", default=[])
    run_parser.add_argument("--yml", type=str, default="report.yml")
    run_parser.add_argument("--no-rich", action="store_true")
    dataset_args.augment_args(run_parser)
    evaluator_args.augment_args(run_parser)

    # === datasets ===
    datasets_parser = subparsers.add_parser("datasets", help="Manage datasets")
    datasets_subparsers = datasets_parser.add_subparsers(dest="datasets_command")
    datasets_subparsers.add_parser("list", help="List available datasets")

    # === plugins ===
    plugins_parser = subparsers.add_parser("plugins", help="Manage plugins")
    plugins_subparsers = plugins_parser.add_subparsers(dest="plugins_command")
    plugins_subparsers.add_parser("list", help="List available plugins")

    # === tactics ===
    tactics_parser = subparsers.add_parser("tactics", help="Manage tactics")
    tactics_subparsers = tactics_parser.add_subparsers(dest="tactics_command")
    tactics_subparsers.add_parser("list", help="List available tactics")

    # === version ===
    version_parser = subparsers.add_parser(
        "version", help="Show Docker image version or upgrade"
    )
    version_subparsers = version_parser.add_subparsers(dest="version_command")
    version_subparsers.add_parser("upgrade", help="Pull the latest Docker image")

    # === Parse arguments ===
    args = parser.parse_args()

    # === Prepare workspace and env ===
    workspace = WorkspaceManager(
        base_dir=DEFAULT_WORKDIR,
        template_dir=TEMPLATES_DIR,
        required_env_vars=REQUIRED_ENV_VARS,
    )
    workspace.prepare()

    # === Handle workspace-only commands ===
    if args.command == "templates":
        workspace.handle_templates(args)

    # === Delegate to Docker CLI ===
    docker_cli = DockerDtxCli(args)
    docker_cli.run()


if __name__ == "__main__":
    main()
