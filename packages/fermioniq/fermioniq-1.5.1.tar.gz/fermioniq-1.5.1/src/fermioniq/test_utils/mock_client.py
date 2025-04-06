from fermioniq import EmulatorJob
from fermioniq.client import (
    Client,
    JobResponse,
    JobResult,
    NoResultsError,
    NoResultsErrorReason,
)
from fermioniq.test_utils.mock_api import MockApi
from qcshared.json.encode import jsonify


class MockClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api = MockApi()
        self.scheduled_job = None

    def set_running(self, job_id: str):
        self._api.job_started = True

    def set_finished(self, job_id: str):
        self._api.job_is_done = True
        self.scheduled_job = None

    def cancel(self, job_id: str):
        self.scheduled_job = None
        return super().cancel(job_id)

    def get_results(self, job_id: str):
        if not self._api.job_is_done:
            raise NoResultsError(
                (
                    f"Error retrieving results for job: {job_id}. The "
                    f"status is '{self.get_status(job_id)}'. Try again later."
                ),
                reason=NoResultsErrorReason.JOB_NOT_FINISHED,
            )

        return JobResult(
            status_code=0,
            job_outputs=_standard_job_output(),
            job_metadata=_standard_job_metadata(self.scheduled_job.config[0]),
        )

    def schedule_async(self, job: EmulatorJob) -> JobResponse:
        self.scheduled_job = job
        return super().schedule_async(job)

    def get_config(self, job_id: str) -> dict:
        if self.scheduled_job is None:
            return None
        return [c["values"] for c in jsonify(self.scheduled_job.config)]


def _standard_job_metadata(config: dict) -> dict:
    return {
        "gpu_used": False,
        "qcsim_version": "mock",
        "total_runs": 1,
        "total_runtime": 0.1,
        "unique_configs": {
            "0": config,
        },
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
