from src.Logger import logger
from src.Converter import Converter

import os

if not os.path.exists('output'):
    os.makedirs('output/')

if not os.path.exists('input'):
    logger.warn('Missing input folder.')
    os.makedirs('input/')    
    logger.info('Created input folder, place STF mod in so that manifest.json is at input/manifest.json')
    logger.info('Press enter to continue.')
    input()


converter = Converter()
converter.convert()

logger.success('Conversion complete!')
logger.info('See your converted mod in output/')