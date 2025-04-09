"""Pydantic model for the input of `Wannier90` version `latest`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from wannier90_input.models.template import Wannier90InputTemplate
from wannier90_input.models.parameters import (
    AtomFrac,
    AtomCart,
    Projection,
    DisentanglementSphere,
    CentreConstraint,
    SpecialPoint,
    Projection,
    NearestNeighborKpoint,
    Coordinate,
    FractionalCoordinate,
)


class Wannier90Input(Wannier90InputTemplate):
    """Pydantic model for the input of `Wannier90.`"""

    num_wann: int = Field(..., description="Number of WF")
    num_bands: int = Field(-1, description="Number of bands passed to the code")
    unit_cell_cart: list[Coordinate] = Field(
        description="Unit cell in cartesian coordinates", min_length=3, max_length=3
    )
    atoms_cart: list[AtomCart] | None = Field(
        None, description="Positions of atoms in Cartesian coordinates"
    )
    atoms_frac: list[AtomFrac] | None = Field(
        None, description="Positions of atoms in fractional coordinates"
    )
    mp_grid: tuple[int, int, int] = Field(
        ..., description="Dimensions of the Monkhorst-Pack grid of k-points"
    )
    kpoints: list[FractionalCoordinate] = Field(
        default_factory=list, description="k-points in relative crystallographic units"
    )
    gamma_only: bool = Field(
        False, description="Wavefunctions from underlying ab initio calculation are manifestly real"
    )
    spinors: bool = Field(False, description="WF are spinors")
    shell_list: list[int] = Field(
        default_factory=list, description="Which shells to use in finite difference formula"
    )
    search_shells: int = Field(
        36, description="The number of shells to search when determining finite difference formula"
    )
    skip_B1_tests: bool = Field(False, description="Check the condition B1 of Ref [@marzari-prb97]")
    nnkpts: list[NearestNeighborKpoint] = Field(
        default_factory=list, description="Explicit list of nearest-neighbour k-points"
    )
    kmesh_tol: float = Field(
        1e-06, description="The tolerance to control if two kpoint belong to the same shell"
    )
    higher_order_n: int = Field(
        1, description="The order of higher-order finite difference to get b-vectors and weights"
    )
    higher_order_nearest_shells: bool = Field(
        False, description="Use the b-vectors on the nearest shells"
    )
    postproc_setup: bool = Field(False, description="To output the `seedname.nnkp` file")
    exclude_bands: list[int] = Field(
        default_factory=list, description="List of bands to exclude from the calculation"
    )
    select_projections: list[int] = Field(
        default_factory=list, description="List of projections to use in Wannierisation"
    )
    auto_projections: bool = Field(
        False, description="To automatically generate initial projections"
    )
    restart: Literal["default", "wannierise", "plot", "transport"] = Field(
        "default", description="Restart from checkpoint file"
    )
    iprint: int = Field(1, description="Output verbosity level")
    length_unit: Literal["Ang", "Bohr"] = Field(
        "Ang", description="System of units to output lengths"
    )
    wvfn_formatted: bool = Field(
        False, description="Read the wavefunctions from a (un)formatted file"
    )
    spin: Literal["up", "down"] = Field("up", description="Which spin channel to read")
    timing_level: int = Field(
        1, description="Determines amount of timing information written to output"
    )
    optimisation: int = Field(3, description="Optimisation level")
    translate_home_cell: bool = Field(
        False,
        description="To translate final Wannier centres to home unit cell when writing xyz file",
    )
    write_xyz: bool = Field(
        False, description="To write atomic positions and final centres in xyz file format"
    )
    write_vdw_data: bool = Field(
        False, description="To write data for futher processing by w90vdw utility"
    )
    write_hr_diag: bool = Field(
        False,
        description="To write the diagonal elements of the Hamiltonian in the Wannier basis to `seedname.wout` (in eV)",
    )
    dis_win_min: float | None = Field(None, description="Bottom of the outer energy window")
    dis_win_max: float | None = Field(None, description="Top of the outer energy window")
    dis_froz_min: float | None = Field(
        None, description="Bottom of the inner (frozen) energy window"
    )
    dis_froz_max: float | None = Field(None, description="Top of the inner (frozen) energy window")
    dis_froz_proj: bool = Field(False, description="To activate projectability disentanglement")
    dis_proj_min: float = Field(
        0.01, description="Lower threshold for projectability disentanglement"
    )
    dis_proj_max: float = Field(
        0.95, description="Upper threshold for projectability disentanglement"
    )
    dis_num_iter: int = Field(
        200, description="Number of iterations for the minimisation of $\\Omega_{\\mathrm{I}}$"
    )
    dis_mix_ratio: float = Field(
        0.5, description="Mixing ratio during the minimisation of $\\Omega_{\\mathrm{I}}$"
    )
    dis_conv_tol: float = Field(
        1e-10, description="The convergence tolerance for finding $\\Omega_{\\mathrm{I}}$"
    )
    dis_conv_window: int = Field(
        3,
        description="The number of iterations over which convergence of $\\Omega_{\\mathrm{I}}$ is assessed.",
    )
    dis_spheres_num: int = Field(
        0, description="Number of spheres in k-space where disentaglement is performed"
    )
    dis_spheres_first_wann: int = Field(
        1, description="Index of the first band to be considered a Wannier function"
    )
    dis_spheres: list[DisentanglementSphere] = Field(
        default_factory=list,
        description="List of centres and radii, for disentanglement only in spheres",
    )
    num_iter: int = Field(100, description="Number of iterations for the minimisation of $\\Omega$")
    num_cg_steps: int = Field(
        5,
        description="During the minimisation of $\\Omega$ the number of Conjugate Gradient steps before resetting to Steepest Descents",
    )
    conv_window: int = Field(
        3, description="The number of iterations over which convergence of $\\Omega$ is assessed"
    )
    conv_tol: float = Field(1e-10, description="The convergence tolerance for finding $\\Omega$")
    precond: bool = Field(False, description="Use preconditioning")
    conv_noise_amp: float = Field(
        -1.0,
        description="The amplitude of random noise applied towards end of minimisation procedure",
    )
    conv_noise_num: int = Field(3, description="The number of times random noise is applied")
    num_dump_cycles: int = Field(100, description="Control frequency of check-pointing")
    num_print_cycles: int = Field(1, description="Control frequency of printing")
    write_r2mn: bool = Field(False, description="Write matrix elements of $r^2$ between WF to file")
    guiding_centres: bool = Field(False, description="Use guiding centres")
    num_guide_cycles: int = Field(1, description="Frequency of guiding centres")
    num_no_guide_iter: int = Field(
        0, description="The number of iterations after which guiding centres are used"
    )
    trial_step: float = Field(
        2.0,
        description="The trial step length for the parabolic line search during the minimisation of $\\Omega$",
    )
    fixed_step: float = Field(
        -999.0,
        description="The fixed step length to take during the minimisation of $\\Omega$, instead of doing a parabolic line search",
    )
    use_bloch_phases: bool = Field(False, description="To use phases for initial projections")
    site_symmetry: bool = Field(
        False, description="To construct symmetry-adapted Wannier functions"
    )
    symmetrize_eps: float = Field(
        0.001, description="The convergence tolerance used in the symmetry-adapted mode"
    )
    slwf_num: int | None = Field(
        None, description="The number of objective WFs for selective localization"
    )
    slwf_constrain: bool = Field(
        False, description="Whether to constrain the centres of the objective WFs"
    )
    slwf_lambda: float = Field(
        0.0, description="Value of the Lagrange multiplier for constraining the objective WFs"
    )
    slwf_centres: list[CentreConstraint] = Field(
        default_factory=list,
        description="The centres to which the objective WFs are to be constrained",
    )
    wannier_plot: bool = Field(False, description="Plot the WF")
    wannier_plot_list: list[int] = Field(default_factory=list, description="List of WF to plot")
    wannier_plot_supercell: int = Field(2, description="Size of the supercell for plotting the WF")
    wannier_plot_format: Literal["xcrysden", "cube"] = Field(
        "xcrysden", description="File format in which to plot the WF"
    )
    wannier_plot_mode: Literal["crystal", "molecule"] = Field(
        "crystal", description="Mode in which to plot the WF, molecule or crystal"
    )
    wannier_plot_radius: float = Field(3.5, description="Cut-off radius of WF")
    wannier_plot_scale: float = Field(1.0, description="Scaling parameter for cube files")
    wannier_plot_spinor_mode: Literal["total", "up", "down"] = Field(
        "total", description="Quantity to plot for spinor WF"
    )
    wannier_plot_spinor_phase: bool = Field(
        True, description="Include the “phase” when plotting spinor WF"
    )
    bands_plot: bool = Field(False, description="Plot interpolated band structure")
    kpoint_path: list[tuple[SpecialPoint, SpecialPoint]] = Field(
        default_factory=list, description="K-point path for the interpolated band structure"
    )
    bands_num_points: int = Field(
        100, description="Number of points along the first section of the k-point path"
    )
    bands_plot_format: Literal["gnuplot", "xmgrace"] = Field(
        "gnuplot", description="File format in which to plot the interpolated bands"
    )
    bands_plot_project: list[int] = Field(
        default_factory=list, description="WF to project the band structure onto"
    )
    bands_plot_mode: Literal["s-k", "cut"] = Field(
        "s-k", description="Slater-Koster type interpolation or Hamiltonian cut-off"
    )
    bands_plot_dim: Annotated[int, Field(ge=1, le=3)] = Field(
        3, description="Dimension of the system"
    )
    fermi_surface_plot: bool = Field(False, description="Plot the Fermi surface")
    fermi_surface_num_points: int = Field(
        50, description="Number of points in the Fermi surface plot"
    )
    fermi_energy: float = Field(0.0, description="The Fermi energy")
    fermi_energy_min: float | None = Field(
        None, description="Lower limit of the Fermi energy range"
    )
    fermi_energy_max: float | None = Field(
        None, description="Upper limit of the Fermi energy range"
    )
    fermi_energy_step: float = Field(
        0.01, description="Step for increasing the Fermi energy in the specified range"
    )
    fermi_surface_plot_format: Literal["xcrysden"] = Field(
        "xcrysden", description="File format for the Fermi surface plot"
    )
    hr_plot: bool = Field(
        False, description="This parameter is not used anymore. Use write_hr instead."
    )
    write_hr: bool = Field(False, description="Write the Hamiltonian in the WF basis")
    write_rmn: bool = Field(False, description="Write the position operator in the WF basis")
    write_bvec: bool = Field(
        False, description="Write to file the matrix elements of the bvectors and their weights"
    )
    write_tb: bool = Field(
        False, description="Write lattice vectors, Hamiltonian, and position operator in WF basis"
    )
    hr_cutoff: float = Field(0.0, description="Cut-off for the absolute value of the Hamiltonian")
    dist_cutoff: float = Field(1000.0, description="Cut-off for the distance between WF")
    dist_cutoff_mode: Literal["three_dim", "two_dim", "one_dim"] = Field(
        "three_dim", description="Dimension in which the distance between WF is calculated"
    )
    translation_centre_frac: FractionalCoordinate | None = Field(
        None, description="Centre of the translation vector"
    )
    use_ws_distance: bool = Field(
        True,
        description="Improve interpolation using minimum distance between WFs, see Chap. [Some notes on the interpolation](notes_interpolations.md)",
    )
    ws_distance_tol: float = Field(
        1e-05, description="Absolute tolerance for the distance to equivalent positions."
    )
    ws_search_size: int = Field(
        2,
        description="Maximum extension in each direction of the super-cell of the Born-von Karmann cell to search for points inside the Wigner-Seitz cell",
    )
    write_u_matrices: bool = Field(
        False, description="Write $U^{(\\bm{k})}$ and $U^{dis(\\bm{k})}$ matrices to files"
    )
    transport: bool = Field(
        False, description="Calculate quantum conductance and density of states"
    )
    transport_mode: Literal["bulk", "lcr"] = Field(
        "bulk", description="Bulk or left-lead_conductor_right-lead calculation"
    )
    tran_win_min: float = Field(
        -3.0, description="Bottom of the energy window for transport calculation"
    )
    tran_win_max: float = Field(
        3.0, description="Top of the energy window for transport calculation"
    )
    tran_energy_step: float = Field(0.01, description="Sampling interval of the energy values")
    tran_num_bb: int = Field(0, description="Size of a bulk Hamiltonian")
    tran_num_ll: int = Field(0, description="Size of a left-lead Hamiltonian")
    tran_num_rr: int = Field(0, description="Size of a right-lead Hamiltonian")
    tran_num_cc: int = Field(0, description="Size of a conductor Hamiltonian")
    tran_num_lc: int = Field(
        0, description="Number of columns in a left-lead_conductor Hamiltonian"
    )
    tran_num_cr: int = Field(0, description="Number of rows in a conductor_right-lead Hamiltonian")
    tran_num_cell_ll: int = Field(0, description="Number of unit cells in PL of left lead")
    tran_num_cell_rr: int = Field(0, description="Number of unit cells in PL of right lead")
    tran_num_bandc: int = Field(
        0, description="Half-bandwidth+1 of a band-diagonal conductor Hamiltonian"
    )
    tran_write_ht: bool = Field(
        False, description="Write the Hamiltonian for transport calculation"
    )
    tran_read_ht: bool = Field(False, description="Read the Hamiltonian for transport calculation")
    tran_use_same_lead: bool = Field(False, description="Left and right leads are the same")
    tran_group_threshold: float = Field(
        0.15, description="Distance that determines the grouping of WFs"
    )
    one_dim_axis: Literal["x", "y", "z", None] = Field(
        None, description="Extended direction for a one-dimensional system"
    )
    projections: list[Projection] = Field(
        default_factory=list, description="Projections for the Wannier functions"
    )
