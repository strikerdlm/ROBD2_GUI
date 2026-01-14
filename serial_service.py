from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from random import gauss, random
from typing import Callable, Dict, Optional

from serial_comm import SerialCommunicator
from data_store import DataStore


@dataclass(frozen=True, slots=True)
class LiveSample:
    timestamp: datetime
    altitude: float
    o2_conc: float
    blp: float
    spo2: float
    pulse: float


class SerialService:
    """
    Thread-safe wrapper around SerialCommunicator for Streamlit use.
    - Bounded polling interval (<=2s) to keep device responsive.
    - Optional demo mode that synthesizes plausible data when no device is connected.
    """

    def __init__(
        self,
        poll_interval: float = 5.0,
        use_demo_if_disconnected: bool = True,
    ) -> None:
        if poll_interval <= 0:
            raise ValueError("poll_interval must be > 0")
        self._serial = SerialCommunicator()
        self._data_store = DataStore(max_points=2000)
        # Device documentation requires queries at least every ~2 seconds to stay responsive.
        self._poll_interval = min(poll_interval, 2.0)
        self._use_demo = use_demo_if_disconnected
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._on_sample: Optional[Callable[[LiveSample], None]] = None
        self._last_sample_at: Optional[float] = None
        self._last_attempt_at: Optional[float] = None
        self._consecutive_errors: int = 0
        self._log = logging.getLogger("robd2_streamlit.serial_service")

    # ---------- public properties ----------
    @property
    def data_store(self) -> DataStore:
        return self._data_store

    @property
    def connected(self) -> bool:
        return self._serial.is_connected

    # ---------- connection control ----------
    def list_ports(self) -> list[str]:
        return self._serial.get_available_ports()

    def connect(self, port: str) -> tuple[bool, str]:
        return self._serial.connect(port)

    def disconnect(self) -> tuple[bool, str]:
        self.stop_polling()
        return self._serial.disconnect()

    # ---------- polling control ----------
    def start_polling(self, on_sample: Optional[Callable[[LiveSample], None]] = None) -> None:
        self._on_sample = on_sample
        self._stop_event.clear()
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop_polling(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=self._poll_interval * 2)

    # ---------- command helpers ----------
    def send_command(self, command: str) -> tuple[bool, str]:
        return self._serial.send_command(command)

    def get_response(self) -> Optional[str]:
        return self._serial.get_response()

    # ---------- internal ----------
    def _poll_loop(self) -> None:
        next_tick = time.monotonic()
        while not self._stop_event.is_set():
            start = time.monotonic()
            self._last_attempt_at = start
            try:
                sample = self._read_sample()
                if sample:
                    self._record_sample(sample)
                    self._consecutive_errors = 0
                    self._last_sample_at = time.monotonic()
                else:
                    self._consecutive_errors += 1
            except Exception as exc:  # noqa: BLE001
                self._consecutive_errors += 1
                self._log.exception("Polling error: %s", exc)
            next_tick += self._poll_interval
            sleep_for = max(0.0, next_tick - time.monotonic())
            # Allow stop requests to break the sleep quickly.
            self._stop_event.wait(timeout=sleep_for)

    def _read_sample(self) -> Optional[LiveSample]:
        if self.connected:
            ok, message = self._serial.send_command("GET RUN ALL")
            if not ok:
                return None
            time.sleep(0.2)
            response = self._serial.get_response()
            if not response:
                return None
            parts = response.strip().split(",")
            if len(parts) < 10:
                return None
            now = datetime.now()
            try:
                return LiveSample(
                    timestamp=now,
                    altitude=float(parts[2]),
                    o2_conc=float(parts[4]),
                    blp=float(parts[5]),
                    spo2=float(parts[8]),
                    pulse=float(parts[9]),
                )
            except ValueError:
                return None

        if not self._use_demo:
            return None

        # Demo data: simple random walk around sea level
        now = datetime.now()
        altitude = 8000 + 2000 * (0.5 - random())
        return LiveSample(
            timestamp=now,
            altitude=max(0.0, altitude),
            o2_conc=max(4.0, 21.0 - altitude / 4000.0 + gauss(0, 0.2)),
            blp=max(0.0, 5.0 + gauss(0, 0.3)),
            spo2=max(50.0, min(100.0, 95.0 - altitude / 12000.0 + gauss(0, 0.5))),
            pulse=max(50.0, min(160.0, 72.0 + (altitude / 5000.0) * 3 + gauss(0, 2.0))),
        )

    def _record_sample(self, sample: LiveSample) -> None:
        self._data_store.add_data(
            sample.timestamp,
            {
                "altitude": sample.altitude,
                "o2_conc": sample.o2_conc,
                "blp": sample.blp,
                "spo2": sample.spo2,
                "pulse": sample.pulse,
                "o2_voltage": 0.0,
                "error_percent": 0.0,
            },
        )
        if self._on_sample:
            self._on_sample(sample)
        # Track freshness in monotonic time to avoid clock jumps.
        self._last_sample_at = time.monotonic()

    # ---------- health / watchdog ----------
    def ensure_polling(self, stale_after: Optional[float] = None) -> None:
        """
        Ensure the polling thread is alive and samples are fresh.

        If the last sample is older than stale_after seconds (default 2.5x interval),
        the poller is restarted to prevent hangs.
        """
        if not self.connected:
            return
        if not self._thread or not self._thread.is_alive():
            self.start_polling(self._on_sample)
            return
        threshold = stale_after or (self._poll_interval * 2.5)
        if self._last_sample_at is None:
            return
        if (time.monotonic() - self._last_sample_at) > threshold:
            self._log.warning(
                "Restarting poller after %.2fs without samples", time.monotonic() - self._last_sample_at
            )
            self.stop_polling()
            self.start_polling(self._on_sample)

    def health(self) -> Dict[str, float | int | bool | None]:
        """Return lightweight health snapshot for UI display."""
        now = time.monotonic()
        return {
            "connected": self.connected,
            "thread_alive": bool(self._thread and self._thread.is_alive()),
            "poll_interval": self._poll_interval,
            "sample_age_sec": None if self._last_sample_at is None else max(0.0, now - self._last_sample_at),
            "attempt_age_sec": None if self._last_attempt_at is None else max(0.0, now - self._last_attempt_at),
            "consecutive_errors": self._consecutive_errors,
        }
