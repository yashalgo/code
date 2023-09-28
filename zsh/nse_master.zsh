#!/usr/bin/env zsh
source ~/.zshrc

# Change directory to the desired path
cd /Users/yash/Desktop/Trading/code
source /Users/yash/Desktop/Trading/code/env/bin/activate

/opt/homebrew/bin/python3 -m trading.exch.nse_master

