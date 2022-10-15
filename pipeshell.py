#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket;
import subprocess;
import logging;
import traceback;

logger = logging.getLogger("dynascii").getChild(__name__);

def Shell(pipeshell : str, *args, **kwargs):

    logger.debug("Initing Pipe Shell...");
    def run(conn, addr) -> None:
        logger.info('Running pipe shell...');
        try:
            logger.debug("Opening piped shell process...");
            _proc = subprocess.Popen(
                pipeshell,
                stdin = subprocess.DEVNULL,
                stdout = subprocess.PIPE,
                stderr = subprocess.DEVNULL,
                shell=True
            );
            _pipe = _proc.stdout;
            logger.debug("Opened piped shell process.");
        except Exception as err:
            logger.debug("Opening piped shell process failed.");
            conn.close();
            _proc = None;
            _pipe = None;
            logger.debug(err);
            logger.debug(traceback.format_exc());
            logger.critical('Shell start failed.');
            return;
        try:
            logger.debug("Sending piped output...");
            _len = 0;
            _chrs = b'\x00';
            #self.conn.send(b'\033[0;33m');
            while _proc.poll() == None and _chrs != b'':
                _chrs = _pipe.read(1);
                _len += 1;
                conn.send(_chrs);
                if (_len % 1024 * 4):
                    logger.debug("Sended piped output of %d k bytes." % (_len // 1024));
            logger.debug("Sending piped output done.");
            logger.debug("Closing piped output...");
            conn.shutdown(socket.SHUT_RDWR);
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError) as err:
            logger.info('User connection aborted.');
        except Exception as err:
            logger.error(err);
            logger.debug(traceback.format_exc());
            logger.critical('Shell failed.');
        finally:
            logger.debug("Closing pipe...");
            conn.close();
            _pipe.close();
            _proc.kill();
            logger.debug("Closed pipe.");
        logger.info('User ended.');
        return;

    for arg in args:
        logger.warning('Unrecognized arg : %s' % arg);
    for key in kwargs:
        logger.warning("Unrecognized arg : %s : %s" % (key, kwargs[key]));
    logger.debug("Inited Pipe Shell.");
    return run;
