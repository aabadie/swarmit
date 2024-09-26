import os
import shlex
import subprocess
import time


try:
    for device_count in range(1, 11):
        durations = []
        num_experiments = 10
        print(f"Running {num_experiments} experiments with {device_count} device{"" if device_count == 1 else "s"}")
        for _ in range(num_experiments):
            start = time.time()
            subprocess.run(
                shlex.split(
                    f"iotlab-experiment submit -d 5 -n aa_test_nrf -l {device_count},archi=nrf52840dk:multi+site=saclay,/work/aio/DotBot/swarmit/sample_dotbot/Output/Debug/Exe/Sample.bin"
                ),
                stdout=open(os.devnull, "w"),
                stderr=subprocess.STDOUT
            )
            subprocess.run(
                shlex.split(
                    "iotlab-experiment wait"
                ),
                stdout=open(os.devnull, "w"),
                stderr=subprocess.STDOUT
            )
            durations.append(time.time() - start)
            subprocess.run(
                shlex.split(
                    "iotlab-experiment stop"
                ),
                stdout=open(os.devnull, "w"),
                stderr=subprocess.STDOUT
            )
            time.sleep(5)
        mean_duration = sum(durations) / num_experiments
        print(f"Mean time: {mean_duration:.3f}s")
except KeyboardInterrupt:
    subprocess.run(shlex.split("iotlab-experiment stop"), stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    print("Experiment stopped")
