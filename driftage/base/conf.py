import os
import logging

DRIFTAGE_LOG_LEVEL = os.environ.get("DRIFTAGE_LOG_LEVEL", "INFO")

def getLogger(name: str, level: str = DRIFTAGE_LOG_LEVEL):
    """[summary]

    :param name: [description]
    :type name: [str]
    :param level: [description]
    :type level: [str]
    """
    default_logger = logging.getLogger("driftage")
    logger = default_logger.getChild(name)
    logger.setLevel(level)
    return logger
