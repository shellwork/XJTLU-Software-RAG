import logging
import langchain
import os

log_verbose = False
langchain.verbose = False

LOG_FORMAT = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format = LOG_FORMAT)

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)