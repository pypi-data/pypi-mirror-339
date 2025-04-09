# Hypertrial: Bitcoin DCA Strategy Framework

A Bitcoin Dollar-Cost Averaging (DCA) framework for evaluating and comparing algorithmic trading strategies.

## Installation

```bash
pip install hypertrial
```

## Quick Start

```python
import pandas as pd
from hypertrial import backtest_dynamic_dca, load_data, register_strategy

# Load Bitcoin data (included with the package)
btc_df = load_data()

# Create a simple custom strategy
@register_strategy("my_custom_strategy")
def custom_dca_strategy(df):
    # Strategy logic goes here
    # Return purchase weights for each day
    return weights_df

# Run backtest with your strategy
results = backtest_dynamic_dca(btc_df, strategy_name="my_custom_strategy")
```

## Key Features

- **DCA Strategy Testing**: Evaluate Bitcoin dollar-cost averaging strategies
- **Performance Metrics**: Analyze strategies using Sats Per Dollar (SPD)
- **Cross-Cycle Analysis**: Test strategies across multiple Bitcoin market cycles
- **Visualization Tools**: Plot performance metrics and strategy behaviors
- **Security Verification**: Security scanning for submitted strategies

## Command Line Interface

Hypertrial comes with a built-in CLI:

```bash
# List available strategies
hypertrial --list

# Run backtest with a specific strategy
hypertrial --strategy dynamic_dca

# Run backtest for all strategies
hypertrial --backtest-all --output-dir results
```

## Contributing

We welcome contributions! Please visit our [GitHub repository](https://github.com/mattfaltyn/hypertrial) for more information.

## License

This project is available under the MIT License.
