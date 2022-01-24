#!/usr/bin/env python3

import argparse
import os
import signal
from datetime import datetime

from isodate import parse_duration
from stomp import *


class FixityListener(ConnectionListener):
    def __init__(self, connection, client_id, fixity_dest, candidate_dest, age, max_messages=1, timeout=30):
        self.conn = connection
        self.client_id = client_id
        self.fixity_dest = fixity_dest
        self.candidate_dest = candidate_dest
        self.newest_allowed = datetime.now() - age
        self.max = max_messages
        self.timeout = timeout

        # set up handler for timeout
        def timeout_handler(_signum, _frame):
            self.stop_processing(f'No messages received in {self.timeout} seconds')

        signal.signal(signal.SIGALRM, timeout_handler)

        self.processed = 0
        self.done = False

    def stop_processing(self, reason):
        print('Stopping:', reason)
        self.conn.unsubscribe(self.client_id)
        self.done = True

    def on_connected(self, _headers, _body):
        print(f'Connected; timeout is {self.timeout} seconds')
        signal.alarm(self.timeout)

    def on_before_message(self, headers, _body):
        # pause alarm
        signal.alarm(0)
        # timestamp on the message is in milliseconds
        timestamp = float(headers['timestamp']) / 1000
        if datetime.fromtimestamp(timestamp) > self.newest_allowed:
            self.stop_processing('Next candidate has been fixity checked recently enough')
        elif self.processed >= self.max:
            self.stop_processing('Reached max messages to be processed in one session')

    def on_message(self, headers, body):
        # only process messages before we are done
        if not self.done:
            self.conn.ack(headers['message-id'], self.client_id)
            print(f'Fixity check candidate {self.processed + 1}:', headers['CamelFcrepoUri'])

            print('-> Sending to fixity checking:', self.fixity_dest)
            self.conn.send(self.fixity_dest, body=body, headers=headers)

            print('-> Sending to end of candidates list:', self.candidate_dest)
            # clear the old timestamp
            headers['timestamp'] = None
            self.conn.send(self.candidate_dest, body=body, headers=headers)

            self.processed += 1

            signal.alarm(self.timeout)


parser = argparse.ArgumentParser()
parser.add_argument(
    '--age', '-a',
    default='P3M',
    help='only process messages older than this age, expressed as an ISO8601 duration. Default is 3 months ("P3M")'
)
parser.add_argument(
    '--number', '-n',
    type=int,
    default=7000,
    help='maximum number of messages to process before exiting. Default is 7000'
)
parser.add_argument(
    '--server', '-s',
    default='127.0.0.1:61613',
    help='STOMP server IP address and port to connect to. Default is "127.0.0.1:61613"'
)
parser.add_argument(
    '--timeout', '-t',
    type=int,
    default=30,
    help='time in seconds to wait without receiving any messages before exiting. Default is 30'
)

args = parser.parse_args()
print('Configuration:', vars(args))

CLIENT_ID = 'nightlyfixity'

conn = Connection([tuple(args.server.split(':'))])
listener = FixityListener(
    conn,
    client_id=CLIENT_ID,
    fixity_dest='/queue/fedorafixity',
    candidate_dest='/queue/fixitycandidates',
    max_messages=args.number,
    age=parse_duration(args.age),
    timeout=args.timeout
)
conn.set_listener('', listener)
conn.start()
conn.connect()
conn.subscribe(
    '/queue/fixitycandidates',
    id=CLIENT_ID,
    ack='client',
    headers={'activemq.prefetchSize': 1}
)

while not listener.done:
    pass

conn.disconnect()
print('Processed', listener.processed, 'message(s)')
