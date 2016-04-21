"""This module contains the general information for LsmaintMaintPolicy ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class LsmaintMaintPolicyConsts():
    INT_ID_NONE = "none"
    POLICY_OWNER_LOCAL = "local"
    POLICY_OWNER_PENDING_POLICY = "pending-policy"
    POLICY_OWNER_POLICY = "policy"
    POLICY_OWNER_UNSPECIFIED = "unspecified"
    UPTIME_DISR_IMMEDIATE = "immediate"
    UPTIME_DISR_TIMER_AUTOMATIC = "timer-automatic"
    UPTIME_DISR_USER_ACK = "user-ack"


class LsmaintMaintPolicy(ManagedObject):
    """This is LsmaintMaintPolicy class."""

    consts = LsmaintMaintPolicyConsts()
    naming_props = set([u'name'])

    mo_meta = MoMeta("LsmaintMaintPolicy", "lsmaintMaintPolicy", "maint-[name]", VersionMeta.Version101a, "InputOutput", 0x1ff, [], ["read-only"], [u'orgDomainGroup', u'orgOrg'], [u'faultInst'], ["Add", "Get", "Remove", "Set"])

    prop_meta = {
        "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version101a, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "descr": MoPropertyMeta("descr", "descr", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x2, None, None, r"""[ !#$%&\(\)\*\+,\-\./:;\?@\[\]_\{\|\}~a-zA-Z0-9]{0,256}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version101a, MoPropertyMeta.READ_ONLY, 0x4, 0, 256, None, [], []), 
        "int_id": MoPropertyMeta("int_id", "intId", "string", VersionMeta.Version101a, MoPropertyMeta.INTERNAL, None, None, None, None, ["none"], ["0-4294967295"]), 
        "name": MoPropertyMeta("name", "name", "string", VersionMeta.Version101a, MoPropertyMeta.NAMING, 0x8, None, None, r"""[\-\.:_a-zA-Z0-9]{1,16}""", [], []), 
        "oper_sched_name": MoPropertyMeta("oper_sched_name", "operSchedName", "string", VersionMeta.Version101a, MoPropertyMeta.READ_ONLY, None, None, None, r"""[\-\.:_a-zA-Z0-9]{0,16}""", [], []), 
        "policy_level": MoPropertyMeta("policy_level", "policyLevel", "uint", VersionMeta.Version101a, MoPropertyMeta.READ_ONLY, None, None, None, None, [], []), 
        "policy_owner": MoPropertyMeta("policy_owner", "policyOwner", "string", VersionMeta.Version101a, MoPropertyMeta.READ_ONLY, None, None, None, None, ["local", "pending-policy", "policy", "unspecified"], []), 
        "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version101a, MoPropertyMeta.READ_ONLY, 0x10, 0, 256, None, [], []), 
        "sched_name": MoPropertyMeta("sched_name", "schedName", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x20, None, None, r"""[\-\.:_a-zA-Z0-9]{0,16}""", [], []), 
        "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x40, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
        "trigger_config": MoPropertyMeta("trigger_config", "triggerConfig", "string", VersionMeta.Version141a, MoPropertyMeta.READ_WRITE, 0x80, None, None, r"""((defaultValue|none|on-next-boot),){0,2}(defaultValue|none|on-next-boot){0,1}""", [], []), 
        "uptime_disr": MoPropertyMeta("uptime_disr", "uptimeDisr", "string", VersionMeta.Version101a, MoPropertyMeta.READ_WRITE, 0x100, None, None, None, ["immediate", "timer-automatic", "user-ack"], []), 
    }

    prop_map = {
        "childAction": "child_action", 
        "descr": "descr", 
        "dn": "dn", 
        "intId": "int_id", 
        "name": "name", 
        "operSchedName": "oper_sched_name", 
        "policyLevel": "policy_level", 
        "policyOwner": "policy_owner", 
        "rn": "rn", 
        "schedName": "sched_name", 
        "status": "status", 
        "triggerConfig": "trigger_config", 
        "uptimeDisr": "uptime_disr", 
    }

    def __init__(self, parent_mo_or_dn, name, **kwargs):
        self._dirty_mask = 0
        self.name = name
        self.child_action = None
        self.descr = None
        self.int_id = None
        self.oper_sched_name = None
        self.policy_level = None
        self.policy_owner = None
        self.sched_name = None
        self.status = None
        self.trigger_config = None
        self.uptime_disr = None

        ManagedObject.__init__(self, "LsmaintMaintPolicy", parent_mo_or_dn, **kwargs)

