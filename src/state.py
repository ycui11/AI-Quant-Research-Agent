"""Typed workflow state for the quant research agent system.

Phase 0 intentionally models state only. Agent behavior, tools, and graph
execution are introduced in later phases.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
    field_validator,
    model_validator,
)


StrategyType = Literal["momentum", "mean_reversion", "breakout"]
StrategyQuality = Literal["promising", "flawed", "inconclusive"]
RiskLevel = Literal["low", "medium", "high"]


class StrictModel(BaseModel):
    """Base model with closed schemas and assignment validation."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class TaskPlan(StrictModel):
    """Structured research plan produced by the planner."""

    asset: str = Field(..., min_length=2, description="Tradable symbol, e.g. BTCUSDT.")
    timeframe: str = Field(..., description="Bar interval such as 5m, 1h, or 1d.")
    strategy_type: StrategyType
    lookback_bars: PositiveInt = Field(..., description="Number of bars used by the signal.")
    holding_period_bars: PositiveInt = Field(
        ..., description="Number of bars the strategy expects to hold a position."
    )
    start_time: datetime | None = None
    end_time: datetime | None = None
    initial_capital: PositiveFloat = 10_000.0
    transaction_cost_bps: NonNegativeFloat = 5.0
    parameters: dict[str, Any] = Field(default_factory=dict)

    @field_validator("asset")
    @classmethod
    def normalize_asset(cls, value: str) -> str:
        symbol = value.strip().upper()
        if not symbol.isalnum():
            raise ValueError("asset must contain only letters and numbers")
        return symbol

    @field_validator("timeframe")
    @classmethod
    def normalize_timeframe(cls, value: str) -> str:
        timeframe = value.strip().lower()
        if not re.fullmatch(r"[1-9][0-9]*[mhdw]", timeframe):
            raise ValueError("timeframe must look like 5m, 1h, 1d, or 1w")
        return timeframe

    @model_validator(mode="after")
    def validate_time_range(self) -> "TaskPlan":
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class EquityPoint(StrictModel):
    """Single point in a strategy equity curve."""

    timestamp: datetime
    equity: float


class BacktestResult(StrictModel):
    """Deterministic output from a backtest run."""

    start_time: datetime | None = None
    end_time: datetime | None = None
    observations: NonNegativeInt = 0
    trade_count: NonNegativeInt = 0
    gross_return: float = 0.0
    net_return: float = 0.0
    equity_curve: list[EquityPoint] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_time_range(self) -> "BacktestResult":
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class PerformanceMetrics(StrictModel):
    """Summary metrics derived from a backtest result."""

    total_return: float
    annualized_return: float | None = None
    volatility: NonNegativeFloat | None = None
    sharpe_ratio: float | None = None
    max_drawdown: float
    win_rate: float | None = Field(default=None, ge=0.0, le=1.0)
    turnover: NonNegativeFloat | None = None
    trade_count: NonNegativeInt = 0


class PerformanceDiagnosis(StrictModel):
    """Reflection output produced by the analysis agent."""

    strategy_quality: StrategyQuality
    key_strengths: list[str] = Field(default_factory=list)
    key_weaknesses: list[str] = Field(default_factory=list)
    overfitting_risk: RiskLevel
    cost_sensitivity: RiskLevel
    regime_concerns: str = ""
    suggested_next_experiments: list[str] = Field(default_factory=list)


class ResearchContext(StrictModel):
    """Central state object shared by all workflow nodes."""

    user_request: str = Field(..., min_length=1)
    task_plan: TaskPlan | None = None
    market_data: list[dict[str, Any]] = Field(default_factory=list)
    factors: list[dict[str, Any]] = Field(default_factory=list)
    backtest_results: BacktestResult | None = None
    performance_metrics: PerformanceMetrics | None = None
    diagnosis: PerformanceDiagnosis | None = None
    experiment_suggestions: list[str] = Field(default_factory=list)
    report: str | None = None

    @field_validator("user_request")
    @classmethod
    def normalize_user_request(cls, value: str) -> str:
        request = value.strip()
        if not request:
            raise ValueError("user_request cannot be blank")
        return request
