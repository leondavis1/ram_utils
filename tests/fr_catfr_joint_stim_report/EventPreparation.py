import os
import os.path
import numpy as np

from ptsa.data.readers import BaseEventReader
from ptsa.data.readers.IndexReader import JsonIndexReader

from RamPipeline import *

from ReportUtils import ReportRamTask

import hashlib


class EventPreparation(ReportRamTask):
    def __init__(self, mark_as_completed=True):
        super(EventPreparation, self).__init__(mark_as_completed)

    def input_hashsum(self):
        subject = self.pipeline.subject
        tmp = subject.split('_')
        subj_code = tmp[0]
        montage = 0 if len(tmp)==1 else int(tmp[1])

        json_reader = JsonIndexReader(os.path.join(self.pipeline.mount_point, 'protocols/r1.json'))

        hash_md5 = hashlib.md5()
        for task in [self.pipeline.task,'cat'+self.pipeline.task]:
            event_files = sorted(list(json_reader.aggregate_values('all_events', subject=subj_code, montage=montage, experiment=task)))
            for fname in event_files:
                with open(fname,'rb') as f: hash_md5.update(f.read())

        return hash_md5.digest()

    def run(self):
        subject = self.pipeline.subject
        task = self.pipeline.task
        tmp = subject.split('_')
        subj_code = tmp[0]
        montage = 0 if len(tmp)==1 else int(tmp[1])

        json_reader = JsonIndexReader(os.path.join(self.pipeline.mount_point, 'protocols/r1.json'))

        events = None


        event_files = sorted(list(json_reader.aggregate_values('all_events', subject=subj_code, montage=montage, experiment=task)))

        for sess_file in event_files:
            e_path = os.path.join(self.pipeline.mount_point, sess_file)
            print e_path
            e_reader = BaseEventReader(filename=e_path, eliminate_events_with_no_eeg=True)

            sess_events = e_reader.read()

            if events is None:
                events = sess_events
            else:
                events = np.hstack((events,sess_events))
        fr_event_fields=list(events.dtype.names)

        cat_event_files = sorted(list(json_reader.aggregate_values('all_events', subject=subj_code, montage=montage, experiment='cat'+task)))
        for sess_file in cat_event_files:
            e_path = os.path.join(self.pipeline.mount_point, sess_file)
            print e_path
            e_reader = BaseEventReader(filename=e_path, eliminate_events_with_no_eeg=True)

            sess_events = e_reader.read()[fr_event_fields].copy()
            sess_events.session +=100

            if events is None:
                events = sess_events
            else:
                events = np.hstack((events,sess_events))


        events = events.view(np.recarray)

        self.pass_object(task+'_all_events', events)

        math_events = events[events.type == 'PROB']

        rec_events = events[events.type == 'REC_WORD']

        intr_events = rec_events[(rec_events.intrusion!=-999) & (rec_events.intrusion!=0)]

        events = events[events.type == 'WORD']

        print len(events), task, 'WORD events'

        self.pass_object(task+'_events', events)
        self.pass_object(task+'_math_events', math_events)
        self.pass_object(task+'_intr_events', intr_events)
        self.pass_object(task+'_rec_events', rec_events)