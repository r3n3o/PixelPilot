import logging

class LoggingConfig:
    def __init__(self):
        logging.basicConfig(filename='PixelPilot.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

