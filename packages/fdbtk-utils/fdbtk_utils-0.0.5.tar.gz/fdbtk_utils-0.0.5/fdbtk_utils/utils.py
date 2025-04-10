import os
import subprocess
import json
import threading
import time
import random


def start_vm_instance(config_path):
    with open(config_path) as f:
        config = json.load(f)
    vm_name = config.get("name", f"vm-{random.randint(1000, 9999)}")
    print(f"Provisioning VM: {vm_name} in region {config.get('region')}")
    time.sleep(2)
    print(f"VM {vm_name} started successfully.")
    return vm_name


def configure_instance_settings(instance_id, settings):
    for key, value in settings.items():
        print(f"Applying setting {key} = {value} on instance {instance_id}")
        time.sleep(0.3)
    print(f"Configuration for {instance_id} completed.")
    return True


def run_system_tests(test_suite_path):
    print(f"Running tests from: {test_suite_path}")
    result = subprocess.run(
        ["echo", f"Simulating test run for {test_suite_path}"], capture_output=True, text=True)
    print(result.stdout)
    print("All tests passed.")
    return True


def gather_logs(instance_id, destination):
    os.makedirs(destination, exist_ok=True)
    log_path = os.path.join(destination, f"{instance_id}_logs.txt")
    with open(log_path, "w") as log_file:
        log_file.write(f"Logs for {instance_id}\n")
        log_file.write("Sample log entry: service started.\n")
        log_file.write("Sample log entry: health check passed.\n")
    print(f"Logs saved to {log_path}")
    return log_path


def destroy_vm_instance(instance_id):
    print(f"Sending termination signal to instance: {instance_id}")
    time.sleep(1)
    print(f"Instance {instance_id} successfully destroyed.")
    return True


def parallel_task_runner(tasks):
    threads = []
    for task in tasks:
        t = threading.Thread(target=task)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("All parallel tasks completed.")


def check_instance_health(instance_id):
    print(f"Pinging instance {instance_id} for health check...")
    time.sleep(0.5)
    status = random.choice(["healthy", "degraded", "unreachable"])
    print(f"Instance {instance_id} is {status}.")
    return status == "healthy"
