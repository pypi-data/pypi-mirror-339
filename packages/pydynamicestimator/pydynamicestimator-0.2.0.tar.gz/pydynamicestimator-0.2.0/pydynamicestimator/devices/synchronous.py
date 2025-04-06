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


from __future__ import annotations  # Postponed type evaluation
from typing import TYPE_CHECKING
from typing import Tuple

import casadi

if TYPE_CHECKING:
    from pydynamicestimator.system import *
from pydynamicestimator.devices.device import *


class SynchronousTransient(Synchronous):
    """Transient two-axis SG with TGOV1 governor and IEEEDC1A AVR"""

    def __init__(self) -> None:
        super().__init__()

        self._type = "Synchronous_machine"
        self._name = 'Synchronous_machine_transient_model'

        # States
        self.ns += 2
        self.states.extend(['e_dprim', 'e_qprim'])
        self.e_dprim = np.array([], dtype=float)
        self.e_qprim = np.array([], dtype=float)

        self._states_noise.update({'e_dprim': 1, 'e_qprim': 1, })
        self._states_init_error.update({'e_dprim': 0.1, 'e_qprim': 0.1})
        self._x0.update({'delta': 0.0, 'omega': 0.0, 'e_dprim': -0.4, 'e_qprim': 1, 'psv': 0.5, 'pm': 0.5, 'Efd': 2.5, 'Rf': 0.0, 'Vr': 2.5})

        # Params
        self._params.update({'x_dprim': 0.05, 'x_qprim': 0.1, 'T_dprim': 8.0, 'T_qprim': 0.8})
        self._descr.update({'T_dprim': 'd-axis transient time constant', 'T_qprim': 'q-axis transient time constant', 'e_dprim': 'd-axis voltage behind transient reactance',
                            'e_qprim': 'q-axis voltage behind transient reactance', 'x_dprim': 'd-axis transient reactance', 'x_qprim': 'q-axis transient reactance'})

        # Parameters
        self.x_dprim = np.array([], dtype=float)
        self.x_qprim = np.array([], dtype=float)
        self.T_dprim = np.array([], dtype=float)
        self.T_qprim = np.array([], dtype=float)

        self.properties.update(
            {'fgcall': True, 'finit': True, 'init_data': True, 'xy_index': True, 'save_data': True, 'qcall': True, 'gcall': True})

        self._init_data()

    def input_current(self, dae: Dae) -> Tuple[casadi.SX, casadi.SX]:
        # differential equations
        i_d = SX.sym('id', self.n)
        i_q = SX.sym('iq', self.n)
        for i in range(self.n):
            adq = SX([[self.R_s[i], -self.x_qprim[i]], [self.x_dprim[i], self.R_s[i]]])
            vd = dae.y[self.vre[i]] * sin(dae.x[self.delta[i]]) + dae.y[self.vim[i]] * -cos(dae.x[self.delta[i]])
            vq = dae.y[self.vre[i]] * cos(dae.x[self.delta[i]]) + dae.y[self.vim[i]] * sin(dae.x[self.delta[i]])
            b1 = -vd + dae.x[self.e_dprim[i]]
            b2 = -vq + dae.x[self.e_qprim[i]]
            b = vertcat(b1, b2)
            i_dq = solve(adq, b) * dae.Sb / self.Sn[i]  # scale the current for the base power inside the machine
            i_d[i] = i_dq[0]
            i_q[i] = i_dq[1]
        return i_d, i_q

    def two_axis(self, dae, i_d: casadi.SX, i_q: casadi.SX):
        dae.f[self.delta] = 2 * np.pi * self.fn * dae.x[self.omega]
        dae.f[self.omega] = 1 / (2 * self.H) * (
                dae.x[self.pm] - dae.x[self.e_dprim] * i_d - dae.x[self.e_qprim] * i_q - (self.x_qprim - self.x_dprim) * i_d * i_q - self.D * dae.x[self.omega] - self.f * (
                dae.x[self.omega] + 1))  # omega
        dae.f[self.e_qprim] = 1 / self.T_dprim * (-dae.x[self.e_qprim] + dae.x[self.Efd] - (self.x_d - self.x_dprim) * i_d)  # Eq
        dae.f[self.e_dprim] = 1 / self.T_qprim * (-dae.x[self.e_dprim] + (self.x_q - self.x_qprim) * i_q)  # Ed

    def fgcall(self, dae: Dae) -> None:
        i_d, i_q = self.input_current(dae)

        self.two_axis(dae, i_d, i_q)

        self.tgov1(dae)

        self.ieeedc1a(dae)

        self.gcall(dae, i_d, i_q)


class SynchronousSubtransient(Synchronous):
    """Subtransient Anderson Fouad SG with TGOV1 governor and IEEEDC1A AVR"""

    def __init__(self) -> None:
        super().__init__()

        # private data
        self._type = "Synchronous_machine"
        self._name = 'Synchronous_machine_subtransient_model'

        # States
        self.ns += 4
        self.states.extend(['e_dprim', 'e_qprim', 'e_dsec', 'e_qsec'])
        self.e_dprim = np.array([], dtype=float)
        self.e_qprim = np.array([], dtype=float)
        self.e_dsec = np.array([], dtype=float)
        self.e_qsec = np.array([], dtype=float)
        self._states_noise.update({'e_dprim': 1, 'e_qprim': 1, 'e_dsec': 1, 'e_qsec': 1})
        self._states_init_error.update({'e_dprim': 0.1, 'e_qprim': 0.1, 'e_dsec': 0.1, 'e_qsec': 0.1})

        self._x0.update({'delta': 0.0, 'omega': 0.0, 'e_dprim': 0.0, 'e_qprim': 1.0, 'psv': 0.5, 'pm': 0.5, 'Efd': 2.3, 'Rf': 0.0, 'Vr': 2.3, 'e_dsec': 0.0, 'e_qsec': 1.0})


        # Params
        self._params.update({'x_dprim': 0.05, 'x_qprim': 0.1, 'T_dprim': 8.0, 'T_qprim': 0.8, 'x_dsec': 0.01, 'x_qsec': 0.01, 'T_dsec': 0.001, 'T_qsec': 0.001})

        self._descr.update({'T_dprim': 'd-axis transient time constant', 'T_qprim': 'q-axis transient time constant', 'x_dprim': 'd-axis transient reactance',
                            'x_qprim': 'q-axis transient reactance', 'e_dprim': 'd-axis voltage behind transient reactance',
                            'e_qprim': 'q-axis voltage behind transient reactance', 'e_dsec': 'd-axis voltage behind subtransient reactance',
                            'e_qsec': 'q-axis voltage behind subtransient reactance', 'T_dsec': 'd-axis subtransient time constant', 'T_qsec': 'q-axis subtransient time constant',
                            'x_dsec': 'd-axis subtransient reactance', 'x_qsec': 'q-axis subtransient reactance', })

        # Parameters
        self.x_dprim = np.array([], dtype=float)
        self.x_qprim = np.array([], dtype=float)
        self.T_dprim = np.array([], dtype=float)
        self.T_qprim = np.array([], dtype=float)
        self.x_dsec = np.array([], dtype=float)
        self.x_qsec = np.array([], dtype=float)
        self.T_dsec = np.array([], dtype=float)
        self.T_qsec = np.array([], dtype=float)

        self.properties.update(
            {'fgcall': True, 'finit': True, 'init_data': True, 'xy_index': True, 'save_data': True, 'qcall': True})

        self._init_data()

    def input_current(self, dae: Dae) -> Tuple[casadi.SX, casadi.SX]:
        # differential equations
        i_d = SX.sym('Id', self.n)
        i_q = SX.sym('Iq', self.n)
        for i in range(self.n):
            adq = SX([[self.R_s[i], -self.x_qsec[i]], [self.x_dsec[i], self.R_s[i]]])
            vd = dae.y[self.vre[i]] * sin(dae.x[self.delta[i]]) + dae.y[self.vim[i]] * -cos(dae.x[self.delta[i]])
            vq = dae.y[self.vre[i]] * cos(dae.x[self.delta[i]]) + dae.y[self.vim[i]] * sin(dae.x[self.delta[i]])
            b1 = -vd + dae.x[self.e_dsec[i]]
            b2 = -vq + dae.x[self.e_qsec[i]]
            b = vertcat(b1, b2)
            i_dq = solve(adq, b) * dae.Sb / self.Sn[i]  # scale the current for the base power inside the machine
            i_d[i] = i_dq[0]
            i_q[i] = i_dq[1]
        return i_d, i_q

    def anderson_fouad(self, dae: Dae, i_d: casadi.SX, i_q: casadi.SX):
        dae.f[self.delta] = 2 * np.pi * self.fn * dae.x[self.omega]
        dae.f[self.omega] = 1 / (2 * self.H) * (
                dae.x[self.pm] - dae.x[self.e_dsec] * i_d - dae.x[self.e_qsec] * i_q - (self.x_qsec - self.x_dsec) * i_d * i_q - self.D * dae.x[self.omega] - self.f * (
                dae.x[self.omega] + 1))  # omega
        dae.f[self.e_qprim] = 1 / self.T_dprim * (-dae.x[self.e_qprim] + dae.x[self.Efd] - (self.x_d - self.x_dprim) * i_d)  # Eq
        dae.f[self.e_dprim] = 1 / self.T_qprim * (-dae.x[self.e_dprim] + (self.x_q - self.x_qprim) * i_q)  # Ed
        dae.f[self.e_qsec] = 1 / self.T_dsec * (dae.x[self.e_qprim] - dae.x[self.e_qsec] - (self.x_dprim - self.x_dsec) * i_d)
        dae.f[self.e_dsec] = 1 / self.T_qsec * (dae.x[self.e_dprim] - dae.x[self.e_dsec] + (self.x_qprim - self.x_qsec) * i_q)

    def fgcall(self, dae: Dae) -> None:
        i_d, i_q = self.input_current(dae)

        self.anderson_fouad(dae, i_d, i_q)

        self.tgov1(dae)

        self.ieeedc1a(dae)

        self.gcall(dae, i_d, i_q)


class SynchronousSubtransientSP(Synchronous):
    """Subtransient Sauper and Pai SG model with stator dynamics with TGOV1 governor and IEEEDC1A AVR"""

    def __init__(self) -> None:
        super().__init__()

        # private data
        self._type = "Synchronous_machine"
        self._name = 'Synchronous_machine_subtransient_model_Sauer_Pai'

        # States
        self.ns += 6
        self.states.extend(['e_dprim', 'e_qprim', 'psid', 'psiq', 'psid2', 'psiq2'])
        self.e_dprim = np.array([], dtype=float)
        self.e_qprim = np.array([], dtype=float)
        self.psid = np.array([], dtype=float)
        self.psiq = np.array([], dtype=float)
        self.psid2 = np.array([], dtype=float)
        self.psiq2 = np.array([], dtype=float)
        self._states_noise.update({'e_dprim': 1.0, 'e_qprim': 1.0, 'psid': 1.0, 'psiq': 1.0, 'psid2': 1.0, 'psiq2': 1.0})
        self._states_init_error.update({'e_dprim': 0.1, 'e_qprim': 0.1, 'psid': 0.1, 'psiq': 0.1, 'psid2': 0.1, 'psiq2': 0.1})

        self._x0.update(
            {'delta': 0.5, 'omega': 0.0, 'e_dprim': 0.2, 'e_qprim': 1.0, 'psid': 1.0, 'psiq': -0.5, 'psid2': 1.0, 'psiq2': -0.5, 'psv': 0.5, 'pm': 0.5, 'Efd': 2.3, 'Rf': 0.0,
             'Vr': 2.3})

        # Params
        self._params.update(
            {'gd1': 1.0, 'gq1': 1.0, 'gd2': 1.0, 'gq2': 1.0, 'x_l': 0.1, 'x_dprim': 0.05, 'x_qprim': 0.1, 'T_dprim': 8.0, 'T_qprim': 0.8, 'x_dsec': 0.01, 'x_qsec': 0.01,
             'T_dsec': 0.001, 'T_qsec': 0.001})

        self._descr.update({'T_dprim': 'd-axis transient time constant', 'T_qprim': 'q-axis transient time constant', 'x_dprim': 'd-axis transient reactance',
                            'x_qprim': 'q-axis transient reactance', 'e_dprim': 'd-axis voltage behind transient reactance',
                            'e_qprim': 'q-axis voltage behind transient reactance', 'T_dsec': 'd-axis subtransient time constant', 'T_qsec': 'q-axis subtransient time constant',
                            'x_dsec': 'd-axis subtransient reactance', 'x_qsec': 'q-axis subtransient reactance', 'x_l': 'leakage reactance', 'psid': 'stator flux in d axis',
                            'psiq': 'stator flux in q axis', 'psiq2': 'subtransient stator flux in q axis', 'psid2': 'subtransient stator flux in d axis'})

        # Parameters
        self.x_l = np.array([], dtype=float)
        self.gd1 = np.array([], dtype=float)
        self.gq1 = np.array([], dtype=float)
        self.gd2 = np.array([], dtype=float)
        self.gq2 = np.array([], dtype=float)
        self.x_dprim = np.array([], dtype=float)
        self.x_qprim = np.array([], dtype=float)
        self.T_dprim = np.array([], dtype=float)
        self.T_qprim = np.array([], dtype=float)
        self.x_dsec = np.array([], dtype=float)
        self.x_qsec = np.array([], dtype=float)
        self.T_dsec = np.array([], dtype=float)
        self.T_qsec = np.array([], dtype=float)

        self.properties.update(
            {'fgcall': True, 'finit': True, 'init_data': True, 'xy_index': True, 'save_data': True, 'qcall': True})

        self._init_data()

    def sauer_pai(self, dae: Dae, i_d: casadi.SX, i_q: casadi.SX):
        vd = dae.y[self.vre] * sin(dae.x[self.delta]) + dae.y[self.vim] * -cos(dae.x[self.delta])
        vq = dae.y[self.vre] * cos(dae.x[self.delta]) + dae.y[self.vim] * sin(dae.x[self.delta])

        dae.f[self.delta] = 2 * np.pi * self.fn * dae.x[self.omega]
        dae.f[self.omega] = 1 / (2 * self.H) * (
                dae.x[self.pm] - (dae.x[self.psid] * i_q - dae.x[self.psiq] * i_d) - self.D * dae.x[self.omega] - self.f * (dae.x[self.omega] + 1))  # omega

        dae.f[self.e_dprim] = 1 / self.T_qprim * (
                    -dae.x[self.e_dprim] + (self.x_q - self.x_qprim) * (i_q - self.gq2 * dae.x[self.psiq2] - (1 - self.gq1) * i_q - self.gq2 * dae.x[self.e_dprim]))
        dae.f[self.e_qprim] = 1 / self.T_dprim * (
                -dae.x[self.e_qprim] - (self.x_d - self.x_dprim) * (i_d - self.gd2 * dae.x[self.psid2] - (1 - self.gd1) * i_d + self.gd2 * dae.x[self.e_qprim]) + dae.x[self.Efd])
        dae.f[self.psid2] = 1 / self.T_dsec * (-dae.x[self.psid2] + dae.x[self.e_qprim] - (self.x_dprim - self.x_l) * i_d)
        dae.f[self.psiq2] = 1 / self.T_qsec * (-dae.x[self.psiq2] - dae.x[self.e_dprim] - (self.x_qprim - self.x_l) * i_q)
        dae.f[self.psid] = 2 * np.pi * self.fn * (self.R_s * i_d + (1 + dae.x[self.omega]) * dae.x[self.psiq] + vd)
        dae.f[self.psiq] = 2 * np.pi * self.fn * (self.R_s * i_q - (1 + dae.x[self.omega]) * dae.x[self.psid] + vq)

    def fgcall(self, dae: Dae) -> None:
        self.gd1 = (self.x_dsec - self.x_l) / (self.x_dprim - self.x_l)
        self.gq1 = (self.x_qsec - self.x_l) / (self.x_qprim - self.x_l)
        self.gd2 = (1 - self.gd1) / (self.x_dprim - self.x_l)
        self.gq2 = (1 - self.gq1) / (self.x_qprim - self.x_l)

        i_d = 1 / self.x_dsec * (-dae.x[self.psid] + self.gd1 * dae.x[self.e_qprim] + (1 - self.gd1) * dae.x[self.psid2])
        i_q = 1 / self.x_qsec * (-dae.x[self.psiq] - self.gq1 * dae.x[self.e_dprim] + (1 - self.gq1) * dae.x[self.psiq2])

        self.sauer_pai(dae, i_d, i_q)

        self.tgov1(dae)

        self.ieeedc1a(dae)

        self.gcall(dae, i_d, i_q)
