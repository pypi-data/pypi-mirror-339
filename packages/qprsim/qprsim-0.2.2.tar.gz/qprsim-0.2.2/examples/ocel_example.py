from datetime import datetime, timedelta, time
from typing import TYPE_CHECKING

import numpy as np
import pm4py

import qprsim.utils.viz
from qprsim.config.impls import WorkweekBusinessHours, StaticSampler, StochasticClassifier, EmptyObjectCreator, \
    ExpSampler, TypeBasedSplitter, LambdaObjectAttributeGenerator, lift, LambdaCarrierAttributeGenerator, \
    LambdaObjectSetCreator
from qprsim.config.oc import *
from qprsim.execution.oc import *
from qprsim.utils import time_utils

if TYPE_CHECKING:
    from qprsim.core.object_def import Carrier

process_start = datetime(2023, 5, 8, 3, 18)
pr_object_type = 'purchase_requisition'
mat_object_type = 'material'
po_object_type = 'purchase_order'
purchase_purposes = ['because i wanted it', 'to trash later', 'to make profit']

mb = ModelBuilder(skip_asserts=True)
RD = mb.add_resource('Requisition Department',
                     ResourceConfig(3, WorkweekBusinessHours.fixed_time((time(9), time(18)), time_utils.Workweek)))
OD = mb.add_resource('Order Department',
                     ResourceConfig(3, WorkweekBusinessHours.fixed_time((time(9), time(18)), time_utils.Workweek)))
PD = mb.add_resource('Procurement Department',
                     ResourceConfig(3, WorkweekBusinessHours.fixed_time((time(9), time(18)), time_utils.Workweek)))

pr_birth = mb.add_birthplace('pr_birth', ObjectBirthplaceConfig(pr_object_type,
                                                                EmptyObjectCreator(pr_object_type)))

mb.add_arrival_process('pr_trigger', OCArrivalProcessConfig(process_start, ExpSampler(60), targets=[pr_birth]))


def gen_mats(id_gen, carrier, **kwargs):
    pr = carrier.as_singleton()
    mats = []
    for i in range(np.random.randint(1, 5)):
        mat = obd.Object(id_gen(mat_object_type), mat_object_type)
        mats.append(mat)
    o2o = {'assigned_materials': {(pr, m) for m in mats}}
    return obd.Carrier(*mats), o2o


material_create = mb.add_transformer_node('material create',
                                          CarrierGeneratorConfig(LambdaObjectSetCreator(gen_mats)))

mb.connect_to_birthplace(material_create, pr_birth)

split_1 = mb.add_split('split 1', SplitConfig(
    TypeBasedSplitter({pr_object_type: 0, mat_object_type: 1}, split_into_singletons=True)))


def gen_pr_attrs(o, **kwargs):
    return {'purchase_department': np.random.choice(['A', 'B', 'C'], p=[0.3, 0.4, 0.3]),
            'purchase_purpose': np.random.choice(purchase_purposes,
                                                 p=[0.7, 0.1, 0.2])}


create_pr_act = mb.add_activity('Create Purchase Requisition', OCActivityConfig(StaticSampler(timedelta(seconds=1)),
                                                                                carrier_attribute_generator=lift(
                                                                                    LambdaObjectAttributeGenerator(
                                                                                        gen_pr_attrs))), [RD])


def gen_mat_event_attrs(o, resource, time, **kwargs):
    target_date = time_utils.add(time, timedelta(days=(7 + np.random.randint(14))))
    return {'delivery_date': target_date, 'price': np.random.randint(10, 10_000),
            'quantity': np.random.randint(1, 50)}


add_mat_act = mb.add_activity('Add Material', OCActivityConfig(StaticSampler(timedelta(seconds=1)),
                                                               carrier_attribute_generator=lift(
                                                                   LambdaObjectAttributeGenerator(
                                                                       gen_mat_event_attrs))), [RD])

mb.connect(material_create, split_1)
mb.connect_between_split_join(split_1, [create_pr_act, add_mat_act])

split_2 = mb.add_split('split 2', SplitConfig(
    TypeBasedSplitter({pr_object_type: 0, mat_object_type: 1}, split_into_singletons=True)))

mb.connect(split_1, split_2)

pr_change_dec = mb.add_decision('pr change', DecisionConfig(StochasticClassifier([0.2, 0.8])))
mat_change_dec = mb.add_decision('mat change', DecisionConfig(StochasticClassifier([0.1, 0.9])))


def pp_change(o: obd.Object, **kwargs):
    options = set(purchase_purposes) - set(o.attributes['purchase_purpose'])
    new = np.random.choice(list(options))
    return {'purchase_purpose': new}


def price_change(o: obd.Object, **kwargs):
    change = 1 + ((np.random.rand() - .5) / 5)  # -10% to +10%
    return {'price': o.attributes['price'] * change}


change_pr_act = mb.add_activity('Change PR', OCActivityConfig(
    carrier_attribute_generator=lift(LambdaObjectAttributeGenerator(pp_change))), [RD])

change_mat_act = mb.add_activity('Change Material', OCActivityConfig(
    carrier_attribute_generator=lift(LambdaObjectAttributeGenerator(price_change)
                                     )), [RD])

mb.connect_as_decision(pr_change_dec, [change_pr_act], add_skip_at_idx=1)
mb.connect_as_decision(mat_change_dec, [change_mat_act], add_skip_at_idx=1)

mb.connect_between_split_join(split_2, [(split_of(pr_change_dec), join_of(pr_change_dec)),
                                        (split_of(mat_change_dec), join_of(mat_change_dec))])


def gen_po(id_gen, carrier, **kwargs):
    pr = carrier.get_first_of_type(pr_object_type)
    po = obd.Object(id_gen(po_object_type), po_object_type)
    return obd.Carrier(po), {'assigned_pr': {(pr, po)}}


po_create = mb.add_transformer_node('po create',
                                    CarrierGeneratorConfig(LambdaObjectSetCreator(gen_po)))

mb.connect(split_2, po_create)


def total_price(carrier, **kwargs):
    po = carrier.get_first_of_type(po_object_type)
    total = sum(o.attributes['price'] for o in carrier.get_of_type(mat_object_type))
    return {po: {'total_price': total}}


create_po_act = mb.add_activity('Create Purchase Order', OCActivityConfig(
    carrier_attribute_generator=LambdaCarrierAttributeGenerator(total_price)), [OD])

mb.connect(po_create, create_po_act)


# split_3 = mb.add('split 3', )

def total_quantity(carrier: obd.Carrier, **kwargs):
    po = carrier.get_first_of_type(po_object_type)
    total = sum(o.attributes['quantity'] for o in carrier.get_of_type(mat_object_type))
    return {po: {'total_quantity': total}}


receive_order_act = mb.add_activity('Receive Order', OCActivityConfig(
    carrier_attribute_generator=LambdaCarrierAttributeGenerator(total_quantity)), [PD])

mb.connect(create_po_act, receive_order_act)

grave = mb.add_graveyard('grave')

mb.connect_to_graveyard(receive_order_act, grave)

sg, cfg = mb.build()

gg = qprsim.model.oc.visualize_sim_graph(sg, extended_node_labels=True)
qprsim.utils.viz.save(gg, filename='test')
print(sg)
print(cfg)

sm = create_simulation_model(sg, cfg,
                             default_execution_parameters() | {OCExecutionParameters.EventsToGenerate: 1_000})

whatif = ButWhatIf(sm)
whatif.schedule_activity_property_change(datetime(2023, 5, 8, 13, 0), create_po_act,
                                         OCActivityProperty.ProcessingTimeSampler, ExpSampler(5))
whatif.apply()

s = simulate(sm, simulation_log_filename='test.log')

for e in s.logged_events[:10]:
    print(e)
for o in list(s.finalized_objects)[:10]:
    print(o)

ocel = s.create_log()

pm4py.write_ocel(ocel, 'test_log.xmlocel')
