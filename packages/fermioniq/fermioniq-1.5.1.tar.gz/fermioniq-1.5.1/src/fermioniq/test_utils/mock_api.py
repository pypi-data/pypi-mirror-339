import datetime
from typing import Any

from fermioniq import EmulatorJob
from fermioniq.api import (
    CancelJobResponse,
    JobResponse,
    JwtResponse,
    Project,
    RemoteConfig,
    SasUrlResponse,
)

REMOTE_JOB_ID = "jr1"
USER_ID = "a_user_id"


class MockApi:
    """Mock of Fermioniq API."""

    def __init__(self):
        """Constructor."""
        self.job_started = False
        self.job_is_done = False
        self.job_cancelled = False

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
                name="proj2",
                default=False,
            ),
        ]

    def get_remote_configs(self, token: str) -> list[RemoteConfig]:
        return [
            RemoteConfig(
                id="rc1",
                name="remote conf",
                description="desc",
                default=True,
            ),
            RemoteConfig(
                id="rc2",
                name="remote conf2",
                description="desc2",
                default=False,
            ),
        ]

    def schedule_job(self, token: str, job: EmulatorJob) -> JobResponse:
        return JobResponse(
            id=REMOTE_JOB_ID,
            user_id=USER_ID,
            creation_time=str(datetime.datetime.now()),
            status="scheduled",
            payload_digest="digest",
            status_code=-1,
        )

    def cancel_job(self, token: str, job_id: str) -> CancelJobResponse:
        self.job_cancelled = True
        return CancelJobResponse(cancelled=True)

    def get_job_by_id(self, token: str, job_id: str) -> JobResponse:
        status = "scheduled"
        status_code = -1
        if self.job_started:
            status = "running"
        if self.job_is_done:
            status = "finished"
            status_code = 0
        if self.job_cancelled:
            status = "cancelled"
            status_code = 1

        return JobResponse(
            id=REMOTE_JOB_ID,
            user_id=USER_ID,
            creation_time=str(datetime.datetime.now()),
            status=status,
            payload_digest="digest",
            status_code=status_code,
        )

    def get_job_results(self, token: str, job_id: str) -> dict[str, Any]:
        return {
            "status_code": 0,
            "emulator_output": [{"output": "output_val", "config": "0"}],
            "metadata": {
                "metadata1": "metadata_value1",
                "unique_configs": {"0": "config_1"},
            },
        }

    def get_job_data_sas_url(self, token: str, job_id: str) -> SasUrlResponse:
        return SasUrlResponse(
            sas_url="http://unittest.fermioniq.nl/sasurl",
            expiry_date="2023-11-03 16:05:15.890243",
        )
