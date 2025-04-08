## QPRsim
_Queueing Processes with Resources Simulator_

This is a package for discrete-event simulation of traditional as well as object-centric event logs.
Generated logs can be converted to and exported in XES or OCEL 2.0 format respectively.
It is based on the interaction of a global event queue and a graph structure which controls the flow of cases/objects.
Activities use an internal queue which along with strict respecting of resource capacities enables waiting times and cascading dynamics to emerge.  
The event system uses discrete time steps but produces real timezone-aware time stamps. It also makes 'business hours', i.e., periodic availability variation a key aspect of arrival processes, activities and resources. 
There is also rudimentary what-if capability implemented via an interface with which users can schedule points in simulation-time when activity/resource/object birthplace properties are changed or arrival processes added/swapped/removed. 

The philosophy of the component structure is that the control flow is separated from the logic of its nodes which is separated from its configuration.
This is to keep everything as flexible as possible and particularly to make the configuration easily exchangeable.
Furthermore, configurable parameters are separated from their base implementations, to facilitate the quick development of new, more complex, key parameters like processing time samplers, routing classifiers, queueing discipline, etc.
Any of these can be extended by subclassing the appropriate base classes.
This is reflected in the package structure. Each main package _core_, _model_, _config_ and _execution_ is set up for traditional event log simulation, while the sub-packages '.oc' include the object-centric versions of components where they have to differ. 

- [qprsim.core[.oc]](qprsim/core) contains the deep internals like the event system and case/object definitions.
- [qprsim.model[.oc]](qprsim/model) contains the simulation graph and models. The configurable properties of the models are also declared here, i.e., the queueing discipline of an activity.
- [qprsim.config[.oc]](qprsim/config) contains configuration classes for each of the models which bundle all the aforementioned properties/parameters. This package also contains the reference/base implementations of these properties. 
- [qprsim.execution[.oc]](qprsim/execution) contains the simulation 'builder' itself that applies a given configuration to a model to synthesize a complete simulation model. In contrast to a graph or model configuration, which are more-or-less immutable, a packed simulation model is use-once and contains all the state that emerges during simulation, i.e, created cases/objects and events. This package also contains the _ButWhatIf_ functionality mentioned before. 
- [qprsim.utils](qprsim/utils) contains miscellaneous utility functions used in the above packages. Worth mentioning are the _time_utils_ which can ease working with timezone aware datetimes.

The defined package imports are setup such that by importing from the config and execution packages, you get most of everything you might need to set up a simulation.
Additionally, the sub package _impls_ of _config_ bundles all reference parameter implementations which can be used to populate the configuration.

```
from qprsim.config[.oc] import *
from qprsim.execution[.oc] import *
from qprsim.config import impls
```
There are also classes prefixed by ```Lambda``` which can wrap any user defined function with the correct signature to easily externalize logic to the user.  
Throughout the tool, we make ample usage of ```**kwargs``` to pass optional information to, in particular, parameter implementations.
Though it can be a bit 'dangerous' to use not statically existence-checked arguments, they provide a way pass around optional objects.
Advanced users can also thus slightly more easily adapt the simulation software itself by passing required objects via these keyword arguments.  

### Usage
There are three sample simulation setups included in this repository.
- [traditional_test](sample/traditional_test.py). In these tests are ultra-basic toy configurations of traditional event log simulations. 
- [ocel_sample](sample/ocel_sample.py). This is the first object-centric simulation setup showcasing a basic process and how to work with object creation, routing and attribute access.
- [udonya](sample/udonya.ipynb). Based on a previous version of this package, this setup showcases all the ways the traditional event log simulation can be used and abused to create interesting dynamics.

As a brief example, the following is a code snippet shows how one can define an 'object birthplace' node which creates objects of type _my_object_type_.
A caveat is that even object attribute initializations have to have a timestamp due to the OCEL 2.0 specification. 

```
mb = ModelBuilder()

def object_creation(object_id: obd.ObjectId, time, **kwargs):
    return obd.Object.with_initial_attributes(object_id, 'my_object_type', initialization_timestamp=time,
                                              my_attribute='Hello')

birthplace = mb.add_birthplace('my_birthplace', ObjectBirthplaceConfig('my_object_type', ocpi.LambdaObjectCreator('my_object_type', object_creation)))
```

### Simulation Models

Simulation models can be built manually using the ModelBuilder. It provides a somewhat simple interface to populate a _simulation graph_ and _model configuration_ object.
The simulation graph is (sadly) not Petri net based but rather a simplified and recursively defined "push-forward" graph.
The idea is that in arrival/birthplace nodes, control-flow tokens enter into the system and are then routed by the graph nodes to a terminal/graveyard node.

The control-flow object in traditional simulation is straightforwardly a case to which activities add events. Routing to different terminal nodes allows simulation of different "types" of cases that still interact, and most importantly, share resources but still end up in separate event logs.
This can be used to simulate cancelled/abandoned cases.
For object-centric simulation, so-called _carrier_ objects are used. They represent (synchronized) sets of objects. They can be split and objects be added or removed from them.
Easily accessible synchronization of separate carrier "streams" is currently limited.

In contrast to Petri nets, there is no global synchronization (yet) on the graph level.
It is, however, a key aspect via the resource management system which strictly respects resource availability and capacity. 
Each node locally decides which successor(s) to route an incoming control-flow token to.
Though all executions are eager, the behavior of nodes can be dynamic:
- Activity nodes access the event system as well as resource management system to either wait a specified amount of time (delay, processing) or until a resource is available (waiting) before forwarding a control-flow token.
- AND split/join constructs wait until a control-flow token has arrived {number of splits}-times before forwarding.
- OC split/join constructs wait until all constituents of a carrier have arrived at the join before forwarding it. 
- Custom nodes can do anything. There are some building off-points and examples in the code, especially the latest traditional sim model extensions but this is advanced topic.

### Model Configuration

For traditional event log simulation, the basic relevant configurable items are:
- Arrival processes which are one-to-one connected to arrival nodes
  - business hours
  - inter arrival time sampler
  - creation count limit
  - initial case attribute generator
- Activities
  - business hours
  - queueing discipline
  - delay & processing time sampler
  - event attribute generator
  - (dangerous and requires extra, extra care) max queue size and discard-on-full handler 
- Resources
  - capacity
  - business hours
- Decision nodes
  - case classifier (decides which successor a case is routed to)
- Activity <=> Resource mapping
  - definition of assignable resources and their assignment propensity

For object-centric simulation they are:
- Arrival Processes which are connected to object birthplaces
  - business hours
  - inter arrival time sampler
  - target birthplaces
- Birthplaces
  - object type
  - object generator (decides initial attributes and o2o relations)
  - creation count limit
- Activities
  - business hours
  - queueing discipline
  - processing time sampler
  - event attribute generator
  - event object qualifier (decides which objects are linked to the event by which qualifier)
  - carrier attribute generator (can optionally override/add attributes to any involved objects)
- Resources
  - capacity
  - business hours
- Decision nodes
  - carrier classifier (decides which successor a carrier is routed to)
- Split nodes
  - carrier splitter (decides which objects within a carrier are routed to which successor)
- Transformation nodes
  - carrier generator (can generate any set of objects to be added to the carrier)
- Activity <=> Resource mapping
  - definition of assignable resources and their assignment propensity

All arrival, activity and resource properties can be scheduled to change within the simulation horizon via the _whatif_ functionality.
