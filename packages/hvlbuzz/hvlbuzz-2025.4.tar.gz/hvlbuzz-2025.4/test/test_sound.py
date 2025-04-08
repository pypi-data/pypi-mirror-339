"""Test suite for hvlbuzz.physics.tower.Tower."""

import numpy as np

from hvlbuzz.physics import sound
from hvlbuzz.physics.line import LineType
from hvlbuzz.physics.sound import Season, Weather

from .example_systems import (
    create_380_kv_ac_systems,
    create_420_kv_ac_systems,
    create_hybrid_systems,
    create_line,
)

GROUND_POINTS = np.vstack(
    (
        np.arange(-60.0, 60.5, 10.0),  # (not including 60.5)
        np.full((13,), 0.0),
    )
)


LINE = create_line(
    line_type=LineType.ac_r,
    line_x=9.0,
    line_y=16.0,
    con_radius=0.015,
    num_con=2,
    bundle_radius=0.2,
    con_angle_offset=0.0,
    E_ac=17.0,
    E_ac_pos_offset=0.0,
    E_ac_neg_offset=0.0,
)


def test_rain_correction_is_delta_a_for_wett_conductor() -> None:
    """Test that rain correction for r=0.75mm/h is equal to delta_A."""
    E = LINE.E_ac
    delta_A = sound.compute_delta_A(
        LINE.num_con, LINE.con_radius * 200.0, LINE.bundle_radius * 200.0, E
    )
    delta_rain = sound.delta_rain(rain_rate=0.75, E=E, line=LINE, reference_rate=6.5)
    np.testing.assert_allclose(delta_rain, delta_A)


def test_rain_correction_is_0_for_heavy_rain() -> None:
    """Test that rain correction for r=6.5mm/h is equal to 0."""
    E = LINE.E_ac
    delta_rain = sound.delta_rain(rain_rate=6.5, E=E, line=LINE, reference_rate=6.5)
    np.testing.assert_allclose(delta_rain, 0.0)


def test_rain_correction_table_lookup_is_0_for_wett_conductor() -> None:
    """Test that rain correction (table lookup method) for r=0.75mm/h is equal to 0."""
    E = LINE.E_ac
    delta_rain = sound.delta_rain_table_lookup(
        weather=Weather.Foul, rain_rate=0.75, _E=E, _line=LINE
    )
    np.testing.assert_allclose(delta_rain, 0.0)


def test_rain_correction_table_lookup_with_delta_a_is_delta_a_for_wett_conductor() -> None:
    """Test that rain correction (table lookup method) for r=0.75mm/h is equal to delta_A."""
    E = LINE.E_ac
    delta_A = sound.compute_delta_A(
        LINE.num_con, LINE.con_radius * 200.0, LINE.bundle_radius * 200.0, E
    )
    delta_rain = sound.delta_rain_table_lookup_plus_delta_A(
        weather=Weather.Foul, rain_rate=0.75, E=E, line=LINE
    )
    np.testing.assert_allclose(delta_rain, delta_A)


def test_ac_epri() -> None:
    """Check AC EPRI routine (AC lines)."""
    systems = create_420_kv_ac_systems()
    parameters = sound.AcEpri(
        weather=Weather.Foul,
        rain_rate=0.75,
        altitude=0.0,
        use_efield_independent_rain_correction=True,
    )
    L, A = parameters.calc_systems(systems, GROUND_POINTS)
    expected_l_w50 = np.array(
        [-55.448738, -55.075042, -58.017581, -82.745488, -84.100858, -83.483141]
    )
    np.testing.assert_allclose([a for _, a in A], expected_l_w50)
    expected_L = np.array(
        [
            43.01703571812674,  # -60
            43.80706260899289,  # -50
            44.67522348195591,  # -40
            45.63865509037108,  # -30
            46.71379238659792,  # -20
            47.89516689279349,  # -10
            49.035587110179904,  # 0
            49.46342478874003,  # 10
            48.713381606903326,  # 20
            47.54835349240712,  # 30
            46.403361794135776,  # 40
            45.362704635051,  # 50
            44.42714518940892,  # 60
        ]
    )
    np.testing.assert_allclose([a for _, a in A], expected_l_w50)
    np.testing.assert_allclose(L, expected_L)


def test_ac_epri_for_hybrid() -> None:
    """Check AC EPRI routine (AC/DC lines)."""
    systems = create_hybrid_systems()
    parameters = sound.AcEpri(
        weather=Weather.Foul,
        rain_rate=0.75,
        altitude=0.0,
        use_efield_independent_rain_correction=True,
    )
    L, A = parameters.calc_systems(systems, GROUND_POINTS)
    expected_l_w50 = np.array([-56.243307, -55.076846, -59.904684])
    np.testing.assert_allclose([a for _, a in A], expected_l_w50)
    expected_L = np.array(
        [
            42.367240136835576,  # -60
            43.15949287616643,  # -50
            44.03097084473674,  # -40
            44.99929167436352,  # -30
            46.08123017794939,  # -20
            47.2705083563077,  # -10
            48.41637314494865,  # 0
            48.85161405550052,  # 10
            48.116192470233344,  # 20
            46.95486026141069,  # 30
            45.80472754769044,  # 40
            44.75706591690656,  # 50
            43.815250622658596,  # 60
        ]
    )
    np.testing.assert_allclose(L, expected_L)


def test_ac_bpa() -> None:
    """Check AC BPA routine (AC lines)."""
    systems = create_420_kv_ac_systems()
    parameters = sound.AcBpa(
        weather=Weather.Foul,
        rain_rate=0.75,
        altitude=0.0,
        use_efield_independent_rain_correction=True,
    )

    L, A = parameters.calc_systems(systems, GROUND_POINTS)
    expected_l_w50 = np.array([-55.136738, -54.777078, -57.54412, -77.91347, -78.813584, -78.40528])
    np.testing.assert_allclose([a for _, a in A], expected_l_w50)
    expected_L = np.array(
        [
            42.22304065532833,  # -60
            42.9095151022299,  # -50
            43.68938317851023,  # -40
            44.58437965401852,  # -30
            45.617136236153485,  # -20
            46.78942404433773,  # -10
            47.95639956909138,  # 0
            48.40060845137807,  # 10
            47.61359177955593,  # 20
            46.428265023230324,  # 30
            45.30205494690069,  # 40
            44.312645236585546,  # 50
            43.45279996789961,  # 60
        ]
    )
    np.testing.assert_allclose(L, expected_L)


def test_ac_bpa_for_hybrid() -> None:
    """Check AC BPA routine (AC/DC lines)."""
    systems = create_hybrid_systems()
    parameters = sound.AcBpa(
        weather=Weather.Foul,
        rain_rate=0.75,
        altitude=0.0,
        use_efield_independent_rain_correction=True,
    )
    L, A = parameters.calc_systems(systems, GROUND_POINTS)
    expected_l_w50 = np.array([-55.893314, -54.778819, -59.244349])
    np.testing.assert_allclose([a for _, a in A], expected_l_w50)
    expected_L = np.array(
        [
            41.588573262684164,  # -60
            42.27616547840959,  # -50
            43.0580641380739,  # -40
            43.95660134149716,  # -30
            44.99530289612751,  # -20
            46.17690535660288,  # -10
            47.353594595299526,  # 0
            47.8080104023072,  # 10
            47.03636726463099,  # 20
            45.85433394796843,  # 30
            44.722228018263394,  # 40
            43.72514884898792,  # 50
            42.85854946194668,  # 60
        ]
    )
    np.testing.assert_allclose(L, expected_L)


def test_ac_bpa_mod() -> None:
    """Check AC BPA MOD routine (AC lines)."""
    systems = create_380_kv_ac_systems()
    parameters = sound.AcBpaMod(weather=Weather.Foul, rain_rate=1.0, altitude=300.0)

    L, A = parameters.calc_systems(systems, GROUND_POINTS)
    # conversion from dBA above 1pW/m to dBA above 1W/m:
    to_W = -120.0
    expected_l_w50 = (
        np.array([59.411859, 60.937129, 59.482608, 59.482608, 60.937129, 59.411859]) + to_W
    )
    np.testing.assert_allclose([a for _, a in A], expected_l_w50)
    expected_L = np.array(
        [
            42.552327,  # -60
            43.353041,  # -50
            44.208034,  # -40
            45.096025,  # -30
            45.939072,  # -20
            46.547744,  # -10
            46.747666,  # 0
            46.547744,  # 10
            45.939072,  # 20
            45.096025,  # 30
            44.208034,  # 40
            43.353041,  # 50
            42.552327,  # 60
        ]
    )
    np.testing.assert_allclose(L, expected_L)


def test_ac_edf_for_hybrid() -> None:
    """Check AC EDF routine (hybrid tower)."""
    systems = create_hybrid_systems()
    parameters = sound.AcEdf(rain_rate=0.8, altitude=0.0)
    L, A = parameters.calc_systems(systems, GROUND_POINTS)
    expected_l_w50 = np.array([-59.409591, -58.407283, -62.530454])
    np.testing.assert_allclose([a for _, a in A], expected_l_w50)
    expected_L = np.array(
        [
            39.211557,  # -60
            40.002381,  # -50
            40.871773,  # -40
            41.837018,  # -30
            42.914527,  # -20
            44.098069,  # -10
            45.238357,  # 0
            45.670200,  # 10
            44.934421,  # 20
            43.776324,  # 30
            42.630619,  # 40
            41.586869,  # 50
            40.648092,  # 60
        ]
    )
    np.testing.assert_allclose(L, expected_L)


def test_dc_epri_for_ac() -> None:
    """Check DC EPRI routine (AC lines)."""
    systems = create_420_kv_ac_systems()
    parameters = sound.DcEpri(weather=Weather.Fair, season=Season.Summer, altitude=0.0)

    L, A = parameters.calc_systems(systems, GROUND_POINTS)
    expected_L = np.array([])
    assert not A
    np.testing.assert_allclose(L, expected_L)


def test_dc_epri_for_hybrid() -> None:
    """Check DC EPRI routine (AC/DC lines)."""
    systems = create_hybrid_systems()
    parameters = sound.DcEpri(weather=Weather.Fair, season=Season.Summer, altitude=0.0)

    L, A = parameters.calc_systems(systems, GROUND_POINTS)
    expected_L = np.array(
        [
            50.55698540533841,  # -60
            51.30691952877234,  # -50
            52.069634730950405,  # -40
            52.796464640257554,  # -30
            53.38415938235837,  # -20
            53.67331144277539,  # -10
            53.55431361575769,  # 0
            53.08775519669655,  # 10
            52.422578511717674,  # 20
            51.67959274220686,  # 30
            50.92708452980608,  # 40
            50.19641863217132,  # 50
            49.49924526944369,  # 60
        ]
    )
    expected_l_w50 = [-45.046944, -53.337112]
    np.testing.assert_allclose([a for _, a in A], expected_l_w50)
    np.testing.assert_allclose(L, expected_L)


def test_dc_bpa_for_ac() -> None:
    """Check DC BPA routine (AC lines)."""
    systems = create_420_kv_ac_systems()
    parameters = sound.DcBpa(weather=Weather.Fair, season=Season.Summer, altitude=0.0)

    L, A = parameters.calc_systems(systems, GROUND_POINTS)
    expected_L = np.array([])
    assert not A
    np.testing.assert_allclose(L, expected_L)


def test_dc_bpa_for_hybrid() -> None:
    """Check DC BPA routine (AC/DC) lines."""
    systems = create_hybrid_systems()
    parameters = sound.DcBpa(weather=Weather.Fair, season=Season.Summer, altitude=0.0)

    L, A = parameters.calc_systems(systems, GROUND_POINTS)
    expected_L = np.array(
        [
            36.02752312289555,  # -60
            36.69976518899075,  # -50
            37.40351713417375,  # -40
            38.09226123141403,  # -30
            38.66147532336236,  # -20
            38.94461373174306,  # -10
            38.82573331940179,  # 0
            38.36971190756896,  # 10
            37.73288060209736,  # 20
            37.03891188628555,  # 30
            36.35509102994553,  # 40
            35.71016505992111,  # 50
            35.11293406486419,  # 60
        ]
    )
    expected_l_w50 = [-58.336057, -66.537302]
    np.testing.assert_allclose([a for _, a in A], expected_l_w50)
    np.testing.assert_allclose(L, expected_L)


def test_dc_criepi_for_ac() -> None:
    """Check DC CRIEPI routine (AC lines)."""
    systems = create_420_kv_ac_systems()

    L, A = sound.DcCriepi().calc_systems(systems, GROUND_POINTS)
    expected_L = np.array([])
    assert not A
    np.testing.assert_allclose(L, expected_L)


def test_dc_criepi_for_hybrid() -> None:
    """Check DC CRIEPI routine (AC/DC) lines."""
    systems = create_hybrid_systems()

    L, A = sound.DcCriepi().calc_systems(systems, GROUND_POINTS)
    expected_L = np.array(
        [
            41.24930248986458,  # -60
            41.83846953200431,  # -50
            42.45490080448708,  # -40
            43.057613146107094,  # -30
            43.55519646968244,  # -20
            43.80309527101656,  # -10
            43.70052819970095,  # 0
            43.30256384968568,  # 10
            42.74515172723338,  # 20
            42.13697291727769,  # 30
            41.53738492611641,  # 40
            40.97178010752616,  # 50
            40.44795333375155,  # 60
        ]
    )
    expected_l_w50 = [-55.634423, -63.853519]
    np.testing.assert_allclose([a for _, a in A], expected_l_w50)
    np.testing.assert_allclose(L, expected_L)
