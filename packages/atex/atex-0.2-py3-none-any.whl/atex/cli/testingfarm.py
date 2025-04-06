import sys
#from datetime import datetime

from .. import util
from .. import testingfarm as tf


def _get_api(args):
    api_args = {}
    if args.url:
        api_args['url'] = args.url
    if args.token:
        api_args['token'] = args.token
    return tf.TestingFarmAPI(**api_args)


def composes(args):
    api = _get_api(args)
    comps = api.composes(ranch=args.ranch)
    comps_list = comps['composes']
    for comp in comps_list:
        print(comp['name'])


def get_request(args):
    api = _get_api(args)
    request = tf.Request(args.request_id, api=api)
    request.update()
    print(str(request))


def search_requests(args):
    api = _get_api(args)
    reply = api.search_requests(
        state=args.state,
        mine=not args.all,
        ranch=args.ranch,
        created_before=args.before,
        created_after=args.after,
    )
    if not reply:
        return

    for req in sorted(reply, key=lambda x: x['created']):
        req_id = req['id']
        #created_utc = req['created'].partition('.')[0]
        #created_dt = datetime.fromisoformat(f'{created_utc}+00:00')
        #created = created_dt.astimezone().isoformat().partition('.')[0]
        created = req['created'].partition('.')[0]

        envs = []
        for env in req['environments_requested']:
            if 'os' in env and env['os'] and 'compose' in env['os']:
                compose = env['os']['compose']
                arch = env['arch']
                if compose and arch:
                    envs.append(f'{compose}@{arch}')
        envs_str = ', '.join(envs)

        print(f'{created} {req_id} : {envs_str}')
        #request = tf.Request(initial_data=req)
        #print(str(request))
    #request.update()
    #print(str(request))


def reserve(args):
    util.info(f"Reserving {args.compose} on {args.arch} for {args.timeout} minutes")

    api = _get_api(args)
    res = tf.Reserve(
        compose=args.compose,
        arch=args.arch,
        timeout=args.timeout,
        api=api,
    )
    with res as m:
        util.info(f"Got machine: {m}")
        util.subprocess_run([
            'ssh', '-q', '-i', m.ssh_key,
            '-oStrictHostKeyChecking=no', '-oUserKnownHostsFile=/dev/null',
            f'{m.user}@{m.host}',
        ])


def watch_pipeline(args):
    api = _get_api(args)
    request = tf.Request(id=args.request_id, api=api)

    util.info(f"Waiting for {args.request_id} to be 'running'")
    try:
        request.wait_for_state('running')
    except tf.GoneAwayError:
        util.info(f"Request {args.request_id} already finished")
        return

    util.info("Querying pipeline.log")
    try:
        for line in tf.PipelineLogStreamer(request):
            sys.stdout.write(line)
            sys.stdout.write('\n')
    except tf.GoneAwayError:
        util.info(f"Request {args.request_id} finished, exiting")


def parse_args(parser):
    parser.add_argument('--url', help='Testing Farm API URL')
    parser.add_argument('--token', help='Testing Farm API auth token')
    cmds = parser.add_subparsers(
        dest='_cmd', help="TF helper to run", metavar='<cmd>', required=True,
    )

    cmd = cmds.add_parser(
        'composes',
        help="list all composes available on a given ranch",
    )
    cmd.add_argument('ranch', nargs='?', help="Testing Farm ranch (autodetected if token)")

    cmd = cmds.add_parser(
        'get-request', aliases=('gr',),
        help="retrieve and print JSON of a Testing Farm request",
    )
    cmd.add_argument('request_id', help="Testing Farm request UUID")

    cmd = cmds.add_parser(
        'search-requests', aliases=('sr',),
        help="return a list of requests matching the criteria",
    )
    cmd.add_argument('--state', help="request state (running, etc.)", required=True)
    cmd.add_argument('--all', help="all requests, not just owned by token", action='store_true')
    cmd.add_argument('--ranch', help="Testing Farm ranch")
    cmd.add_argument('--before', help="only requests created before ISO8601")
    cmd.add_argument('--after', help="only requests created after ISO8601")

    cmd = cmds.add_parser(
        'reserve',
        help="reserve a system and ssh into it",
    )
    cmd.add_argument('--compose', '-c', help="OS compose to install", required=True)
    cmd.add_argument('--arch', '-a', help="system HW architecture", default='x86_64')
    cmd.add_argument('--timeout', '-t', help="pipeline timeout (in minutes)", type=int, default=60)
    cmd.add_argument('--ssh-key', help="path to a ssh private key file like 'id_rsa'")

    cmd = cmds.add_parser(
        'watch-pipeline', aliases=('wp',),
        help="continuously output pipeline.log like 'tail -f'",
    )
    cmd.add_argument('request_id', help="Testing Farm request UUID")


def main(args):
    if args._cmd == 'composes':
        composes(args)
    elif args._cmd in ('get-request', 'gr'):
        get_request(args)
    elif args._cmd in ('search-requests', 'sr'):
        search_requests(args)
    elif args._cmd == 'reserve':
        reserve(args)
    elif args._cmd in ('watch-pipeline', 'wp'):
        watch_pipeline(args)
    else:
        raise RuntimeError(f"unknown args: {args}")


CLI_SPEC = {
    'aliases': ('tf',),
    'help': "various utils for Testing Farm",
    'args': parse_args,
    'main': main,
}
