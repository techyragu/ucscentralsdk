# Copyright 2015 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging

from . import ucscentralgenutils
from . import ucscentralcoreutils
from .ucscentralexception import UcsCentralException
from .ucscentralconstants import NamingId
from .ucscentralsession import UcsCentralSession
from .ucscentralmethodfactory import config_resolve_classes

log = logging.getLogger('ucs')


class UcsCentralHandle(UcsCentralSession):
    """
    UcsCentralHandle class is the user interface point for any Ucs related
    communication.

    Args:
        ip (str): The IP or Hostname of the UCS Server
        username (str): The username as configured on the UCS Server
        password (str): The password as configured on the UCS Server
        port (int or None): The port number to be used during connection
        secure (bool or None): True for secure connection, otherwise False
        proxy (str): The proxy object to be used to connect

    Example:
        handle = UcsCentralHandle("192.168.1.1","admin","password")\n
        handle = UcsCentralHandle("192.168.1.1","admin","password",
                                    secure=True)\n
        handle = UcsCentralHandle("192.168.1.1","admin","password",
                                    secure=False)\n
        handle = UcsCentralHandle("192.168.1.1","admin","password", port=80)\n
        handle = UcsCentralHandle("192.168.1.1","admin","password", port=443)\n
        handle = UcsCentralHandle("192.168.1.1","admin","password", port=100,
                            secure=True)\n
        handle = UcsCentralHandle("192.168.1.1","admin","password", port=100,
                            secure=False)\n
    """

    def __init__(self, ip, username, password, port=None, secure=None,
                 proxy=None):
        UcsCentralSession.__init__(self, ip, username, password, port, secure,
                                   proxy)
        self.__to_commit = {}

    def set_dump_xml(self):
        """
        Enables the logging of xml requests and responses.
        """

        self._set_dump_xml()

    def unset_dump_xml(self):
        """
        Disables the logging of xml requests and responses.
        """

        self._unset_dump_xml()

    def login(self, auto_refresh=False, force=False):
        """
        Initiates a connection to the server referenced by the
        UcsCentralHandle.
        A cookie is populated in the UcsCentralHandle, if the login is
        successful.

        Args:
            auto_refresh (bool): if set to True, it refresh the cookie
                continuously
            force (bool): if set to True it reconnects even if cookie exists
                and is valid for respective connection.

        Returns:
            True on successful connect

        Example:
            handle.login()\n
            handle.login(auto_refresh=True)\n
            handle.login(force=True)\n
            handle.login(auto_refresh=True, force=True)\n

            where handle is UcsCentralHandle()
        """

        return self._login(auto_refresh, force)

    def logout(self):
        """
        Disconnects from the server referenced by the UcsCentralHandle.

        Args:
            None

        Returns:
            True on successful disconnect

        Example:
            handle.logout()

            where handle is UcsCentralHandle()
        """

        return self._logout()

    def process_xml_elem(self, elem):
        """
        process_xml_elem is a helper method which posts xml elements to the
        server and returns parsed response. It's role is to operate on the
        output of methods from ucscentralmethodfactory, which return xml
        element node(s).

        Args:
            elem (xml element object)

        Returns:
            mo list or external method object

        Example:
            elem = ucscentralmethodfactory.config_find_dns_by_class_id(
                   cookie=handle.cookie, class_id="LsServer", in_filter=None)\n
            dn_objs = handle.process_xml_elem(elem)
        """

        response = self.post_elem(elem)
        if response.error_code != 0:
            raise UcsCentralException(response.error_code,
                                      response.error_descr)

        if hasattr(response, "out_config"):
            return response.out_config.child
        elif hasattr(response, "out_configs"):
            mo_list = []
            pair_flag = False
            for ch_ in response.out_configs.child:
                if pair_flag or ch_.get_class_id() != "Pair":
                    mo_list.append(ch_)
                elif ch_.get_class_id() == "Pair":
                    mo_list.extend(ch_.child)
                    pair_flag = True
            return mo_list
        elif hasattr(response, "out_dns"):
            return response.out_dns.child
        else:
            return response

    def get_auth_token(self):
        """
        Returns a token that is used for UCS Central authentication.

        Args:
            None

        Returns:
            auth_token (str)

        Example:
            handle.get_auth_token()

        """

        from .ucscentralmethodfactory import aaa_get_n_compute_auth_token_by_dn

        auth_token = None
        mo = self.query_classid(class_id=NamingId.COMPUTE_BLADE)
        if not mo:
            mo = self.query_classid(class_id=NamingId.COMPUTE_RACK_UNIT)

        if mo:
            elem = aaa_get_n_compute_auth_token_by_dn(
                cookie=self.cookie,
                in_cookie=self.cookie,
                in_dn=mo[0].dn,
                in_number_of=1)
            response = self.post_elem(elem)
            if response.error_code != 0:
                raise UcsCentralException(response.error_code,
                                   response.error_descr)

            # cat = self.AaaGetNComputeAuthTokenByDn(mo[0].Dn, 1, None)
            auth_token = response.out_tokens.split(',')[0]

        return auth_token

    def query_dns(self, *dns):
        """
        Queries multiple obects from the server based of a comma separated list
        of their distinguised names.

        Args:
            dns (comma separated strings): distinguished names to be
                queried for

        Returns:
            Dictionary {dn1: object, dn2: object2}

        Example:
            obj = handle.lookup_by_dns("fabric/lan/net-100",
                                       "fabric/lan/net-101")
        """

        from .ucscentralbasetype import DnSet, Dn
        from .ucscentralmethodfactory import config_resolve_dns

        if not dns:
            raise ValueError("Provide Comma Separated string of Dns")

        dn_list = [dn.strip() for dn in dns]
        dn_dict = {}
        for dn_ in dn_list:
            dn_dict[dn_] = None

        dn_set = DnSet()
        for dn_ in dn_dict:
            dn_obj = Dn()
            dn_obj.value = dn_
            dn_set.child_add(dn_obj)

        elem = config_resolve_dns(cookie=self.cookie, in_dns=dn_set)
        response = self.post_elem(elem)
        if response.error_code != 0:
            raise UcsCentralException(response.error_code,
                                      response.error_descr)

        for out_mo in response.out_configs.child:
            dn_dict[out_mo.dn] = out_mo

        return dn_dict

    def query_classids(self, *class_ids):
        """
        Queries multiple obects from the server based of a comma separated list
        of their class Ids.

        Args:
            class_ids (comma separated strings): Class Ids to be queried for

        Returns:
        Dictionary {class_id1: [objects], class_id2: [objects]}

        Example:
            obj = handle.lookup_by_dns("OrgOrg", "LsServer")
        """

        from .ucscentralbasetype import ClassIdSet, ClassId
        from .ucscentralmeta import MO_CLASS_ID

        if not class_ids:
            raise ValueError("Provide Comma Separated string of Class Ids")

        class_id_list = [class_id.strip() for class_id in class_ids]
        class_id_dict = {}
        class_id_set = ClassIdSet()

        for class_id_ in class_id_list:
            class_id_obj = ClassId()

            meta_class_id = ucscentralgenutils.word_u(class_id_)
            if meta_class_id in MO_CLASS_ID:
                class_id_dict[meta_class_id] = []
                class_id_obj.value = ucscentralgenutils.word_l(class_id_)
            else:
                class_id_dict[class_id_] = []
                class_id_obj.value = class_id_

            class_id_set.child_add(class_id_obj)

        elem = config_resolve_classes(cookie=self.cookie, in_ids=class_id_set)
        response = self.post_elem(elem)
        if response.error_code != 0:
            raise UcsCentralException(response.error_code, response.error_descr)

        for out_mo in response.out_configs.child:
            class_id_dict[out_mo.get_class_id()].append(out_mo)

        return class_id_dict

    def query_dn(self, dn, hierarchy=False, need_response=False):
        """
        Finds an object using it's distinguished name.

        Args:
            dn (str): distinguished name of the object to be queried for.
            hierarchy(bool): True/False,
                                get all objects in hierarchy if True
            need_response(bool): True/False,
                                return the response xml node, instead of parsed
                                objects

        Returns:
            managedobject or None   by default\n
            managedobject list      if hierarchy=True\n
            externalmethod object   if need_response=True\n

        Example:
            obj = handle.lookup_by_dn("fabric/lan/net-100")\n
            obj = handle.lookup_by_dn("fabric/lan/net-100", hierarchy=True)\n
            obj = handle.lookup_by_dn("fabric/lan/net-100",
                                      need_response=True)\n
            obj = handle.lookup_by_dn("fabric/lan/net-100", hierarchy=True,
                                       need_response=True)\n
        """

        from .ucscentralbasetype import DnSet, Dn
        from .ucscentralmethodfactory import config_resolve_dns

        if not dn:
            raise ValueError("Provide dn.")

        dn_set = DnSet()
        dn_obj = Dn()
        dn_obj.value = dn
        dn_set.child_add(dn_obj)

        elem = config_resolve_dns(cookie=self.cookie,
                                  in_dns=dn_set,
                                  in_hierarchical=hierarchy)
        response = self.post_elem(elem)
        if response.error_code != 0:
            raise UcsCentralException(response.error_code, response.error_descr)

        if need_response:
            return response

        if hierarchy:
            out_mo_list = \
                ucscentralcoreutils.extract_molist_from_method_response(
                    response,
                    hierarchy)
            return out_mo_list

        mo = None
        if len(response.out_configs.child) > 0:
            mo = response.out_configs.child[0]
        return mo

    def query_classid(self, class_id=None, filter_str=None, hierarchy=False,
                      need_response=False):
        """
        Finds an object using it's class id.

        Args:
            class_id (str): class id of the object to be queried for.
            filter_str(str): query objects with specific property with
                             specific value or pattern specifying value.

                      (property_name, "property_value, type="filter_type")\n
                      property_name: Name of the Property\n
                      property_value: Value of the property (str or
                                      regular expression)\n
                      filter_type: eq - equal to\n
                                   ne - not equal to\n
                                   ge - greater than or equal to\n
                                   gt - greater than\n
                                   le - less than or equal to\n
                                   lt - less than\n
                                   re - regular expression\n

                      logical filter type: not, and, or\n

                      e.g. '(dn,"org-root/ls-C1_B1", type="eq")
                            or (name, "event", type="re", flag="I")'\n
            hierarchy(bool): if set to True will return all the child
                             hierarchical objects.
            need_response(bool): if set to True will return only response
                                object.


        Returns:
            managedobjectlist or None   by default\n
            managedobjectlist or None   if hierarchy=True\n
            methodresponse              if need_response=True\n

        Example:
            obj = handle.query_classid(class_id="LsServer")\n
            obj = handle.query_classid(class_id="LsServer", hierarchy=True)\n
            obj = handle.query_classid(class_id="LsServer",
                                       need_response=True)\n

            filter_str = '(dn,"org-root/ls-C1_B1", type="eq") or
                        (name, "event", type="re", flag="I")'\n
            obj = handle.query_classid(class_id="LsServer",
                                       filter_str=filter_str)\n
        """

        from .ucscentralfilter import generate_infilter
        from .ucscentralmethodfactory import config_resolve_class

        if not class_id:
            raise ValueError("Provide Parameter class_id")

        meta_class_id = \
            ucscentralcoreutils.find_class_id_in_mo_meta_ignore_case(class_id)
        if meta_class_id:
            is_meta_class_id = True
        else:
            meta_class_id = class_id
            is_meta_class_id = False

        if filter_str:
            in_filter = generate_infilter(meta_class_id, filter_str,
                                          is_meta_class_id)
        else:
            in_filter = None

        elem = config_resolve_class(cookie=self.cookie,
                                    class_id=meta_class_id,
                                    in_filter=in_filter,
                                    in_hierarchical=hierarchy)
        response = self.post_elem(elem)
        if response.error_code != 0:
            raise UcsCentralException(response.error_code, response.error_descr)

        if need_response:
            return response

        out_mo_list = ucscentralcoreutils.extract_molist_from_method_response(
            response, hierarchy)
        return out_mo_list

    def query_children(self, in_mo=None, in_dn=None, class_id=None,
                       filter_str=None, hierarchy=False):
        """
        Finds children of a given managed object or distinguished name.
        Arguments can be specified to query only a specific type(class_id)
        of children.
        Arguments can also be specified to query only direct children or the
        entire hierarchy of children.

        Args:
            in_mo (managed object): query children managed object under this
                                        object.
            in_dn (dn string): query children managed object for a
                                given managed object of the respective dn.
            class_id(str): by default None, if given find only specific
                            children object for a given class_id.
            filter_str(str): query objects with specific property with specific
                            value or pattern specifying value.

                      (property_name, "property_value, type="filter_type")\n
                      property_name: Name of the Property\n
                      property_value: Value of the property (str or regular
                                      expression)\n
                      filter_type: eq - equal to\n
                                   ne - not equal to\n
                                   ge - greater than or equal to\n
                                   gt - greater than\n
                                   le - less than or equal to\n
                                   lt - less than\n
                                   re - regular expression\n

                      logical filter type: not, and, or\n

                      e.g. '(dn,"org-root/ls-C1_B1", type="eq") or (name,
                                            "event", type="re", flag="I")'\n
            hierarchy(bool): if set to True will return all the child
                             hierarchical objects.
            need_response(bool): if set to True will return only response
                                object.
            hierarchy(bool): if set to True will return all the child
                              hierarchical objects.

        Returns:
            managedobjectlist or None   by default\n
            managedobjectlist or None   if hierarchy=True\n

        Example:
            mo_list = handle.query_children(in_mo=mo)\n
            mo_list = handle.query_children(in_mo=mo, class_id="classid")\n
            mo_list = handle.query_children(in_dn=dn)\n
            mo_list = handle.query_children(in_dn=dn, class_id="classid")\n
            mo_list = handle.query_children(in_dn="org-root",
                        class_id="LsServer", filter_str="(usr_lbl, 'test')")
            mo_list = handle.query_children(in_dn="org-root",
                class_id="LsServer", filter_str="(usr_lbl, 'test', type='eq')")
        """

        from .ucscentralfilter import generate_infilter
        from .ucscentralmethodfactory import config_resolve_children

        if not in_mo and not in_dn:
            raise ValueError('[Error]: GetChild: Provide in_mo or in_dn.')

        parent_dn = None
        if in_mo:
            parent_dn = in_mo.dn
        elif in_dn:
            parent_dn = in_dn

        in_filter = None

        if class_id:
            meta_class_id = \
                ucscentralcoreutils.find_class_id_in_mo_meta_ignore_case(
                    class_id)
            if meta_class_id:
                is_meta_class_id = True
            else:
                meta_class_id = class_id
                is_meta_class_id = False

            if filter_str:
                in_filter = generate_infilter(meta_class_id, filter_str,
                                              is_meta_class_id)
        else:
            meta_class_id = class_id

        elem = config_resolve_children(cookie=self.cookie,
                                       class_id=meta_class_id,
                                       in_dn=parent_dn,
                                       in_filter=in_filter,
                                       in_hierarchical=hierarchy)
        response = self.post_elem(elem)
        if response.error_code != 0:
            raise UcsCentralException(response.error_code, response.error_descr)

        out_mo_list = ucscentralcoreutils.extract_molist_from_method_response(
            response, hierarchy)

        return out_mo_list

    def add_mo(self, mo, modify_present=False):
        """
        Adds a managed object to the UcsCentralHandle commit buffer.
        This method does not trigger a commit by itself.
        This needs to be followed by a handle.commit() either immediately or
        after more operations to ensure successful addition of object on server

        Args:
            mo (managedobject): ManagedObject to be added.
            modify_present (bool): True/False,
                                    overwrite existing object if True

        Returns:
            None

        Example:
            obj = handle.add_mo(mo)\n
            handle.commit()\n
        """

        if modify_present in ucscentralgenutils.AFFIRMATIVE_LIST:
            mo.status = "created,modified"
        else:
            mo.status = "created"

        self.__to_commit[mo.dn] = mo

    def set_mo(self, mo):
        """
        Modifies a managed object and adds it to UcsCentralHandle commit buffer (if
         not already in it).
        This method does not trigger a commit by itself.
        This needs to be followed by a handle.commit() either immediately or
        after more operations to ensure successful modification of object on
        server.

        Args:
            mo (managedobject): Managed object with modified properties.

        Returns:
            None

        Example:
            obj = handle.set_mo(mo)\n
            handle.commit()\n
        """

        mo.status = "modified"
        self.__to_commit[mo.dn] = mo

    def remove_mo(self, mo):
        """
        Removes a managed object.
        This method does not trigger a commit by itself.
        This needs to be followed by a handle.commit() either immediately or
        after more operations to ensure successful removal of object from the
        server.

        Args:
            mo (managedobject): Managed object to be removed.

        Returns:
            None

        Example:
            obj = handle.remove_mo(mo)\n
            handle.commit()\n
        """

        mo.status = "deleted"
        if mo.parent_mo:
            mo.parent_mo.child_remove(mo)

        self.__to_commit[mo.dn] = mo

    def commit(self):
        """
        Commit the buffer to the server. Pushes all the configuration changes
        so far to the server.
        Configuration could be added to the commit buffer using add_mo(),
        set_mo(), remove_mo() prior to making a handle.commit()

        Args:
            None

        Returns:
            None

        Example:
            handle.commit()\n
        """

        from .ucscentralbasetype import ConfigMap, Dn, DnSet, Pair
        from .ucscentralmethodfactory import config_resolve_dns
        from .ucscentralmethodfactory import config_conf_mos

        refresh_dict = {}
        mo_dict = self.__to_commit
        if not mo_dict:
            log.debug("No Mo to be Committed")
            return None

        config_map = ConfigMap()
        for mo_dn in mo_dict:
            mo = mo_dict[mo_dn]
            child_list = mo.child
            while len(child_list) > 0:
                current_child_list = child_list
                child_list = []
                for child_mo in current_child_list:
                    if child_mo.is_dirty():
                        refresh_dict[child_mo.dn] = child_mo
                    child_list.extend(child_mo.child)

            pair = Pair()
            pair.key = mo_dn
            pair.child_add(mo_dict[mo_dn])
            config_map.child_add(pair)

        elem = config_conf_mos(self.cookie, config_map, False)
        response = self.post_elem(elem)
        if response.error_code != 0:
            raise UcsCentralException(response.error_code,
                                      response.error_descr)

        for pair_ in response.out_configs.child:
            for out_mo in pair_.child:
                out_mo.sync_mo(mo_dict[out_mo.dn])

        if refresh_dict:
            dn_set = DnSet()
            for dn_ in refresh_dict:
                dn_obj = Dn()
                dn_obj.value = dn_
                dn_set.child_add(dn_obj)

            elem = config_resolve_dns(cookie=self.cookie,
                                      in_dns=dn_set)
            response = self.post_elem(elem)
            if response.error_code != 0:
                raise UcsCentralException(response.error_code,
                                          response.error_descr)

            for out_mo in response.out_configs.child:
                out_mo.sync_mo(refresh_dict[out_mo.dn])

        self.__to_commit = {}

    def commit_buffer_discard(self):
        """
        Discard the configuration changes in the commit buffer.

        Args:
            None

        Returns:
            None

        Example:
            handle.commit_buffer_discard()
        """

        self.__to_commit = {}
