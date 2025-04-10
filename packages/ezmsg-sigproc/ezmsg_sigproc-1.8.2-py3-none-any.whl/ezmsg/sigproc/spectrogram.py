import typing

import ezmsg.core as ez
from ezmsg.util.messages.axisarray import AxisArray
from ezmsg.util.generator import consumer, compose
from ezmsg.util.messages.modify import modify_axis

from .window import windowing, Anchor
from .spectrum import spectrum, WindowFunction, SpectralTransform, SpectralOutput
from .base import GenAxisArray


@consumer
def spectrogram(
    window_dur: float | None = None,
    window_shift: float | None = None,
    window_anchor: str | Anchor = Anchor.BEGINNING,
    window: WindowFunction = WindowFunction.HANNING,
    transform: SpectralTransform = SpectralTransform.REL_DB,
    output: SpectralOutput = SpectralOutput.POSITIVE,
) -> typing.Generator[AxisArray | None, AxisArray, None]:
    """
    Calculate a spectrogram on streaming data.

    Chains :obj:`ezmsg.sigproc.window.windowing` to apply a moving window on the data,
    :obj:`ezmsg.sigproc.spectrum.spectrum` to calculate spectra for each window,
    and finally :obj:`ezmsg.util.messages.modify.modify_axis` to convert the win axis back to time axis.

    Args:
        window_dur: See :obj:`ezmsg.sigproc.window.windowing`
        window_shift: See :obj:`ezmsg.sigproc.window.windowing`
        window_anchor: See :obj:`ezmsg.sigproc.window.windowing`
        window: See :obj:`ezmsg.sigproc.spectrum.spectrum`
        transform: See :obj:`ezmsg.sigproc.spectrum.spectrum`
        output: See :obj:`ezmsg.sigproc.spectrum.spectrum`

    Returns:
        A primed generator object that expects an :obj:`AxisArray` via `.send(axis_array)`
        with continuous data in its .data payload, and yields an :obj:`AxisArray` of time-frequency power values.
    """

    pipeline = compose(
        windowing(
            axis="time",
            newaxis="win",
            window_dur=window_dur,
            window_shift=window_shift,
            zero_pad_until="shift" if window_shift is not None else "input",
            anchor=window_anchor,
        ),
        spectrum(axis="time", window=window, transform=transform, output=output),
        modify_axis(name_map={"win": "time"}),
    )

    # State variables
    msg_out: AxisArray | None = None

    while True:
        msg_in: AxisArray = yield msg_out
        msg_out = pipeline(msg_in)


class SpectrogramSettings(ez.Settings):
    """
    Settings for :obj:`Spectrogram`.
    See :obj:`spectrogram` for a description of the parameters.
    """

    window_dur: float | None = None  # window duration in seconds
    window_shift: float | None = None
    """"window step in seconds. If None, window_shift == window_dur"""
    window_anchor: str | Anchor = Anchor.BEGINNING

    # See SpectrumSettings for details of following settings:
    window: WindowFunction = WindowFunction.HAMMING
    transform: SpectralTransform = SpectralTransform.REL_DB
    output: SpectralOutput = SpectralOutput.POSITIVE


class Spectrogram(GenAxisArray):
    """
    Unit for :obj:`spectrogram`.
    """

    SETTINGS = SpectrogramSettings

    def construct_generator(self):
        self.STATE.gen = spectrogram(
            window_dur=self.SETTINGS.window_dur,
            window_shift=self.SETTINGS.window_shift,
            window_anchor=self.SETTINGS.window_anchor,
            window=self.SETTINGS.window,
            transform=self.SETTINGS.transform,
            output=self.SETTINGS.output,
        )
