import coloredlogs, logging


# Create a logger object.
def get_colour_logs():
    mylogs = logging.getLogger(__name__)

    log_format = "%(asctime)s [%(levelname)s] ~ [%(filename)s > %(funcName)s() > %(lineno)s] ~ %(message)s"

    logging.basicConfig(
        filename="logs.txt", encoding="utf-8", level=logging.ERROR, format=log_format
    )

    fieldstyle = {
        "asctime": {"color": "green"},
        "levelname": {"bold": True, "color": "black"},
        "filename": {"color": "cyan"},
        "funcName": {"color": "blue"},
    }

    levelstyles = {
        "critical": {"bold": True, "color": "red"},
        "debug": {"color": "green"},
        "error": {"color": "red"},
        "info": {"color": "magenta"},
        "warning": {"color": "yellow"},
    }

    coloredlogs.install(
        level=logging.CRITICAL,
        logger=mylogs,
        fmt=log_format,
        datefmt="%H:%M:%S",
        field_styles=fieldstyle,
        level_styles=levelstyles,
    )

    return mylogs


# mylogs.debug("This is debug")
# mylogs.info("This is info")
# mylogs.warning("This is warning")
# mylogs.error("This is an error")
# mylogs.critical("This is a critical message")
