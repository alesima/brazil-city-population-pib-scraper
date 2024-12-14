import sys
import argparse
import asyncio
from src.dashboard import Dashboard
from src.seeder import Seeder
from src.updater import Updater


def main():
    parser = argparse.ArgumentParser(
        description="City Population and PIB Scraper")
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Enable verbose logging"
    )
    parser.add_argument(
        '--mode',
        choices=['dashboard', 'seed', 'update'],
        default='dashboard',
        help="Choose the mode to run: dashboard, seed or update (default: dashboard)"
    )

    args = parser.parse_args()

    if args.mode == 'dashboard':
        if 'streamlit' in sys.modules:
            dashboard = Dashboard()
            asyncio.run(dashboard.run())
        else:
            print(
                "Dashboard can only be run using Streamlit. Please run this script with Streamlit.")
    elif args.mode == 'seed':
        seeder = Seeder(verbose=args.verbose)
        asyncio.run(seeder.run())
    elif args.mode == 'update':
        updater = Updater()
        asyncio.run(updater.run())
    else:
        print("Invalid mode. Please choose 'dashboard', 'seed' or 'update'.")


if __name__ == "__main__":
    main()
