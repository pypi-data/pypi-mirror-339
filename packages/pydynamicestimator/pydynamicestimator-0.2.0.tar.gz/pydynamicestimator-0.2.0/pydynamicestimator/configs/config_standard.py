# Created: 2024-12-01
# Last Modified: 2025-04-05
# (c) Copyright 2024 ETH Zurich, Milos Katanic
# https://doi.org/10.5905/ethz-1007-842
#
# Licensed under the GNU General Public License v3.0;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     https://www.gnu.org/licenses/gpl-3.0.en.html
#
# This software is distributed "AS IS", WITHOUT WARRANTY OF ANY KIND,
# express or implied. See the License for specific language governing
# permissions and limitations under the License.
#

# The code is based on the publication: Katanic, M., Lygeros, J., Hug, G.: Recursive dynamic state estimation for power systems with an incomplete nonlinear DAE model.
# IET Gener. Transm. Distrib. 18, 3657–3668 (2024). https://doi.org/10.1049/gtd2.13308
# The full paper version is available at: https://arxiv.org/abs/2305.10065v2
# See full metadata at: README.md
# For inquiries, contact: mkatanic@ethz.ch


from pydynamicestimator.config import Config
from pathlib import Path
import os

base_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent

config = Config(
    # *******************The excel parameters for the simulation/estimation***************
    testsystemfile=base_dir / 'data' / 'IEEE39_bus',
    fn=50,  # only tested for 50
    Sb=100,  # parameters in .txt table are assumed to be given for 100 MW
    # #########General input data##################
    ts=0.005,  # Simulation time step
    te=0.02,  # Estimation time step
    T_start=0.0,  # It has to be 0.0
    T_end=15.0,
    # integration ('trapezoidal' or 'backward')
    int_scheme='backward',
    # ###initialize estimation##########
    init_error_diff=1,  # 1 = 10%
    init_error_alg=True,  # 1 = flat start; 0 = true values
    # #########Plot###############
    plot=False,
    plot_voltage=False,
    plot_diff=False,
    proc_noise_alg=1e-3,
    proc_noise_diff=1e-4,
)
