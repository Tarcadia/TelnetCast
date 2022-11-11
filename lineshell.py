
import logging;

logger = logging.getLogger("dynascii").getChild(__name__);

def Shell(lines = [], *args, **kwargs):

    logger.debug("Initing Reject Shell...");

    def run(conn, addr) -> None:
        conn.send(b'\x1Bc\x1B[H');
        for line in lines:
            logger.info("Sending: %s" % line);
            conn.send((line+"\n\r").encode("utf8"));

    for arg in args:
        logger.debug('Unrecognized arg : %s' % arg);
    for key in kwargs:
        logger.debug("Unrecognized arg : %s : %s" % (key, kwargs[key]));
    logger.debug("Inited Line Shell.");
    return run;
