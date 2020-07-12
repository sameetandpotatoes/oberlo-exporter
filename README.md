# README

This is an Oberlo exporter to export products to csv with their original Shopify link.

## Requirements / Usage

You need a chromedriver. Install on macOS with homebrew:

```
brew cask install chromedriver
```

For Windows, https://chromedriver.chromium.org/. Might be a problem because it's very version specific.

## Running the Script

Before running the script, you must copy `settings.json.template` over.

```
cp settings.json.template cp settings.json
```

Fill out settings.json with your Shopify credentials.

```
python main.py
```

## Output

Outputs to CSV
