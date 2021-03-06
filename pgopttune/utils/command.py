import subprocess
import os
import sys
import logging
import traceback
import shlex

logger = logging.getLogger(__name__)


def run_command(cmd_str, stdin=None, stdout_devnull=False):
    """
    run command
    """
    cmd = shlex.split(cmd_str)
    try:
        if stdout_devnull: # for pg_ctl command
            with open(os.devnull, 'w') as devnull:
                res = subprocess.run(cmd, stdout=devnull)
        else:
            res = subprocess.run(cmd, check=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=stdin)
    except subprocess.CalledProcessError as e:
        logger.critical(traceback.format_exc())
        logger.info('Command: {} '.format(cmd_str))
        logger.info('Stdout: {}'.format(e.stdout.decode("utf8")))
        logger.info('Stderr: {}'.format(e.stderr.decode("utf8")))
        sys.exit(1)
    return res


if __name__ == "__main__":
    result1 = run_command('ls -l /tmp')
    print(result1.stdout.decode("utf8"))
    result2 = run_command('ls -l 4312aaaa')
    print(result2.stdout.decode("utf8"))
