#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket;
import subprocess;
import logging;
import traceback;

logger = logging.getLogger("dynascii").getChild(__name__);

def Shell(pipeshell : str, *args, **kwargs):

    def run(conn, addr) -> None:
        logger.info('Running pipe shell...');
        try:
            _proc = subprocess.Popen(
                pipeshell,
                stdin = subprocess.DEVNULL,
                stdout = subprocess.PIPE,
                stderr = subprocess.DEVNULL,
                shell=True
            );
            _pipe = _proc.stdout;
        except Exception as err:
            conn.close();
            _proc = None;
            _pipe = None;
            logger.debug(err);
            logger.debug(traceback.format_exc());
            logger.critical('Shell start failed.');
            return;
        try:
            _chrs = b'\x00';
            #self.conn.send(b'\033[0;33m');
            while _proc.poll() == None and _chrs != b'':
                _chrs = _pipe.read(1);
                conn.send(_chrs);
            conn.shutdown(socket.SHUT_RDWR);
            _pipe.close();
            _proc.kill();
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError) as err:
            conn.close();
            _pipe.close();
            _proc.kill();
            logger.info('User connection aborted.');
        except Exception as err:
            conn.close();
            _pipe.close();
            _proc.kill();
            logger.error(err);
            logger.debug(traceback.format_exc());
            logger.critical('Shell failed.');
        logger.info('User ended.');
        return;

    for arg in args:
        logger.warning('Unrecognized arg : %s' % arg);
    for key in kwargs:
        logger.warning("Unrecognized arg : %s : %s" % (key, kwargs[key]));
    return run;
