from typing import Any, Dict, List, Optional

from typing_extensions import TypedDict


class StructLog(TypedDict):
    depth: int
    gas: int
    gasCost: int
    op: str
    pc: int
    stack: List[str]
    error: Optional[str]
    memory: Optional[List[str]]
    storage: Optional[Dict[str, Any]]


class DebugTraceResult(TypedDict):
    gas: str
    returnValue: str
    structLogs: List[StructLog]
    failed: Optional[bool]
    storage: Optional[Dict[str, Any]]


class SeedSequenceTransaction(TypedDict):
    address: str
    gasLimit: str
    gasPrice: str
    input: str
    origin: str
    value: str
    blockCoinbase: str
    blockDifficulty: str
    blockGasLimit: str
    blockNumber: str
    blockTime: str


EVMTransaction = TypedDict(
    "EVMTransaction",
    {
        "blockCoinbase": str,
        "blockDifficulty": str,
        "blockGasLimit": str,
        "blockTimestamp": str,
        "blockHash": str,
        "blockNumber": str,
        "transactionIndex": str,
        "hash": str,
        "nonce": str,
        "from": str,
        "to": str,
        "value": str,
        "gas": str,
        "gasPrice": str,
        "input": str,
        "v": str,
        "r": str,
        "s": str,
    },
)

EVMBlock = TypedDict(
    "EVMBlock",
    {
        "number": str,
        "hash": str,
        "parentHash": str,
        "mixHash": str,
        "nonce": str,
        "sha3Uncles": str,
        "logsBloom": str,
        "transactionsRoot": str,
        "stateRoot": str,
        "receiptsRoot": str,
        "miner": str,
        "difficulty": str,
        "totalDifficulty": str,
        "extraData": str,
        "size": str,
        "gasLimit": str,
        "gasUsed": str,
        "timestamp": str,
        "transactions": List[EVMTransaction],
        "uncles": List[str],
    },
)
