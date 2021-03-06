from RamPipeline import *

from os.path import join

from loc_to_df import loc_to_df


class GetLocalization(RamTask):
    def __init__(self, mark_as_completed=True):
        RamTask.__init__(self, mark_as_completed)

    def run(self):
        subject = self.pipeline.subject

        df = None
        try:
            l_path = join(self.pipeline.mount_point, 'data/eeg', subject, 'docs/localization', subject+' Localization.xlsx')
            df = loc_to_df(l_path)
        except:
            df = dict()

        self.pass_object('loc_info', df)
