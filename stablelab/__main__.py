import argparse,json,sys
from .core import analyze
from .oracle import verify
from .equivalence import compare
from .equivalence_oracle import verify_comparison


def main():
    p=argparse.ArgumentParser(description='Finite normal-program stable-model evidence')
    p.add_argument('command',choices=['analyze','verify','compare','verify-comparison']);p.add_argument('path');args=p.parse_args()
    try:
        with open(args.path,encoding='utf-8') as f:data=json.load(f)
        print(json.dumps({'analyze':analyze,'verify':verify,'compare':compare,'verify-comparison':verify_comparison}[args.command](data),indent=2,allow_nan=False))
    except (OSError,ValueError,TypeError,KeyError) as e:
        print(str(e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
