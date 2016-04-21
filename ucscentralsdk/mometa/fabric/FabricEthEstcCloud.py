"""This module contains the general information for FabricEthEstcCloud ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class FabricEthEstcCloudConsts():
    pass


class FabricEthEstcCloud(ManagedObject):
    """This is FabricEthEstcCloud class."""

    consts = FabricEthEstcCloudConsts()
    naming_props = set([])

    mo_meta = MoMeta("FabricEthEstcCloud", "fabricEthEstcCloud", "eth-estc", VersionMeta.Version111a, "InputOutput", 0xf, [], ["admin", "ext-lan-config", "ext-lan-policy"], [u'fabricEp'], [u'fabricEthEstc', u'fabricVlan', u'nwctrlDefinition', u'statsThresholdPolicy'], ["Get"])

    prop_meta = {
        "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version111a, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version111a, MoPropertyMeta.READ_ONLY, 0x2, 0, 256, None, [], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version111a, MoPropertyMeta.READ_ONLY, 0x4, 0, 256, None, [], []), 
        "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version111a, MoPropertyMeta.READ_WRITE, 0x8, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
    }

    prop_map = {
        "childAction": "child_action", 
        "dn": "dn", 
        "rn": "rn", 
        "status": "status", 
    }

    def __init__(self, parent_mo_or_dn, **kwargs):
        self._dirty_mask = 0
        self.child_action = None
        self.status = None

        ManagedObject.__init__(self, "FabricEthEstcCloud", parent_mo_or_dn, **kwargs)

