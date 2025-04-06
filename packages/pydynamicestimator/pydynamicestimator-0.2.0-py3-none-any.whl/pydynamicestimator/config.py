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

from typing import Any
import os
from typing import Literal

from pydantic import BaseModel
from pathlib import Path

IntegrationSchema = Literal['backward', 'trapezoidal']


class Config(BaseModel):

    testsystemfile: Path

    fn: int  # only tested for 50
    Sb: int  # parameters in .txt table are assumed to be given for 100 MW
    ##########General input data##################
    ts: float  # Simulation time step
    te: float  # Estimation time step
    T_start: float  # It has to be 0.0
    T_end: float
    # integration ('trapezoidal' or 'backward')
    int_scheme: IntegrationSchema

    ####initialize estimation##########
    init_error_diff: float   # 0.5 = 5%; 1.0 = 10% etc.
    init_error_alg: bool  # 1 = flat start; 0 = true values

    ##########Plot###############
    plot: bool
    plot_voltage: bool
    plot_diff: bool

    proc_noise_alg: float
    proc_noise_diff: float

    def updated(self, **kwargs: Any) -> "Config":
        return self.model_copy(update=kwargs)


base_dir = Path(os.path.dirname(os.path.abspath(__file__)))

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
    init_error_diff=1,  # 0.5 = 5%; 1.0 = 10% etc.
    init_error_alg=True,  # 1 = flat start; 0 = true values
    # #########Plot###############
    plot=True,
    plot_voltage=True,
    plot_diff=True,
    proc_noise_alg=1e-3,
    proc_noise_diff=1e-4,
)


