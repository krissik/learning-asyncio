# https://pymotw.com/3/asyncio/subprocesses.html

import asyncio
import functools


async def run_df(loop):
    print('in run_df')
    cmd_done = asyncio.Future(loop=loop)
    factory = functools.partial(DFProtocol, cmd_done)
    proc = loop.subprocess_exec(
        factory,
        'df', '-hl',
        stdin=None,
        stderr=None,
    )

    try:
        print('launching process')
        transport, protocol = await proc
        print('waiting for process to complete')
        await cmd_done
    finally:
        transport.close()

    return cmd_done.result()


class DFProtocol(asyncio.SubprocessProtocol):
    FD_NAMES = ['stdin', 'stdout', 'stderr']

    def __init__(self, done_future):
        self.done = done_future
        self.buffer = bytearray()
        super().__init__()

    def connection_made(self, transport):
        # is invoked when the input channels to the new process are set up
        print('process started {}'.format(transport.get_pid()))
        self.transport = transport

    def pipe_data_received(self, fd, data):
        # when the process has generated output
        print('read {} bytes from {}'.format(len(data), self.FD_NAMES[fd]))
        if fd == 1:
            self.buffer.extend(data)

    def process_exited(self):
        # called when the process terminates
        print('process exited')
        return_code = self.transport.get_returncode()
        print('return code {}'.format(return_code))
        if not return_code:
            cmd_output = bytes(self.buffer).decode()
            results = self._parse_results(cmd_output)
        else:
            results = []
        self.done.set_result((return_code, results))

    def _parse_results(self, output):
        print('parsing results')
        # Output has one row of headers, all single words
        # The remaining rows are one per filesystem, with colums
        # matching the headers (assuming that none of the mount points
        # have whitespace in the names)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # LANGUAGE has to be en_EN => `export LANGUAGE=en_EN`
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if not output:
            return []
        lines = output.splitlines()
        headers = lines[0].split()
        devices = lines[1:]
        result = [
            dict(zip(headers, line.split()))
            for line in devices
        ]
        return result

event_loop = asyncio.get_event_loop()
try:
    return_code, results = event_loop.run_until_complete(
        run_df(event_loop)
    )
    print('run df finished')
finally:
    event_loop.close()

if return_code:
    print('error exit {}'.format(return_code))
else:
    print(' ### df output ###')
    print('\nFree space:')
    for r in results:
        print('{Mounted:25}: {Avail}'.format(**r))


