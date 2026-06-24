# AI Quant Research Agent

An AI-powered quantitative research assistant that can generate trading hypotheses, fetch market data, build factors, run backtests, analyze performance, and produce structured research reports.

## Project Motivation

Quantitative research often involves a repetitive workflow:

1. Form a market hypothesis
2. Collect and clean data
3. Build trading signals
4. Run backtests
5. Evaluate performance
6. Write research notes
7. Iterate on the idea

This project builds an AI Agent that automates parts of this workflow while keeping the final decision-making transparent and auditable.

The goal is not to create a production trading system, but to demonstrate skills in:

* AI Agent design
* Quantitative research workflow
* Financial data engineering
* Backtesting
* Statistical evaluation
* LLM tool orchestration

## Example Use Case

User input:

```text
Research a BTC 5-minute momentum strategy.
```

Agent workflow:

```text
1. Parse research request
2. Fetch BTC historical OHLCV data
3. Generate candidate momentum factors
4. Run backtests
5. Calculate Sharpe ratio, drawdown, win rate, turnover
6. Analyze failure modes
7. Generate a research report
8. Suggest next experiments
```

## Core Features

### 1. Research Agent

Interprets user requests and converts them into structured research tasks.

Example:

```json
{
  "asset": "BTC",
  "timeframe": "5m",
  "strategy_type": "momentum",
  "holding_period": "30m",
  "objective": "maximize risk-adjusted return"
}
```

### 2. Data Agent

Fetches and stores historical market data.

Supported sources:

* Binance public market data
* CSV files
* Local DuckDB database

Data types:

* OHLCV data
* Future extension: L2 order book data

### 3. Factor Generation Agent

Generates candidate trading signals such as:

* Return momentum
* Moving average crossover
* Volatility breakout
* RSI-based signal
* Volume-adjusted momentum
* Mean-reversion signals

### 4. Backtest Engine

Runs historical simulations with realistic assumptions.

Metrics:

* Total return
* Annualized return
* Sharpe ratio
* Maximum drawdown
* Win rate
* Turnover
* Transaction cost impact
* Exposure
* Number of trades

### 5. Analysis Agent

Evaluates strategy performance and identifies weaknesses.

Examples:

* Overfitting risk
* High turnover
* Poor performance after transaction costs
* Sensitivity to parameter changes
* Regime dependency

### 6. Report Agent

Generates a structured research report in Markdown.

Report sections:

* Research question
* Data used
* Strategy logic
* Backtest assumptions
* Performance summary
* Risk analysis
* Limitations
* Suggested next experiments

## Architecture

```text
User Request
    ↓
LangGraph Research Workflow
    ↓
Research Planner Agent
    ↓
Data Tool
    ↓
Factor Generator Tool
    ↓
Backtest Tool
    ↓
Performance Analyzer
    ↓
Report Generator
    ↓
Markdown Research Report
```

## Tech Stack

* Python
* LangGraph
* OpenAI / Claude API
* Pandas
* NumPy
* DuckDB
* Backtrader or vectorbt
* Matplotlib
* FastAPI
* Streamlit
* Docker

## Project Structure

```text
ai-quant-research-agent/
│
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_factor_research.ipynb
│   └── 03_backtest_validation.ipynb
│
├── src/
│   ├── agents/
│   │   ├── research_planner.py
│   │   ├── factor_agent.py
│   │   ├── analysis_agent.py
│   │   └── report_agent.py
│   │
│   ├── tools/
│   │   ├── data_loader.py
│   │   ├── factor_builder.py
│   │   ├── backtester.py
│   │   └── metrics.py
│   │
│   ├── database/
│   │   └── duckdb_client.py
│   │
│   ├── workflows/
│   │   └── research_graph.py
│   │
│   └── app/
│       └── streamlit_app.py
│
├── reports/
│   └── sample_btc_momentum_report.md
│
├── tests/
│   ├── test_data_loader.py
│   ├── test_backtester.py
│   └── test_metrics.py
│
└── docker/
    └── Dockerfile
```

## Sample Research Report Output

```markdown
# BTC 5-Minute Momentum Strategy Research Report

## Research Question

Can short-term BTC momentum on 5-minute candles produce positive risk-adjusted returns after transaction costs?

## Strategy Logic

The strategy computes the past 6-bar return and enters a long position when momentum is positive. It exits after a fixed holding period or when momentum turns negative.

## Backtest Assumptions

- Asset: BTCUSDT
- Timeframe: 5 minutes
- Transaction cost: 5 bps per trade
- No leverage
- Long-only
- No look-ahead bias

## Performance Summary

| Metric | Value |
|---|---:|
| Total Return | 12.4% |
| Sharpe Ratio | 1.18 |
| Max Drawdown | -8.7% |
| Win Rate | 52.1% |
| Turnover | High |

## Analysis

The strategy shows mild positive momentum behavior before transaction costs, but performance is sensitive to trading costs. High turnover reduces profitability.

## Limitations

- Only tested on BTC
- No order book features
- No slippage model
- Limited market regime analysis

## Next Experiments

1. Add volatility filter
2. Compare with mean-reversion strategy
3. Test multiple assets
4. Add transaction cost sensitivity analysis
5. Evaluate performance across market regimes
```

## Resume Description

Built an AI-powered quantitative research agent using LangGraph, Python, DuckDB, and backtesting tools to automate factor generation, strategy backtesting, performance analysis, and research report generation for crypto market data.

## Interview Talking Points

This project demonstrates:

* How to design an AI Agent workflow
* How to prevent look-ahead bias in backtesting
* How to evaluate trading strategies statistically
* How to handle financial time-series data
* How to separate research logic from execution logic
* How to use LLMs as research assistants rather than black-box predictors
