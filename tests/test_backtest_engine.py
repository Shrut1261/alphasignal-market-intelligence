import pytest
from alphasignal_backtest.engine import run_vector_backtest
from alphasignal_backtest.strategies import threshold_weights


def test_threshold_weights_convert_confidence_to_weights() -> None:
    weights = threshold_weights([0.6, 0.5, 0.4])

    assert weights == [1.0, 0.0, 0.0]


def test_run_vector_backtest_lags_weights_to_avoid_lookahead() -> None:
    result = run_vector_backtest(
        strategy_name="unit",
        asset_returns=[0.10, 0.05],
        target_weights=[1.0, 1.0],
        transaction_cost_bps=0,
    )

    assert result.strategy_returns == [0.0, 0.05]
    assert result.final_equity == pytest.approx(105_000.0)


def test_run_vector_backtest_rejects_mismatched_inputs() -> None:
    with pytest.raises(ValueError, match="same length"):
        run_vector_backtest(
            strategy_name="bad",
            asset_returns=[0.01],
            target_weights=[1.0, 0.0],
        )
