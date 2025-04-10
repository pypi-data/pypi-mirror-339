import unittest

from bhr.borehole import Borehole


class TestBorehole(unittest.TestCase):
    def test_init_single_u_uhf(self):
        bh = Borehole()
        bh.init_single_u_borehole(
            borehole_diameter=0.14,
            pipe_outer_diameter=0.042,
            pipe_dimension_ratio=11,
            length=100,
            shank_space=0.01,
            pipe_conductivity=0.4,
            grout_conductivity=1.2,
            soil_conductivity=2.5,
            fluid_type="PROPYLENEGLYCOL",
            fluid_concentration=0.2,
        )

        self.assertAlmostEqual(bh.calc_bh_resist(temperature=20, mass_flow_rate=0.5), 0.20425, delta=0.0001)

    def test_init_single_u_ubwt(self):
        bh = Borehole()
        bh.init_single_u_borehole(
            borehole_diameter=0.14,
            pipe_outer_diameter=0.042,
            pipe_dimension_ratio=11,
            length=100,
            shank_space=0.01,
            pipe_conductivity=0.4,
            grout_conductivity=1.2,
            soil_conductivity=2.5,
            fluid_type="PROPYLENEGLYCOL",
            fluid_concentration=0.2,
            boundary_condition="uniform_borehole_wall_temp",
        )

        self.assertAlmostEqual(bh.calc_bh_resist(temperature=20, mass_flow_rate=0.5), 0.20414, delta=0.0001)

    def test_init_single_u_from_dict(self):
        inputs = {
            "fluid_type": "PROPYLENEGLYCOL",
            "fluid_concentration": 0.2,
            "boundary_condition": "uniform_heat_flux",
            "borehole_type": "single_u_tube",
            "single_u_tube": {
                "pipe_outer_diameter": 0.042,
                "pipe_dimension_ratio": 11,
                "pipe_conductivity": 0.4,
                "shank_space": 0.01,
            },
            "grout_conductivity": 1.2,
            "soil_conductivity": 2.5,
            "length": 100,
            "borehole_diameter": 0.14,
        }

        bh = Borehole()
        bh.init_from_dict(inputs)

        # only pass flow rate, so pipe resistance should be computed in the process of this call

        self.assertAlmostEqual(bh.calc_bh_resist(temperature=20, mass_flow_rate=0.5), 0.20425, delta=0.0001)

    def test_init_double_u_uhf(self):
        bh = Borehole()
        bh.init_double_u_borehole(
            borehole_diameter=0.115,
            pipe_outer_diameter=0.032,
            pipe_dimension_ratio=18.9,
            length=200,
            shank_space=0.02263,
            pipe_conductivity=0.389,
            pipe_inlet_arrangement="ADJACENT",
            grout_conductivity=1.5,
            soil_conductivity=3,
            fluid_type="WATER",
            fluid_concentration=0,
        )

        # only pass flow rate, so pipe resistance should be computed in the process of this call
        self.assertAlmostEqual(bh.calc_bh_resist(temperature=20, mass_flow_rate=0.4154), 0.1090, delta=0.0001)

    def test_init_double_u_ubwt(self):
        bh = Borehole()
        bh.init_double_u_borehole(
            borehole_diameter=0.115,
            pipe_outer_diameter=0.032,
            pipe_dimension_ratio=18.9,
            length=200,
            shank_space=0.02263,
            pipe_conductivity=0.389,
            pipe_inlet_arrangement="ADJACENT",
            grout_conductivity=1.5,
            soil_conductivity=3,
            fluid_type="WATER",
            fluid_concentration=0,
            boundary_condition="uniform_borehole_wall_temp",
        )

        # only pass flow rate, so pipe resistance should be computed in the process of this call
        self.assertAlmostEqual(bh.calc_bh_resist(temperature=20, mass_flow_rate=0.4154), 0.1065, delta=0.0001)

    def test_init_double_u_from_dict(self):
        inputs = {
            "fluid_type": "WATER",
            "fluid_concentration": 0,
            "boundary_condition": "uniform_heat_flux",
            "borehole_type": "double_u_tube",
            "double_u_tube": {
                "pipe_outer_diameter": 0.032,
                "pipe_dimension_ratio": 18.9,
                "pipe_conductivity": 0.389,
                "shank_space": 0.02263,
                "pipe_inlet_arrangement": "ADJACENT",  # or DIAGONAL
            },
            "grout_conductivity": 1.5,
            "soil_conductivity": 3,
            "length": 200,
            "borehole_diameter": 0.115,
        }

        bh = Borehole()
        bh.init_from_dict(inputs)

        # only pass flow rate, so pipe resistance should be computed in the process of this call
        self.assertAlmostEqual(bh.calc_bh_resist(temperature=20, mass_flow_rate=0.4154), 0.1090, delta=0.0001)

    def test_init_coaxial_uhf(self):
        bh = Borehole()
        bh.init_coaxial_borehole(
            borehole_diameter=0.115,
            outer_pipe_outer_diameter=0.064,
            outer_pipe_dimension_ratio=11,
            outer_pipe_conductivity=0.389,
            inner_pipe_outer_diameter=0.032,
            inner_pipe_dimension_ratio=11,
            inner_pipe_conductivity=0.389,
            length=200,
            grout_conductivity=1.5,
            soil_conductivity=3.0,
            fluid_type="WATER",
            fluid_concentration=0,
        )

        # only pass flow rate, so pipe resistance should be computed in the process of this call
        self.assertAlmostEqual(bh.calc_bh_resist(mass_flow_rate=0.5, temperature=20), 0.18048, delta=0.0001)

    def test_init_coaxial_ubwt(self):
        bh = Borehole()
        bh.init_coaxial_borehole(
            borehole_diameter=0.115,
            outer_pipe_outer_diameter=0.064,
            outer_pipe_dimension_ratio=11,
            outer_pipe_conductivity=0.389,
            inner_pipe_outer_diameter=0.032,
            inner_pipe_dimension_ratio=11,
            inner_pipe_conductivity=0.389,
            length=200,
            grout_conductivity=1.5,
            soil_conductivity=3.0,
            fluid_type="WATER",
            fluid_concentration=0,
            boundary_condition="uniform_borehole_wall_temp",
        )

        # only pass flow rate, so pipe resistance should be computed in the process of this call
        self.assertAlmostEqual(bh.calc_bh_resist(mass_flow_rate=0.5, temperature=20), 0.18365, delta=0.0001)

    def test_init_coaxial_from_dict(self):
        inputs = {
            "fluid_type": "WATER",
            "fluid_concentration": 0,
            "boundary_condition": "uniform_heat_flux",
            "borehole_type": "coaxial",
            "coaxial": {
                "outer_pipe_outer_diameter": 0.064,
                "outer_pipe_dimension_ratio": 11,
                "outer_pipe_conductivity": 0.389,
                "inner_pipe_outer_diameter": 0.032,
                "inner_pipe_dimension_ratio": 11,
                "inner_pipe_conductivity": 0.389,
            },
            "grout_conductivity": 1.5,
            "soil_conductivity": 3,
            "length": 200,
            "borehole_diameter": 0.115,
        }

        bh = Borehole()
        bh.init_from_dict(inputs)

        # only pass flow rate, so pipe resistance should be computed in the process of this call
        self.assertAlmostEqual(bh.calc_bh_resist(mass_flow_rate=0.5, temperature=20), 0.18048, delta=0.0001)
