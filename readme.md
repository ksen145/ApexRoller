# Apex Roller

## Introduction

This program enables four participants to take turns forming groups of three. It guarantees that any participant excluded from the current group will be automatically included in the next iteration.

## How It Works

### First Round
1. User enters four names into input fields
2. Program randomly selects three names from the four
3. One name remains unselected

### Subsequent Rounds
1. The name excluded from the previous round is automatically included
2. One name is randomly excluded from the three selected in the previous round
3. New group is formed from the guaranteed name and two randomly selected names

## Functionality

- **Roll** Button:
  - Performs random selection
  - Locks input fields after first use
  - Displays results in history log with color coding:
    - 🟢 Green - selected names
    - 🔴 Red - excluded name

- **Reset** Button:
  - Unlocks input fields
  - Clears results history
  - Allows starting with new set of names

## Installation & Setup

1. Activate virtual environment using Poetry:
```bash
poetry shell