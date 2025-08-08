import logging
import torch.distributed as dist
import os

def create_logger(logging_dir):
    """
    Create a logger that writes to a log file and stdout.
    """
    if dist.get_rank() == 0:  # real logger
        if os.path.exists(f"{logging_dir}/log.txt"):
            cur = 2
            while os.path.exists(f"{logging_dir}/log_{cur}.txt"):
                cur += 1
            log_file = f"{logging_dir}/log_{cur}.txt"
        else:
            log_file = f"{logging_dir}/log.txt"
        logging.basicConfig(
            level=logging.INFO,
            format='[\033[34m%(asctime)s\033[0m] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[logging.StreamHandler(), logging.FileHandler(log_file)]
        )
        logger = logging.getLogger(__name__)
    else:  # dummy logger (does nothing)
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.NullHandler())
    return logger