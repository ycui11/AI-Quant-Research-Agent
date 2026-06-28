# 01 State Design

## Goal

Phase 0 defines the state contract before implementing agents, tools, or a
LangGraph workflow. The central idea is that every workflow node should read
from and write to a typed `ResearchContext`, making the state of the research
process inspectable and reproducible.

## Core State

`ResearchContext` contains the nine fields described in the README:

- `user_request`
- `task_plan`
- `market_data`
- `factors`
- `backtest_results`
- `performance_metrics`
- `diagnosis`
- `experiment_suggestions`
- `report`

The context is intentionally sparse at the beginning of a run. Fields such as
`task_plan`, `backtest_results`, `performance_metrics`, and `diagnosis` start as
`None` because they are produced by later workflow nodes.

## Why Explicit State

An agent should not rely on hidden conversation history as its only source of
truth. Chat history is useful for interaction, but it is weak as a system
interface because it is hard to validate, hard to replay, and hard to audit.

Explicit state gives the workflow:

- clear contracts between nodes
- validation before downstream execution
- serialization for persistence
- a stable debugging surface
- a path toward experiment replay

This is especially important for quant research, where a report should be
traceable back to its plan, input data, factor values, backtest output, and
diagnosis.

## Why Pydantic

Pydantic is used instead of plain dictionaries because this project needs more
than flexible containers. The state should reject invalid shapes early, normalize
common inputs, and serialize cleanly.

Examples:

- `TaskPlan.asset` is normalized to uppercase.
- `TaskPlan.timeframe` must look like `5m`, `1h`, or `1d`.
- date ranges must have `end_time` after `start_time`.
- unknown fields are rejected.
- nested state can round-trip through JSON.

## Alternatives Considered

### Plain Dictionary

A plain dictionary is easy to update in a graph, but it provides no schema,
weak validation, and no reliable interface for downstream nodes. It would make
early prototyping slightly faster while making later debugging harder.

### Dataclass

A dataclass gives a clearer structure than a dictionary, but runtime validation
and JSON serialization would need to be added manually or through additional
helpers.

### TypedDict

`TypedDict` is useful for static type checking, but it does not validate runtime
LLM outputs or user inputs. Since future planner nodes will consume structured
LLM output, runtime validation is a core requirement.

## DataFrame Boundary

The Phase 0 state uses serializable records for `market_data` and `factors`
instead of storing Pandas DataFrames directly. The deterministic tool layer can
convert records into DataFrames internally and return records or artifact
references to the context.

This keeps the central state easier to persist in JSON or DuckDB and prevents
workflow memory from becoming tied to a single in-process Python object.

## Current Tradeoff

The state model is strict, but the `market_data` and `factors` records are still
typed as dictionaries. This is intentional for Phase 0 because the exact market
data and factor schemas should be finalized when the deterministic tools are
implemented. Once those tools exist, these fields can be narrowed to explicit
OHLCV and factor record models.
