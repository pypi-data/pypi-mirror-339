import unittest

from datetime import datetime


def sequential_model_builder():
    from qprsim.config import ModelBuilder, ActivityConfig, ResourceConfig, ArrivalProcessConfig
    from qprsim.config.impls import Fifo, ExpSampler, ZeroSampler
    mb = ModelBuilder(use_defaults=True)
    mb.add_arrival()
    mb.add_terminal()
    mb.set_default_arrival_config(
        ArrivalProcessConfig(datetime(2021, 4, 17, 13, 15), ExpSampler(60)))
    mb.add_activity('A', ActivityConfig(Fifo, ZeroSampler), 'R1',
                    connect_to_arrival=True)
    mb.add_activity('B', ActivityConfig(Fifo, ExpSampler(90)), 'R2')
    mb.add_activity('C', ActivityConfig(Fifo, ExpSampler(60)), 'R3',
                    connect_to_terminal=True)
    mb.add_resource('R1', ResourceConfig(100))
    mb.add_resource('R2', ResourceConfig(1))
    mb.add_resource('R3', ResourceConfig(1))
    mb.connect('A', 'B')
    mb.connect('B', 'C')
    return mb


def two_headed_sequential_model_builder():
    from qprsim.config import ArrivalProcessConfig
    from qprsim.config.impls import ExpSampler
    mb = sequential_model_builder()
    mb.add_arrival('secondary_arrival', ArrivalProcessConfig(datetime(2021, 4, 27, 13, 15), ExpSampler(20)))
    mb.connect_to_arrival('A', 'secondary_arrival')
    return mb


class ModelBuilderTestCase(unittest.TestCase):
    def test_modeling(self):
        m = sequential_model_builder().build()
        self.assertIsNotNone(m)
        self.assertIsNotNone(m[0])
        self.assertIsNotNone(m[1])


class SimulationExecutionTestCase(unittest.TestCase):
    def test_sim(self):
        from qprsim.execution import Simulator, create_simulation_model, ExecutionParameters
        sg, sc = two_headed_sequential_model_builder().build()
        sm = create_simulation_model(sg, sc, {ExecutionParameters.CasesToGenerate: 100})
        s = Simulator(sm)
        s.run(simulation_log_filename='logging/sample_test_log')
        self.assertIsNotNone(s.generated_cases)
        sc = s.simulation_model.simulation_context
        self.assertEqual(100, sc.started_cases_count)
        self.assertEqual(0, sc.aborted_cases_count)
        self.assertEqual(100, sc.completed_cases_count)
        self.assertFalse(sc.are_active_cases_remaining())
        first = s.generated_cases[0]
        last = s.generated_cases[-1]
        print(first)
        print(last)
        self.assertEqual(100, len(s.generated_cases))
        self.assertEqual(100, len(set(c.case_id for c in s.generated_cases)))


if __name__ == '__main__':
    unittest.main()
