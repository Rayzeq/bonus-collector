#!/bin/env python3

import argparse
import logging
from getpass import getpass
from time import sleep, time

from rbrapi import RocketBotRoyale
from rbrapi.errors import APIError, AuthenticationError, PasswordTooShortError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RocketBotRoyale bonus collector.")
    parser.add_argument("--email", type=str, help="Email for RocketBotRoyale account")
    parser.add_argument(
        "--password",
        type=str,
        help="Password for RocketBotRoyale account",
    )
    parser.add_argument(
        "--auto-open-crates",
        action="store_true",
        help="Automatically open crates if available",
    )
    return parser.parse_args()


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler.flush()

    return logger


def mainloop(
    logger: logging.Logger,
    email: str,
    password: str,
    *,
    auto_open_crates: bool,
) -> None:
    client = RocketBotRoyale(email, password)

    while True:
        try:
            client.collect_timed_bonus()
            logger.info("Coins collected successfully")
        except APIError:
            logger.info("Bonus not available yet")

        account_data = client.account()
        # print(account_data)
        coins = account_data.wallet["coins"]
        logger.info("Your coins now: %s", coins)

        if auto_open_crates and coins >= 1000:
            try:
                award = client.buy_crate()
                logger.info("Crate award is: %s", award.award_id)
            except APIError:
                logger.exception("Unable to open crates")

        last_collect = account_data.user["metadata"]["timed_bonus_last_collect"]

        while time() < last_collect + 30 * 60:
            sleep(60)


def main() -> None:
    args = parse_args()

    email = args.email if args.email else input("Enter email: ")
    password = args.password if args.password else getpass()

    logger = get_logger(__name__)

    while True:
        try:
            mainloop(logger, email, password, auto_open_crates=args.auto_open_crates)
        except AuthenticationError as e:  # noqa: PERF203
            if e.message != "Auth token invalid":
                logger.error("Unable to authenticate: %s", e.message)  # noqa: TRY400
                return
        except PasswordTooShortError as e:
            logger.error("Invalid password: %s", e.message)  # noqa: TRY400
            return
        except Exception:
            logger.exception("Unexpected exception")


if __name__ == "__main__":
    main()
