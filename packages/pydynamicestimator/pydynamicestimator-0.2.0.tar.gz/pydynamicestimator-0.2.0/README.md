# PowerDynamicEstimator (pydynamicestimator)
**Version 0.2.0** released on 21.02.2025  
[DOI: 10.5905/ethz-1007-842](https://doi.org/10.5905/ethz-1007-842)

## About

PowerDynamicEstimator is a state estimation tool for power systems using a recursive dynamic state estimator based on an incomplete nonlinear DAE (Differential Algebraic Equations) model. The estimator combines dynamic evolution equations, algebraic network equations, and phasor measurements to recursively estimate dynamic and algebraic states. It is suitable for centralized power systems dynamic estimation, even when some component models are missing or unknown.

## Features

- Centralized recursive dynamic state estimation based on a nonlinear DAE power system model
- Works with missing or unknown component models
- Customizable Kalman filter settings easily configurable via a `./config.py` file for precise estimation
- Network topology and parameters and dynamic models easily editable via `./data` subfolder
- Supports integration with Phasor Measurement Units (PMUs) in `./measurements.py`
- User defined models can be integrated in `./devices` subfolder


## Citation

If you use PowerDynamicEstimator in your academic work, please cite the following paper:
- **Katanic, Milos, Lygeros, John, Hug, Gabriela**. "Recursive dynamic state estimation for power systems with an incomplete nonlinear DAE model." *IET Generation, Transmission & Distribution*, 18(22), 3657-3668, 2024.  
  DOI: [https://doi.org/10.1049/gtd2.13308](https://doi.org/10.1049/gtd2.13308)
```bibtex
@article{powerdynamicestimator,
  author = {Katanic, Milos and Lygeros, John and Hug, Gabriela},
  title = {Recursive dynamic state estimation for power systems with an incomplete nonlinear DAE model},
  journal = {IET Generation, Transmission \& Distribution},
  volume = {18},
  number = {22},
  pages = {3657-3668},
  keywords = {differential algebraic equations, Kalman filters, state estimation},
  doi = {https://doi.org/10.1049/gtd2.13308}, 
  url = {https://ietresearch.onlinelibrary.wiley.com/doi/abs/10.1049/gtd2.13308},
  eprint = {https://ietresearch.onlinelibrary.wiley.com/doi/pdf/10.1049/gtd2.13308},
  year = {2024}
}
```

The full version of the paper is available on [ArXiv](https://arxiv.org/abs/2305.10065v2).

## Installation

To get started with PowerDynamicEstimator, follow these steps:

1. **Clone the repository**:
```bash
git clone https://gitlab.nccr-automation.ch/mkatanic/powerdynamicestimator
```
```bash
cd PowerDynamicEstimator
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

## Documentation

The documentation follows the Sphinx standard and can be found by opening `./docs/build/html/index.html` from the root folder:

### Windows:
```bash
start docs/build/html/index.html
```
### Linux:
```bash
xdg-open docs/build/html/index.html
```
### macOS:
```bash
open docs/build/html/index.html
```


## Usage

### Running the Estimator

1. **Navigate to the root directory**:
    ```bash
    cd pydynamicestimator
    ```

2. **Run the main script**:
    ```bash
    python -m main
    ```
   


### Running the Estimator

The primary script `./main.py`. You can define the simulation and estimation settings in `./config.py`. System parameters are stored in the `./data` subfolder. Refer to the documentation for additional details.

## Important Notes

- **Injector Limitation**: Currently, the system supports only one injector per node due to initialization ambiguity. To handle multiple injectors per node, you can create a new node connected via a branch with very small impedance to simulate this behavior.

### Parameters

System dynamic and static parameters, including the topology, are specified in the `./data` subfolder. You can define the loads, generators, and their characteristics at specific nodes in the power system. Refer to the documentation for additional details.

Phasor Measurement Units (PMUs) used for estimation and their associated characteristics are defined in the file: `./data/.../est_param.txt`.

### Kalman Filter Settings

Adjust parameters related to the recursive state estimation process (e.g., noise covariance, initial error) in the `./config.py` file. Refer to the documentation for additional details.

## License

This software is licensed under the [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html).

## Contact
For any questions or if you desired to contribute to this project, please contact me at mkatanic@ethz.ch.
