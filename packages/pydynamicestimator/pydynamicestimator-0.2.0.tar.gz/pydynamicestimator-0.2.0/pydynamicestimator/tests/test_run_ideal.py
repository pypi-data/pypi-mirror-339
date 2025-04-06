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


from pydynamicestimator import run
import numpy as np
from pydynamicestimator.run import run
from pydynamicestimator.configs.config_ideal import config


def test_run():

    dae_est, dae_sim = run(config)
    for key in dae_est.grid.yf:
        assert np.allclose(dae_sim.grid.yf[key][:, round(dae_est.T_start / dae_sim.t):round(dae_est.T_end / dae_sim.t):round(dae_est.t / dae_sim.t)], dae_est.grid.yf[key],
                           atol=1e-03), "The error of voltages estimation is too large even without noise"
