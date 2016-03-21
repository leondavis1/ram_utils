from RamPipeline import RamTask
from ReportUtils import MissingExperimentError, MissingDataError, ReportError, ReportStatus
import inspect

class ReportRamTask(RamTask):
    def __init__(self, mark_as_completed):
        super(ReportRamTask, self).__init__(mark_as_completed=mark_as_completed)

    def get_code_data(self):
        """
        returns name of the file and line number of the calling function
        :return {tuple: str, int}: filename, line number
        """
        (frame, file, line,function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        return file, line

    def add_report_status(self, message=''):
        (frame, file, line,function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]

        rs = ReportStatus(task=self.__class__.__name__, message=message, file=file, line=line)

        self.pipeline.report_summary.add_report_status_obj(status_obj=rs)


    def pre(self):
        self.pipeline.report_summary.set_subject(self.pipeline.subject)

    def post(self):
        message = 'TASK COMPLETED OK'
        (frame, file, line,function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[0]
        file, line = self.get_code_data()
        rs = ReportStatus(task=self.__class__.__name__, message=message, file=file, line=line)

        self.pipeline.report_summary.add_report_status_obj(status_obj=rs)

    def raise_and_log_report_exception(self, exception_type='', exception_message=''):

        if exception_type == 'MissingExperimentError':
            # rs = ReportStatus(subject=self.pipeline.subject)
            excpt = MissingExperimentError(
                message=exception_message,
                # status=rs
            )
        elif exception_type == 'MissingDataError':
            # rs = ReportStatus(subject=self.pipeline.subject)
            excpt = MissingDataError(
                message=exception_message,
                # status=rs
            )

        else:
            # rs = ReportStatus(subject=self.pipeline.subject)
            excpt = ReportError(
                message=exception_message,
                # status=rs
            )

        # file, line = self.get_code_data()
        (frame, file, line,function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        error_rs = ReportStatus(task=self.__class__.__name__, error=excpt, file=file, line=line)

        self.pipeline.report_summary.add_report_error_status(error_status=error_rs)


        raise excpt
