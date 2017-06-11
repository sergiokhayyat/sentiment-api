#!/usr/bin/env python3

import connexion
import json
import os
import logging
import sys

# Define logger
LOGGER = logging.getLogger(__name__)

if __name__ == '__main__':
    # Launch app
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'Sentiment Analysis API powered by Machine Box'})
    app.run(port=80, debug=(os.getenv('DEBUG')=='true'))
