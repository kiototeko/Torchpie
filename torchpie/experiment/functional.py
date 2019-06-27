import time
from argument.base import Args

def get_experiment_path(args: Args) -> Optional[str]:
    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())

    if args.experiment is None:
        if args.debug:
            experiment_path = os.path.join(
                'output', '{}_debug'.format(timestamp))
        else:
            experiment_path = os.path.join('output', timestamp)
    else:
        # No experiment path
        if args.experiment == '!default':
            return None
        else:
            experiment_path = args.experiment

    # Make sure path is only made once
    if args.local_rank == 0 and args.resume is None:
        os.makedirs(experiment_path)
    return experiment_path