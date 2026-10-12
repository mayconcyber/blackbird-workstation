import argparse
import json
from .network import collect_snapshot


def main():
    parser = argparse.ArgumentParser(description='BLACKBIRD Workstation')
    parser.add_argument('--snapshot', action='store_true', help='Consultar rede local sem abrir a interface')
    args = parser.parse_args()
    if args.snapshot:
        try:
            print(json.dumps(collect_snapshot(), ensure_ascii=False, indent=2))
        except (RuntimeError, ValueError) as exc:
            parser.exit(1, str(exc) + '\n')
    else:
        from .ui import run
        run()


if __name__ == '__main__':
    main()
