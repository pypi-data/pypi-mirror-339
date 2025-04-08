from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Sequence, TypeVar

from pm4py.objects.petri_net.obj import PetriNet, Marking

if TYPE_CHECKING:
    pass

import os


def ensure_path_exists(path):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except Exception:
            ...


class DataframeEventLogKeys:
    case_id = 'case:concept:name'
    time = 'time:timestamp'
    activity = 'concept:name'
    lifecycle = 'lifecycle:transition'


@dataclass
class AcceptingPetrinet:
    net: PetriNet
    im: Marking
    fm: Marking


def nice_dict_str(dic: dict):
    return '{' + ','.join((str(k) + ': ' + str(v) for k, v in dic.items())) + '}'


T = TypeVar('T')


def first_k(k: int) -> Callable[[Iterable[T]], Sequence[T]]:
    def select(seq: Iterable[T], k=k) -> Sequence[T]:
        return [v for _, v in zip(range(k), seq)]

    return select
