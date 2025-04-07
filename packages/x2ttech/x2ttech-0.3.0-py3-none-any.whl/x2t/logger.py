
# -*- coding: utf-8 -*-
import base64
import requests
import unidecode
import re
import platform
import os
from pathlib import Path
from loguru import logger
from threading import Thread


def path(filename):
    system = platform.system()
    if system == "Windows":
        # C:\Users\<User>\AppData\Local\Odoo\logs\custom.log
        log_dir = Path.home() / "AppData" / "Local" / "Odoo" / "logs"
    elif system == "Darwin":
        # /Users/<User>/Library/Logs/Odoo/custom.log
        log_dir = Path.home() / "Library" / "Logs" / "Odoo"
    else:
        # Linux / Ubuntu
        default_log_dir = Path("/var/log/odoo")
        if os.access(default_log_dir, os.W_OK):
            log_dir = default_log_dir
        else:
            log_dir = Path.home() / "odoo_logs"

    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / filename


def setup(filename="loguru.odoo.log", level="INFO"):
    log_path = path(filename)
    logger.remove()
    logger.add(
        str(log_path),
        rotation="10 MB",
        retention="10 days",
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>"
    )
    return logger
