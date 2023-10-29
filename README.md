# PropAlphaEvalSolver

PropAlphaEvalSolver is a simulation tool for estimating the expected full payout 
of a trading strategy on a prop account. This tool is designed to work with 
a single trading setup, considering specific parameters such as a defined order 
bracket, known win percentage, and average maximum favorable excursion (MFE). It 
factors in costs and rules of the prop trading account. The front-end is powered 
by Streamlit.

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

