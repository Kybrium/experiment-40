import io
import logging
import logging.config

from django.conf import settings
from django.test import SimpleTestCase


class LoggingConfigTests(SimpleTestCase):
    def test_logging_dict_structure(self):
        cfg = settings.LOGGING

        # Basic keys exist
        self.assertEqual(cfg.get("version"), 1)
        self.assertFalse(cfg.get("disable_existing_loggers", True))

        # Formatter
        self.assertIn("console", cfg["formatters"])
        fmt = cfg["formatters"]["console"]
        self.assertEqual(fmt["format"], settings.DJANGO_LOG_FORMAT)
        self.assertEqual(fmt["datefmt"], "%d.%m.%Y %H:%M:%S")

        # Handler
        self.assertIn("console", cfg["handlers"])
        h = cfg["handlers"]["console"]
        self.assertEqual(h["class"], "logging.StreamHandler")
        self.assertEqual(h["formatter"], "console")
        self.assertIn("stream", h)
        self.assertEqual(h["level"], settings.LOG_LEVEL)

        # Loggers
        self.assertIn("core", cfg["loggers"])
        self.assertIn("django", cfg["loggers"])
        self.assertIn("django.request", cfg["loggers"])
        self.assertIn("django.db.backends", cfg["loggers"])

        self.assertFalse(cfg["loggers"]["core"]["propagate"])
        self.assertFalse(cfg["loggers"]["django"]["propagate"])
        self.assertFalse(cfg["loggers"]["django.request"]["propagate"])
        self.assertFalse(cfg["loggers"]["django.db.backends"]["propagate"])

        self.assertEqual(cfg["loggers"]["core"]["level"], settings.LOG_LEVEL)
        self.assertEqual(cfg["loggers"]["django"]["level"], settings.LOG_LEVEL)
        self.assertEqual(cfg["loggers"]["django.request"]["level"], "WARNING")
        self.assertEqual(cfg["loggers"]["django.db.backends"]["level"], "INFO")

        # Root logger honors LOG_LEVEL
        self.assertIn("root", cfg)
        self.assertEqual(cfg["root"]["level"], settings.LOG_LEVEL)
        self.assertIn("console", cfg["root"]["handlers"])

    def test_formatter_outputs_expected_shape(self):
        """
        Build a formatter equivalent to the 'console' formatter, attach it to a
        temporary StreamHandler writing to an in-memory buffer, emit one record,
        and assert the output matches the expected pattern:
        [dd.mm.YYYY HH:MM:SS] [LEVEL] [logger.name] | message (filename.py:lineno)
        """
        buffer = io.StringIO()
        handler = logging.StreamHandler(buffer)
        formatter = logging.Formatter(
            fmt=settings.DJANGO_LOG_FORMAT,
            datefmt="%d.%m.%Y %H:%M:%S",
        )
        handler.setFormatter(formatter)

        logger = logging.getLogger("core.tests.logging")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.propagate = False

        logger.info("hello world")

        output = buffer.getvalue().strip()
        # Example:
        # [17.10.2025 12:34:56] [INFO] [core.tests.logging] | hello world (test_logging.py:XX)
        pattern = (
            r"^\[\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}\] "      # timestamp
            r"\[(DEBUG|INFO|WARNING|ERROR|CRITICAL)\] "         # level
            r"\[core\.tests\.logging\] \| hello world "         # logger + message
            r"\([A-Za-z0-9_]+\.py:\d+\)$"                       # filename:lineno
        )
        self.assertRegex(output, pattern)

        # Cleanup
        logger.removeHandler(handler)
        handler.close()

    def test_dictconfig_applies_cleanly(self):
        """
        Ensure dictConfig doesn't raise and can be applied.
        (This won't change Django's configured logging for the rest of the run,
        but should execute without exceptions.)
        """
        logging.config.dictConfig(settings.LOGGING)

    def test_log_level_consistency(self):
        """
        Since LOG_LEVEL is derived at settings import time, verify the dict uses
        settings.LOG_LEVEL consistently rather than the current DEBUG flag.
        """
        cfg = settings.LOGGING
        expected = settings.LOG_LEVEL

        self.assertEqual(cfg["handlers"]["console"]["level"], expected)
        self.assertEqual(cfg["loggers"]["core"]["level"], expected)
        self.assertEqual(cfg["loggers"]["django"]["level"], expected)
        self.assertEqual(cfg["root"]["level"], expected)