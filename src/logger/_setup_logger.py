import logging

import seqlog

from src.conf import LOG_LEVEL, SEQ_URL, is_dotenv_loaded


def setup_logger() -> None:
    logging.basicConfig(
        encoding="utf-8",
        level=LOG_LEVEL,
        filemode="w",
        format="%(name)s [%(asctime)s] %(levelname)s %(message)s",
    )
    logging.getLogger("httpcore").setLevel(
        logging.WARNING,
    )  # The minimal loglevel for this module when its logs are useful
    logging.getLogger("httpx").setLevel(logging.WARNING)

    if SEQ_URL:
        seqlog.log_to_seq(
            server_url=SEQ_URL,
            level=LOG_LEVEL,
            batch_size=10,
            auto_flush_timeout=10,
            override_root_logger=True,
            support_extra_properties=True,
            support_stack_info=True,
            use_clef=True,
        )
    else:
        logging.getLogger(__name__).warning("No SEQ_URL provided, logging to console")

    logger = logging.getLogger(__name__)
    logger.debug(
        "Config is set, env vars are loaded %s",
        "from file" if is_dotenv_loaded else "already",
    )
