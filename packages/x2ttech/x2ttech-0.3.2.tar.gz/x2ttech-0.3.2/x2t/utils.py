
# -*- coding: utf-8 -*-
import base64
import requests
import unidecode
import re
from threading import Thread
from x2t.logger import setup

logger = setup()


def slugify(text):
    text = unidecode.unidecode(text).upper()
    text = re.sub(r'[^A-Z0-9]', '', text)
    return text


def _prepare_thread(self, api, resIds, resModel, func):
    try:
        with self.pool.cursor() as cr:
            env = api.Environment(cr, self._uid, self._context)
            records = env[resModel].sudo().browse(resIds)
            if resModel and func:
                if hasattr(records, func):
                    _method = getattr(records, func)
                    if callable(_method):
                        return _method()
    except Exception as e:
        logger.exception(
            "❌ Error running %s in background thread: %s", (func, str(e)))


def _start_thread(kwargs, daemon=True):
    Thread(target=_prepare_thread, kwargs=kwargs, daemon=daemon).start()


def convert_u2b(url):
    try:
        return base64.b64encode(requests.get(url.strip()).content).replace(b"\n", b"").decode()
    except:
        return False
