import matplotlib.pyplot as plt
import numpy as np
from .qubit_base import QubitBase
from scipy.linalg import cosm, sinm, eigh, expm
from typing import Any, Dict, Optional, Tuple, Union, Iterable, List
from .operators import destroy, creation, sigma_z, sigma_y, sigma_x

class Ferbo(QubitBase):
    PARAM_LABELS = {
        'Ec': r'$E_C$',
        'El': r'$E_L$',
        'Gamma': r'$\Gamma$',
        'delta_Gamma': r'$\delta \Gamma$',
        'er': r'$\epsilon_r$',
        'phase': r'$\Phi_{\mathrm{ext}} / \Phi_0$'
    }
    
    OPERATOR_LABELS = {
    'n_operator': r'\hat{n}',
    'phase_operator': r'\hat{\phi}',
    'd_hamiltonian_d_ng': r'\partial \hat{H} / \partial n_g',
    'd_hamiltonian_d_phase': r'\partial \hat{H} / \partial \phi_{{ext}}',
    'd_hamiltonian_d_EL': r'\partial \hat{H} / \partial E_L',
    'd_hamiltonian_d_deltaGamma': r'\partial \hat{H} / \partial \delta \Gamma',
    'd_hamiltonian_d_er': r'\partial \hat{H} / \partial \epsilon_r',
    }
    
    def __init__(self, Ec, El, Gamma, delta_Gamma, er, phase, dimension, flux_grouping: str = 'ABS', Delta = 40):
        """
        Initializes the Ferbo class with the given parameters.

        Parameters
        ----------
        Ec : float
            Charging energy.
        El : float
            Inductive energy.
        Gamma : float
            Coupling strength.
        delta_Gamma : float
            Coupling strength difference.
        er : float
            Energy relaxation rate.
        phase : float
            External magnetic phase.
        dimension : int
            Dimension of the Hilbert space.
        flux_grouping : str, optional
            Flux grouping ('EL' or 'ABS') (default is 'EL').
        Delta : float
            Superconducting gap.
        """
        if flux_grouping not in ['EL', 'ABS']:
            raise ValueError("Invalid flux grouping; must be 'EL' or 'ABS'.")
        
        self.Ec = Ec
        self.El = El
        self.Gamma = Gamma
        self.delta_Gamma = delta_Gamma
        self.er = er
        self.phase = phase
        self.dimension = dimension // 2 * 2
        self.flux_grouping = flux_grouping
        self.Delta = Delta
        super().__init__(self.dimension)
        
    @property
    def phase_zpf(self) -> float:
        """
        Returns the zero-point fluctuation of the phase.

        Returns
        -------
        float
            Zero-point fluctuation of the phase.
        """
        return (2 * self.Ec / self.El) ** 0.25
    
    @property
    def n_zpf(self) -> float:
        """
        Returns the zero-point fluctuation of the charge number.

        Returns
        -------
        float
            Zero-point fluctuation of the charge number.
        """
        return 1/2 * (self.El / 2 / self.Ec) ** 0.25
    
    def phi_osc(self) -> float:
        """
        Returns the oscillator length for the LC oscillator composed of the inductance and capacitance.

        Returns
        -------
        float
            Oscillator length.
        """
        return (8.0 * self.Ec / self.El) ** 0.25
    
    def n_operator(self) -> np.ndarray:
        """
        Returns the charge number operator.

        Returns
        -------
        np.ndarray
            The charge number operator.
        """
        single_mode_n_operator = 1j * self.n_zpf * (creation(self.dimension //2 ) - destroy(self.dimension // 2))
        return np.kron(np.eye(2), single_mode_n_operator)
    
    def phase_operator(self) -> np.ndarray:
        """
        Returns the total phase operator.

        Returns
        -------
        np.ndarray
            The total phase operator.
        """
        single_mode_phase_operator = self.phase_zpf * (creation(self.dimension //2) + destroy(self.dimension //2))
        return np.kron(np.eye(2), single_mode_phase_operator)        
    
    def jrl_potential(self) -> np.ndarray:
        """
        Returns the Josephson Resonance Level potential.

        Returns
        -------
        np.ndarray
            The Josephson Resonance Level potential.
        """
        phase_op = self.phase_operator()[:self.dimension//2, :self.dimension//2]
        if self.flux_grouping == 'ABS':
            phase_op -= self.phase * np.eye(self.dimension // 2)
        
        return - self.Gamma * np.kron(sigma_z(), cosm(phase_op/2)) \
            - self.delta_Gamma * np.kron(sigma_y(), sinm(phase_op/2)) \
                + self.er * np.kron(sigma_x(), np.eye(self.dimension // 2))

    
    # def zazunov_potential(self) -> np.ndarray:
        
    def hamiltonian(self) -> np.ndarray:
        """
        Returns the Hamiltonian of the system.

        Returns
        -------
        np.ndarray
            The Hamiltonian of the system.
        """
        n_x = self.delta_Gamma/4/(self.Gamma+self.Delta)
        n_op = self.n_operator() + n_x * np.kron(sigma_x(),np.eye(self.dimension//2))
        
        charge_term = 4 * self.Ec * n_op @ n_op
        phase_op = self.phase_operator()
        
        if self.flux_grouping == 'ABS':
            inductive_term = 0.5 * self.El * phase_op @ phase_op
        else:
            phase_op += self.phase * np.eye(self.dimension)
            inductive_term = 0.5 * self.El * phase_op @ phase_op
            
        potential = self.jrl_potential()
        return charge_term + inductive_term + potential
    
    def d_hamiltonian_d_EL(self) -> np.ndarray:
        
        if self.flux_grouping == 'EL':
            phase_op = self.phase_operator()
        elif self.flux_grouping == 'ABS':
            phase_op = self.phase_operator() - self.phase * np.eye(self.dimension)

        return 1/2 * np.dot(phase_op, phase_op)
    
    def d_hamiltonian_d_ng(self) -> np.ndarray:
        """
        Returns the derivative of the Hamiltonian with respect to the number of charge offset.
        
        Returns
        -------
        np.ndarray
            The derivative of the Hamiltonian with respect to the number of charge offset.
        
        """
        n_x = self.delta_Gamma/4/(self.Gamma+self.Delta)
        return - 8 * self.Ec * (self.n_operator() + n_x * np.kron(sigma_x(), np.eye(self.dimension//2)))
    
    def d2_hamiltonian_d_ng2(self) -> np.ndarray:
        """
        Returns the second derivative of the Hamiltonian with respect to the number of charge offset.
        
        Returns
        -------
        np.ndarray
            The second derivative of the Hamiltonian with respect to the number of charge offset.
        
        """
        return 8 * self.Ec * np.eye(self.dimension)
    
    def d_hamiltonian_d_phase(self) -> np.ndarray:
        """
        Returns the derivative of the Hamiltonian with respect to the external magnetic phase.

        Returns
        -------
        np.ndarray
            The derivative of the Hamiltonian with respect to the external magnetic phase.
        """
        if self.flux_grouping == 'EL':
            return self.El * (self.phase_operator() + self.phase * np.eye(self.dimension))
        elif self.flux_grouping == 'ABS':
            phase_op = self.phase_operator()[:self.dimension//2,:self.dimension//2] - self.phase * np.eye(self.dimension // 2)
            return - self.Gamma/2 * np.kron(sigma_z(), sinm(phase_op/2)) + self.delta_Gamma/2 * np.kron(sigma_y(), cosm(phase_op/2))
        
    def d2_hamiltonian_d_phase2(self) -> np.ndarray:
        """
        Returns the second derivative of the Hamiltonian with respect to the external magnetic phase.

        Returns
        -------
        np.ndarray
            The second derivative of the Hamiltonian with respect to the external magnetic phase.
        """
        if self.flux_grouping == 'EL':
            return self.El * np.eye(self.dimension)
        elif self.flux_grouping == 'ABS':
            phase_op = self.phase_operator()[:self.dimension//2,:self.dimension//2] - self.phase * np.eye(self.dimension // 2)
            return self.Gamma/4 * np.kron(sigma_z(), cosm(phase_op/2)) + self.delta_Gamma/4 * np.kron(sigma_y(), sinm(phase_op/2))
        
    def d_hamiltonian_d_Gamma(self) -> np.ndarray:
        """
        Returns the derivative of the Hamiltonian with respect to Gamma.

        Returns
        -------
        np.ndarray
            The derivative of the Hamiltonian with respect to Gamma.
        """
        phase_op = self.phase_operator()[:self.dimension//2,:self.dimension//2]
        if self.flux_grouping == 'ABS':
            phase_op -= self.phase * np.eye(self.dimension // 2)
        
        return - np.kron(sigma_z(), sinm(phase_op/2))
                
    def d_hamiltonian_d_er(self) -> np.ndarray:
        """
        Returns the derivative of the Hamiltonian with respect to the energy relaxation rate.

        Returns
        -------
        Qobj
            The derivative of the Hamiltonian with respect to the energy relaxation rate.
        """
        return + np.kron(sigma_x(), np.eye(self.dimension // 2))
    
    def d_hamiltonian_d_deltaGamma(self) -> np.ndarray:
        """
        Returns the derivative of the Hamiltonian with respect to the coupling strength difference.

        Returns
        -------
        Qobj
            The derivative of the Hamiltonian with respect to the coupling strength difference.
        """
        phase_op = self.phase_operator()[:self.dimension//2,:self.dimension//2]
        if self.flux_grouping == 'ABS':
            phase_op -= self.phase * np.eye(self.dimension // 2)
            
        return - np.kron(sigma_y(), sinm(phase_op/2))
    
    def wavefunction(
        self, 
        which: int = 0,
        phi_grid: np.ndarray = None,
        esys: Tuple[np.ndarray, np.ndarray] = None,
        basis: str = 'phase',
        rotate: str = False,
        ) -> Dict[str, Any]:
        """
        Returns a wave function in the phi basis.

        Parameters
        ----------
        which : int, optional
            Index of desired wave function (default is 0).
        phi_grid : np.ndarray, optional
            Custom grid for phi; if None, a default grid is used.
        basis : str, optional
            Basis in which to return the wavefunction ('phase' or 'charge') (default is 'phase').
        rotate : bool, optional
            Whether to rotate the basis (default is False).
        Returns
        -------
        Dict[str, Any]
            Wave function data containing basis labels, amplitudes, and energy.
        """
        if esys is None:
            evals_count = max(which + 1, 3)
            evals, evecs = self.eigensys(evals_count)
        else:
            evals, evecs = esys
            
        dim = self.dimension//2
                
        if rotate:
            
            I = np.eye(self.dimension//2)
            change_of_basis_operator = (1/np.sqrt(2)) * np.block([[I, I],
                                        [I, -I]])
    
            evecs = (change_of_basis_operator @ evecs)
        
        evecs = evecs.T
        
        if basis == 'phase':
            l_osc = self.phase_zpf
        elif basis == 'charge':
            l_osc = self.n_zpf     
                                
        if phi_grid is None:
            phi_grid = np.linspace(-5 * np.pi, 5 * np.pi, 151)

        phi_basis_labels = phi_grid
        wavefunc_osc_basis_amplitudes = evecs[which, :]
        phi_wavefunc_amplitudes = np.zeros((2, len(phi_grid)), dtype=np.complex128)
        
        for n in range(dim):
            phi_wavefunc_amplitudes[0] += wavefunc_osc_basis_amplitudes[n] * self.harm_osc_wavefunction(n, phi_basis_labels, l_osc)
            phi_wavefunc_amplitudes[1] += wavefunc_osc_basis_amplitudes[self.dimension//2 + n] * self.harm_osc_wavefunction(n, phi_basis_labels, l_osc)

        return {
            "basis_labels": phi_basis_labels,
            "amplitudes": phi_wavefunc_amplitudes,
            "energy": evals[which]
        }
        
                
    def potential(self, phi: Union[float, np.ndarray]) -> np.ndarray:
        """
        Calculates the potential energy for given values of phi.

        Parameters
        ----------
        phi : Union[float, np.ndarray]
            The phase values at which to calculate the potential.

        Returns
        -------
        np.ndarray
            The potential energy values.
        """
        phi_array = np.atleast_1d(phi)
        evals_array = np.zeros((len(phi_array), 2))

        for i, phi_val in enumerate(phi_array):
            if self.flux_grouping == 'ABS':
                inductive_term = 0.5 * self.El * phi_val**2 * np.eye(2)
                andreev_term = -self.Gamma * np.cos((phi_val + self.phase) / 2) * sigma_z() - self.delta_Gamma * np.sin((phi_val + self.phase) / 2) * sigma_y() + self.er * sigma_x()
            elif self.flux_grouping == 'EL':
                inductive_term = 0.5 * self.El * (phi_val + self.phase)**2 * np.eye(2)
                andreev_term = -self.Gamma * np.cos(phi_val / 2) * sigma_z() - self.delta_Gamma * np.sin(phi_val / 2) * sigma_y() + self.er * sigma_x()
            
            potential_operator = inductive_term + andreev_term
            evals_array[i] = eigh(
                potential_operator,
                eigvals_only=True,
                check_finite=False,
        )

        return evals_array
    
    def tphi_1_over_f_flux(
        self, 
        A_noise: float = 1e-6,
        esys: Tuple[np.ndarray, np.ndarray] = None, 
        get_rate: bool = False, 
        **kwargs
        ) -> float:
        return self.tphi_1_over_f(A_noise, ['d_hamiltonian_d_phase', 'd2_hamiltonian_d_phase'], esys=esys, get_rate=get_rate, **kwargs)

    def plot_wavefunction(
        self, 
        which: Union[int, Iterable[int]] = 0, 
        phi_grid: np.ndarray = None, 
        esys: Tuple[np.ndarray, np.ndarray] = None, 
        scaling: Optional[float] = 1,
        plot_potential: bool = False,
        basis: str = 'phase',
        rotate: bool = False,
        mode: str = 'abs',
        **kwargs
        ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Plot the wave function in the phi basis.

        Parameters
        ----------
        which : Union[int, Iterable[int]], optional
            Index or indices of desired wave function(s) (default is 0).
        phi_grid : np.ndarray, optional
            Custom grid for phi; if None, a default grid is used.
        esys : Tuple[np.ndarray, np.ndarray], optional
            Precomputed eigenvalues and eigenvectors.
        scaling : float, optional
            Scaling factor for the wavefunction (default is 1).
        plot_potential : bool, optional
            Whether to plot the potential (default is False).
        basis: str, optional
            Basis in which to return the wavefunction ('phase' or 'charge') (default is 'phase').
        rotate : bool, optional
            Whether to rotate the basis (default is False).
        mode: str, optional
            Mode of the wavefunction ('abs', 'real', or 'imag') (default is 'abs').
        **kwargs
            Additional arguments for plotting. Can include:
            - fig_ax: Tuple[plt.Figure, plt.Axes], optional
                Figure and axes to use for plotting. If not provided, a new figure and axes are created.

        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            The figure and axes of the plot.
        """
        if isinstance(which, int):
            which = [which]
            
        if phi_grid is None:
            phi_grid = np.linspace(-5 * np.pi, 5 * np.pi, 151)
            
        fig_ax = kwargs.get("fig_ax")
        if fig_ax is None:
            fig, ax = plt.subplots()
            fig.suptitle(self._generate_suptitle())
        else:
            fig, ax = fig_ax
        
        if plot_potential:
            potential = self.potential(phi=phi_grid)
            ax.plot(phi_grid, potential[:, 0], color='black', label='Potential')
            ax.plot(phi_grid, potential[:, 1], color='black')

        for idx in which:
            wavefunc_data = self.wavefunction(which=idx, phi_grid=phi_grid, esys=esys, basis=basis, rotate=rotate)
            phi_basis_labels = wavefunc_data["basis_labels"]
            wavefunc_amplitudes = wavefunc_data["amplitudes"]
            wavefunc_energy = wavefunc_data["energy"]
            
            if mode == 'abs':
                y_values = np.abs(wavefunc_amplitudes[0])
                y_values_down = np.abs(wavefunc_amplitudes[1])
            elif mode == 'real':
                y_values = wavefunc_amplitudes[0].real
                y_values_down = wavefunc_amplitudes[1].real
            elif mode == 'imag':
                y_values = wavefunc_amplitudes[0].imag
                y_values_down = wavefunc_amplitudes[1].imag
            else:
                raise ValueError("Invalid mode; must be 'abs', 'real', or 'imag'.")

            ax.plot(
                phi_basis_labels,
                wavefunc_energy + scaling * y_values,
                label=rf"$\Psi_{idx} \uparrow $"
                )
            ax.plot(
                phi_basis_labels, 
                wavefunc_energy + scaling * y_values_down,
                label=rf"$\Psi_{idx} \downarrow $"
                )
            
        if basis == 'phase':
            ax.set_xlabel(r"$2 \pi \Phi / \Phi_0$")
            ax.set_ylabel(r"$\psi(\varphi)$, Energy [GHz]")
        elif basis == 'charge':
            ax.set_xlabel(r"$n$")
            ax.set_ylabel(r"$\psi(n)$, Energy [GHz]")
        
        ax.legend()
        ax.grid(True)

        return fig, ax      