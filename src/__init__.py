import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s: %(message)s")
handler.setFormatter(formatter)
LOG.addHandler(handler)
