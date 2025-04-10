from dataclasses import field
import typing

import numpy as np
import ezmsg.core as ez
from ezmsg.util.messages.axisarray import AxisArray
from ezmsg.util.generator import consumer, compose

from .spectrogram import spectrogram, SpectrogramSettings
from .aggregate import ranged_aggregate, AggregationFunction
from .base import GenAxisArray


@consumer
def bandpower(
    spectrogram_settings: SpectrogramSettings,
    bands: list[tuple[float, float]] | None = [
        (17, 30),
        (70, 170),
    ],
) -> typing.Generator[AxisArray, AxisArray, None]:
    """
    Calculate the average spectral power in each band.

    Args:
        spectrogram_settings: Settings for spectrogram calculation.
        bands: (min, max) tuples of band limits in Hz.

    Returns:
        A primed generator object ready to yield an :obj:`AxisArray` for each .send(axis_array)
        with the data payload being the average spectral power in each band of the input data.
    """
    msg_out = AxisArray(np.array([]), dims=[""])

    f_spec = spectrogram(
        window_dur=spectrogram_settings.window_dur,
        window_shift=spectrogram_settings.window_shift,
        window_anchor=spectrogram_settings.window_anchor,
        window=spectrogram_settings.window,
        transform=spectrogram_settings.transform,
        output=spectrogram_settings.output,
    )
    f_agg = ranged_aggregate(
        axis="freq", bands=bands, operation=AggregationFunction.MEAN
    )
    pipeline = compose(f_spec, f_agg)

    while True:
        msg_in: AxisArray = yield msg_out
        msg_out = pipeline(msg_in)


class BandPowerSettings(ez.Settings):
    """
    Settings for ``BandPower``.
    See :obj:`bandpower` for details.
    """

    spectrogram_settings: SpectrogramSettings = field(
        default_factory=SpectrogramSettings
    )
    bands: list[tuple[float, float]] | None = field(
        default_factory=lambda: [(17, 30), (70, 170)]
    )


class BandPower(GenAxisArray):
    """:obj:`Unit` for :obj:`bandpower`."""

    SETTINGS = BandPowerSettings

    def construct_generator(self):
        self.STATE.gen = bandpower(
            spectrogram_settings=self.SETTINGS.spectrogram_settings,
            bands=self.SETTINGS.bands,
        )
