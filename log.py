import logging


def setup(debug=False):
    logging.basicConfig(
        format=(u'%(asctime)s %(levelname)-8s [%(name)s] %(message)s')
    )
    root_logger = logging.getLogger()

    if debug is True:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    # add_sentry_handler(root_logger)

    for l in ['requests', 'urllib3', 'sh']:
        log = logging.getLogger(l)
        log.setLevel(logging.WARN)

    for l in ['peewee', 'huey', 'PIL']:
        log = logging.getLogger(l)
        log.setLevel(logging.INFO)