from dotenv import load_dotenv
from importlib import metadata
import argparse
import os
import sys

from .modules import data_save

__prog__ = "Dumb Badge(s) Remover"
__prg__ = "DBR"
__desc__ = "Removes Roblox badges very quickly"
try:
    __version__ = metadata.version(__package__ or __name__)
except metadata.PackageNotFoundError:
    __version__ = "dev"  # fallback version
__author__ = "exurd"
__copyright__ = "copyright (c) 2025, exurd"
__credits__ = ["exurd"]
__license__ = "MIT"
__long_license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
    base_cache_path = os.path.dirname(sys.executable)
else:
    base_path = os.getcwd()
    base_cache_path = os.getcwd()


def get_parser() -> argparse.ArgumentParser:
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser(
        prog=__prog__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__desc__,
        epilog=__long_license__
    )
    version = "%(prog)s " + __version__
    parser.add_argument("--version", action="version", version=version)

    # related to input
    parser.add_argument("--file", type=str, default=None,
                        help="Filename path with 'https://roblox.com/[TYPE]/[ID]' urls you want gone from your account.")
    parser.add_argument("--badge", "-b", type=int, default=None, metavar="BADGE_ID",
                        help="Specify a badge ID you want gone from your account.")
    parser.add_argument("--place", "-p", type=int, default=None, metavar="PLACE_ID",
                        help="Specify a place ID you want gone from your account.")
    parser.add_argument("--user", "-u", type=int, default=None, metavar="USER_ID",
                        help="Specify a user ID you want gone from your account.")
    parser.add_argument("--group", "-g", "--community", type=int, default=None, metavar="GROUP_ID",
                        help="Specify a group / community ID you want gone from your account.")
    parser.add_argument("--mgs-id", type=int, default=None, metavar="MGS_ID",
                        help="Specify a MetaGamerScore game ID you want gone from your account.")

    # related to roblox account authentication
    parser.add_argument("--env-file", "-e", default=None,  # type=argparse.FileType("w"),
                        help=f"""An .env file allows you to specify settings
                              (the below options) for {parser.prog} to follow
                              without cluttering the terminal or risking
                              important tokens. More information on .env files
                              can be found in the README.""")
    parser.add_argument("--rbx-token", "-t", default=None,
                        help=""".ROBLOSECURITY token. By using this option, you
                             agree that this is your unique token and not anyone
                             else's. DO NOT SHARE YOUR ROBLOX TOKEN WITH ANYONE!
                             More info can be found here:
                             https://ro.py.jmk.gg/dev/tutorials/roblosecurity/""")

    # related to downloading lists
    parser.add_argument("--download-mgs-invalid-list", action="store_true",
                        help="""Download MetaGamerScore's list of Roblox games
                             that were detected as problematic. May contain
                             games that are not considered spam, so use with
                             caution.""")
    parser.add_argument("--download-badge-spam-lists", action="store_true",
                        help="""Download text files from exurd/badge-spam-lists;
                             a bunch of text files containing place IDs from
                             various Roblox badge chains.""")

    # related to inventory scanning
    parser.add_argument("--check-inventory", "-c", type=int, default=None, metavar="USER_ID",
                        help="""Checks a user's inventory for spam badges. DOES
                             NOT DELETE BADGES. Requires a list of place IDs to
                             check (use download arguments above).""")

    # misc.
    parser.add_argument("--cache-directory", "-cd", default=os.path.join(base_cache_path, "dbr_cache"),
                        help="The directory where cache data is kept.")

    parser.add_argument("--user-agent", "-ua", default=f"{__prg__}/{__version__}",
                        help="Sets the user agent for requests made by the program.")

    parser.description += f"\n\nThere are {str(len(parser._actions) - 1)} arguments available."

    return parser


def load_env_file(filename) -> dict:
    """
    Loads env file from a filename and puts data found into dict.
    """
    # env_loaded = False
    if os.path.isfile(filename):
        load_dotenv(filename)
        env_data = {}
        if os.getenv("RBX_TOKEN"):
            env_data["RBX_TOKEN"] = str(os.getenv("RBX_TOKEN"))
        if os.getenv("USER_AGENT"):
            env_data["USER_AGENT"] = str(os.getenv("USER_AGENT"))
        return env_data
    return {}


def main(args=None):
    """
    Main function for DBR.
    """
    parser = get_parser()
    args = parser.parse_args(args)

    print(f"{__prog__} {__version__}\n{__copyright__}\n")

    data_save.init(root_folder=args.cache_directory)

    # if requested, download spam lists
    if args.download_mgs_invalid_list:
        from .modules.metagamerscore import download_mgs_invalid_games
        download_mgs_invalid_games()
        sys.exit(0)
    if args.download_badge_spam_lists:
        from .modules.badge_spam_list import download_spam_lists
        download_spam_lists()
        sys.exit(0)

    if args.check_inventory:
        from .modules.spam_scanner import scan_inventory
        if scan_inventory(args.check_inventory):
            sys.exit(0)
        sys.exit(1)

    user_agent = args.user_agent
    rbx_token = args.rbx_token

    env_file = args.env_file
    if env_file is not None:
        print(f"Loading .env file [{args.env_file}]...")
        data = load_env_file(env_file)
        if rbx_token == parser.get_default("RBX_TOKEN"):
            if "RBX_TOKEN" in data and data["USER_AGENT"] != "":
                rbx_token = data["RBX_TOKEN"]
        if user_agent == parser.get_default("USER_AGENT"):
            if "USER_AGENT" in data and data["USER_AGENT"] != "":
                user_agent = data["USER_AGENT"]

    if all(val is None for val in [args.rbx_token, args.env_file]):
        parser.error("the following arguments are required to continue: --rbx-token or --env-file containing `RBX_TOKEN=`")

    if all(val is None for val in [args.file, args.user, args.group, args.place, args.badge, args.mgs_id]):
        parser.error("the following arguments are required to continue: --file, --user, --group, --place, --badge or --mgs-id")

    from .modules import remover
    if remover.init(user_agent, rbx_token) is False:
        print("Exiting.")
        sys.exit(1)

    if args.badge is not None:
        remover.delete_badge(args.badge)
    if args.mgs_id is not None:
        from .modules.metagamerscore import get_game_from_mgs_id
        place_id = get_game_from_mgs_id(args.mgs_id)
        if place_id:
            remover.delete_from_game(place_id)
    if args.place is not None:
        remover.delete_from_game(args.place)
    if args.group is not None:
        remover.delete_from_group(args.group)
    if args.user is not None:
        remover.delete_from_player(args.user)
    if args.file is not None:
        lines = []
        try:
            with open(args.file, mode="r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
        except UnicodeDecodeError:
            if ".txt.zst" in args.file:
                from .modules.badge_spam_list import zstd_extract_lines
                lines = zstd_extract_lines(args.file)
        except OSError as e:
            parser.error(e)
        if lines == []:
            parser.error("text file is empty or unreadable")

        remover.delete_from_text_file(lines)


if __name__ == "__main__":
    main()
