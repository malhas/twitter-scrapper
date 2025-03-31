import argparse
import pandas as pd
import os
from utils.TwitterGlavierAPI import TwitterGlavierAPI

EXCEPTIONS = "exceptions.csv"


PARSER = argparse.ArgumentParser()
PARSER.add_argument("-u", "--username", action="store", required=True, type=str)
PARSER.add_argument(
    "-r", "--request", choices=["followers", "following"], default="followers", action="store", type=str
)
PARSER.add_argument("-t", "--type", choices=["nonverified", "verified", "all"], default="all", action="store", type=str)
PARSER.add_argument("-c", "--cursor", action="store", type=str)
PARSER.add_argument(
    "-a",
    "--api",
    choices=["twitter_glavier"],
    default="twitter_glavier",
    action="store",
    type=str,
)
PARSER.add_argument("-s", "--supplier", action="store", choices=["rapidapi", "jojapi"], default="rapidapi", type=str)
ARGS = PARSER.parse_args()


def main():
    if os.path.exists(EXCEPTIONS):
        exceptions = pd.read_csv(EXCEPTIONS)["Handle"].to_list()
    else:
        exceptions = []
    if ARGS.api == "twitter_glavier":
        twitter_api = TwitterGlavierAPI(supplier=ARGS.supplier)

    username = ARGS.username
    if ARGS.cursor is not None:
        cursor = ARGS.cursor
    else:
        cursor = None
    if ARGS.request == "followers":
        accounts = twitter_api.get_followers(username, cursor)
    elif ARGS.request == "following":
        accounts = twitter_api.get_following(username, cursor)

    if ARGS.type == "nonverified":
        accounts = accounts[accounts.is_blue_verified == False]
    elif ARGS.type == "verified":
        accounts = accounts[accounts.is_blue_verified == True]

    accounts_clean = pd.DataFrame(columns=accounts.columns)

    if len(exceptions) > 0:
        accounts_clean = accounts[~accounts["screen_name"].isin(exceptions)]
    else:
        accounts_clean = accounts.copy()

    accounts_clean["x_link"] = accounts_clean["screen_name"].apply(lambda x: f"https://x.com/{x}")

    exceptions += accounts_clean["screen_name"].to_list()
    df = pd.DataFrame(exceptions, columns=["Handle"])
    df.to_csv(EXCEPTIONS, index=False)
    accounts_clean.to_csv(f"{ARGS.username}_{ARGS.request}.csv", index=False)


if __name__ == "__main__":
    main()
