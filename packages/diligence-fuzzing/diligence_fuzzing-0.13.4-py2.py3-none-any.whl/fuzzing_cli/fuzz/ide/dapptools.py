import json
import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from fuzzing_cli.fuzz.config import FuzzingOptions
from fuzzing_cli.fuzz.exceptions import BuildArtifactsError
from fuzzing_cli.fuzz.ide.generic import IDEArtifacts
from fuzzing_cli.fuzz.types import Contract, Source
from fuzzing_cli.util import get_content_from_file

LOGGER = logging.getLogger("fuzzing-cli")


class DapptoolsArtifacts(IDEArtifacts):
    def __init__(
        self,
        options: FuzzingOptions,
        build_dir: Path,
        sources_dir: Path,
        targets: Optional[List[str]] = None,
        map_to_original_source=False,
    ):
        super(DapptoolsArtifacts, self).__init__(
            options, build_dir, sources_dir, targets, map_to_original_source
        )

    @classmethod
    def get_name(cls) -> str:
        return "dapptools"

    @classmethod
    def validate_project(cls) -> bool:
        root_dir = Path.cwd().absolute()
        files = list(os.walk(root_dir))[0][2]
        return ".dapprc" in files

    @staticmethod
    def get_default_build_dir() -> Path:
        return Path.cwd().joinpath("out")

    @staticmethod
    def get_default_sources_dir() -> Path:
        return Path.cwd().joinpath("src")

    @staticmethod
    def _get_build_artifacts(build_dir) -> tuple:
        build_files_by_source_file = {}
        source_files = {}

        build_dir = Path(build_dir)

        if not build_dir.is_dir():
            raise BuildArtifactsError("Build directory doesn't exist")

        for child in build_dir.glob("**/*"):
            if not child.is_file():
                continue
            if not child.name.endswith(".json"):
                continue

            data = json.loads(child.read_text("utf-8"))
            build_files_by_source_file.update(data["contracts"])
            source_files.update(data["sources"])

        return build_files_by_source_file, source_files

    @lru_cache(maxsize=1)
    def process_artifacts(self) -> Tuple[Dict[str, List[Contract]], Dict[str, Source]]:
        """example build_files_by_source_file
        {
            'contracts': {
                'src/Token.sol':{
                    'Ownable':{
                        abi:[...],
                        evm: {
                            bytecode: {...},
                            deployedBytecode: {...},
                        }
                    },
                    'OtherContractName'
                }
            },
            'sources': {
                'src/Token.sol':{
                    ast: '',
                    id: 0
                }
            }
        }
        """
        # self._get_build_artifacts goes through each .json build file and extracts the Source file it references
        # A source file may contain several contracts, so it is possible that a given source file
        # will be pointed to by multiple build artifacts
        # build_files_by_source_file is a dictionary where the key is a source file name
        # and the value is an array of build artifacts (contracts)
        build_files_by_source_file, source_files = self._get_build_artifacts(
            self.build_dir
        )
        result_contracts: Dict[str, List[Contract]] = {}
        result_sources = {}

        source_ids: List[int] = []

        for source_file_path, source_file in source_files.items():
            # We can select any dict on the build_files_by_source_file[source_file] array
            # because the .source and .ast values will be the same in all.
            target_file = build_files_by_source_file[source_file_path]
            result_sources[source_file_path] = {
                "fileIndex": source_file["id"],
                "source": get_content_from_file(source_file_path),
                "ast": source_file["ast"],
            }
            source_ids.append(source_file["id"])

            if (
                self.map_to_original_source
                and Path(source_file_path + ".original").is_file()
            ):
                # we check if the current source file has a non instrumented version
                # if it does, we include that one as the source code
                result_sources[source_file_path]["source"] = get_content_from_file(
                    source_file_path + ".original"
                )

        # ( 'contracts/Token.sol', {'allSourcePaths':..., 'deployedSourceMap': ... } )
        for source_file, contracts in build_files_by_source_file.items():
            result_contracts[source_file] = []
            for contract_name, contract in contracts.items():
                # We get the build items from dapptools and rename them into the properties used by the FaaS
                try:
                    ignored_sources = self.get_ignored_sources(
                        generated_sources=contract["evm"]["deployedBytecode"].get(
                            "generatedSources"
                        ),
                        source_map=contract["evm"]["deployedBytecode"]["sourceMap"],
                        source_ids=source_ids,
                    )

                    result_contracts[source_file] += [
                        {
                            "sourcePaths": self.get_used_sources(
                                {
                                    str(source_file["id"]): file_path
                                    for file_path, source_file in source_files.items()
                                },
                                contract["evm"]["deployedBytecode"]["sourceMap"],
                            ),
                            "deployedSourceMap": contract["evm"]["deployedBytecode"][
                                "sourceMap"
                            ],
                            "deployedBytecode": contract["evm"]["deployedBytecode"][
                                "object"
                            ],
                            "sourceMap": contract["evm"]["bytecode"]["sourceMap"],
                            "bytecode": contract["evm"]["bytecode"]["object"],
                            "contractName": contract_name,
                            "mainSourceFile": source_file,
                            "ignoredSources": ignored_sources,
                        }
                    ]
                except KeyError as e:
                    raise BuildArtifactsError(
                        f"Build artifact did not contain expected key. Contract: {contract}: \n{e}"
                    )

        return result_contracts, result_sources

    def unlinked_libraries(self) -> List[Tuple[Contract, Set[str]]]:
        # We'll deprecate Dapptools in the future, so we don't implement this method
        return []
