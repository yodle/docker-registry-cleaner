"""Primary functions for cleaning docker registry images

    untag: not implemented yet
    scrub: remove unused images
    revert: restore images if save_delete was used
    validate: check integrity of the registry
    report: report space usage

"""

import argparse
import sys
import pprint

try:
    from repository import Repository
except ImportError:
    from cleaner.repository import Repository


def pretty_print(data):
    """Pretty print a dict"""
    pprint.PrettyPrinter(indent=4).pprint(data)


def parse_args():
    """Parse commandline arguments for cleaner"""
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", help="the repository path")
    parser.add_argument("command", help="untag, validate, report, scrub, revert")
    parser.add_argument("--hostname", dest='hostname', nargs='*',
                        help="the registry hostname. Required for untag")

    parser.add_argument("--path", dest='path',
                        help="path to tmp directory to restore")
    args = parser.parse_args()
    # {'hostname': args.hostname,
    #  'command': args.command,
    #  'repository': args.repository}
    return args


def untag():
    """Remove unused tags - not yet implemented"""
    return True


def scrub(repo):
    """Remove unused images"""
    to_scrub = repo.unused_images()
    for img in to_scrub:
        repo.remove(img)
    return True


def revert(repo, path):
    """Revert clean from temp path if possible"""
    print(repo, path)
    repo.revert(path)
    return True


def validate(repo):
    """Verify the registry is in a valid state"""
    invalids = repo.validate()
    if invalids == set():
        print("The registry is in a valid state")
    else:
        print("The registry is in an invalid state. The following images are referenced but not present", invalids)
    return invalids


def report(repo):
    """Report disk usage for garbage images"""
    result = repo.report()
    print("The following images are unreferenced <image id: size on disk>:")
    pretty_print(result)
    return result


def main():
    """Entry for cli tool"""
    args = parse_args()
    print(args)
    repo = Repository(args.repository)

    if args.command == 'report':
        return report(repo)
    if args.command == 'validate':
        return validate(repo)
    if args.command == 'untag':
        return untag()
    if args.command == 'revert':
        path = args.path
        return revert(repo, path)
    if args.command == 'scrub':
        return scrub(repo)
    else:
        print("Invalid command %s" % args.command)
        sys.exit(1)
