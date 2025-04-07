import base64
import json
import os
import tarfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from fuzzing_cli.fuzz.analytics import Session
from fuzzing_cli.fuzz.config import AuthHandler
from fuzzing_cli.fuzz.storage import LocalStorage

# DO NOT DELETE: fixtures import
from tests.testdata.foundry_tests_project.mocks import (
    foundry_build_mock,
    foundry_config_mock,
    foundry_test_list_mock,
)


@pytest.fixture()
def truffle_project(tmp_path):
    with tarfile.open(
        Path(__file__).parent.joinpath(
            "testdata", "truffle_project", "artifacts.tar.gz"
        )
    ) as f:

        def is_within_directory(directory, target):

            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)

            prefix = os.path.commonprefix([abs_directory, abs_target])

            return prefix == abs_directory

        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")

            tar.extractall(path, members, numeric_owner=numeric_owner)

        safe_extract(f, tmp_path)

    for artifact_path in Path(tmp_path).joinpath("build", "contracts").glob("*.json"):
        if artifact_path.name.startswith(
            "."
        ):  # some hidden file (probably created by OS, especially the Mac OS)
            continue
        with artifact_path.open() as f:
            artifact = json.load(f)
            artifact["sourcePath"] = str(
                Path(tmp_path).joinpath("contracts", Path(artifact["sourcePath"]).name)
            )
        with artifact_path.open("w") as f:
            json.dump(artifact, f)

    os.chdir(tmp_path)
    yield {
        "ide": "truffle",
        "build_directory": "build/contracts",
        "sources_directory": "contracts",
        "targets": [
            "contracts/Migrations.sol",
            "contracts/Foo.sol",
            "contracts/Bar.sol",
            "contracts/ABC.sol",
        ],
        "deployed_contract_address": "0x07D9Fb5736CD151C8561798dFBdA5dBCf54cB9E6",
        "additional_addresses": [
            "0x1672fB2eb51789aBd1a9f2FE83d69C6f4C883065",
            "0x6a432C13a2E980a78F941c136ec804e7CB67E0D9",
            "0x6Bcb21De38753e485f7678C7Ada2a63F688b8579",
        ],
    }


@pytest.fixture()
def hardhat_fuzzing_lessons_project(tmp_path):
    with tarfile.open(
        Path(__file__).parent.joinpath(
            "testdata", "hardhat_fuzzing_lessons_project", "artifacts.tar.gz"
        )
    ) as f:

        def is_within_directory(directory, target):

            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)

            prefix = os.path.commonprefix([abs_directory, abs_target])

            return prefix == abs_directory

        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")

            tar.extractall(path, members, numeric_owner=numeric_owner)

        safe_extract(f, tmp_path)
    os.chdir(tmp_path)


@pytest.fixture()
def hardhat_project_with_unlinked_libraries(tmp_path):
    with tarfile.open(
        Path(__file__).parent.joinpath(
            "testdata", "hardhat_project_with_unlinked_libraries", "artifacts.tar.gz"
        )
    ) as f:
        f.extractall(tmp_path)
    os.chdir(tmp_path)
    yield {
        "ide": "hardhat",
        "build_directory": "artifacts",
        "sources_directory": "contracts",
        "targets": [
            "contracts/ABC.sol",
            "contracts/Bar.sol",
            "contracts/Foo.sol",
        ],
        "deployed_contract_address": "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
        "additional_addresses": [
            "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0",
            "0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9",
        ],
    }


@pytest.fixture()
def hardhat_project(tmp_path):
    with tarfile.open(
        Path(__file__).parent.joinpath(
            "testdata", "hardhat_project", "artifacts.tar.gz"
        )
    ) as f:

        def is_within_directory(directory, target):

            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)

            prefix = os.path.commonprefix([abs_directory, abs_target])

            return prefix == abs_directory

        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")

            tar.extractall(path, members, numeric_owner=numeric_owner)

        safe_extract(f, tmp_path)
    os.chdir(tmp_path)
    yield {
        "ide": "hardhat",
        "build_directory": "artifacts",
        "sources_directory": "contracts",
        "targets": [
            "contracts/ABC.sol",
            "contracts/Bar.sol",
            "contracts/Foo.sol",
            "contracts/Migrations.sol",
        ],
        "deployed_contract_address": "0x128B125f3D14338E71AA0C213B3FfC3D545C8c47",
        "additional_addresses": [
            "0x89cf0b64A1612d8AB6320FE8aCfb99E2A1654Dc5",
            "0x81c5D21c4a70ADE85b39689DF5a14B5b5027C28e",
            "0xa5528c75E001Eff845A36577D14a7d3F6F5Ed4C4",
        ],
    }


@pytest.fixture()
def brownie_project(tmp_path):
    with tarfile.open(
        Path(__file__).parent.joinpath(
            "testdata", "brownie_project", "artifacts.tar.gz"
        )
    ) as f:

        def is_within_directory(directory, target):

            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)

            prefix = os.path.commonprefix([abs_directory, abs_target])

            return prefix == abs_directory

        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")

            tar.extractall(path, members, numeric_owner=numeric_owner)

        safe_extract(f, tmp_path)
    os.chdir(tmp_path)
    yield {
        "ide": "brownie",
        "build_directory": "build/contracts",
        "sources_directory": "contracts",
        "targets": [
            "contracts/Foo.sol",
            "contracts/Bar.sol",
            "contracts/ABC.sol",
            "contracts/Migrations.sol",
        ],
        "deployed_contract_address": "0xD94bC01dF83804b671912a866F659E63CC76CfC8",
        "additional_addresses": [
            "0x44C9Fb4D18748B5cc1967fBCF3c1Bd29EDa3B897",
            "0x55DB595E6912454eEE515c44b6D66BC2607DD8e6",
            "0x4d18850465B8a522E98a450Dd951b67f3f159092",
        ],
    }


@pytest.fixture()
def dapptools_project(tmp_path):
    with tarfile.open(
        Path(__file__).parent.joinpath(
            "testdata", "dapptools_project", "artifacts.tar.gz"
        )
    ) as f:

        def is_within_directory(directory, target):

            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)

            prefix = os.path.commonprefix([abs_directory, abs_target])

            return prefix == abs_directory

        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")

            tar.extractall(path, members, numeric_owner=numeric_owner)

        safe_extract(f, tmp_path)
    os.chdir(tmp_path)
    yield {
        "ide": "dapptools",
        "build_directory": "out",
        "sources_directory": "src",
        "targets": ["src/Foo.sol", "src/Bar.sol", "src/ABC.sol", "src/Migrations.sol"],
        "deployed_contract_address": "0xCBB2e00b2EbdAF0296252f3301107052B599B11f",
        "additional_addresses": [
            "0x44F916B4598182465c7C2fDcC559c3d9c6A344fA",
            "0x4D6026D3457843C1f653fC29A8c1033Af6F7D25b",
            "0xA2817092A47fc56E5C88409322E11d5A853B1D31",
        ],
    }


@pytest.fixture()
def scribble_project(tmp_path):
    with tarfile.open(
        Path(__file__).parent.joinpath(
            "testdata", "scribble_project", "artifacts.tar.gz"
        )
    ) as f:

        def is_within_directory(directory, target):

            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)

            prefix = os.path.commonprefix([abs_directory, abs_target])

            return prefix == abs_directory

        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")

            tar.extractall(path, members, numeric_owner=numeric_owner)

        safe_extract(f, tmp_path)
    os.chdir(tmp_path)
    yield {
        "ide": "truffle",
        "build_directory": "build/contracts",
        "sources_directory": "contracts",
        "targets": ["contracts/VulnerableToken.sol"],
        "deployed_contract_address": "0x07D9Fb5736CD151C8561798dFBdA5dBCf54cB9E6",
        "additional_addresses": [
            "0x1672fB2eb51789aBd1a9f2FE83d69C6f4C883065",
            "0x6a432C13a2E980a78F941c136ec804e7CB67E0D9",
            "0x6Bcb21De38753e485f7678C7Ada2a63F688b8579",
        ],
    }


@pytest.fixture()
def truffle_echidna_project(tmp_path, request):
    project_type = (hasattr(request, "param") and request.param) or "annotated"
    with tarfile.open(
        Path(__file__).parent.joinpath(
            "testdata",
            f"quickcheck_project",
            "echidna",
            f"artifacts_{project_type}.tar.gz",
        )
    ) as f:

        def is_within_directory(directory, target):

            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)

            prefix = os.path.commonprefix([abs_directory, abs_target])

            return prefix == abs_directory

        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")

            tar.extractall(path, members, numeric_owner=numeric_owner)

        safe_extract(f, tmp_path)
    os.chdir(tmp_path)
    yield {
        "ide": "truffle",
        "build_directory": "build/contracts",
        "sources_directory": "contracts",
        "targets": [
            "contracts/VulnerableTokenTest.sol",
            "contracts/SecondVulnerableTokenTest.sol",
        ],
    }


@pytest.fixture()
def foundry_project(tmp_path):
    with tarfile.open(
        Path(__file__).parent.joinpath(
            "testdata", "foundry_project", "artifacts.tar.gz"
        )
    ) as f:
        f.extractall(tmp_path)
    os.chdir(tmp_path)
    yield {
        "ide": "foundry",
        "build_directory": "out",
        "sources_directory": "src",
        "targets": ["src/Foo.sol", "src/Bar.sol", "src/ABC.sol"],
        "deployed_contract_address": "0x0c91f9338228f19315BE34E5CA5307DF586CBD99",
        "additional_addresses": [
            "0x9B92063B8B94A9EF8b5fDE3Df8D375B39bC9fC10",
            "0x694D08b77D2499E161635005Fd4A77233cedD761",
        ],
    }


@pytest.fixture()
def foundry_project_with_unlinked_libraries(tmp_path):
    with tarfile.open(
        Path(__file__).parent.joinpath(
            "testdata", "foundry_project_with_unlinked_libraries", "artifacts.tar.gz"
        )
    ) as f:
        f.extractall(tmp_path)
    os.chdir(tmp_path)
    yield {
        "ide": "foundry",
        "build_directory": "out",
        "sources_directory": "src",
        "targets": ["src/Foo.sol", "src/Bar.sol", "src/ABC.sol"],
        "deployed_contract_address": "0x0c91f9338228f19315BE34E5CA5307DF586CBD99",
        "additional_addresses": [
            "0x9B92063B8B94A9EF8b5fDE3Df8D375B39bC9fC10",
            "0x694D08b77D2499E161635005Fd4A77233cedD761",
        ],
    }


@pytest.fixture()
def foundry_tests_project(tmp_path):
    with tarfile.open(
        Path(__file__).parent.joinpath(
            "testdata", "foundry_tests_project", "artifacts.tar.gz"
        )
    ) as f:
        f.extractall(tmp_path)
    os.chdir(tmp_path)
    yield {
        "ide": "foundry",
        "build_directory": "out",
        "sources_directory": "src",
        "targets": ["src/Foo.sol", "src/Bar.sol", "src/ABC.sol"],
        "deployed_contract_address": "0x0c91f9338228f19315BE34E5CA5307DF586CBD99",
        "additional_addresses": [
            "0x9B92063B8B94A9EF8b5fDE3Df8D375B39bC9fC10",
            "0x694D08b77D2499E161635005Fd4A77233cedD761",
        ],
    }


@pytest.fixture()
def api_key(monkeypatch):
    monkeypatch.setenv(
        "FUZZ_API_KEY", "dGVzdC1jbGllbnQtMTIzOjpleGFtcGxlLXVzLmNvbQ==::2"
    )
    yield
    monkeypatch.delenv("FUZZ_API_KEY", raising=False)


@pytest.fixture(autouse=True)
def setup_storages(tmp_path):
    Session.set_session_path(Path(str(tmp_path) + "/session.json"))
    LocalStorage.set_instance(LocalStorage(str(tmp_path)))


@pytest.fixture(autouse=True)
def mocked_auth_handler():
    mocked_jwt_token = f"header.{base64.b64encode(json.dumps({'sub': 'test-user'}).encode()).decode()}.tail"
    orig = AuthHandler._get_access_token
    with patch.object(
        AuthHandler,
        "_get_access_token",
        new=Mock(return_value=(mocked_jwt_token, 100000)),
    ) as _get_access_token_mock:

        def restore_original():
            AuthHandler._get_access_token = orig

        setattr(_get_access_token_mock, "restore_original", restore_original)
        yield _get_access_token_mock


@pytest.fixture(autouse=True)
def no_analytics(monkeypatch):
    monkeypatch.setenv("FUZZ_ALLOW_ANALYTICS", "false")


@pytest.fixture()
def ci_mode(monkeypatch):
    monkeypatch.setenv("FUZZ_CI_MODE", "true")


@pytest.fixture(autouse=True)
def no_updates_check(monkeypatch):
    monkeypatch.setenv("FUZZ_CHECK_UPDATES", "false")
    yield
    monkeypatch.delenv("FUZZ_CHECK_UPDATES", raising=False)


@pytest.fixture()
def allow_updates_check(monkeypatch):
    monkeypatch.setenv("FUZZ_CHECK_UPDATES", "true")
    yield
    monkeypatch.delenv("FUZZ_CHECK_UPDATES", raising=False)
