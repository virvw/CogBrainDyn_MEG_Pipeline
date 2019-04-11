"""
============================================
03. Extract events from the stimulus channel
============================================

Here, all events indicated by triggers in the stimulus channel an described in the config.stim_channel
are extracted. The events are saved to the subject's MEG directory.
This is done early in the pipeline to avoid distorting event-time, for instance when you resample the data.  
"""

import os.path as op

import mne
from mne.parallel import parallel_func

import config


def run_events(subject):
    print("processing subject: %s" % subject)
    meg_subject_dir = op.join(config.meg_dir, subject)

    for run in config.runs:
        extension = run + '_sss_raw'
        raw_fname_in = op.join(meg_subject_dir,
                               config.base_fname.format(**locals()))
        eve_fname_out = op.splitext(raw_fname_in)[0] + '-eve.fif'

        raw = mne.io.read_raw_fif(raw_fname_in)
        events = mne.find_events(raw, stim_channel=config.stim_channel)

        print("Input: ", raw_fname_in)
        print("Output: ", eve_fname_out)

        mne.write_events(eve_fname_out, events)

        if config.plot:
            # plot events
            figure = mne.viz.plot_events(events)
            figure.show()


parallel, run_func, _ = parallel_func(run_events, n_jobs=config.N_JOBS)
parallel(run_func(subject) for subject in config.subjects_list)
