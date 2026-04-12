from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple


class AssemblyContractError(ValueError):
    """Raised when a DAG assembly contract is invalid."""


@dataclass
class AssemblyNode:
    node_id: str
    in_dim: int
    out_dim: int
    op: str = "linear"
    merge: str = "sum"


@dataclass
class AssemblyGraphContract:
    name: str
    nodes: List[AssemblyNode]
    edges: List[Tuple[str, str]]
    input_nodes: List[str]
    output_nodes: List[str]


def _acyclic(node_ids: List[str], edges: List[Tuple[str, str]]) -> bool:
    indeg: Dict[str, int] = {n: 0 for n in node_ids}
    outgoing: Dict[str, List[str]] = {n: [] for n in node_ids}
    for a, b in edges:
        indeg[b] += 1
        outgoing[a].append(b)

    queue = [n for n in node_ids if indeg[n] == 0]
    seen = 0
    while queue:
        n = queue.pop()
        seen += 1
        for nxt in outgoing[n]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    return seen == len(node_ids)


def validate_contract(payload: dict) -> AssemblyGraphContract:
    if not isinstance(payload, dict):
        raise AssemblyContractError("contract must be a JSON object")

    name = str(payload.get("name", "")).strip()
    if not name:
        raise AssemblyContractError("missing contract name")

    raw_nodes = payload.get("nodes")
    if not isinstance(raw_nodes, list) or not raw_nodes:
        raise AssemblyContractError("nodes must be a non-empty list")

    nodes: List[AssemblyNode] = []
    node_ids: List[str] = []
    for idx, raw in enumerate(raw_nodes):
        if not isinstance(raw, dict):
            raise AssemblyContractError(f"node[{idx}] must be an object")
        node_id = str(raw.get("id", "")).strip()
        if not node_id:
            raise AssemblyContractError(f"node[{idx}] missing id")
        if node_id in node_ids:
            raise AssemblyContractError(f"duplicate node id: {node_id}")
        try:
            in_dim = int(raw.get("in_dim"))
            out_dim = int(raw.get("out_dim"))
        except Exception as exc:
            raise AssemblyContractError(f"node {node_id} requires numeric in_dim/out_dim") from exc
        if in_dim <= 0 or out_dim <= 0:
            raise AssemblyContractError(f"node {node_id} requires positive in_dim/out_dim")
        merge = str(raw.get("merge", "sum")).strip() or "sum"
        if merge not in {"sum", "concat"}:
            raise AssemblyContractError(f"node {node_id} has invalid merge '{merge}'")
        nodes.append(
            AssemblyNode(
                node_id=node_id,
                in_dim=in_dim,
                out_dim=out_dim,
                op=str(raw.get("op", "linear")),
                merge=merge,
            )
        )
        node_ids.append(node_id)

    raw_edges = payload.get("edges")
    if not isinstance(raw_edges, list):
        raise AssemblyContractError("edges must be a list")

    edges: List[Tuple[str, str]] = []
    for idx, edge in enumerate(raw_edges):
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            raise AssemblyContractError(f"edge[{idx}] must be [from, to]")
        a, b = str(edge[0]).strip(), str(edge[1]).strip()
        if not a or not b:
            raise AssemblyContractError(f"edge[{idx}] contains empty node id")
        if a not in node_ids or b not in node_ids:
            raise AssemblyContractError(f"edge[{idx}] references unknown node")
        if a == b:
            raise AssemblyContractError(f"edge[{idx}] self-loop is invalid in DAG")
        edges.append((a, b))

    if not _acyclic(node_ids, edges):
        raise AssemblyContractError("graph must be acyclic")

    indeg: Dict[str, int] = {n: 0 for n in node_ids}
    outdeg: Dict[str, int] = {n: 0 for n in node_ids}
    for a, b in edges:
        indeg[b] += 1
        outdeg[a] += 1

    input_nodes = payload.get("input_nodes")
    if input_nodes is None:
        input_nodes = [n for n in node_ids if indeg[n] == 0]
    if not input_nodes:
        raise AssemblyContractError("at least one input node is required")
    for node_id in input_nodes:
        if node_id not in node_ids:
            raise AssemblyContractError(f"input node not declared: {node_id}")

    output_nodes = payload.get("output_nodes")
    if output_nodes is None:
        output_nodes = [n for n in node_ids if outdeg[n] == 0]
    if not output_nodes:
        raise AssemblyContractError("at least one output node is required")
    for node_id in output_nodes:
        if node_id not in node_ids:
            raise AssemblyContractError(f"output node not declared: {node_id}")

    # all non-input nodes need incoming edges
    for node_id in node_ids:
        if node_id not in input_nodes and indeg[node_id] == 0:
            raise AssemblyContractError(f"non-input node without predecessors: {node_id}")

    return AssemblyGraphContract(
        name=name,
        nodes=nodes,
        edges=edges,
        input_nodes=list(input_nodes),
        output_nodes=list(output_nodes),
    )


def contract_summary(contract: AssemblyGraphContract) -> dict:
    return {
        "name": contract.name,
        "node_count": len(contract.nodes),
        "edge_count": len(contract.edges),
        "input_nodes": contract.input_nodes,
        "output_nodes": contract.output_nodes,
        "ops": sorted({n.op for n in contract.nodes}),
        "merges": sorted({n.merge for n in contract.nodes}),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Mom4AI DAG->Model assembly contract.")
    parser.add_argument("--contract-json", required=True, help="Path to contract JSON")
    parser.add_argument("--summary-out", default=None, help="Optional JSON output path for summary")
    args = parser.parse_args()

    payload = json.loads(Path(args.contract_json).read_text(encoding="utf-8"))
    contract = validate_contract(payload)
    summary = contract_summary(contract)

    if args.summary_out:
        out = Path(args.summary_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"summary_written={out}")
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
