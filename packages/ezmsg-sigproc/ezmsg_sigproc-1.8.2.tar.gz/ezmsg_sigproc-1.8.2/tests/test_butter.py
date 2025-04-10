import numpy as np
import pytest
import scipy.signal
from frozendict import frozendict
from ezmsg.util.messages.axisarray import AxisArray

from ezmsg.sigproc.butterworthfilter import butter
from ezmsg.sigproc.butterworthfilter import (
    ButterworthFilterSettings as LegacyButterSettings,
)


@pytest.mark.parametrize(
    "cutoff, cuton",
    [
        (30.0, None),  # lowpass
        (None, 30.0),  # highpass
        (45.0, 30.0),  # bandpass
        (30.0, 45.0),  # bandstop
    ],
)
@pytest.mark.parametrize("order", [2, 4, 8])
def test_butterworth_legacy_filter_settings(cutoff: float, cuton: float, order: int):
    """
    Test the butterworth legacy filter settings generation of btype and Wn.
    We test them explicitly because we assume they are correct when used in our later settings.

    Parameters:
        cutoff (float): The cutoff frequency for the filter. Can be None for highpass filters.
        cuton (float): The cuton frequency for the filter. Can be None for lowpass filters.
            If cuton is larger than cutoff we assume bandstop.
        order (int): The order of the filter.
    """
    btype, Wn = LegacyButterSettings(
        order=order, cuton=cuton, cutoff=cutoff
    ).filter_specs()
    if cuton is None:
        assert btype == "lowpass"
        assert Wn == cutoff
    elif cutoff is None:
        assert btype == "highpass"
        assert Wn == cuton
    elif cuton <= cutoff:
        assert btype == "bandpass"
        assert Wn == (cuton, cutoff)
    else:
        assert btype == "bandstop"
        assert Wn == (cutoff, cuton)


@pytest.mark.parametrize(
    "cutoff, cuton",
    [
        (30.0, None),  # lowpass
        (None, 30.0),  # highpass
        (45.0, 30.0),  # bandpass
        (30.0, 45.0),  # bandstop
    ],
)
@pytest.mark.parametrize("order", [0, 2, 5, 8])  # 0 = passthrough
# All fs entries must be greater than 2x the largest of cutoff | cuton
@pytest.mark.parametrize("fs", [200.0])
@pytest.mark.parametrize("n_chans", [3])
@pytest.mark.parametrize("n_dims, time_ax", [(1, 0), (3, 0), (3, 1), (3, 2)])
@pytest.mark.parametrize("coef_type", ["ba", "sos"])
def test_butterworth(
    cutoff: float,
    cuton: float,
    order: int,
    fs: float,
    n_chans: int,
    n_dims: int,
    time_ax: int,
    coef_type: str,
):
    dur = 2.0
    n_freqs = 5
    n_splits = 4

    n_times = int(dur * fs)
    if n_dims == 1:
        dat_shape = [n_times]
        dat_dims = ["time"]
        other_axes = {}
    else:
        dat_shape = [n_freqs, n_chans]
        dat_shape.insert(time_ax, n_times)
        dat_dims = ["freq", "ch"]
        dat_dims.insert(time_ax, "time")
        other_axes = {
            "freq": AxisArray.LinearAxis(unit="Hz", offset=0.0, gain=1.0),
            "ch": AxisArray.CoordinateAxis(
                data=np.arange(n_chans).astype(str), dims=["ch"]
            ),
        }
    in_dat = np.arange(np.prod(dat_shape), dtype=float).reshape(*dat_shape)

    # Calculate Expected Result
    btype, Wn = LegacyButterSettings(
        order=order, cuton=cuton, cutoff=cutoff
    ).filter_specs()
    coefs = scipy.signal.butter(order, Wn, btype=btype, output=coef_type, fs=fs)
    tmp_dat = np.moveaxis(in_dat, time_ax, -1)
    if coef_type == "ba":
        if order == 0:
            # butter does not return correct coefs under these conditions; Set manually.
            coefs = (np.array([1.0, 0.0]),) * 2
        zi = scipy.signal.lfilter_zi(*coefs)
        if n_dims == 3:
            zi = np.tile(zi[None, None, :], (n_freqs, n_chans, 1))
        out_dat, _ = scipy.signal.lfilter(*coefs, tmp_dat, zi=zi)
    elif coef_type == "sos":
        zi = scipy.signal.sosfilt_zi(coefs)
        if n_dims == 3:
            zi = np.tile(zi[:, None, None, :], (1, n_freqs, n_chans, 1))
        out_dat, _ = scipy.signal.sosfilt(coefs, tmp_dat, zi=zi)
    expected = np.moveaxis(out_dat, -1, time_ax)

    # Split the data into multiple messages
    n_seen = 0
    messages = []
    for split_dat in np.array_split(in_dat, n_splits, axis=time_ax):
        _time_axis = AxisArray.TimeAxis(fs=fs, offset=n_seen / fs)
        messages.append(
            AxisArray(
                split_dat,
                dims=dat_dims,
                axes=frozendict({**other_axes, "time": _time_axis}),
                key="test_butterworth",
            )
        )
        n_seen += split_dat.shape[time_ax]

    # Test axis_name `None` when target axis idx is 0.
    axis_name = "time" if time_ax != 0 else None
    gen = butter(
        axis=axis_name,
        order=order,
        cuton=cuton,
        cutoff=cutoff,
        coef_type=coef_type,
    )

    result = np.concatenate([gen.send(_).data for _ in messages], axis=time_ax)
    assert np.allclose(result, expected)


def test_butterworth_empty_msg():
    proc = butter(
        axis="time",
        order=2,
        cuton=0.1,
        cutoff=1.0,
        coef_type="sos",
    )
    msg_in = AxisArray(
        data=np.zeros((0, 2)),
        dims=["time", "ch"],
        axes={
            "time": AxisArray.TimeAxis(fs=19.0, offset=0),
            "ch": AxisArray.CoordinateAxis(data=np.arange(2).astype(str), dims=["ch"]),
        },
        key="test_butterworth_empty_msg",
    )
    res = proc.send(msg_in)
    assert res.data.size == 0
