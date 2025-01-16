import os
import sys
import argparse
import importlib

from dotenv import load_dotenv

__prog__ = "Dumb Badge(s) Remover"
__prg__ = "DBR"
__desc__ = "Removes Roblox badges very quickly"
try:
    __version__ = importlib.metadata.version(__package__ or __name__)
except:
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
    parser.add_argument("--file", type=argparse.FileType('r'), default=None,
                        help="Filename path with 'https://roblox.com/[TYPE]/[ID]' urls.")
    parser.add_argument("--badge", "-b", type=int, default=None, metavar="BADGE_ID",
                        help="Specify a badge ID.")
    parser.add_argument("--place", "-p", type=int, default=None, metavar="PLACE_ID",
                        help="Specify a place ID.")
    parser.add_argument("--user", "-u", type=int, default=None, metavar="USER_ID",
                        help="Specify a user ID.")
    parser.add_argument("--group", "-g", "--community", type=int, default=None, metavar="GROUP_ID",
                        help="Specify a group / community ID.")


    # related to roblox account authentication
    parser.add_argument("--env-file", "-e", default=None,  # type=argparse.FileType("w"),
                        help=f"An .env file allows you to specify settings (the below options) for {parser.prog} to follow without cluttering the terminal or risking important tokens. More information on .env files can be found in the README.")
    parser.add_argument("--rbx-token", "-t", default=None,
                        help=".ROBLOSECURITY token. By using this option, you agree that this is your unique token and not anyone else's. DO NOT SHARE YOUR ROBLOX TOKEN WITH ANYONE! More info can be found here: https://ro.py.jmk.gg/dev/tutorials/roblosecurity/")


    # parser.add_argument("--seconds", "-s", type=int, default=-1,
    #                     help="How many seconds before killing the Roblox process. Setting to -1 (default) disables the timer.")

    # parser.add_argument("--verbose", "-v", action="store_true",
    #                     help="Verbose mode. Prints out things to help with debugging.")


    # related to downloading lists
    parser.add_argument("--download-mgs-invalid-list", action="store_true",
                        help="Download MetaGamerScore's list of Roblox games that were detected as problematic. May contain games that are not considered spam, so use with caution.")


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

    if args.download_mgs_invalid_list:
        from .modules.download import download_mgs_invalid_games
        download_mgs_invalid_games()
        sys.exit(0)

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

    from dbr.modules import data_save

    if all(val is None for val in [args.rbx_token, args.env_file]):
        parser.error("the following arguments are required to continue: --rbx-token or --env-file containing `RBX_TOKEN`.")

    if all(val is None for val in [args.file, args.user, args.group, args.place, args.badge]):
        parser.error("the following arguments are required to continue: --file, --user, --group, --place or --badge")

    # if requested, download game list from mgs
    from dbr.modules import remover
    if remover.init(user_agent, rbx_token) is False:
        sys.exit(1)

    data_save.init(root_folder=args.cache_directory)

    if args.badge is not None:
        remover.delete_badge(args.badge)
    if args.place is not None:
        remover.delete_from_game(args.place)
    if args.group is not None:
        remover.delete_from_group(args.group)
    if args.user is not None:
        remover.delete_from_player(args.user)
    if args.file is not None:
        lines = []
        lines = args.file.readlines()
        args.file.close()
        if lines == []:
            parser.error("text file is empty")
        remover.delete_from_text_file(lines)


if __name__ == "__main__":
    main()
