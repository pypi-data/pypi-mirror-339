# Created: 2025-03-20
# Last Modified: 2025-04-05
# (c) Copyright 2025 ETH Zurich, Emma Laub, Milos Katanic
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

from __future__ import annotations  # Postponed type evaluation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydynamicestimator.system import *
from pydynamicestimator.devices.device import *

class Inverter(DeviceRect):

    """ Metaclass for inverters """

    def __init__(self):
        super().__init__()
        self._params.update(
            {'omega_net': 1.0, 'Kp': 0.02, 'Kq': 0.1, 'Kpv': 0.59, 'Kiv': 736, 'Kffv': 0, 'Kpc': 1.27, 'Kic': 14.3,
             'Kffc': 0, 'Rv': 0, 'Lv': 0.2, 'Rf': 0.0001, 'Lf': 0.08, 'Cf': 0.074, 'Rt': 0.01, 'Lt': 0.2,
             'omega_f': 2 * np.pi * 5 })

        self._descr.update({
            'Pref': 'Active power set point',
            'Qref': 'Reactive power set point',
            'Vref': 'Voltage set point',
            'Kp': 'Droop coefficient for P-f',
            'Kq': 'Droop coefficient for Q-V',
            'Rf': 'Filter resistance',
            'Xf': 'Filter reactance',
            'Cf': 'Filter capacitance',
            'omega_net': 'Network frequency in p.u. (generally 1.0)',
            'Vdf_ext': 'd-component of external filter voltage',
            'Vfq_ext': 'q-component of external filter voltage',
            'ifd_ext': 'd-component of external filter current',
            'ifq_ext': 'q-component of external filter current',
            'Pc_tilde': 'Filtered internal active power',
            'Qc_tilde': 'Filtered internal reactive power',
            'xi_d': 'Integrator state of the d-component of the internal voltage',
            'xi_q': 'Integrator state of the q-component of the internal voltage',
            'gamma_d': 'Integrator state of the d-component of the internal current',
            'gamma_q': 'Integrator state of the q-component of the internal current',
            'Rt': 'Resistance of the line connecting the external end of the filter to the terminal (i.e. grid)',
            'omega_f': 'cut-off frequency for the low pass filter',
            'Kpc': 'Proportional gain for current controller',
            'Kic': 'Integral gain for current controller',
            'Kffc': 'Feed-forward gain of current controller',
            'Kpv': 'Proportional gain for voltage controller',
            'Kiv': 'Integral gain for voltage controller',
            'Kffv': 'Feed-forward gain of voltage controller',
            'Rv': 'Virtual impedance resistance',
            'Lv': 'Virtual impedance inductance',
            'Pc': 'Unfiltered internal active power',
            'Qc': 'Unfiltered internal reactive power'
        })

        # params
        self.omega_net = np.array([], dtype=float)
        self.Kp = np.array([], dtype=float)
        self.Kq = np.array([], dtype=float)
        self.Kpv = np.array([], dtype=float)
        self.Kiv = np.array([], dtype=float)
        self.Kffv = np.array([], dtype=float)
        self.Kpc = np.array([], dtype=float)
        self.Kic = np.array([], dtype=float)
        self.Kffc = np.array([], dtype=float)
        self.Rv = np.array([], dtype=float)
        self.Lv = np.array([], dtype=float)
        self.Rf = np.array([], dtype=float)
        self.Lf = np.array([], dtype=float)
        self.Cf = np.array([], dtype=float)
        self.Rt = np.array([], dtype=float)
        self.Lt = np.array([], dtype=float)
        self.omega_f = np.array([], dtype=float)

        # States
        self.ns = 13
        self.states.extend(['Vfd_ext', 'Vfq_ext', 'ifd_ext', 'ifq_ext', 'itd_ext', 'itq_ext', 'Pc_tilde', 'delta_c',
                            'Qc_tilde', 'xi_d', 'xi_q', 'gamma_d', 'gamma_q'])
        self.Vfd_ext = np.array([], dtype=float)
        self.Vfq_ext = np.array([], dtype=float)
        self.ifd_ext = np.array([], dtype=float)
        self.ifq_ext = np.array([], dtype=float)
        self.itd_ext = np.array([], dtype=float)
        self.itq_ext = np.array([], dtype=float)
        self.Pc_tilde = np.array([], dtype=float)
        self.delta_c = np.array([], dtype=float)
        self.Qc_tilde = np.array([], dtype=float)
        self.xi_d = np.array([], dtype=float)
        self.xi_q = np.array([], dtype=float)
        self.gamma_d = np.array([], dtype=float)
        self.gamma_q = np.array([], dtype=float)

        self._states_noise.update(
            {'Vfd_ext': 1e-2, 'Vfq_ext': 1e-2, 'ifd_ext': 1e-2, 'ifq_ext': 1e-2, 'itd_ext': 1e-2, 'itq_ext': 1e-2,
             'Pc_tilde': 1e-2, 'delta_c': 1e-2, 'Qc_tilde': 1e-2, 'xi_d': 1e-2, 'xi_q': 1e-2, 'gamma_d': 1e-2,
             'gamma_q': 1e-2})
        self._states_init_error.update(
            {'Vfd_ext': 1e-2, 'Vfq_ext': 1e-2, 'ifd_ext': 1e-2, 'ifq_ext': 1e-2, 'itd_ext': 1e-2, 'itq_ext': 1e-2,
             'Pc_tilde': 1e-2, 'delta_c': 1e-2, 'Qc_tilde': 1e-2, 'xi_d': 1e-2, 'xi_q': 1e-2, 'gamma_d': 1e-2,
             'gamma_q': 1e-2})
        self._x0.update(
            {'Vfd_ext': 1.0, 'Vfq_ext': 0, 'ifd_ext': 0.1, 'ifq_ext': 0, 'itd_ext': 0, 'itq_ext': 0, 'Pc_tilde': 0.1,
             'delta_c': 0, 'Qc_tilde': 0, 'xi_d': 0, 'xi_q': 0, 'gamma_d': 0, 'gamma_q': 0})

        # Set points
        self._setpoints.update({'Pref': 0.5, 'Qref': 0.01, 'Vref': 1.05})
        self.Pref = np.array([], dtype=float)
        self.Qref = np.array([], dtype=float)
        self.Vref = np.array([], dtype=float)
        self.properties.update({'fplot': True})

    def gcall(self, dae: Dae):
        # algebraic equations (current balance in rectangular coordinates) + scale the current back to the grid reference power
        dae.g[self.vre] -= self.Sn / dae.Sb * dae.x[self.itd_ext]
        dae.g[self.vim] -= self.Sn / dae.Sb * dae.x[self.itq_ext]

    def filter_init(self, dae):
        """
        Steady-state initialization of the inverter filter.
        Based on methods used in https://github.com/NREL-Sienna/PowerSimulationsDynamics.jl

        Args:
            dae (pydynamicestimator.system.DAE): DAE object

        Returns:
            Vswd (ndarray): d-component of the switching block voltage
            Vswq (ndarray): q-component of the switching block voltage
            ifd_ext (ndarray): d-component of the filter current in the network (external) dq-reference frame
            ifq_ext (ndarray): q-component of the filter current in the network (external) dq-reference frame
            Vfd_ext (ndarray): d-component of the filter voltage in the network (external) dq-reference frame
            Vfq_ext (ndarray): q-component of the filter voltage in the network (external) dq-reference frame
            itd_ext (ndarray): d-component of the terminal current in the network (external) dq-reference frame
            itq_ext (ndarray): q-component of the terminal current in the network (external) dq-reference frame
        """
        n_unknowns = 6  # number of unknowns per device

        # Solve for Vfd_ext, Vfq_ext, ifd_ext, ifq_ext, Vtd_ext, Vtq_ext
        Vswd = SX.sym('Vswd', self.n)
        Vswq = SX.sym('Vswq', self.n)
        ifd_ext = SX.sym('ifd_ext', self.n)
        ifq_ext = SX.sym('ifq_ext', self.n)
        Vfd_ext = SX.sym('Vfd_ext', self.n)
        Vfq_ext = SX.sym('Vfq_ext', self.n)

        inputs = [vertcat(Vswd, Vswq, ifd_ext, ifq_ext, Vfd_ext, Vfq_ext)]
        outputs = SX(np.zeros(n_unknowns * self.n))

        omega_b = 2 * np.pi * np.array(self.fn)
        itd_ext = dae.Sb / self.Sn * dae.iinit[self.vre]
        itq_ext = dae.Sb / self.Sn * dae.iinit[self.vim]
        vre = dae.yinit[self.vre]
        vim = dae.yinit[self.vim]

        # d ifd_ext / dt
        outputs[0:self.n] = omega_b / self.Lf * (
                    Vswd - Vfd_ext) - omega_b * self.Rf / self.Lf * ifd_ext + self.omega_net * omega_b * ifq_ext
        # d ifq_ext / dt
        outputs[self.n: 2 * self.n] = omega_b / self.Lf * (
                    Vswq - Vfq_ext) - omega_b * self.Rf / self.Lf * ifq_ext - self.omega_net * omega_b * ifd_ext

        # d vfd_ext / dt
        outputs[2 * self.n: 3 * self.n] = omega_b / self.Cf * (ifd_ext - itd_ext) + self.omega_net * omega_b * Vfq_ext
        # d vfq_ext / dt
        outputs[3 * self.n: 4 * self.n] = omega_b / self.Cf * (ifq_ext - itq_ext) - self.omega_net * omega_b * Vfd_ext

        # d itd_ext / dt
        outputs[4 * self.n: 5 * self.n] = omega_b / self.Lt * (
                    Vfd_ext - vre) - omega_b * self.Rt / self.Lt * itd_ext + self.omega_net * omega_b * itq_ext
        # # d itq_ext / dt
        outputs[5 * self.n: 6 * self.n] = omega_b / self.Lt * (
                    Vfq_ext - vim) - omega_b * self.Rt / self.Lt * itq_ext - self.omega_net * omega_b * itd_ext

        outputs = [vertcat(outputs)]

        h = Function('h', inputs, outputs)
        G = rootfinder('G', 'newton', h)

        sol = vertcat(np.zeros(n_unknowns * self.n))
        solution = G(sol)
        solution = np.array(solution).flatten()

        Vswd = solution[0:self.n]
        Vswq = solution[self.n: 2 * self.n]
        ifd_ext = solution[2 * self.n: 3 * self.n]
        ifq_ext = solution[3 * self.n: 4 * self.n]
        Vfd_ext = solution[4 * self.n: 5 * self.n]
        Vfq_ext = solution[5 * self.n: 6 * self.n]

        return Vswd, Vswq, ifd_ext, ifq_ext, Vfd_ext, Vfq_ext, itd_ext, itq_ext

    def frequency_estimator_init(self, Vfd_ext, Vfq_ext):
        """
        Steady-state initialization of the frequency estimator.
        Based on methods used in https://github.com/NREL-Sienna/PowerSimulationsDynamics.jl

        Args:
            Vfd_ext (ndarray): d-component of the filter voltage in the network (external) dq-reference frame
            Vfq_ext (ndarray): q-component of the filter voltage in the network (external) dq-reference frame

        Returns:
            Vfq_pll (ndarray): q-component of the filter voltage in the PLL's dq-reference frame
            epsilon (ndarray): integrator state of the PLL
            delta_pll (ndarray): angle difference between the dq-reference frame of the PLL and the network
        """
        n_unknowns = 3

        # Solve for Vfq_pll, epsilon, and delta_pll
        Vfq_pll = SX.sym('Vfq_pll', self.n)
        epsilon = SX.sym('epsilon', self.n)
        delta_pll = SX.sym('delta_pll', self.n)

        inputs = [vertcat(Vfq_pll, epsilon, delta_pll)]
        outputs = SX(np.zeros(n_unknowns*self.n))

        outputs[:self.n] = Vfd_ext * np.sin(-delta_pll) + Vfq_ext * np.cos(-delta_pll) - Vfq_pll
        outputs[self.n:2*self.n] = Vfq_pll
        outputs[2*self.n:3*self.n] = self.Kpll_p * Vfq_pll + self.Kpll_i * epsilon

        outputs = [vertcat(outputs)]

        h = Function('h', inputs, outputs)
        G = rootfinder('G', 'newton', h)

        sol = vertcat(np.zeros(n_unknowns * self.n))
        solution = G(sol)
        solution = np.array(solution).flatten()

        Vfq_pll = solution[:self.n]
        epsilon = solution[self.n:2*self.n]
        delta_pll = solution[2*self.n:3*self.n]

        return Vfq_pll, epsilon, delta_pll

    def outer_loop_init(self, dae, Vfd_ext, Vfq_ext):
        """
        Steady-state initialization of the inverter outer loop.
        Based on methods used in https://github.com/NREL-Sienna/PowerSimulationsDynamics.jl

        Args:
            dae (pydynamicestimator.system.DAE): DAE object
            Vfd_ext (ndarray): d-component of the filter voltage in the network (external) dq-reference frame
            Vfq_ext (ndarray): q-component of the filter voltage in the network (external) dq-reference frame

        Returns:
            Pref (ndarray): active power reference
            Qref (ndarray): reactive power reference
        """
        itd_ext = dae.Sb / self.Sn * dae.iinit[self.vre]
        itq_ext = dae.Sb / self.Sn * dae.iinit[self.vim]

        Pc_ext = Vfd_ext * itd_ext + Vfq_ext * itq_ext
        Qc_ext = -Vfd_ext * itq_ext + Vfq_ext * itd_ext

        Pref = Pc_ext
        Qref = Qc_ext

        return Pref, Qref

    def inner_loop_init(self, dae, ifd_ext, ifq_ext, Vfd_ext, Vfq_ext, Vswd, Vswq):
        """
        Steady-state initialization of the inverter inner loop.
        Based on methods used in https://github.com/NREL-Sienna/PowerSimulationsDynamics.jl

        Args:
            dae (pydynamicestimator.system.DAE): DAE object
            ifd_ext
            ifq_ext
            Vfd_ext
            Vfq_ext
            Vswd
            Vswq

        Returns:
            delta_c
            Vref
            xi_d
            xi_q
            gamma_d
            gamma_q
            Pc_tilde
            Qc_tilde
        """
        n_unknowns = 8

        # Solve for delta_c, Vref, xi_d, xi_q, gamma_d, gamma_q, phi_d, phi_q
        delta_c = SX.sym('delta_c', self.n)
        Vref = SX.sym('Vref', self.n)
        xi_d = SX.sym('xi_d', self.n)
        xi_q = SX.sym('xi_q', self.n)
        gamma_d = SX.sym('gamma_d', self.n)
        gamma_q = SX.sym('gamma_q', self.n)
        Pc_tilde = SX.sym('Pc_tilde', self.n)
        Qc_tilde = SX.sym('Qc_tilde', self.n)

        itd_int = SX.sym('itd_int', self.n)
        itq_int = SX.sym('itq_int', self.n)
        ifd_int = SX.sym('ifd_int', self.n)
        ifq_int = SX.sym('ifq_int', self.n)
        Vfd_int = SX.sym('Vfd_int', self.n)
        Vfq_int = SX.sym('Vfq_int', self.n)
        Vswd_int = SX.sym('Vswd_int', self.n)
        Vswq_int = SX.sym('Vswq_int', self.n)
        Vfd_ref = SX.sym('Vfd_ref', self.n)
        Vfq_ref = SX.sym('Vfq_ref', self.n)
        ifd_ref = SX.sym('ifd_ref', self.n)
        ifq_ref = SX.sym('ifq_ref', self.n)
        Vswd_ref = SX.sym('Vswd_ref', self.n)
        Vswq_ref = SX.sym('Vswq_ref', self.n)
        Pc = SX.sym('Pc', self.n)
        Qc = SX.sym('Qc', self.n)

        inputs = [vertcat(delta_c, Vref, xi_d, xi_q, gamma_d, gamma_q, Pc_tilde, Qc_tilde)]
        outputs = SX(np.zeros(n_unknowns * self.n))

        itd_ext = dae.Sb / self.Sn * dae.iinit[self.vre]
        itq_ext = dae.Sb / self.Sn * dae.iinit[self.vim]

        omega_c = self.omega_net

        for i in range(self.n):
            # Reference Frame Transformations
            itd_int[i] = itd_ext[i] * np.cos(-delta_c[i]) - itq_ext[i] * np.sin(-delta_c[i])
            itq_int[i] = itd_ext[i] * np.sin(-delta_c[i]) + itq_ext[i] * np.cos(-delta_c[i])

            ifd_int[i] = ifd_ext[i] * np.cos(-delta_c[i]) - ifq_ext[i] * np.sin(-delta_c[i])
            ifq_int[i] = ifd_ext[i] * np.sin(-delta_c[i]) + ifq_ext[i] * np.cos(-delta_c[i])

            Vfd_int[i] = Vfd_ext[i] * np.cos(-delta_c[i]) - Vfq_ext[i] * np.sin(-delta_c[i])
            Vfq_int[i] = Vfd_ext[i] * np.sin(-delta_c[i]) + Vfq_ext[i] * np.cos(-delta_c[i])

            Vswd_int[i] = Vswd[i] * np.cos(-delta_c[i]) - Vswq[i] * np.sin(-delta_c[i])
            Vswq_int[i] = Vswd[i] * np.sin(-delta_c[i]) + Vswq[i] * np.cos(-delta_c[i])

            # Voltage controller references
            Vfd_ref[i] = Vref[i] - self.Rv[i] * itd_int[i] + omega_c[i] * self.Lv[i] * itq_int[i]
            Vfq_ref[i] = -self.Rv[i] * itq_int[i] - omega_c[i] * self.Lv[i] * itd_int[i]

            # Current controller references
            ifd_ref[i] = self.Kpv[i] * (Vfd_ref[i] - Vfd_int[i]) + self.Kiv[i] * xi_d[i] - omega_c[i] * self.Cf[i] * Vfq_int[i] + self.Kffv[i] * itd_int[i]
            ifq_ref[i] = self.Kpv[i] * (Vfq_ref[i] - Vfq_int[i]) + self.Kiv[i] * xi_q[i] + omega_c[i] * self.Cf[i] * Vfd_int[i] + self.Kffv[i] * itq_int[i]

            # References for converter output voltage
            Vswd_ref[i] = self.Kpc[i] * (ifd_ref[i] - ifd_int[i]) + self.Kic[i] * gamma_d[i] - omega_c[i] * self.Lf[i] * ifq_int[i] + self.Kffc[i] * Vfd_int[i]
            Vswq_ref[i] = self.Kpc[i] * (ifq_ref[i] - ifq_int[i]) + self.Kic[i] * gamma_q[i] + omega_c[i] * self.Lf[i] * ifd_int[i] + self.Kffc[i] * Vfq_int[i]

            # Below differs from NREL script, since we still need to calculate initial values for Pc_tilde and Qc_tilde which is not done in the NREL script
            Pc[i] = Vfd_int[i] * itd_int[i] + Vfq_int[i] * itq_int[i]
            Qc[i] = -Vfd_int[i] * itq_int[i] + Vfq_int[i] * itd_int[i]


        outputs[0:self.n] = Vfd_ref - Vfd_int
        outputs[self.n:2*self.n] = Vfq_ref - Vfq_int
        outputs[2*self.n:3*self.n] = ifd_ref - ifd_int
        outputs[3*self.n:4*self.n] = ifq_ref - ifq_int
        outputs[4*self.n:5*self.n] = Vswd_ref - Vswd_int
        outputs[5*self.n:6*self.n] = Vswq_ref - Vswq_int
        outputs[6*self.n:7*self.n] = self.omega_f * (Pc - Pc_tilde) # this equation and the next are not in the NREL script, used to calulate Pc_tilde and Qc_tilde
        outputs[7*self.n:8*self.n] = self.omega_f * (Qc - Qc_tilde)

        outputs = [vertcat(outputs)]

        h = Function('h', inputs, outputs)
        G = rootfinder('G', 'newton', h)

        sol = vertcat(np.zeros(n_unknowns * self.n))
        solution = G(sol)
        solution = np.array(solution).flatten()

        delta_c = solution[0:self.n]
        Vref = solution[self.n: 2 * self.n]
        xi_d = solution[2 * self.n: 3 * self.n]
        xi_q = solution[3 * self.n: 4 * self.n]
        gamma_d = solution[4 * self.n: 5 * self.n]
        gamma_q = solution[5 * self.n: 6 * self.n]
        Pc_tilde = solution[6 * self.n: 7 * self.n]
        Qc_tilde = solution[7 * self.n: 8 * self.n]


        return delta_c, Vref, xi_d, xi_q, gamma_d, gamma_q, Pc_tilde, Qc_tilde


class GridFollowing(Inverter):  #
    """
    Grid-Following Inverter (with Droop)
    Based on the grid-following inverter model in https://doi.org/10.1109/TPWRS.2021.3061434
    """

    def __init__(self) -> None:
        super().__init__()

        # private data
        self._type = "Inverter"
        self._name = 'GridFollowing_inverter_model'

        # States
        self.ns += 2
        self.states.extend(['epsilon', 'delta_pll'])
        self.epsilon = np.array([], dtype=float)
        self.delta_pll = np.array([], dtype=float)
        self._states_noise.update({'epsilon': 1e-2, 'delta_pll': 1e-2})
        self._states_init_error.update({'epsilon': 1e-2, 'delta_pll': 1e-2})

        self._x0.update({'epsilon': 0, 'delta_pll': 0})

        # Params
        self._params.update({'Kpll_p': 0.5, 'Kpll_i': 4.69})

        self._descr.update({
            'Kpll_p': 'Proportional gain for PLL',
            'Kpll_i': 'Integral gain for PLL',
            'epsilon': 'PLL integrator state',
            'delta_pll': 'angle difference between the dq-reference frame of the PLL and the network',})

        # Parameters
        self.Kpll_p = np.array([], dtype=float)
        self.Kpll_i = np.array([], dtype=float)

        self.properties.update(
            {'fgcall': True, 'finit': True, 'init_data': True, 'xy_index': True, 'save_data': True, 'qcall': True})
        self._init_data()

    def fgcall(self, dae):
        omega_b = SX.sym('omega_b', self.n)

        delta_omega_pll = SX.sym('delta_omega_pll', self.n)

        Vswd = SX.sym('Vswd', self.n)
        Vswq = SX.sym('Vswq', self.n)

        Vfq_pll = SX.sym('Vfq_pll', self.n)
        Pc = SX.sym('Pc', self.n)
        Qc = SX.sym('Qc', self.n)
        delta_omega_c = SX.sym('delta_omega_c', self.n)

        Vfd_ref = SX.sym('Vfd_ref', self.n)
        Vfq_ref = SX.sym('Vfq_ref', self.n)
        Vfd_int = SX.sym('Vfd_int', self.n)
        Vfq_int = SX.sym('Vfq_int', self.n)

        ifd_ref = SX.sym('ifd_ref', self.n)
        ifq_ref = SX.sym('ifq_ref', self.n)
        ifd_int = SX.sym('ifd_int', self.n)
        ifq_int = SX.sym('ifq_int', self.n)

        itd_int = SX.sym('itd_int', self.n)
        itq_int = SX.sym('itq_int', self.n)

        vn = dae.y

        for i in range(self.n):
            omega_b[i] = 2 * np.pi * self.fn[i]

            Vfd_int[i] = dae.x[self.Vfd_ext[i]] * np.cos(-dae.x[self.delta_c[i]]) - dae.x[self.Vfq_ext[i]] * np.sin(-dae.x[self.delta_c[i]])
            Vfq_int[i] = dae.x[self.Vfd_ext[i]] * np.sin(-dae.x[self.delta_c[i]]) + dae.x[self.Vfq_ext[i]] * np.cos(-dae.x[self.delta_c[i]])

            itd_int[i] = dae.x[self.itd_ext[i]] * np.cos(-dae.x[self.delta_c[i]]) - dae.x[self.itq_ext[i]] * np.sin(-dae.x[self.delta_c[i]])
            itq_int[i] = dae.x[self.itd_ext[i]] * np.sin(-dae.x[self.delta_c[i]]) + dae.x[self.itq_ext[i]] * np.cos(-dae.x[self.delta_c[i]])

            ifd_int[i] = dae.x[self.ifd_ext[i]] * np.cos(-dae.x[self.delta_c[i]]) - dae.x[self.ifq_ext[i]] * np.sin(-dae.x[self.delta_c[i]])
            ifq_int[i] = dae.x[self.ifd_ext[i]] * np.sin(-dae.x[self.delta_c[i]]) + dae.x[self.ifq_ext[i]] * np.cos(-dae.x[self.delta_c[i]])

            Pc[i] = Vfd_int[i] * itd_int[i] + Vfq_int[i] * itq_int[i]
            Qc[i] = -Vfd_int[i] * itq_int[i] + Vfq_int[i] * itd_int[i]

            Vfq_pll[i] = dae.x[self.Vfd_ext[i]] * np.sin(-dae.x[self.delta_pll[i]]) + dae.x[self.Vfq_ext[i]] * np.cos(
                -dae.x[self.delta_pll[i]])
            omega_pll = 1.0 + self.Kpll_p[i] * Vfq_pll[i] + self.Kpll_i[i] * dae.x[
                self.epsilon[i]]  # 1.0 p.u. is set as the nominal omega here
            delta_omega_pll[i] = omega_pll - self.omega_net[i]

            omega_c = omega_pll + self.Kp[i] * (self.Pref[i] - dae.x[self.Pc_tilde[i]])
            delta_omega_c[i] = omega_c - self.omega_net[i]

            Vcd = self.Vref[i] + self.Kq[i] * (self.Qref[i] - dae.x[self.Qc_tilde[i]])

            Vfd_ref[i] = Vcd - self.Rv[i] * itd_int[i] + omega_c * self.Lv[i] * itq_int[i]
            Vfq_ref[i] = -self.Rv[i] * itq_int[i] - omega_c * self.Lv[i] * itd_int[i]

            ifd_ref[i] = self.Kpv[i] * (Vfd_ref[i] - Vfd_int[i]) + self.Kiv[i] * dae.x[self.xi_d[i]] - omega_c * self.Cf[i] * Vfq_int[i] + self.Kffv[i] * itd_int[i]
            ifq_ref[i] = self.Kpv[i] * (Vfq_ref[i] - Vfq_int[i]) + self.Kiv[i] * dae.x[self.xi_q[i]] + omega_c * self.Cf[i] * Vfd_int[i] + self.Kffv[i] * itq_int[i]


            Vswd_ref = self.Kpc[i] * (ifd_ref[i] - ifd_int[i]) + self.Kic[i] * dae.x[self.gamma_d[i]] - omega_c * self.Lf[i] * ifq_int[i] + self.Kffc[i] * Vfd_int[i]
            Vswq_ref = self.Kpc[i] * (ifq_ref[i] - ifq_int[i]) + self.Kic[i] * dae.x[self.gamma_q[i]] + omega_c * self.Lf[i] * ifd_int[i] + self.Kffc[i] * Vfq_int[i]

            Vswd[i] = Vswd_ref * np.cos(dae.x[self.delta_c[i]]) - Vswq_ref * np.sin(dae.x[self.delta_c[i]])
            Vswq[i] = Vswd_ref * np.sin(dae.x[self.delta_c[i]]) + Vswq_ref * np.cos(dae.x[self.delta_c[i]])


        # Define differential equations
        dae.f[self.Vfd_ext] = omega_b / self.Cf * (dae.x[self.ifd_ext] - dae.x[self.itd_ext]) + self.omega_net * omega_b * dae.x[self.Vfq_ext]
        dae.f[self.Vfq_ext] = omega_b / self.Cf * (dae.x[self.ifq_ext] - dae.x[self.itq_ext]) - self.omega_net * omega_b * dae.x[self.Vfd_ext]

        dae.f[self.ifd_ext] = omega_b / self.Lf * (Vswd - dae.x[self.Vfd_ext]) - omega_b * self.Rf / self.Lf * dae.x[self.ifd_ext] + self.omega_net * omega_b * dae.x[self.ifq_ext]
        dae.f[self.ifq_ext] = omega_b / self.Lf * (Vswq - dae.x[self.Vfq_ext]) - omega_b * self.Rf / self.Lf * dae.x[self.ifq_ext] - self.omega_net * omega_b * dae.x[self.ifd_ext]

        dae.f[self.itd_ext] = omega_b / self.Lt * (dae.x[self.Vfd_ext] - vn[self.vre]) - omega_b * self.Rt / self.Lt * dae.x[self.itd_ext] + self.omega_net * omega_b * dae.x[self.itq_ext]
        dae.f[self.itq_ext] = omega_b / self.Lt * (dae.x[self.Vfq_ext] - vn[self.vim]) - omega_b * self.Rt / self.Lt * dae.x[self.itq_ext] - self.omega_net * omega_b * dae.x[self.itd_ext]

        dae.f[self.epsilon] = Vfq_pll

        dae.f[self.delta_pll] = omega_b * delta_omega_pll

        dae.f[self.Pc_tilde] = self.omega_f * (Pc - dae.x[self.Pc_tilde])

        dae.f[self.delta_c] = omega_b * delta_omega_c

        dae.f[self.Qc_tilde] = self.omega_f * (Qc - dae.x[self.Qc_tilde])

        dae.f[self.xi_d] = Vfd_ref - Vfd_int
        dae.f[self.xi_q] = Vfq_ref - Vfq_int

        dae.f[self.gamma_d] = ifd_ref - ifd_int
        dae.f[self.gamma_q] = ifq_ref - ifq_int

        self.gcall(dae)

    def finit(self, dae):

        Vswd, Vswq, ifd_ext, ifq_ext, Vfd_ext, Vfq_ext, itd_ext, itq_ext = self.filter_init(dae)

        # Initialize Frequency Estimator
        Vfq_pll, epsilon, delta_pll = self.frequency_estimator_init(Vfd_ext, Vfq_ext)

        # Initialize outer loop
        Pref, Qref = self.outer_loop_init(dae, Vfd_ext, Vfq_ext)

        # Initialize inner loop
        delta_c, Vref, xi_d, xi_q, gamma_d, gamma_q, Pc_tilde, Qc_tilde = self.inner_loop_init(dae, ifd_ext, ifq_ext, Vfd_ext, Vfq_ext, Vswd, Vswq)

        solution = [Vfd_ext, Vfq_ext, ifd_ext, ifq_ext, itd_ext, itq_ext, Pc_tilde, delta_c,
                    Qc_tilde, xi_d, xi_q, gamma_d, gamma_q, epsilon, delta_pll, Pref, Qref, Vref]

        solution = np.array(solution)

        # put solution into the correct order so that the right values are loaded into xinit and the setpoints
        states_solution = [item for sublist in np.transpose(solution[:self.ns]) for item in sublist]
        setpoints_solution = solution[self.ns:].flatten()
        solution = np.concatenate((states_solution, setpoints_solution))

        # Find the indices of differential equations for this type of generator
        diff = [self.__dict__[arg] for arg in self.states]
        diff_index = [item for sublist in np.transpose(diff) for item in sublist]

        # Now load the initial states into DAE class such that simulation/estimation actually starts from those values
        dae.xinit[diff_index] = solution[:self.ns * self.n]

        # Load initial setpoint values
        for idx, s in enumerate(self._setpoints):
            self.__dict__[s] = solution[(self.ns + idx) * self.n:(idx + 1 + self.ns) * self.n]


class GridForming(Inverter):
    """
    Grid-Forming Inverter (Droop-Based)
    Based on the grid-forming inverter model in https://doi.org/10.1109/TPWRS.2021.3061434
    """

    def __init__(self) -> None:
        super().__init__()

        # private data
        self._type = "Inverter"
        self._name = 'GridForming_inverter_model'

        # States
        self.ns += 0

        self.properties.update(
            {'fgcall': True, 'finit': True, 'init_data': True, 'xy_index': True, 'save_data': True, 'qcall': True})
        self._init_data()

    def fgcall(self, dae: Dae) -> None:
        omega_b = SX.sym('omega_b', self.n)

        Vswd = SX.sym('Vswd', self.n)
        Vswq = SX.sym('Vswq', self.n)

        Pc = SX.sym('Pc', self.n)
        Qc = SX.sym('Qc', self.n)
        delta_omega_c = SX.sym('delta_omega_c', self.n)

        Vfd_ref = SX.sym('Vfd_ref', self.n)
        Vfq_ref = SX.sym('Vfq_ref', self.n)
        Vfd_int = SX.sym('Vfd_int', self.n)
        Vfq_int = SX.sym('Vfq_int', self.n)

        ifd_ref = SX.sym('ifd_ref', self.n)
        ifq_ref = SX.sym('ifq_ref', self.n)
        ifd_int = SX.sym('ifd_int', self.n)
        ifq_int = SX.sym('ifq_int', self.n)

        itd_int = SX.sym('itd_int', self.n)
        itq_int = SX.sym('itq_int', self.n)

        vn = dae.y

        for i in range(self.n):
            omega_b[i] = 2 * np.pi * self.fn[i]

            Vfd_int[i] = dae.x[self.Vfd_ext[i]] * np.cos(-dae.x[self.delta_c[i]]) - dae.x[self.Vfq_ext[i]] * np.sin(-dae.x[self.delta_c[i]])
            Vfq_int[i] = dae.x[self.Vfd_ext[i]] * np.sin(-dae.x[self.delta_c[i]]) + dae.x[self.Vfq_ext[i]] * np.cos(-dae.x[self.delta_c[i]])

            itd_int[i] = dae.x[self.itd_ext[i]] * np.cos(-dae.x[self.delta_c[i]]) - dae.x[self.itq_ext[i]] * np.sin(-dae.x[self.delta_c[i]])
            itq_int[i] = dae.x[self.itd_ext[i]] * np.sin(-dae.x[self.delta_c[i]]) + dae.x[self.itq_ext[i]] * np.cos(-dae.x[self.delta_c[i]])

            ifd_int[i] = dae.x[self.ifd_ext[i]] * np.cos(-dae.x[self.delta_c[i]]) - dae.x[self.ifq_ext[i]] * np.sin(-dae.x[self.delta_c[i]])
            ifq_int[i] = dae.x[self.ifd_ext[i]] * np.sin(-dae.x[self.delta_c[i]]) + dae.x[self.ifq_ext[i]] * np.cos(-dae.x[self.delta_c[i]])

            Pc[i] = Vfd_int[i] * itd_int[i] + Vfq_int[i] * itq_int[i]
            Qc[i] = -Vfd_int[i] * itq_int[i] + Vfq_int[i] * itd_int[i]

            omega_c = 1.0 + self.Kp[i] * (self.Pref[i] - dae.x[self.Pc_tilde[i]])

            delta_omega_c[i] = omega_c - self.omega_net[i]

            Vcd = self.Vref[i] + self.Kq[i] * (self.Qref[i] - dae.x[self.Qc_tilde[i]])

            Vfd_ref[i] = Vcd - self.Rv[i] * itd_int[i] + omega_c * self.Lv[i] * itq_int[i]
            Vfq_ref[i] = -self.Rv[i] * itq_int[i] - omega_c * self.Lv[i] * itd_int[i]

            ifd_ref[i] = self.Kpv[i] * (Vfd_ref[i] - Vfd_int[i]) + self.Kiv[i] * dae.x[self.xi_d[i]] - omega_c * self.Cf[i] * Vfq_int[i] + self.Kffv[i] * itd_int[i]
            ifq_ref[i] = self.Kpv[i] * (Vfq_ref[i] - Vfq_int[i]) + self.Kiv[i] * dae.x[self.xi_q[i]] + omega_c * self.Cf[i] * Vfd_int[i] + self.Kffv[i] * itq_int[i]

            Vswd_ref = self.Kpc[i] * (ifd_ref[i] - ifd_int[i]) + self.Kic[i] * dae.x[self.gamma_d[i]] - omega_c * self.Lf[i] * ifq_int[i] + self.Kffc[i] * Vfd_int[i]
            Vswq_ref = self.Kpc[i] * (ifq_ref[i] - ifq_int[i]) + self.Kic[i] * dae.x[self.gamma_q[i]] + omega_c * self.Lf[i] * ifd_int[i] + self.Kffc[i] * Vfq_int[i]

            Vswd[i] = Vswd_ref * np.cos(dae.x[self.delta_c[i]]) - Vswq_ref * np.sin(dae.x[self.delta_c[i]])
            Vswq[i] = Vswd_ref * np.sin(dae.x[self.delta_c[i]]) + Vswq_ref * np.cos(dae.x[self.delta_c[i]])


        # Define differential equations
        dae.f[self.Vfd_ext] = omega_b / self.Cf * (dae.x[self.ifd_ext] - dae.x[self.itd_ext]) + self.omega_net * omega_b * dae.x[self.Vfq_ext]
        dae.f[self.Vfq_ext] = omega_b / self.Cf * (dae.x[self.ifq_ext] - dae.x[self.itq_ext]) - self.omega_net * omega_b * dae.x[self.Vfd_ext]

        dae.f[self.ifd_ext] = omega_b / self.Lf * (Vswd - dae.x[self.Vfd_ext]) - omega_b * self.Rf / self.Lf * dae.x[self.ifd_ext] + self.omega_net * omega_b * dae.x[self.ifq_ext]
        dae.f[self.ifq_ext] = omega_b / self.Lf * (Vswq - dae.x[self.Vfq_ext]) - omega_b * self.Rf / self.Lf * dae.x[self.ifq_ext] - self.omega_net * omega_b * dae.x[self.ifd_ext]

        dae.f[self.itd_ext] = omega_b / self.Lt * (dae.x[self.Vfd_ext] - vn[self.vre]) - omega_b * self.Rt / self.Lt * dae.x[self.itd_ext] + self.omega_net * omega_b * dae.x[self.itq_ext]
        dae.f[self.itq_ext] = omega_b / self.Lt * (dae.x[self.Vfq_ext] - vn[self.vim]) - omega_b * self.Rt / self.Lt * dae.x[self.itq_ext] - self.omega_net * omega_b * dae.x[self.itd_ext]

        dae.f[self.Pc_tilde] = self.omega_f * (Pc - dae.x[self.Pc_tilde])

        dae.f[self.delta_c] = omega_b * delta_omega_c

        dae.f[self.Qc_tilde] = self.omega_f * (Qc - dae.x[self.Qc_tilde])

        dae.f[self.xi_d] = Vfd_ref - Vfd_int
        dae.f[self.xi_q] = Vfq_ref - Vfq_int

        dae.f[self.gamma_d] = ifd_ref - ifd_int
        dae.f[self.gamma_q] = ifq_ref - ifq_int

        self.gcall(dae)

    def finit(self, dae):
        Vswd, Vswq, ifd_ext, ifq_ext, Vfd_ext, Vfq_ext, itd_ext, itq_ext = self.filter_init(dae)

        # Initialize inner loop
        delta_c, Vref, xi_d, xi_q, gamma_d, gamma_q, Pc_tilde, Qc_tilde = self.inner_loop_init(dae, ifd_ext, ifq_ext, Vfd_ext, Vfq_ext, Vswd, Vswq)

        Pref = Pc_tilde
        Qref = Qc_tilde

        # solution = [itd_ext, itq_ext, Vfd_ext, Vfq_ext, ifd_ext, ifq_ext, Pc_tilde, delta_c,
        #             Qc_tilde, xi_d, xi_q, gamma_d, gamma_q, Pref, Vref, Qref] # Note: needs to be in the same order as self._states and self._setpoints

        solution = [Vfd_ext, Vfq_ext, ifd_ext, ifq_ext, itd_ext, itq_ext, Pc_tilde, delta_c,
                    Qc_tilde, xi_d, xi_q, gamma_d, gamma_q, Pref, Qref, Vref]

        solution = np.array(solution)

        # put solution into the correct order so that the right values are loaded into xinit and the setpoints
        states_solution = [item for sublist in np.transpose(solution[:self.ns]) for item in sublist]
        setpoints_solution = solution[self.ns:].flatten()
        solution = np.concatenate((states_solution, setpoints_solution))

        # Find the indices of differential equations for this type of generator
        diff = [self.__dict__[arg] for arg in self.states]
        diff_index = [item for sublist in np.transpose(diff) for item in sublist]

        # Now load the initial states into DAE class such that simulation/estimation actually starts from those values
        dae.xinit[diff_index] = solution[:self.ns * self.n]

        # Load initial setpoint values
        for idx, s in enumerate(self._setpoints):
            self.__dict__[s] = solution[(self.ns + idx) * self.n:(idx + 1 + self.ns) * self.n]

