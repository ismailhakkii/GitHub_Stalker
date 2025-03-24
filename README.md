# GitHub Follower Analyzer

A tool for analyzing GitHub follow relationships without requiring API access.

## Features

* Lists followers and following users
* Identifies users not following you back
* Identifies users you don't follow back
* Identifies mutual follows
* Exports results to CSV/Excel

## Requirements

```
pip install requests beautifulsoup4 pandas
```

## Usage

```
python github_follower_analyzer.py
```

Enter your GitHub username when prompted and view the analysis results. Option to save results as CSV/Excel is available.

## Notes

* May require updates if GitHub's page structure changes
* Excessive usage may lead to temporary IP restrictions by GitHub

## Purpose

This tool simplifies the process of identifying discrepancies in GitHub follow relationships, eliminating the need for manual checking.
