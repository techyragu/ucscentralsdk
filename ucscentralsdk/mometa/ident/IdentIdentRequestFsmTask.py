"""This module contains the general information for IdentIdentRequestFsmTask ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class IdentIdentRequestFsmTaskConsts():
    COMPLETION_CANCELLED = "cancelled"
    COMPLETION_COMPLETED = "completed"
    COMPLETION_PROCESSING = "processing"
    COMPLETION_SCHEDULED = "scheduled"
    ITEM_NOP = "nop"
    ITEM_UPDATE_IDENT = "updateIdent"


class IdentIdentRequestFsmTask(ManagedObject):
    """This is IdentIdentRequestFsmTask class."""

    consts = IdentIdentRequestFsmTaskConsts()
    naming_props = set([u'item'])

    mo_meta = MoMeta("IdentIdentRequestFsmTask", "identIdentRequestFsmTask", "task-[item]", VersionMeta.Version111a, "OutputOnly", 0xf, [], [""], [u'identIdentRequest'], [], [None])

    prop_meta = {
        "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version111a, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "completion": MoPropertyMeta("completion", "completion", "string", VersionMeta.Version111a, MoPropertyMeta.READ_ONLY, None, None, None, None, ["cancelled", "completed", "processing", "scheduled"], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version111a, MoPropertyMeta.READ_ONLY, 0x2, 0, 256, None, [], []), 
        "flags": MoPropertyMeta("flags", "flags", "string", VersionMeta.Version111a, MoPropertyMeta.READ_ONLY, None, None, None, r"""(defaultValue){0,1}""", [], []), 
        "item": MoPropertyMeta("item", "item", "string", VersionMeta.Version111a, MoPropertyMeta.NAMING, None, None, None, None, ["nop", "updateIdent"], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version111a, MoPropertyMeta.READ_ONLY, 0x4, 0, 256, None, [], []), 
        "seq_id": MoPropertyMeta("seq_id", "seqId", "uint", VersionMeta.Version111a, MoPropertyMeta.READ_ONLY, None, None, None, None, [], []), 
        "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version111a, MoPropertyMeta.READ_WRITE, 0x8, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
    }

    prop_map = {
        "childAction": "child_action", 
        "completion": "completion", 
        "dn": "dn", 
        "flags": "flags", 
        "item": "item", 
        "rn": "rn", 
        "seqId": "seq_id", 
        "status": "status", 
    }

    def __init__(self, parent_mo_or_dn, item, **kwargs):
        self._dirty_mask = 0
        self.item = item
        self.child_action = None
        self.completion = None
        self.flags = None
        self.seq_id = None
        self.status = None

        ManagedObject.__init__(self, "IdentIdentRequestFsmTask", parent_mo_or_dn, **kwargs)

