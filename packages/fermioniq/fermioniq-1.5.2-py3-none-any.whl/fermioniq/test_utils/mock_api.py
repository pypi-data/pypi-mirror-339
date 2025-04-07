import datetime
import uuid
from typing import Any, NamedTuple

from fermioniq import EmulatorJob
from fermioniq.api import (
    ApiError,
    CancelJobResponse,
    JobResponse,
    JobResponseList,
    JwtResponse,
    Project,
    RemoteConfig,
    SasUrlResponse,
)

REMOTE_JOB_ID = "jr1"
USER_ID = "a_user_id"


class JobInfo(NamedTuple):
    job: dict
    job_response: JobResponse


class MockApi:
    """Mock of Fermioniq API."""

    def __init__(self):
        """Constructor."""
        self.jobs: dict[str, JobInfo] = {}

    def get_token(
        self,
        access_token_id: str,
        access_token_secret: str,
    ) -> JwtResponse:
        return JwtResponse(
            jwt_token="a_token",
            user_id=USER_ID,
            expiration_date=datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(minutes=1),
        )

    def get_projects(self, token: str) -> list[Project]:
        return [
            Project(
                id="project1",
                name="defaultproj",
                default=True,
            ),
            Project(
                id="project2",
                name="defaultproj2",
                default=False,
            ),
        ]

    def get_remote_configs(self, token: str) -> list[RemoteConfig]:
        return [
            RemoteConfig(
                id="rc1",
                name="remote-conf",
                description="desc",
                default=True,
            ),
            RemoteConfig(
                id="rc2",
                name="remote-conf2",
                description="desc2",
                default=False,
            ),
        ]

    def schedule_job(self, token: str, job: EmulatorJob) -> JobResponse:
        _id = uuid.uuid4().hex
        _jr = JobResponse(
            id=_id,
            user_id=USER_ID,
            creation_time=str(datetime.datetime.now()),
            status="scheduled",
            payload_digest="digest",
            status_code=-1,
        )
        self.jobs[_id] = JobInfo(job=job, job_response=_jr)
        return _jr

    def set_running(self, job_id: str | None = None):
        # Set all jobs to running if job_id is None (for testing purposes)
        if job_id is None:
            for _jid in self.jobs:
                self.jobs[_jid].job_response.status = "running"
            return None

        if job_id not in self.jobs:
            raise ValueError(f"Job with id {job_id} not found.")
        if self.jobs[job_id].job_response.status != "scheduled":
            raise ValueError(f"Job with id {job_id} is not in scheduled state.")

        self.jobs[job_id].job_response.status = "running"

    def set_finished(self, job_id: str | None = None):
        # Set all jobs to finished if job_id is None (for testing purposes)
        if job_id is None:
            for _jid in self.jobs:
                self.jobs[_jid].job_response.status = "finished"
            return None

        if job_id not in self.jobs:
            raise ValueError(f"Job with id {job_id} not found.")
        if self.jobs[job_id].job_response.status != "running":
            raise ValueError(f"Job with id {job_id} is not in running state.")
        self.jobs[job_id].job_response.status = "finished"
        self.jobs[job_id].job_response.status_code = 0

    def cancel_job(self, token: str, job_id: str) -> CancelJobResponse:
        try:
            self.jobs[job_id].job_response.status = "cancelled"
            self.jobs[job_id].job_response.status_code = 1
        except KeyError:
            raise ApiError(
                message="Job not found",
                status_code=500,
                reason="Internal server error",
                url="https://fermioniq-api-prod.azurewebsites.net/api/jobs/a/cancel",
                body="",
            )
        return CancelJobResponse(cancelled=True)

    def get_job_by_id(self, token: str, job_id: str) -> JobResponse:
        try:
            return self.jobs[job_id].job_response
        except KeyError:
            raise ApiError(
                message="Job not found",
                status_code=500,
                reason="Internal server error",
                url="https://fermioniq-api-prod.azurewebsites.net/api/jobs/a/cancel",
                body="",
            )

    def get_job_response_list(
        self, token: str, offset: int = 0, limit: int = 10
    ) -> JobResponseList:
        return JobResponseList(
            job_list=[job.job_response for job in self.jobs.values()]
        )

    def get_job_results(self, token: str, job_id: str) -> dict[str, Any]:
        try:
            _job_info = self.jobs[job_id]
            if _job_info.job_response.status != "finished":
                return None

            return {
                "status_code": 0,
                "emulator_output": _standard_job_output(),
                "metadata": _standard_job_metadata(_job_info.job["config"]),
            }
        except KeyError:
            raise ApiError(
                message="Job not found",
                status_code=500,
                reason="Internal server error",
                url="https://fermioniq-api-prod.azurewebsites.net/api/jobs/a/cancel",
                body="",
            )

    def get_job_config(self, token: str, job_id: str) -> dict:
        try:
            return {"configs": [c["values"] for c in self.jobs[job_id].job["config"]]}
        except KeyError:
            raise ApiError(
                message="Job not found",
                status_code=500,
                reason="Internal server error",
                url="https://fermioniq-api-prod.azurewebsites.net/api/jobs/a/cancel",
                body="",
            )

    def get_job_data_sas_url(self, token: str, job_id: str) -> SasUrlResponse:
        return SasUrlResponse(
            sas_url="http://unittest.fermioniq.nl/sasurl",
            expiry_date="2023-11-03 16:05:15.890243",
        )


def _standard_job_metadata(configs: list[dict]) -> dict:
    return {
        "gpu_used": False,
        "qcsim_version": "mock",
        "total_runs": 1,
        "total_runtime": 0.1,
        "unique_configs": {f"{i}": configs[i]["values"] for i in range(len(configs))},
    }


def _standard_job_output() -> dict:
    return [
        {
            "circuit_number": 0,
            "run_number": 0,
            "output": {"qubits": ["q_0", "q_1"], "samples": {"00": 500, "11": 500}},
            "metadata": {
                "runtime": 0.099,
                "status": "Completed",
                "fidelity_product": 1.0,
                "extrapolated_2qubit_gate_fidelity": 1.0,
                "num_subcircuits": 1,
                "number_1qubit_gates": 1,
                "number_2qubit_gates": 1,
                "output_metadata": {"samples": {"time_taken": 0.01}},
            },
            "config": "0",
        }
    ]
