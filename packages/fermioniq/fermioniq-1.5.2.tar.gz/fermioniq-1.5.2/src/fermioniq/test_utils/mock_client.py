import fermioniq.test_utils
from fermioniq.client import Client, JobResult, NoResultsError, NoResultsErrorReason
from fermioniq.test_utils.mock_api import MockApi


class MockClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api = MockApi()
        self.scheduled_job = None

    def set_running(self, job_id: str | None = None):
        self._api.set_running(job_id)

    def set_finished(self, job_id: str | None = None):
        self._api.set_finished(job_id)

    def get_results(self, job_id: str):
        _res = self._api.get_job_results(self._token, job_id)
        if not _res:
            raise NoResultsError(
                reason=NoResultsErrorReason.JOB_NOT_FINISHED,
                msg="No results found for job",
            )
        return JobResult(
            status_code=_res["status_code"],
            job_outputs=_res["emulator_output"],
            job_metadata=_res["metadata"],
        )
