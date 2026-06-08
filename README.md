# pycbc-redshift-waveforms

`pycbc-redshift-waveforms` is a small PyCBC waveform plugin package that generates waveforms in the source frame and then redshifts them into the detector frame with `pycbc.waveform.utils.redshift_waveform`.

It provides two plugin approximants:

- `SourceFrameTD` for time-domain waveforms
- `SourceFrameFD` for frequency-domain waveforms

Each plugin takes a source-frame waveform approximant name through `waveform_approximant`, source-frame component masses through `srcmass1` and `srcmass2`, and a redshift `z`. The waveform is generated internally in the source frame, then converted back to the detector frame before being returned by PyCBC.

## Installation

Install the package from the repository root:

```bash
pip install .
```

If you want an isolated build from source, you can also create a wheel and install it:

```bash
python -m build --wheel
pip install dist/pycbc_redshift_waveforms-0.1.0-py3-none-any.whl
```

The package depends on PyCBC, so make sure PyCBC is available in the environment first.

## Usage

After installation, the approximants can be called through PyCBC like any other plugin waveform:

```python
from pycbc import waveform

hp, hc = waveform.get_td_waveform(
    approximant="SourceFrameTD",
    waveform_approximant="IMRPhenomTPHM",
    srcmass1=3.6,
    srcmass2=1.4,
    z=0.3,
    f_lower=10,
    delta_t=1.0 / 16384,
)
```

For a frequency-domain waveform, use `approximant="SourceFrameFD"` and pass `delta_f` instead of `delta_t`.
