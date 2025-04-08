import signal
import subprocess
import time
import threading
import asyncio

from framefox.core.di.service_container import ServiceContainer
from framefox.terminal.commands.abstract_command import AbstractCommand
from framefox.terminal.commands.server.worker_command import WorkerCommand


class ServerStartCommand(AbstractCommand):
    def __init__(self):
        super().__init__("start")
        self.process = None
        self.running = True
        self.worker_thread = None
        self.worker_command = None
        self.worker_stop_event = None

    def execute(self, *args, **kwargs):
        port = 8000
        with_workers = False

        i = 0
        while i < len(args):
            arg = args[i]
            if arg == "--port" and i + 1 < len(args):
                try:
                    port = int(args[i + 1])
                    i += 2
                except ValueError:
                    self.printer.print_msg(
                        f"Invalid port: {args[i + 1]}", theme="error")
                    return 1
            elif arg.startswith("--port="):
                try:
                    port = int(arg.split("=")[1])
                    i += 1
                except (ValueError, IndexError):
                    self.printer.print_msg(
                        f"Invalid port: {arg}", theme="error")
                    return 1
            elif arg == "--with-workers":
                with_workers = True
                i += 1
            else:
                i += 1

        self.printer.print_msg(
            f"Starting the server on port {port}",
            theme="success",
            linebefore=True,
        )

        if with_workers:
            self._setup_workers()

        self._setup_signal_handlers()

        try:
            self.process = subprocess.Popen(
                ["uvicorn", "main:app", "--reload", "--port", str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )

            while self.running and self.process.poll() is None:
                line = self.process.stdout.readline().rstrip()
                if line:
                    print(line)
                time.sleep(0.1)

            if self.process.poll() is None:
                self._graceful_shutdown()

            return 0
        except KeyboardInterrupt:
            self._graceful_shutdown()
            return 0

    def _setup_workers(self):
        self.printer.print_msg(
            "Starting worker process in background...",
            theme="info",
            linebefore=True,
        )

        self.worker_command = WorkerCommand()
        self.worker_stop_event = threading.Event()
        self.worker_thread = threading.Thread(
            target=self._run_worker_thread,
            daemon=True
        )
        self.worker_thread.start()
        time.sleep(1)

    def _run_worker_thread(self):
        try:
            from framefox.core.task.worker_manager import WorkerManager
            worker_manager = ServiceContainer().get(WorkerManager)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            async def run_worker():
                worker_manager.running = True
                try:
                    await worker_manager._process_loop()
                except Exception as e:
                    print(f"Worker process loop error: {e}")

            async def check_stop_event():
                while not self.worker_stop_event.is_set():
                    await asyncio.sleep(0.5)
                worker_manager.running = False
                print("Worker stop event detected, shutting down worker...")

            loop.create_task(run_worker())
            loop.create_task(check_stop_event())
            loop.run_forever()
        except Exception as e:
            print(f"Worker error: {e}")

    def _setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, sig, frame):
        self.printer.print_msg("\nStopping the server...", theme="warning")
        self.running = False
        if self.worker_stop_event:
            self.worker_stop_event.set()

    def _graceful_shutdown(self):
        if self.worker_thread and self.worker_thread.is_alive() and self.worker_stop_event:
            self.printer.print_msg("Stopping workers...", theme="warning")
            self.worker_stop_event.set()
            self.worker_thread.join(1.0)

        if self.process and self.process.poll() is None:
            self.process.send_signal(signal.SIGINT)

            try:
                self.process.wait(timeout=5)
                self.printer.print_msg(
                    "Server stopped successfully", theme="success")
            except subprocess.TimeoutExpired:
                self.printer.print_msg(
                    "Timeout exceeded, forcing server shutdown", theme="warning"
                )
                self.process.terminate()
                try:
                    self.process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.printer.print_msg(
                        "Server forcibly terminated", theme="error")
