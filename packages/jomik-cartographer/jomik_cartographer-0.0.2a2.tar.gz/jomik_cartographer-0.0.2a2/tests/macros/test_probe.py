from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pytest

from cartographer.macros.probe import ProbeAccuracyMacro, ProbeMacro, QueryProbeMacro, ZOffsetApplyProbeMacro
from cartographer.printer_interface import MacroParams, Position, Probe, Toolhead

if TYPE_CHECKING:
    from pytest import LogCaptureFixture
    from pytest_mock import MockerFixture


@pytest.fixture
def probe(mocker: MockerFixture) -> Probe:
    return mocker.Mock(spec=Probe, autospec=True)


@pytest.fixture
def toolhead(mocker: MockerFixture) -> Toolhead:
    return mocker.Mock(spec=Toolhead, autospec=True)


@pytest.fixture
def params(mocker: MockerFixture):
    return mocker.Mock(
        spec=MacroParams,
        autospec=True,
    )


def test_probe_macro_output(
    mocker: MockerFixture,
    caplog: LogCaptureFixture,
    probe: Probe,
    params: MacroParams,
):
    macro = ProbeMacro(probe)
    probe.probe = mocker.Mock(return_value=5.0)

    with caplog.at_level(logging.INFO):
        macro.run(params)

    assert "Result is z=5.000000" in caplog.messages


def test_probe_accuracy_macro_output(
    mocker: MockerFixture,
    caplog: LogCaptureFixture,
    probe: Probe,
    toolhead: Toolhead,
    params: MacroParams,
):
    macro = ProbeAccuracyMacro(probe, toolhead)
    params.get_int = mocker.Mock(return_value=10)
    toolhead.get_position = lambda: Position(0, 0, 0)
    params.get_float = mocker.Mock(return_value=1)
    i = -1
    measurements: list[float] = [50 + i * 10 for i in range(10)]

    def mock_probe(**_) -> float:
        nonlocal i
        i += 1
        return measurements[i]

    probe.probe = mock_probe

    with caplog.at_level(logging.INFO):
        macro.run(params)

    assert "probe accuracy results" in caplog.text
    assert "minimum 50" in caplog.text
    assert "maximum 140" in caplog.text
    assert "range 90" in caplog.text
    assert "average 95" in caplog.text
    assert "median 95" in caplog.text
    assert "standard deviation 28" in caplog.text


def test_probe_accuracy_macro_sample_count(
    mocker: MockerFixture,
    caplog: LogCaptureFixture,
    probe: Probe,
    toolhead: Toolhead,
    params: MacroParams,
):
    macro = ProbeAccuracyMacro(probe, toolhead)
    params.get_int = mocker.Mock(return_value=3)
    toolhead.get_position = lambda: Position(0, 0, 0)
    params.get_float = mocker.Mock(return_value=1)
    i = -1
    measurements: list[float] = [50 + i * 10 for i in range(10)]

    def mock_probe(**_) -> float:
        nonlocal i
        i += 1
        return measurements[i]

    probe.probe = mock_probe

    with caplog.at_level(logging.INFO):
        macro.run(params)

    assert "probe accuracy results" in caplog.text
    assert "minimum 50" in caplog.text
    assert "maximum 70" in caplog.text
    assert "range 20" in caplog.text
    assert "average 60" in caplog.text
    assert "median 60" in caplog.text
    assert "standard deviation 8" in caplog.text


def test_query_probe_macro_triggered_output(
    caplog: LogCaptureFixture,
    probe: Probe,
    toolhead: Toolhead,
    params: MacroParams,
):
    macro = QueryProbeMacro(probe, toolhead)
    probe.query_is_triggered = lambda print_time=...: True

    with caplog.at_level(logging.INFO):
        macro.run(params)

    assert "probe: TRIGGERED" in caplog.text


def test_query_probe_macro_open_output(
    caplog: LogCaptureFixture,
    probe: Probe,
    toolhead: Toolhead,
    params: MacroParams,
):
    macro = QueryProbeMacro(probe, toolhead)
    probe.query_is_triggered = lambda print_time=...: False

    with caplog.at_level(logging.INFO):
        macro.run(params)

    assert "probe: open" in caplog.text


def test_z_offset_apply_probe_output(caplog: LogCaptureFixture, toolhead: Toolhead, params: MacroParams):
    macro = ZOffsetApplyProbeMacro(toolhead)
    toolhead.get_gcode_z_offset = lambda: -42.0

    with caplog.at_level(logging.INFO):
        macro.run(params)

    assert "cartographer: z_offset: 42" in caplog.text
    assert "SAVE_CONFIG" in caplog.text
