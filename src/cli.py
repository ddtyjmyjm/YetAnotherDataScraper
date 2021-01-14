from src import config, manage
import argparse


def parse_args(args=None):
    """Parsing args. Explict 'args' argument for testing."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('-r', '--resource')
    return parser.parse_args(args)


def main():
    """
    Grating
    """
    print('YADS')

    args = parse_args()

    config_file = None
    if args.config:
        config_file = args.config
    config_f = config.Config(config_file)

    if args.resource:
        config_f.resource_folder = (lambda: args.resource)

    manage_f = manage.Manage(config_f)
    manage_f.manage_main_mode()


if __name__ == '__main__':
    main()
