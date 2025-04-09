"""
    QApp Platform Project ibm_cloud_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from time import time

from qapp_common.config.logging_config import logger
from qapp_common.data.device.circuit_running_option import CircuitRunningOption
from qapp_common.enum.status.job_status import JobStatus
from qapp_common.model.device.custom_device import CustomDevice
from qapp_common.model.provider.provider import Provider
from qcaas_client.client import QPUTask, CompilerConfig
from qiskit.qasm2 import dumps

from qapp_braket.util.circuit_convert_utils import CircuitConvertUtils


class OqcCloudDevice(CustomDevice):

    def __init__(self, provider: Provider, device_specification: str):
        super().__init__(provider, device_specification)

        self.device_specification = device_specification

    def _create_job(self, circuit, options: CircuitRunningOption):
        logger.debug("[OqcCloudDevice] _create_job() with {0} shots".format(options.shots))

        start_time = time()

        qiskit_circuit = CircuitConvertUtils.braket_to_qiskit(circuit)
        qiskit_circuit.measure_all()
        qasm_str = dumps(qiskit_circuit)
        circuit_submit_options = CompilerConfig(repeats=options.shots)

        task = QPUTask(program=qasm_str, config=circuit_submit_options)
        job = self.device.execute_tasks(task, qpu_id=self.device_specification)

        self.execution_time = time() - start_time

        return job

    def _is_simulator(self) -> bool:
        logger.debug("[OqcCloudDevice] _is_simulator()")

        return True

    def _produce_histogram_data(self, job_result) -> dict | None:
        logger.debug("[OqcCloudDevice] _produce_histogram_data()")

        return next(iter(job_result.result.values()))

    def _get_provider_job_id(self, job) -> str:
        logger.debug("[OqcCloudDevice] _get_provider_job_id()")

        return job[0].id

    def _get_job_status(self, job) -> str:
        logger.debug("[OqcCloudDevice] _get_job_status()")

        oqc_status = self.device.get_task_status(task_id=job[0].id,
                                                 qpu_id=self.device_specification)
        logger.debug("[OqcCloudDevice] job status: {0} ".format(oqc_status))

        if "FAILED".__eq__(oqc_status):
            return JobStatus.ERROR.value
        elif "COMPLETED".__eq__(oqc_status):
            return JobStatus.DONE.value

        return oqc_status

    def _calculate_execution_time(self, job_result):
        logger.debug("[OqcCloudDevice] _calculate_execution_time()")

        logger.debug("[OqcCloudDevice] Execution time calculation was: {0} seconds"
                     .format(self.execution_time))

    def _get_job_result(self, job):
        logger.debug("[OqcCloudDevice] _get_job_result()")

        return job[0]

    def _get_shots(self, job_result) -> int | None:
        """
        Retrieve the total number of measurement shots from the job result.

        This method checks if the job result contains measurement data
        and calculates the total number of shots based on the measurement
        results. If the measurement data is not available, the method
        returns None.

        Args:
            job_result: An object representing the result of a job, which
                        may contain measurement results under the 'result'
                        attribute.

        Returns:
            int | None: The total number of shots if measurement data is
                         available; otherwise, None.
        """
        logger.debug("[OqcCloudDevice] _get_shots()")

        result_meas = getattr(job_result, 'result', {}).get('meas')
        return sum(result_meas.values()) if result_meas else None
