"""This module contains the general information for LstorageDiskGroupQualifier ManagedObject."""

from ...ucscentralmo import ManagedObject
from ...ucscentralcoremeta import UcsCentralVersion, MoPropertyMeta, MoMeta
from ...ucscentralmeta import VersionMeta


class LstorageDiskGroupQualifierConsts():
    DRIVE_TYPE_HDD = "HDD"
    DRIVE_TYPE_SSD = "SSD"
    DRIVE_TYPE_UNSPECIFIED = "unspecified"
    MIN_DRIVE_SIZE_UNSPECIFIED = "unspecified"
    NUM_DED_HOT_SPARES_UNSPECIFIED = "unspecified"
    NUM_DRIVES_UNSPECIFIED = "unspecified"
    NUM_GLOB_HOT_SPARES_UNSPECIFIED = "unspecified"
    USE_REMAINING_DISKS_FALSE = "false"
    USE_REMAINING_DISKS_NO = "no"
    USE_REMAINING_DISKS_TRUE = "true"
    USE_REMAINING_DISKS_YES = "yes"


class LstorageDiskGroupQualifier(ManagedObject):
    """This is LstorageDiskGroupQualifier class."""

    consts = LstorageDiskGroupQualifierConsts()
    naming_props = set([])

    mo_meta = MoMeta("LstorageDiskGroupQualifier", "lstorageDiskGroupQualifier", "disk-group-qual", VersionMeta.Version131a, "InputOutput", 0x3ff, [], ["admin", "ls-compute", "ls-config", "ls-config-policy", "ls-server", "ls-storage", "ls-storage-policy"], [u'lstorageDiskGroupConfigDef', u'lstorageDiskGroupConfigPolicy'], [], ["Add", "Get", "Remove", "Set"])

    prop_meta = {
        "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version131a, MoPropertyMeta.INTERNAL, None, None, None, r"""((deleteAll|ignore|deleteNonPresent),){0,2}(deleteAll|ignore|deleteNonPresent){0,1}""", [], []), 
        "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version131a, MoPropertyMeta.READ_ONLY, 0x2, 0, 256, None, [], []), 
        "drive_type": MoPropertyMeta("drive_type", "driveType", "string", VersionMeta.Version131a, MoPropertyMeta.READ_WRITE, 0x4, None, None, None, ["HDD", "SSD", "unspecified"], []), 
        "min_drive_size": MoPropertyMeta("min_drive_size", "minDriveSize", "string", VersionMeta.Version131a, MoPropertyMeta.READ_WRITE, 0x8, None, None, None, ["unspecified"], ["0-10240"]), 
        "num_ded_hot_spares": MoPropertyMeta("num_ded_hot_spares", "numDedHotSpares", "string", VersionMeta.Version131a, MoPropertyMeta.READ_WRITE, 0x10, None, None, None, ["unspecified"], ["0-24"]), 
        "num_drives": MoPropertyMeta("num_drives", "numDrives", "string", VersionMeta.Version131a, MoPropertyMeta.READ_WRITE, 0x20, None, None, None, ["unspecified"], ["0-24"]), 
        "num_glob_hot_spares": MoPropertyMeta("num_glob_hot_spares", "numGlobHotSpares", "string", VersionMeta.Version131a, MoPropertyMeta.READ_WRITE, 0x40, None, None, None, ["unspecified"], ["0-24"]), 
        "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version131a, MoPropertyMeta.READ_ONLY, 0x80, 0, 256, None, [], []), 
        "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version131a, MoPropertyMeta.READ_WRITE, 0x100, None, None, r"""((removed|created|modified|deleted),){0,3}(removed|created|modified|deleted){0,1}""", [], []), 
        "use_remaining_disks": MoPropertyMeta("use_remaining_disks", "useRemainingDisks", "string", VersionMeta.Version131a, MoPropertyMeta.READ_WRITE, 0x200, None, None, None, ["false", "no", "true", "yes"], []), 
    }

    prop_map = {
        "childAction": "child_action", 
        "dn": "dn", 
        "driveType": "drive_type", 
        "minDriveSize": "min_drive_size", 
        "numDedHotSpares": "num_ded_hot_spares", 
        "numDrives": "num_drives", 
        "numGlobHotSpares": "num_glob_hot_spares", 
        "rn": "rn", 
        "status": "status", 
        "useRemainingDisks": "use_remaining_disks", 
    }

    def __init__(self, parent_mo_or_dn, **kwargs):
        self._dirty_mask = 0
        self.child_action = None
        self.drive_type = None
        self.min_drive_size = None
        self.num_ded_hot_spares = None
        self.num_drives = None
        self.num_glob_hot_spares = None
        self.status = None
        self.use_remaining_disks = None

        ManagedObject.__init__(self, "LstorageDiskGroupQualifier", parent_mo_or_dn, **kwargs)

