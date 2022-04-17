# coding:utf-8
from loguru import logger

logger.add("./log/file_{time}.log", rotation="20 MB")


def logger_error(msg):
    logger.error(msg)


def logger_warning(msg):
    logger.warning(msg)


def logger_debug(msg):
    logger.debug(msg)


def logger_exception(msg):
    logger.exception(msg)


def logger_critical(msg):
    logger.critical(msg)


def logger_success(msg):
    logger.success(msg)


def logger_info(msg):
    logger.info(msg)


def logger_trace(msg):
    logger.trace(msg)
