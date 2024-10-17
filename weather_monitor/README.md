# Weather Monitoring Application

## Overview
This application monitors real-time weather conditions for various cities in India using the OpenWeatherMap API. It provides summarized insights, including daily temperature aggregates, dominant weather conditions, and alerting mechanisms for extreme temperatures.

## Features
- Fetches weather data for multiple cities at regular intervals.
- Calculates daily weather summaries, including average, maximum, and minimum temperatures.
- Generates visualizations of the weather summaries.
- Sends alerts if temperature thresholds are breached.

## Installation

### Prerequisites
- Python 3.8 or higher
- Internet connection to access the OpenWeatherMap API

### Dependencies
Install the necessary libraries using `pip`:
```bash
pip install requests schedule matplotlib
