# MIT Pokerbots 2024 Engine
MIT Pokerbots engine and skeleton bots in Python, Java, and C++.

The command to run the engine is `python3 engine.py`. The engine is configured via `config.py`.

## Dependencies
 - python>=3.12
 - cython (pip install cython)
 - eval7 (pip install eval7)
 - Java>=8 for java_skeleton
 - C++17 for cpp_skeleton
 - boost for cpp_skeleton (`sudo apt install libboost-all-dev`)
 - fmt for cpp_skeleton

## Linting
Use pylint.

## Notes
- The current version on the server is in bot_version_1
- The current developing version in bot_version_3
- Bot_version_1 is currently the best

## Ideas to develop:
- A script to generate data from the game logs after playing on the server.
- A strategy that considers the action of the opponent as currently, bot_version_1 does not play according to the opponent's action.
- Functions to predict opponent's cards. For example, based on the dealt card, calculate the change for the opponent to have a better hand. 


