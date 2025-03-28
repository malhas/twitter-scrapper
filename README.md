# Twitter Follower/Following Scraper

A Python script to fetch and analyze Twitter/X followers and following data using the Twitter API through RapidAPI or JoJAPI.

## Prerequisites

-   Python 3.x
-   Required Python packages (install using `pip install -r requirements.txt`):
    -   python-dotenv
    -   pandas
    -   requests

## API Keys Setup

This script requires API keys from either RapidAPI or JoJAPI (or both).

### RapidAPI Setup

1. Create an account on [RapidAPI](https://rapidapi.com/)
2. Subscribe to the [Twitter135 API](https://rapidapi.com/Glavier/api/twitter135)
3. Copy your API key from your RapidAPI dashboard

### JoJAPI Setup

1. Create an account on [JoJAPI](https://jojapi.com)
2. Subscribe to their Twitter API service
3. Get your API key from your account dashboard

## Setup

1. Clone this repository:

```sh
git clone https://github.com/yourusername/twitter-scrapper.git
cd twitter-scrapper
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

3. Configure API keys:
    - Copy `.env_sample` to `.env`
    - Add your API keys in the `.env` file:

```
X-RapidAPI-Key="your_rapidapi_key"
X-JoJAPI-Key="your_jojapi_key"
```

## Usage

Basic command structure:

```sh
python twitterAPIrequest.py -u USERNAME [OPTIONS]
```

### Required Arguments

-   `-u`, `--username`: Target Twitter username to scrape

### Optional Arguments

-   `-r`, `--request`: Type of data to fetch
    -   `followers` (default)
    -   `following`
-   `-t`, `--type`: Filter accounts by verification status
    -   `all` (default)
    -   `verified`
    -   `nonverified`
-   `-c`, `--cursor`: Pagination cursor for large datasets
-   `-s`, `--supplier`: API provider to use
    -   `rapidapi` (default)
    -   `jojapi`
-   `-a`, `--api`: API implementation to use
    -   `twitter_glavier` (default)

### Examples

1. Get all followers of a user:

```sh
python twitterAPIrequest.py -u elonmusk
```

2. Get verified following of a user:

```sh
python twitterAPIrequest.py -u twitter -r following -t verified
```

3. Use JoJAPI instead of RapidAPI:

```sh
python twitterAPIrequest.py -u github -s jojapi
```

## Output

The script generates two files:

-   `{username}_{request}.csv`: Contains the fetched account data
-   `exceptions.csv`: Tracks previously fetched accounts to avoid duplicates

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
