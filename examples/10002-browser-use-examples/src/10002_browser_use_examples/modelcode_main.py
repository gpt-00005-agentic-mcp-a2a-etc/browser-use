
"""Top-level helpers for the 10002_browser_use_examples package.

This file provides a minimal, safe default implementation so the package
can be imported and run as a module (e.g. `python -m 10002_browser_use_examples`).
"""

from __future__ import annotations

import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

__all__ = ["Config", "get_config", "main", "__version__"]

__version__ = "0.1.0"


@dataclass
class Config:
	"""Runtime configuration loaded from environment variables.

	Keep this dataclass small; add fields as your project needs them.
	"""

	groq_api_base_url: str
	groq_api_key: Optional[str]
	groq_project_id: Optional[str]
	groq_region: Optional[str]
	groq_model: Optional[str]
	groq_timeout_seconds: int

	def masked(self) -> dict:
		"""Return a copy of the config with secrets masked for safe printing."""
		masked_key = None
		if self.groq_api_key:
			masked_key = self.groq_api_key[:4] + "..." + self.groq_api_key[-4:]
		return {
			"groq_api_base_url": self.groq_api_base_url,
			"groq_api_key": masked_key,
			"groq_project_id": self.groq_project_id,
			"groq_region": self.groq_region,
			"groq_model": self.groq_model,
			"groq_timeout_seconds": self.groq_timeout_seconds,
		}


def get_config() -> Config:
	"""Load configuration from environment variables with sensible defaults.

	This function intentionally avoids loading .env files so callers can control
	how secrets are provided (dotenv, CI secrets, OS env, etc.).
	"""
	# Attempt to load a .env file located next to this package if present.
	# Prefer python-dotenv if installed; otherwise fall back to a simple parser.
	_load_dotenv_from_package()
	base_url = os.getenv("GROQ_API_BASE_URL", "https://api.groq.ai")
	key = os.getenv("GROQ_API_KEY")
	project_id = os.getenv("GROQ_PROJECT_ID")
	region = os.getenv("GROQ_REGION")
	model = os.getenv("GROQ_MODEL")
	try:
		timeout = int(os.getenv("GROQ_TIMEOUT_SECONDS", "30"))
	except ValueError:
		timeout = 30

	return Config(
		groq_api_base_url=base_url,
		groq_api_key=key,
		groq_project_id=project_id,
		groq_region=region,
		groq_model=model,
		groq_timeout_seconds=timeout,
	)


def main() -> int:
	"""Simple CLI entrypoint: print loaded config (with secrets masked).

	Returns an exit code (0 on success).
	"""
	# configure logging early so import-time logs are captured
	setup_logging()
	cfg = get_config()
	logging.getLogger(__name__).info("10002_browser_use_examples v%s", __version__)
	logging.getLogger(__name__).info("Loaded config: %s", cfg.masked())
	# also print a short friendly output on console
	print("10002_browser_use_examples v{}".format(__version__))
	for k, v in cfg.masked().items():
		print(f"  {k}: {v}")
	return 0


def _load_dotenv_from_package(dotenv_path: Optional[str] = None) -> None:
	"""Load environment variables from a .env file.

	Tries to use python-dotenv (if installed). If not available, uses a tiny
	fallback parser that supports simple KEY=VALUE lines and ignores comments.

	By default it looks for a `.env` file in the package directory.
	"""
	# Determine default path: package directory .env
	if dotenv_path is None:
		pkg_dir = Path(__file__).resolve().parent
		dotenv_path = str(pkg_dir / ".env")
	# Try python-dotenv first
	try:
		from dotenv import load_dotenv as _load
		_load(dotenv_path, override=False)
		return
	except Exception:
		# fallback to manual parser
		pass

	try:
		p = Path(dotenv_path)
		if not p.exists():
			return
		for raw in p.read_text(encoding="utf-8").splitlines():
			line = raw.strip()
			if not line or line.startswith("#"):
				continue
			if "=" not in line:
				continue
			k, v = line.split("=", 1)
			k = k.strip()
			v = v.strip().strip('"').strip("'")
			# Do not overwrite an already-set environment variable
			if k not in os.environ:
				os.environ[k] = v
	except Exception:
		# be conservative: don't crash the app due to .env parsing issues
		return


def setup_logging(log_dir: str = ".log", level: str = "INFO") -> None:
	"""Configure root logging with a rotating file handler and a console handler.

	Creates `log_dir` if missing. Uses a RotatingFileHandler that rolls when the
	file reaches 10MB with 5 backups. Logs include timestamps, level, module, and message.
	"""
	log_path = Path(log_dir)
	log_path.mkdir(parents=True, exist_ok=True)
	logfile = log_path / "application.log"

	level_no = getattr(logging, level.upper(), logging.INFO)
	root = logging.getLogger()
	root.setLevel(level_no)

	# File handler (rotating)
	file_handler = RotatingFileHandler(str(logfile), maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8")
	file_formatter = logging.Formatter(
		"%(asctime)s %(levelname)-8s [%(name)s:%(lineno)d] %(message)s",
		datefmt="%Y-%m-%d %H:%M:%S",
	)
	file_handler.setFormatter(file_formatter)
	file_handler.setLevel(level_no)
	root.addHandler(file_handler)

	# Console handler (stream)
	console = logging.StreamHandler()
	console.setFormatter(logging.Formatter("%(levelname)-8s: %(message)s"))
	console.setLevel(level_no)
	root.addHandler(console)


if __name__ == "__main__":
	raise SystemExit(main())

