# PropAlphaEvalSolver

Prop trading accounts are essentially path-dependent call options. The player/customer
purchases a game with limited downside (i.e. the combine/Eval cost and funded account costs)
and theoretically uncapped upside. Not every path with the same terminal account value
is an admissible path (due to drawdown rules etc) and therefore the option payout is path-
dependent. Pricing this option thus necessitates a monte carlo simulation of the possible
account paths.

PropAlphaEvalSolver is a simulation tool for estimating the expected full payout 
of a trading strategy on a prop account. This tool is designed to work with 
a single trading setup, considering specific parameters such as a defined order 
bracket, known win percentage, and average maximum favorable excursion (MFE). It 
factors in costs and rules of the prop trading account. The front-end is powered 
by Streamlit. Created by Prop Alpha (www.prop-alpha.com) in collaboration with 
[vespatrades](https://github.com/vespatrades).


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contribute](#contribute)
- [License](#license)

## Installation

1. Clone the repo:
   ```
   git clone https://github.com/Prop-Alpha/PropAlphaEvalSolver.git
   ```

2. Navigate to the directory:
   ```
   cd PropAlphaEvalSolver
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```

## Usage

After running the Streamlit app, users will be presented with an interface
where they can input their strategy's parameters, initiate the Monte Carlo
simulation, and retrieve the results.


## Contribute

We welcome contributions from the community! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and submit a pull request.

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>

