import sys
from os.path import *

sys.path.append(expanduser('~/RAM_UTILS_GIT'))

from  MatlabUtils import *
from RamPipeline import *


class PS2ReportPipeline(RamPipeline):

    def __init__(self,subject_id, workspace_dir,matlab_paths=[]):
        RamPipeline.__init__(self)
        self.subject_id = subject_id
        self.set_workspace_dir(workspace_dir+self.subject_id)
        self.matlab_paths = matlab_paths
        add_matlab_search_paths(*matlab_paths)


        # self.subject_id = 'R1086M'

        # self.set_workspace_dir('~/scratch/py_run_4/'+self.subject_id)
        # self.classifier_dir = self.create_dir_in_workspace('biomarker/L2LR/Feat_Freq')

class CreateParamsTask(MatlabRamTask):
    def __init__(self): MatlabRamTask.__init__(self)

    def run(self):

        self.eng.CreateParams(self.pipeline.subject_id, self.pipeline.workspace_dir)

class ComputePowersAndClassifierTask(MatlabRamTask):
    def __init__(self): MatlabRamTask.__init__(self)

    def run(self):

        params_path = join(self.get_workspace_dir(),'bm_params.mat')
        # print 'params_path=',params_path
        self.eng.ComputePowersAndClassifier(self.pipeline.subject_id, self.get_workspace_dir(), params_path)

class SaveEventsTask(MatlabRamTask):
    def __init__(self): MatlabRamTask.__init__(self)

    def run(self):
        self.eng.SaveEvents(self.pipeline.subject_id, self.get_workspace_dir())


class GenerateTex(RamTask):
    def __init__(self): RamTask.__init__(self)

    def run(self):
        import TextTemplateUtils
        import datetime
        tex_template = 'report.tex.tpl'

        # self.set_file_resources_to_copy('ps2_report.tex')
        self.set_file_resources_to_move('report.tex', dst='reports')

        import numpy as np
        a = np.fromfunction(lambda x,y: (x+1)*y, shape=(4,4))

        import TexUtils
        patient_table = TexUtils.generate_tex_table(caption='Numpy_table', header=['col1', 'col2', 'col3'], columns=[ a[:, 1] , a[:, 2], a[:, 3] ], label='tab:numpy_table')
        print 'patient_table=\n',patient_table

        replace_dict={
            '<HEADER_LEFT>':'RAM FR1 report v 2.0',
            '<DATE>': str(datetime.date.today()),
            '<SECTION_TITLE>': 'R1074M RAM FR1 Free Recall Report',
            '<PATIENT_TABLE>': patient_table,
            # '<PT>': r'\begin'

        }


        TextTemplateUtils.replace_template(template_file_name=tex_template, replace_dict=replace_dict)
        raise

class GenerateTexTable(RamTask):
    def __init__(self): RamTask.__init__(self)

    def run(self):
        import numpy as np
        a = np.fromfunction(lambda x,y: (x+1)*y, shape=(4,4))
        print a
        print a[:,1]
        print a[:,2]
        print a[:,3]

        import TexUtils
        self.set_file_resources_to_move('mytable.tex', dst='reports')
        TexUtils.generate_tex_table(caption='Numpy_table', header=['col1', 'col2', 'col3'], columns=[ a[:, 1] , a[:, 2], a[:, 3] ], label='tab:numpy_table')






a = 'my \n string'

print a.encode('string-escape')

ps_report_pipeline = PS2ReportPipeline(subject_id='R1086M', workspace_dir='~/scratch/py_run_6/', matlab_paths=['~/RAM_MATLAB','.'])

ps_report_pipeline.add_task(CreateParamsTask())

ps_report_pipeline.add_task(ComputePowersAndClassifierTask())

ps_report_pipeline.add_task(SaveEventsTask())

ps_report_pipeline.add_task(GenerateTex())

# ps_report_pipeline.add_task(GenerateTexTable())


ps_report_pipeline.execute_pipeline()