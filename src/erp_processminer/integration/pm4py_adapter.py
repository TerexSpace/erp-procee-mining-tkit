"""
Optional wrapper/stub for converting data structures to and from the
pm4py library.
"""

from erp_processminer.eventlog.structures import EventLog
from erp_processminer.models.petri_net import PetriNet

def to_pm4py_log(log: EventLog):
    """
    Converts an erp-processminer EventLog to a pm4py EventLog.

    This requires pm4py to be installed.
    :param log: An erp-processminer EventLog.
    :return: A pm4py EventLog.
    """
    try:
        import pm4py
        from pm4py.objects.log.obj import EventLog as Pm4pyEventLog, Trace, Event
    except ImportError:
        raise ImportError("pm4py is not installed. Please install it with 'pip install pm4py'")

    pm4py_log = Pm4pyEventLog()
    for trace in log:
        pm4py_trace = Trace()
        pm4py_trace.attributes['concept:name'] = trace.case_id
        for event in trace:
            pm4py_event = Event()
            pm4py_event['concept:name'] = event.activity
            pm4py_event['time:timestamp'] = event.timestamp
            for k, v in event.attributes.items():
                pm4py_event[k] = v
            pm4py_trace.append(pm4py_event)
        pm4py_log.append(pm4py_trace)
        
    return pm4py_log

def from_pm4py_log(pm4py_log) -> EventLog:
    """
    Converts a pm4py EventLog to an erp-processminer EventLog.

    :param pm4py_log: A pm4py EventLog.
    :return: An erp-processminer EventLog.
    """
    raise NotImplementedError("Conversion from pm4py is not yet implemented.")

def to_pm4py_petri_net(net: PetriNet):
    """
    Converts an erp-processminer PetriNet to a pm4py PetriNet.

    :param net: An erp-processminer PetriNet.
    :return: A pm4py PetriNet, initial_marking, and final_marking.
    """
    raise NotImplementedError("Petri net conversion to pm4py is not yet implemented.")