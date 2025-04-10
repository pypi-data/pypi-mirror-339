from utils import (
    start_vm_instance,
    configure_instance_settings,
    run_system_tests,
    gather_logs,
    destroy_vm_instance,
    check_instance_health,
    parallel_task_runner
)


class FDBProvisioner:
    def __init__(self, config_path):
        self.config_path = config_path
        self.instance_id = None

    def provision(self):
        self.instance_id = start_vm_instance(self.config_path)
        return self.instance_id

    def configure(self, settings):
        if not self.instance_id:
            raise RuntimeError("VM not provisioned yet")
        return configure_instance_settings(self.instance_id, settings)

    def destroy(self):
        if self.instance_id:
            return destroy_vm_instance(self.instance_id)


class FDBHealthChecker:
    def __init__(self, instance_id):
        self.instance_id = instance_id

    def check(self):
        return check_instance_health(self.instance_id)


class FDBTestRunner:
    def __init__(self, suite_path):
        self.suite_path = suite_path

    def execute(self):
        return run_system_tests(self.suite_path)


class FDBLogCollector:
    def __init__(self, instance_id, output_dir):
        self.instance_id = instance_id
        self.output_dir = output_dir

    def collect(self):
        return gather_logs(self.instance_id, self.output_dir)


class FDBParallelExecutor:
    def __init__(self, task_list):
        self.task_list = task_list

    def run_all(self):
        parallel_task_runner(self.task_list)


class FDBDeploymentWorkflow:
    def __init__(self, config_path, settings, test_path, log_dir):
        self.config_path = config_path
        self.settings = settings
        self.test_path = test_path
        self.log_dir = log_dir
        self.instance_id = None

    def run(self):
        provisioner = FDBProvisioner(self.config_path)
        self.instance_id = provisioner.provision()
        provisioner.configure(self.settings)

        if not FDBHealthChecker(self.instance_id).check():
            raise Exception("Instance health check failed")

        if not FDBTestRunner(self.test_path).execute():
            raise Exception("System tests failed")

        FDBLogCollector(self.instance_id, self.log_dir).collect()
        provisioner.destroy()
        print("Deployment workflow completed successfully.")
