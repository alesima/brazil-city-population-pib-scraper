# Brazil Cities Population and PIB Scraper

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-0.84.2-orange?style=for-the-badge&logo=streamlit)
![Poetry](https://img.shields.io/badge/Poetry-1.1.13-brightgreen?style=for-the-badge&logo=poetry)

This project is a scraper for Brasil cities population and PIB (Gross Domestic Product) data. It provides three modes of operation: dashboard, seed, and update.

## Features

- **Dashboard**: A visual interface to display the scraped data.
- **Seeder**: A tool to seed the initial data.
- **Updater**: A tool to update the existing data.

## Requirements

- Python 3.7+
- Streamlit (for dashboard mode)
- Poetry (for dependency management)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/alesima/brazil-city-population-pib-scraper.git
    cd brazil-city-population-pib-scraper
    ```

2. Install Poetry if you haven't already:
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. Install the required dependencies using Poetry:
    ```sh
    poetry install
    ```

## Usage

### Dashboard Mode

To run the dashboard, you need to use Streamlit. Make sure Streamlit is installed and then run the script with the `dashboard` mode:

```sh
poetry run streamlit run main.py -- --mode dashboard
```

### Seeder Mode

To seed the initial data, run the script with the `seed` mode:

```sh
poetry run python main.py --mode seed
```

You can enable verbose logging by adding the `--verbose` flag:

```sh
poetry run python main.py --mode seed --verbose
```

### Updater Mode

To update the existing data, run the script with the `update` mode:

```sh
poetry run python main.py --mode update
```

## Arguments

- `-v`, `--verbose`: Enable verbose logging.
- `--mode`: Choose the mode to run: `dashboard`, `seed`, or `update` (default: `dashboard`).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact [alexe@codingwithalex.com](mailto:alex@codingwithalex.com).

---

Made with ❤️ by [Alex Silva](https://github.com/alesima)
