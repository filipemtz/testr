

from testr.autojudge.unsafe_runner import UnsafeRunner
from testr.autojudge.runner_interface import RunnerInterface


class DockerRunner(RunnerInterface):
    KNOWN_WARNINGS = [
        "WARNING: Your kernel does not support swap limit capabilities or the cgroup is not mounted. Memory limited without swap."
    ]

    def __init__(self,
                 command: str,
                 cpu: float = 1.0,
                 memory_mb: int = 1024,
                 timeout_seconds: float = 60.0,
                 docker_dir: str = "/",
                 host_dir: str = ""
                 ):

        self._docker_cmd = self._assemble_command(
            command,
            cpu,
            memory_mb,
            timeout_seconds,
            docker_dir,
            host_dir
        )

        self._runner = UnsafeRunner(self._docker_cmd, running_dir=host_dir)

    def run(self, input_str: str = '', verbose: bool = False):
        result = self._runner.run(
            input_str,
            discard_outputs=DockerRunner.KNOWN_WARNINGS,
            verbose=verbose
        )

        if result['result']:
            # when running with docker, we use the timeout function that returns
            # error 124 when the program takes longer to finish than than the
            # given time.
            if result['result'].returncode == 124:
                result['time_limit_exceeded'] = True

        return result

    def _assemble_command(self, command: str, cpu: float = 1.0, memory_mb: int = 1024, timeout_seconds: float = 60.0, docker_dir: str = "/", host_dir: str = ""):
        docker_cmd = "docker run"
        docker_cmd += f" --memory={memory_mb}m"
        docker_cmd += f" --cpus={cpu}"
        docker_cmd += f" -i --rm"
        docker_cmd += f" -v \"{host_dir}\":\"{docker_dir}\""
        docker_cmd += f" -w \"{docker_dir}\""
        docker_cmd += f" testr_docker_image"
        docker_cmd += f" timeout -s SIGKILL {timeout_seconds}s"
        docker_cmd += f" {command}"
        return docker_cmd
