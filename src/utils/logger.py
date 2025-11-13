import logging
from doctest import debug

root = logging.getLogger('Informações')
logging.basicConfig(level=logging.DEBUG)
root.info('OI')
