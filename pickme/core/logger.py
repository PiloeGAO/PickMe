"""
    :package:   PickMe
    :file:      logger.py
    :brief:     Logger Management.
    :author:    PiloeGAO (Leo DEPOIX)
    :version:   0.0.1
"""
import os
import logging

from pickme.core.path import LOCAL_CONFIG_DIR

def get_logger(module_name="PickMe", debug=True):
    """Get the logger for PickMe.
    Args:
        module_name (str): Name of the module to log.
        debug (bool, optional): Enable debug logging. Defaults to True.
    Returns:
        :obj:`logging`: Logger to be used.
    """
    logger = logging.getLogger(module_name)
    
    if(not logger.handlers):
        # If logger isn't setup, create one.
        formatter = logging.Formatter(
            "PickMe | %(levelname)s - %(message)s @ [%(asctime)s] | %(pathname)s:%(lineno)d",
            "%y-%m-%d %H:%M:%S"
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        log_path = os.path.join(LOCAL_CONFIG_DIR, "logs.log")
        if(os.path.isfile(log_path)):
            os.remove(log_path)

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if(debug):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.debug("Logging system setup successfully.")
    
    return logger

def shutdown_logger():
    logging.shutdown()