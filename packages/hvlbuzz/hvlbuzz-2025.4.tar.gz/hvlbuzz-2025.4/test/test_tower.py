"""Test suite for hvlbuzz.physics.tower.Tower."""

import numpy as np

from hvlbuzz.physics.tower import Tower

from .example_systems import create_420_kv_ac_systems, create_hybrid_systems


def create_ac_tower() -> Tower:
    """Create a tower instance for testing."""
    return Tower(num_contour=120, systems=create_420_kv_ac_systems())


def create_ac_dc_tower() -> Tower:
    """Create a tower instance for testing."""
    return Tower(num_contour=120, systems=create_hybrid_systems())


def test_calc_magnetic_field() -> None:
    """Check AC magnetic fields."""
    tower = create_ac_tower()
    ground_points = np.arange(-50.0, 50.5, 10.0)  # (not including 50.5)
    height_above_ground = 1.0
    assert tower.calc_magnetic_field(ground_points, height_above_ground)
    expected_b_ac = np.array(
        [
            1.18668067,  # -50
            2.06655993,  # -40
            3.84583962,  # -30
            7.49292302,  # -20
            13.59221128,  # -10
            18.59573725,  # 0
            17.56050665,  # 10
            10.88729982,  # 20
            6.07530656,  # 30
            3.56088208,  # 40
            2.23334125,  # 50
        ]
    )
    np.testing.assert_allclose(tower.B_ac, expected_b_ac)
    np.testing.assert_allclose(tower.B_dc, 0.0)


def test_calc_magnetic_field_ac_dc() -> None:
    """Check AC and DC magnetic fields."""
    tower = create_ac_dc_tower()
    ground_points = np.arange(-50.0, 50.5, 10.0)  # (not including 50.5)
    height_above_ground = 1.0
    assert tower.calc_magnetic_field(ground_points, height_above_ground)
    expected_b_ac = np.array(
        [
            2.24722419,  # -50
            3.06381684,  # -40
            4.3607552,  # -30
            6.52434095,  # -20
            10.25012425,  # -10
            16.00987629,  # 0
            18.85115832,  # 10
            13.70426307,  # 20
            8.60337173,  # 30
            5.55042869,  # 40
            3.77409964,  # 50
        ]
    )
    expected_b_dc = np.array(
        [
            1.72019248,  # -50
            2.38389232,  # -40
            3.31979635,  # -30
            4.39889371,  # -20
            5.0152964,  # -10
            4.5898795,  # 0
            3.56118111,  # 10
            2.58642144,  # 20
            1.86830679,  # 30
            1.37554702,  # 40
            1.03933753,  # 50
        ]
    )
    np.testing.assert_allclose(tower.B_ac, expected_b_ac)
    np.testing.assert_allclose(tower.B_dc, expected_b_dc)


def test_calc_currents() -> None:
    """Check system currents."""
    tower = create_ac_tower()
    I_ac, I_dc = tower.calc_currents()
    zeta = np.exp(-1j * 2.0 * np.pi / 3)
    np.testing.assert_allclose(
        I_ac,
        [
            1265.0,
            1265.0,
            1265.0 * zeta,
            1265.0 * zeta,
            1265.0 * zeta**2,
            1265.0 * zeta**2,
            975.0,
            975.0,
            975.0 * zeta,
            975.0 * zeta,
            975.0 * zeta**2,
            975.0 * zeta**2,
            0.0,
        ],
    )
    np.testing.assert_allclose(I_dc, 0.0)


def test_calc_currents_ac_dc() -> None:
    """Check system currents."""
    tower = create_ac_dc_tower()
    I_ac, I_dc = tower.calc_currents()
    zeta = np.exp(-1j * 2.0 * np.pi / 3)
    np.testing.assert_allclose(
        I_ac,
        [
            1265.0,
            1265.0,
            1265.0 * zeta,
            1265.0 * zeta,
            1265.0 * zeta**2,
            1265.0 * zeta**2,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
    )
    np.testing.assert_allclose(
        I_dc,
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1000.0,
            1000.0,
            -1000.0,
            -1000.0,
            0.0,
            0.0,
        ],
    )


def test_calc_electric_field() -> None:
    """Check AC electric fields."""
    tower = create_ac_tower()
    ground_points = np.arange(-60.0, 60.5, 10.0)  # (not including 60.5)
    height_above_ground = 1.0
    assert tower.calc_electric_field(ground_points, height_above_ground)
    expected_e_ac_ground = np.array(
        [
            0.022092536849252768,  # -60
            0.05518420003745094,  # -50
            0.13340399549807883,  # -40
            0.32581059024666487,  # -30
            0.7835570439750872,  # -20
            1.1669312960612392,  # -10
            1.6874779936673123,  # 0
            3.2769437176021294,  # 10
            1.5736748425327867,  # 20
            0.4899938439364043,  # 30
            0.18290551386839374,  # 40
            0.12248946972151138,  # 50
            0.10352610437095844,  # 60
        ]
    )
    np.testing.assert_allclose(tower.E_ac_ground, expected_e_ac_ground)
    np.testing.assert_allclose(tower.E_dc_ground, 0.0)


def test_calc_electric_field_ac_dc() -> None:
    """Check AC and DC electric fields."""
    tower = create_ac_dc_tower()
    ground_points = np.arange(-60.0, 60.5, 10.0)  # (not including 60.5)
    height_above_ground = 1.0
    assert tower.calc_electric_field(ground_points, height_above_ground)
    expected_e_ac_ground = np.array(
        [
            0.09415402024865299,  # -60
            0.1042620999575971,  # -50
            0.10441921446220173,  # -40
            0.07297073269016173,  # -30
            0.12461061142333994,  # -20
            0.7427281356012887,  # -10
            2.520973770729131,  # 0
            3.5930245777540124,  # 10
            1.6282989346712475,  # 20
            0.4736210412667247,  # 30
            0.20150268452578485,  # 40
            0.17637944277327922,  # 50
            0.15976170935799816,  # 60
        ]
    )
    expected_e_dc_ground = np.array(
        [
            0.017486290585237204,  # -60
            0.08489613049122142,  # -50
            0.3136233509058645,  # -40
            0.7574823786680219,  # -30
            1.3126738195575498,  # -20
            1.389473230405492,  # -10
            0.8805278233621988,  # 0
            0.28934161668088154,  # 10
            0.025492714272303926,  # 20
            0.1277147944378494,  # 30
            0.1541145320953777,  # 40
            0.14817946792974174,  # 50
            0.13203911219933756,  # 60
        ]
    )
    np.testing.assert_allclose(tower.E_ac_ground, expected_e_ac_ground)
    np.testing.assert_allclose(tower.E_dc_ground, expected_e_dc_ground)


def test_calc_ave_max_conductor_surface_gradient() -> None:
    """Check surface gradients."""
    tower = create_ac_tower()
    assert tower.calc_ave_max_conductor_surface_gradient()
    e_ac = np.array([line.E_ac for system in tower.systems for line in system.lines])
    e_dc = np.array([line.E_dc for system in tower.systems for line in system.lines])
    expected_e_ac = np.array(
        [17.065661, 17.183843, 16.295271, 12.085395, 11.878453, 11.971882, 1.332797]
    )
    np.testing.assert_allclose(e_ac, expected_e_ac, rtol=2e-07)
    np.testing.assert_allclose(e_dc, 0.0)


def test_calc_ave_max_conductor_surface_gradient_for_ac_dc() -> None:
    """Check surface gradients."""
    tower = create_ac_dc_tower()
    assert tower.calc_ave_max_conductor_surface_gradient()
    e_ac = np.array([line.E_ac for system in tower.systems for line in system.lines])
    e_dc = np.array([line.E_dc for system in tower.systems for line in system.lines])
    expected_e_ac = np.array(
        [16.819703, 17.183268, 15.772227, 2.310766, 1.744768, 0.455796, 0.608085]
    )
    expected_e_dc = np.array(
        [0.362669, -0.037602, -1.387532, -3.421853, 32.247164, -33.353473, 3.526994]
    )
    np.testing.assert_allclose(e_ac, expected_e_ac, rtol=1e-06)
    np.testing.assert_allclose(e_dc, expected_e_dc, rtol=1e-05)
