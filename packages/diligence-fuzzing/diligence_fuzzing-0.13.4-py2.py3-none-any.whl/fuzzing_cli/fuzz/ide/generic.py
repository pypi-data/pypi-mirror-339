import json
import re
from abc import ABC, abstractmethod
from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

import cbor2

from fuzzing_cli.fuzz.config import FuzzingOptions
from fuzzing_cli.fuzz.exceptions import BuildArtifactsError, EmptyArtifactsError
from fuzzing_cli.fuzz.types import Contract, IDEPayload, Source
from fuzzing_cli.util import LOGGER, sol_files_by_directory

ContractKind = Literal["contract", "interface", "library"]

UNLINKED_LIB_HASH_REGEX = re.compile("__\$(\w{34})\$__")


class IDEArtifacts(ABC):
    def __init__(
        self,
        options: FuzzingOptions,
        build_dir: Path,
        sources_dir: Path,
        targets: Optional[List[str]] = None,
        map_to_original_source: bool = False,
    ):
        self._payload: Optional[IDEPayload] = None
        self._options = options
        self.targets = targets
        self.build_dir = build_dir
        self.sources_dir = sources_dir
        self.map_to_original_source = map_to_original_source

        # self._include is an array with all the solidity file paths under the targets
        self._include: Set[str] = set([])
        if targets:
            self.set_targets(targets)

    def set_targets(self, targets: List[str]):
        include = set([])
        for target in targets:
            include.update(
                [self.normalize_path(p) for p in sol_files_by_directory(Path(target))]
            )
        self._include = include

    @staticmethod
    def instance_for_targets(
        artifacts: "IDEArtifacts", targets: List[str]
    ) -> "IDEArtifacts":
        _artifacts_for_targets = deepcopy(artifacts)
        _artifacts_for_targets.set_targets(targets)
        return _artifacts_for_targets

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:  # pragma: no cover
        pass

    @classmethod
    @abstractmethod
    def validate_project(cls) -> bool:  # pragma: no cover
        pass

    @property
    def contracts(self) -> List[Contract]:
        return self.fetch_data()[0]

    @property
    def sources(self) -> Dict[str, Source]:
        return self.fetch_data()[1]

    @staticmethod
    @abstractmethod
    def get_default_build_dir() -> Path:  # pragma: no cover
        pass

    @staticmethod
    @abstractmethod
    def get_default_sources_dir() -> Path:  # pragma: no cover
        pass

    @staticmethod
    def _get_build_artifacts(build_dir: Path) -> Dict:
        # _get_build_artifacts goes through each .json build file and extracts the Source file it references
        # A source file may contain several contracts, so it is possible that a given source file
        # will be pointed to by multiple build artifacts
        # build_files_by_source_file is a dictionary where the key is a source file name
        # and the value is an array of build artifacts (contracts)
        build_files_by_source_file = {}

        if not build_dir.is_dir():
            raise BuildArtifactsError("Build directory doesn't exist")

        for child in build_dir.glob("**/*"):
            if not child.is_file():
                continue
            if not child.name.endswith(".json"):
                continue

            if child.name.startswith(
                "."
            ):  # some hidden file (probably created by OS, especially the Mac OS)
                continue

            data = json.loads(child.read_text("utf-8"))

            source_path = str(Path(data["sourcePath"]).as_posix())
            data["sourcePath"] = source_path

            if source_path not in build_files_by_source_file:
                # initialize the array of contracts with a list
                build_files_by_source_file[source_path] = []

            build_files_by_source_file[source_path].append(data)

        return build_files_by_source_file

    def flatten_contracts(self, contracts: Dict[str, List[Contract]]) -> List[Contract]:
        return [
            c for contracts_for_file in contracts.values() for c in contracts_for_file
        ]

    @staticmethod
    def compare_bytecode(x: str, y: str) -> bool:
        if x.startswith("0x"):
            x = x[2:]
        if y.startswith("0x"):
            y = y[2:]
        return x == y

    @staticmethod
    def get_metadata_hash(deployed_bytecode) -> Optional[str]:
        if not deployed_bytecode or deployed_bytecode == "0x":
            return None
        metadata_length = int(deployed_bytecode[-4:], 16) * 2
        encoded_metadata = deployed_bytecode[-(metadata_length + 4) : -4]
        try:
            metadata = cbor2.loads(bytes.fromhex(encoded_metadata))
            if (
                type(metadata) is not dict
            ):  # maybe we've got break_marker thus parsing wasn't successful
                # It's possible when metadata hash wasn't included in the bytecode (--metadata-hash=none param to solc)
                # or it's just an invalid bytecode
                return None
            for _hash_type in ("ipfs", "bzzr0", "bzzr1"):
                if _hash_type not in metadata:
                    continue
                return metadata[_hash_type].hex().lower()
            LOGGER.debug(
                f'Cannot find suitable metadata hash. Encoded metadata "{encoded_metadata}". Decoded metadata "{json.dumps(metadata)}"'
            )
            return None
        except Exception as e:
            LOGGER.debug(
                f'Exception decoding metadata from the bytecode. Encoded metadata "{encoded_metadata}". Exception: {e}'
            )
            return None

    def get_contract(self, deployed_bytecode: str) -> Optional[Contract]:
        metadata_hash = self.get_metadata_hash(deployed_bytecode)
        if metadata_hash is None:
            LOGGER.debug(
                f"Could not get metadata hash from the deployed bytecode: {deployed_bytecode}. "
                f"Falling back to bytecode comparison"
            )
        result_contracts, _ = self.process_artifacts()
        LOGGER.debug(
            f"Searching a contract with the deployed bytecode metadata hash: {metadata_hash}"
        )
        for _, contracts in result_contracts.items():
            for contract in contracts:
                if metadata_hash is None:
                    # Search for contract by comparing whole bytecode instead of metadata hash comparison.
                    # It's handy for cases when metadata hash is not present in the bytecode
                    # (due to metadata.bytecodeHash = none in solc params)
                    if self.compare_bytecode(
                        deployed_bytecode, contract["deployedBytecode"]
                    ):
                        LOGGER.debug("Matching contract is found")
                        return contract
                    continue

                contract_metadata_hash = self.get_metadata_hash(
                    contract["deployedBytecode"]
                )
                if contract_metadata_hash is None:
                    LOGGER.debug(
                        f"Skipping the contract \"{contract['contractName']}\" because of metadata hash absence"
                    )
                    continue
                LOGGER.debug(
                    f"Comparing with the contract \"{contract['contractName']}\" with metadata hash: {contract_metadata_hash}"
                )
                if metadata_hash == contract_metadata_hash:
                    LOGGER.debug("Matching contract is found")
                    return contract
        return None

    @lru_cache(1)
    def _contracts_kind_mapping(self) -> Dict[str, Dict[str, ContractKind]]:
        _result_contracts, _result_sources = self.process_artifacts()
        types_mapping = defaultdict(dict)
        for source_file_name, _ in _result_contracts.items():
            # we need to `get` `source_file_name` because it's possible that some source files
            # are not present in the sources directory.
            ast = _result_sources.get(source_file_name, {}).get("ast")
            if not ast:
                continue
            for node in ast["nodes"]:
                if node["nodeType"] != "ContractDefinition":
                    continue
                contract_name = node["name"]
                types_mapping[source_file_name][contract_name] = node["contractKind"]
        return types_mapping

    def _get_contract_kind(self, contract: Contract) -> ContractKind:
        return (
            self._contracts_kind_mapping().get(contract["mainSourceFile"], {})
            # if contract is not found in the mapping, we assume it's a contract
            .get(contract["contractName"], "contract")
        )

    def include_contract(self, contract: Contract) -> bool:
        # if contract is library, we would not include it by default
        # (because it will be included by default in the main contract). However,
        # there are cases when we need to include libraries as well (because it supposed to be deployed),
        # so we need to check `include_library_contracts` option.
        if (
            self._get_contract_kind(contract) == "library"
            and not self._options.include_library_contracts
        ):
            return False

        if len(self._include) == 0:
            # for case when targets are not specified
            return True

        source_path = contract["mainSourceFile"]
        if not contract["bytecode"] or not contract["deployedBytecode"]:
            return False
        if self.normalize_path(source_path) not in self._include:
            return False
        if (
            self._options.target_contracts
            and not contract["contractName"]
            in self._options.target_contracts[source_path]
        ):
            return False

        return True

    @staticmethod
    def fallback_check_unlinked_libraries(
        contracts: List[Contract],
    ) -> List[Tuple[Contract, Set[str]]]:
        unlinked_libraries = []
        for contract in contracts:
            libs_hashes = set(
                UNLINKED_LIB_HASH_REGEX.findall(contract["bytecode"])
                + UNLINKED_LIB_HASH_REGEX.findall(contract["deployedBytecode"])
            )
            if len(libs_hashes) > 0:
                unlinked_libraries.append((contract, libs_hashes))
        return unlinked_libraries

    @abstractmethod
    def unlinked_libraries(
        self,
    ) -> List[Tuple[Contract, Dict[str, Set[str]]]]:  # pragma: no cover
        pass

    @lru_cache(maxsize=1)
    def fetch_data(self) -> Tuple[List[Contract], Dict[str, Source]]:
        _result_contracts, _result_sources = self.process_artifacts()
        result_contracts = [
            contract
            for contract in self.flatten_contracts(_result_contracts)
            if self.include_contract(contract)
        ]

        unlinked_libs = self.unlinked_libraries()

        if len(unlinked_libs) > 0:
            _details = []
            for contract, libs in unlinked_libs:
                for lib_path, lib_names in libs.items():
                    for lib_name in lib_names:
                        _details.append(
                            f"  ◦ Contract: \"{contract['contractName']}\" "
                            f"Contract path: \"{contract['mainSourceFile']}\" Library: \"{lib_name}\" Library path: \"{lib_path}\""
                        )

            details = "\n".join(_details)
            raise BuildArtifactsError(
                f"Following contracts have unlinked libraries:\n{details}\n"
                f"For more info on library linking please visit "
                f"https://docs.soliditylang.org/en/latest/using-the-compiler.html#library-linking"
            )
        else:
            unlinked_libs = self.fallback_check_unlinked_libraries(result_contracts)
            if len(unlinked_libs) > 0:
                details = "\n".join(
                    [
                        f"  ◦ Contract: {contract['contractName']} "
                        f"Contract path: {contract['mainSourceFile']} Library hash: {lib_hash}"
                        for contract, libs in unlinked_libs
                        for lib_hash in libs
                    ]
                )
                raise BuildArtifactsError(
                    f"Following contracts have unlinked libraries:\n{details}\n"
                    f"Fuzzing CLI provides only library hashes because it wasn't able to one's name and path "
                    f"from compilation artifacts. Please check your IDE settings to enable full solc compiler output.\n"
                    f"For more info on library linking please visit "
                    f"https://docs.soliditylang.org/en/latest/using-the-compiler.html#library-linking"
                )

        used_files = set()
        for contract in result_contracts:
            used_files.update(contract["sourcePaths"].values())

        result_sources = {k: v for k, v in _result_sources.items() if k in used_files}
        return result_contracts, result_sources

    @abstractmethod
    def process_artifacts(
        self,
    ) -> Tuple[Dict[str, List[Contract]], Dict[str, Source]]:  # pragma: no cover
        pass

    def normalize_path(self, path: Union[str, Path]) -> Path:
        if Path(path).is_absolute():
            return Path(path)
        _path = self.sources_dir.parent.joinpath(path)
        LOGGER.debug(
            f'Normalizing path "{path}" relative to source_dir. Absolute path "{_path}"'
        )
        return _path

    @staticmethod
    def as_posix(path: str) -> str:
        return str(Path(path).as_posix())

    def validate(self) -> None:
        if len(self.sources.keys()) == 0 or len(self.contracts) == 0:
            raise EmptyArtifactsError()

    @staticmethod
    def get_ignored_sources(
        generated_sources: Optional[List[Dict[str, any]]] = None,
        source_map: str = "",
        source_ids: List[int] = [],
    ) -> List[int]:
        if generated_sources:  # compiler output has generated sources data
            ignored_sources = set()
            for generated_source in generated_sources:
                if generated_source["language"].lower() == "yul" and type(
                    generated_source["id"] is int
                ):
                    ignored_sources.add(generated_source["id"])
            return sorted(list(ignored_sources))

        sm = source_map.split(";")
        all_file_ids = set()
        for c in sm:
            component = c.split(":")
            if len(component) < 3 or component[2] == "":
                continue
            all_file_ids.add(component[2])
        return sorted(
            [int(file_id) for file_id in all_file_ids if int(file_id) not in source_ids]
        )

    @staticmethod
    def get_used_sources(
        source_paths: Dict[str, str], source_map: str
    ) -> Dict[str, str]:
        sm = source_map.split(";")
        all_file_ids = set()
        for c in sm:
            component = c.split(":")
            if len(component) < 3 or component[2] == "":
                continue
            all_file_ids.add(component[2])
        return {
            file_id: name
            for file_id, name in source_paths.items()
            if file_id in all_file_ids
        }

    @staticmethod
    def detect_unlinked_libs(contract: Dict[str, Any]) -> Dict[str, Set[str]]:
        unlinked_libs: Dict[str, Set[str]] = defaultdict(set)

        bytecode_link_ref = contract["evm"]["bytecode"].get("linkReferences", {})
        deployed_bytecode_link_ref = contract["evm"]["deployedBytecode"].get(
            "linkReferences", {}
        )

        if bytecode_link_ref:
            # here we are collecting all the unlinked libraries for the contract
            for lib_file_path in bytecode_link_ref.keys():
                for lib_name in bytecode_link_ref[lib_file_path].keys():
                    unlinked_libs[lib_file_path].add(lib_name)

        if deployed_bytecode_link_ref:
            for lib_file_path in deployed_bytecode_link_ref.keys():
                for lib_name in deployed_bytecode_link_ref[lib_file_path].keys():
                    unlinked_libs[lib_file_path].add(lib_name)

        return unlinked_libs
