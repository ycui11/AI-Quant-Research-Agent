from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.state import (
    BacktestResult,
    EquityPoint,
    PerformanceDiagnosis,
    PerformanceMetrics,
    ResearchContext,
    TaskPlan,
)


def test_research_context_has_expected_core_fields() -> None:
    expected_fields = {
        "user_request",
        "task_plan",
        "market_data",
        "factors",
        "backtest_results",
        "performance_metrics",
        "diagnosis",
        "experiment_suggestions",
        "report",
    }

    assert set(ResearchContext.model_fields) == expected_fields


def test_research_context_defaults_are_safe_and_empty() -> None:
    first = ResearchContext(user_request="Research BTC momentum")
    second = ResearchContext(user_request="Research ETH mean reversion")

    first.market_data.append({"timestamp": "2026-01-01T00:00:00Z", "close": 100.0})

    assert first.task_plan is None
    assert first.factors == []
    assert second.market_data == []
    assert second.experiment_suggestions == []


def test_task_plan_normalizes_symbol_and_timeframe() -> None:
    plan = TaskPlan(
        asset=" btcusdt ",
        timeframe=" 5M ",
        strategy_type="momentum",
        lookback_bars=12,
        holding_period_bars=6,
    )

    assert plan.asset == "BTCUSDT"
    assert plan.timeframe == "5m"


def test_task_plan_rejects_invalid_inputs() -> None:
    with pytest.raises(ValidationError):
        TaskPlan(
            asset="BTC/USDT",
            timeframe="5m",
            strategy_type="momentum",
            lookback_bars=12,
            holding_period_bars=6,
        )

    with pytest.raises(ValidationError):
        TaskPlan(
            asset="BTCUSDT",
            timeframe="five minutes",
            strategy_type="momentum",
            lookback_bars=12,
            holding_period_bars=6,
        )


def test_task_plan_rejects_inverted_time_range() -> None:
    with pytest.raises(ValidationError):
        TaskPlan(
            asset="BTCUSDT",
            timeframe="5m",
            strategy_type="momentum",
            lookback_bars=12,
            holding_period_bars=6,
            start_time=datetime(2026, 1, 2, tzinfo=timezone.utc),
            end_time=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )


def test_research_context_serializes_nested_state() -> None:
    timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
    context = ResearchContext(
        user_request="Research a BTC 5-minute momentum strategy",
        task_plan=TaskPlan(
            asset="btcusdt",
            timeframe="5m",
            strategy_type="momentum",
            lookback_bars=12,
            holding_period_bars=6,
        ),
        market_data=[{"timestamp": timestamp.isoformat(), "open": 100.0, "close": 101.0}],
        factors=[{"timestamp": timestamp.isoformat(), "momentum": 0.01}],
        backtest_results=BacktestResult(
            observations=1,
            trade_count=1,
            gross_return=0.01,
            net_return=0.0095,
            equity_curve=[EquityPoint(timestamp=timestamp, equity=10_095.0)],
        ),
        performance_metrics=PerformanceMetrics(
            total_return=0.0095,
            annualized_return=0.12,
            volatility=0.2,
            sharpe_ratio=0.8,
            max_drawdown=-0.03,
            win_rate=1.0,
            turnover=0.5,
            trade_count=1,
        ),
        diagnosis=PerformanceDiagnosis(
            strategy_quality="inconclusive",
            key_strengths=["Positive net return in the sample"],
            key_weaknesses=["Only one observation"],
            overfitting_risk="high",
            cost_sensitivity="medium",
            regime_concerns="Sample is too short for regime analysis.",
            suggested_next_experiments=["Run on a longer history"],
        ),
        experiment_suggestions=["Increase the sample size"],
        report="Mock report",
    )

    serialized = context.model_dump_json()
    restored = ResearchContext.model_validate_json(serialized)

    assert restored.user_request == "Research a BTC 5-minute momentum strategy"
    assert restored.task_plan is not None
    assert restored.task_plan.asset == "BTCUSDT"
    assert restored.backtest_results is not None
    assert restored.backtest_results.equity_curve[0].equity == 10_095.0
    assert restored.diagnosis is not None
    assert restored.diagnosis.overfitting_risk == "high"


def test_closed_schemas_reject_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        ResearchContext(user_request="Research BTC momentum", unexpected=True)


def test_metrics_validate_rate_bounds() -> None:
    with pytest.raises(ValidationError):
        PerformanceMetrics(
            total_return=0.1,
            max_drawdown=-0.05,
            win_rate=1.2,
        )
