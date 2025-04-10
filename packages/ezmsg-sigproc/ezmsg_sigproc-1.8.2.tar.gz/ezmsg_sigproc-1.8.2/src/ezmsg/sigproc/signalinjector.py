import typing

import ezmsg.core as ez
from ezmsg.util.messages.axisarray import AxisArray
from ezmsg.util.messages.util import replace
import numpy as np
import numpy.typing as npt

from .util.profile import profile_subpub


class SignalInjectorSettings(ez.Settings):
    time_dim: str = "time"  # Input signal needs a time dimension with units in sec.
    frequency: float | None = None  # Hz
    amplitude: float = 1.0
    mixing_seed: int | None = None


class SignalInjectorState(ez.State):
    cur_shape: tuple[int, ...] | None = None
    cur_frequency: float | None = None
    cur_amplitude: float
    mixing: npt.NDArray


class SignalInjector(ez.Unit):
    """
    Add a sinusoidal signal to the input signal. Each feature gets a different amplitude of the sinusoid.
    All features get the same frequency sinusoid. The frequency and base amplitude can be changed while running.
    """

    SETTINGS = SignalInjectorSettings
    STATE = SignalInjectorState

    INPUT_FREQUENCY = ez.InputStream(float | None)
    INPUT_AMPLITUDE = ez.InputStream(float)
    INPUT_SIGNAL = ez.InputStream(AxisArray)
    OUTPUT_SIGNAL = ez.OutputStream(AxisArray)

    async def initialize(self) -> None:
        self.STATE.cur_frequency = self.SETTINGS.frequency
        self.STATE.cur_amplitude = self.SETTINGS.amplitude
        self.STATE.mixing = np.array([])

    @ez.subscriber(INPUT_FREQUENCY)
    async def on_frequency(self, msg: float | None) -> None:
        self.STATE.cur_frequency = msg

    @ez.subscriber(INPUT_AMPLITUDE)
    async def on_amplitude(self, msg: float) -> None:
        self.STATE.cur_amplitude = msg

    @ez.subscriber(INPUT_SIGNAL)
    @ez.publisher(OUTPUT_SIGNAL)
    @profile_subpub(trace_oldest=False)
    async def inject(self, msg: AxisArray) -> typing.AsyncGenerator:
        if self.STATE.cur_shape != msg.shape:
            self.STATE.cur_shape = msg.shape
            rng = np.random.default_rng(self.SETTINGS.mixing_seed)
            self.STATE.mixing = rng.random((1, msg.shape2d(self.SETTINGS.time_dim)[1]))
            self.STATE.mixing = (self.STATE.mixing * 2.0) - 1.0

        if self.STATE.cur_frequency is None:
            yield self.OUTPUT_SIGNAL, msg
        else:
            out_msg = replace(msg, data=msg.data.copy())
            t = out_msg.ax(self.SETTINGS.time_dim).values[..., np.newaxis]
            signal = np.sin(2 * np.pi * self.STATE.cur_frequency * t)
            mixed_signal = signal * self.STATE.mixing * self.STATE.cur_amplitude
            with out_msg.view2d(self.SETTINGS.time_dim) as view:
                view[...] = view + mixed_signal.astype(view.dtype)
            yield self.OUTPUT_SIGNAL, out_msg
