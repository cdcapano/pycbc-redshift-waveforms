#!/usr/bin/env python

"""PyCBC waveform plugin models that generate in the source frame.

This module provides two custom waveform models intended for plugin use:

- SourceFrameTD
- SourceFrameFD

Both models generate a waveform in the source frame using a user-specified
``waveform_approximant`` and then redshift that waveform into the detector
frame using ``pycbc.waveform.utils.redshift_waveform``.

Written with assistance from GPT-5.3 Codex in VS Code.
"""

from pycbc import waveform


_TD_APPROXIMANT_NAME = "SourceFrameTD"
_FD_APPROXIMANT_NAME = "SourceFrameFD"


def _pop_required(args, key):
	"""Pop a required key from args with a helpful message."""
	if key not in args:
		raise ValueError(f"Missing required parameter '{key}'")
	return args.pop(key)


def _validate_redshift(z):
	if z < 0:
		raise ValueError("'z' must be >= 0")


def source_frame_td(**kwargs):
	"""Generate a TD waveform in the source frame and redshift to detector frame.

	Required keyword arguments:
	- waveform_approximant: detector/source model used internally by PyCBC
	- srcmass1, srcmass2: source-frame component masses
	- z: redshift
	- f_lower: detector-frame low-frequency cutoff
	- delta_t: detector-frame sample spacing

	Any additional keyword arguments are passed through to
	``pycbc.waveform.get_td_waveform``.
	"""
	params = dict(kwargs)

	approximant = _pop_required(params, "waveform_approximant")

	srcmass1 = _pop_required(params, "srcmass1")
	srcmass2 = _pop_required(params, "srcmass2")
	z = _pop_required(params, "z")
	_validate_redshift(z)

	f_lower_det = _pop_required(params, "f_lower")
	delta_t_det = _pop_required(params, "delta_t")

	# Convert detector-frame sampling/cutoff to source-frame equivalents.
	params["f_lower"] = f_lower_det * (1. + z)
	params["delta_t"] = delta_t_det / (1. + z)
	params["approximant"] = approximant
	params["mass1"] = srcmass1
	params["mass2"] = srcmass2

	hp_src, hc_src = waveform.get_td_waveform(**params)
	hp_det = waveform.utils.redshift_waveform(hp_src, z)
	hc_det = waveform.utils.redshift_waveform(hc_src, z)
	return hp_det, hc_det


def source_frame_fd(**kwargs):
	"""Generate an FD waveform in the source frame and redshift to detector frame.

	Required keyword arguments:
	- waveform_approximant: detector/source model used internally by PyCBC
	- srcmass1, srcmass2: source-frame component masses
	- z: redshift
	- f_lower: detector-frame low-frequency cutoff
	- delta_f: detector-frame frequency spacing

	Any additional keyword arguments are passed through to
	``pycbc.waveform.get_fd_waveform``.
	"""
	params = dict(kwargs)

	approximant = _pop_required(params, "waveform_approximant")

	srcmass1 = _pop_required(params, "srcmass1")
	srcmass2 = _pop_required(params, "srcmass2")
	z = _pop_required(params, "z")
	_validate_redshift(z)

	f_lower_det = _pop_required(params, "f_lower")
	delta_f_det = _pop_required(params, "delta_f")

	# Convert detector-frame sampling/cutoff to source-frame equivalents.
	params["f_lower"] = f_lower_det * (1. + z)
	params["delta_f"] = delta_f_det * (1. + z)
	params["approximant"] = approximant
	params["mass1"] = srcmass1
	params["mass2"] = srcmass2

	hp_src, hc_src = waveform.get_fd_waveform(**params)
	hp_det = waveform.utils.redshift_waveform(hp_src, z)
	hc_det = waveform.utils.redshift_waveform(hc_src, z)
	return hp_det, hc_det


# Register SourceFrameTD/SourceFrameFD for use in PyCBC
if False:
    waveform.add_custom_waveform(
        _TD_APPROXIMANT_NAME, source_frame_td, "time", force=False
    )
    waveform.add_custom_waveform(
        _FD_APPROXIMANT_NAME, source_frame_fd, "frequency", force=False
    )


__all__ = [
	"source_frame_td",
	"source_frame_fd",
]
