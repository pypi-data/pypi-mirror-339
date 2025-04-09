r'''
# `openstack_compute_quotaset_v2`

Refer to the Terraform Registry for docs: [`openstack_compute_quotaset_v2`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ComputeQuotasetV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeQuotasetV2.ComputeQuotasetV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2 openstack_compute_quotaset_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        project_id: builtins.str,
        cores: typing.Optional[jsii.Number] = None,
        fixed_ips: typing.Optional[jsii.Number] = None,
        floating_ips: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        injected_file_content_bytes: typing.Optional[jsii.Number] = None,
        injected_file_path_bytes: typing.Optional[jsii.Number] = None,
        injected_files: typing.Optional[jsii.Number] = None,
        instances: typing.Optional[jsii.Number] = None,
        key_pairs: typing.Optional[jsii.Number] = None,
        metadata_items: typing.Optional[jsii.Number] = None,
        ram: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        security_group_rules: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[jsii.Number] = None,
        server_group_members: typing.Optional[jsii.Number] = None,
        server_groups: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ComputeQuotasetV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2 openstack_compute_quotaset_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#project_id ComputeQuotasetV2#project_id}.
        :param cores: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#cores ComputeQuotasetV2#cores}.
        :param fixed_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#fixed_ips ComputeQuotasetV2#fixed_ips}.
        :param floating_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#floating_ips ComputeQuotasetV2#floating_ips}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#id ComputeQuotasetV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param injected_file_content_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#injected_file_content_bytes ComputeQuotasetV2#injected_file_content_bytes}.
        :param injected_file_path_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#injected_file_path_bytes ComputeQuotasetV2#injected_file_path_bytes}.
        :param injected_files: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#injected_files ComputeQuotasetV2#injected_files}.
        :param instances: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#instances ComputeQuotasetV2#instances}.
        :param key_pairs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#key_pairs ComputeQuotasetV2#key_pairs}.
        :param metadata_items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#metadata_items ComputeQuotasetV2#metadata_items}.
        :param ram: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#ram ComputeQuotasetV2#ram}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#region ComputeQuotasetV2#region}.
        :param security_group_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#security_group_rules ComputeQuotasetV2#security_group_rules}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#security_groups ComputeQuotasetV2#security_groups}.
        :param server_group_members: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#server_group_members ComputeQuotasetV2#server_group_members}.
        :param server_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#server_groups ComputeQuotasetV2#server_groups}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#timeouts ComputeQuotasetV2#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831c2b1427dce070f5c5b7c29624875452e9b1cdd3280f53ead27c723bcff5f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeQuotasetV2Config(
            project_id=project_id,
            cores=cores,
            fixed_ips=fixed_ips,
            floating_ips=floating_ips,
            id=id,
            injected_file_content_bytes=injected_file_content_bytes,
            injected_file_path_bytes=injected_file_path_bytes,
            injected_files=injected_files,
            instances=instances,
            key_pairs=key_pairs,
            metadata_items=metadata_items,
            ram=ram,
            region=region,
            security_group_rules=security_group_rules,
            security_groups=security_groups,
            server_group_members=server_group_members,
            server_groups=server_groups,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ComputeQuotasetV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeQuotasetV2 to import.
        :param import_from_id: The id of the existing ComputeQuotasetV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeQuotasetV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8fd454a8c40b20beb2400622fa25031f51a11afd079215f6e925f96b573ce41)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#create ComputeQuotasetV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#delete ComputeQuotasetV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#update ComputeQuotasetV2#update}.
        '''
        value = ComputeQuotasetV2Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCores")
    def reset_cores(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCores", []))

    @jsii.member(jsii_name="resetFixedIps")
    def reset_fixed_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedIps", []))

    @jsii.member(jsii_name="resetFloatingIps")
    def reset_floating_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFloatingIps", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInjectedFileContentBytes")
    def reset_injected_file_content_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInjectedFileContentBytes", []))

    @jsii.member(jsii_name="resetInjectedFilePathBytes")
    def reset_injected_file_path_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInjectedFilePathBytes", []))

    @jsii.member(jsii_name="resetInjectedFiles")
    def reset_injected_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInjectedFiles", []))

    @jsii.member(jsii_name="resetInstances")
    def reset_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstances", []))

    @jsii.member(jsii_name="resetKeyPairs")
    def reset_key_pairs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPairs", []))

    @jsii.member(jsii_name="resetMetadataItems")
    def reset_metadata_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataItems", []))

    @jsii.member(jsii_name="resetRam")
    def reset_ram(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRam", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecurityGroupRules")
    def reset_security_group_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupRules", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetServerGroupMembers")
    def reset_server_group_members(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerGroupMembers", []))

    @jsii.member(jsii_name="resetServerGroups")
    def reset_server_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerGroups", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeQuotasetV2TimeoutsOutputReference":
        return typing.cast("ComputeQuotasetV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="coresInput")
    def cores_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coresInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedIpsInput")
    def fixed_ips_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fixedIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="floatingIpsInput")
    def floating_ips_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "floatingIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="injectedFileContentBytesInput")
    def injected_file_content_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "injectedFileContentBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="injectedFilePathBytesInput")
    def injected_file_path_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "injectedFilePathBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="injectedFilesInput")
    def injected_files_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "injectedFilesInput"))

    @builtins.property
    @jsii.member(jsii_name="instancesInput")
    def instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instancesInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPairsInput")
    def key_pairs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keyPairsInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataItemsInput")
    def metadata_items_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metadataItemsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ramInput")
    def ram_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ramInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupRulesInput")
    def security_group_rules_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "securityGroupRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="serverGroupMembersInput")
    def server_group_members_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serverGroupMembersInput"))

    @builtins.property
    @jsii.member(jsii_name="serverGroupsInput")
    def server_groups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serverGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeQuotasetV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeQuotasetV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cores")
    def cores(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cores"))

    @cores.setter
    def cores(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83e173e0e970247848d23050d0bcb56d439d808e9c7c695443e2daa7005f41d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cores", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedIps")
    def fixed_ips(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fixedIps"))

    @fixed_ips.setter
    def fixed_ips(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6487be82210eceb375aaa7f4cd112b429ffc5f487cac17bb5499911ce839880b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="floatingIps")
    def floating_ips(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "floatingIps"))

    @floating_ips.setter
    def floating_ips(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98754d6662308c79b390006b45b5ccb3b9ba907f6b2e9b30f093707eb83d2895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "floatingIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12bd3679c3f6ae27741a6656e642101d5c920a51cdd25e2cd76c662fc62a5843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="injectedFileContentBytes")
    def injected_file_content_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "injectedFileContentBytes"))

    @injected_file_content_bytes.setter
    def injected_file_content_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b38ad8bf6e76a4f76e4d0c6a2125c79f2fb16607c8ad8d9c273e8612825cf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "injectedFileContentBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="injectedFilePathBytes")
    def injected_file_path_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "injectedFilePathBytes"))

    @injected_file_path_bytes.setter
    def injected_file_path_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26bdca1360cfa26b531de30dbd09147be1a32210b748e4fe8e4080484f3d4f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "injectedFilePathBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="injectedFiles")
    def injected_files(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "injectedFiles"))

    @injected_files.setter
    def injected_files(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87268e107ba705b93a15a63d9453287887df70b6b60eea4712929d01a9a8a0f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "injectedFiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instances"))

    @instances.setter
    def instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a376a9331f29a5743a1fc66ba9c1fdf2e900778bb809d7677e4bb9682bd802)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPairs")
    def key_pairs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyPairs"))

    @key_pairs.setter
    def key_pairs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9be5f16c53490d8d8c7a9748023f19ab11499ebd40be6d440944c5ccdc59288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPairs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadataItems")
    def metadata_items(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metadataItems"))

    @metadata_items.setter
    def metadata_items(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d0c13d078d0c565cfc6767783a6cb6ec1df7e79b581970514d768199846b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataItems", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3da6e4ca6161848cb4e8d0574360f771bc44350b0a73d0cf223b0a75cdbbadc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ram")
    def ram(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ram"))

    @ram.setter
    def ram(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43cbae62eab20b6be3b7711723210761277c7d49e24298a2e7f48e321f93d0df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ram", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8735030f6725bf6733ac4089256cdff5c10469a14c18b8efa5cfc8bad94f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupRules")
    def security_group_rules(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "securityGroupRules"))

    @security_group_rules.setter
    def security_group_rules(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8615c0a92963bc58a312ba208f16343e1ddca7c1d07d855c1de54bab41318ea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f977ec660ae55ae8cb291fab73c5d5e279b82beac502822eb29cb159892b1902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverGroupMembers")
    def server_group_members(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serverGroupMembers"))

    @server_group_members.setter
    def server_group_members(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24716f7fb1d1d5dfcd3b8223ab844e5fd0fd854ee996ce78a146db2cd779c14a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverGroupMembers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverGroups")
    def server_groups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serverGroups"))

    @server_groups.setter
    def server_groups(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263ab170bffa0bcd464de99af06150188d1bb6c02b1d60c599a523fb131e2904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverGroups", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.computeQuotasetV2.ComputeQuotasetV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "project_id": "projectId",
        "cores": "cores",
        "fixed_ips": "fixedIps",
        "floating_ips": "floatingIps",
        "id": "id",
        "injected_file_content_bytes": "injectedFileContentBytes",
        "injected_file_path_bytes": "injectedFilePathBytes",
        "injected_files": "injectedFiles",
        "instances": "instances",
        "key_pairs": "keyPairs",
        "metadata_items": "metadataItems",
        "ram": "ram",
        "region": "region",
        "security_group_rules": "securityGroupRules",
        "security_groups": "securityGroups",
        "server_group_members": "serverGroupMembers",
        "server_groups": "serverGroups",
        "timeouts": "timeouts",
    },
)
class ComputeQuotasetV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        project_id: builtins.str,
        cores: typing.Optional[jsii.Number] = None,
        fixed_ips: typing.Optional[jsii.Number] = None,
        floating_ips: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        injected_file_content_bytes: typing.Optional[jsii.Number] = None,
        injected_file_path_bytes: typing.Optional[jsii.Number] = None,
        injected_files: typing.Optional[jsii.Number] = None,
        instances: typing.Optional[jsii.Number] = None,
        key_pairs: typing.Optional[jsii.Number] = None,
        metadata_items: typing.Optional[jsii.Number] = None,
        ram: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        security_group_rules: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[jsii.Number] = None,
        server_group_members: typing.Optional[jsii.Number] = None,
        server_groups: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ComputeQuotasetV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#project_id ComputeQuotasetV2#project_id}.
        :param cores: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#cores ComputeQuotasetV2#cores}.
        :param fixed_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#fixed_ips ComputeQuotasetV2#fixed_ips}.
        :param floating_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#floating_ips ComputeQuotasetV2#floating_ips}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#id ComputeQuotasetV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param injected_file_content_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#injected_file_content_bytes ComputeQuotasetV2#injected_file_content_bytes}.
        :param injected_file_path_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#injected_file_path_bytes ComputeQuotasetV2#injected_file_path_bytes}.
        :param injected_files: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#injected_files ComputeQuotasetV2#injected_files}.
        :param instances: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#instances ComputeQuotasetV2#instances}.
        :param key_pairs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#key_pairs ComputeQuotasetV2#key_pairs}.
        :param metadata_items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#metadata_items ComputeQuotasetV2#metadata_items}.
        :param ram: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#ram ComputeQuotasetV2#ram}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#region ComputeQuotasetV2#region}.
        :param security_group_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#security_group_rules ComputeQuotasetV2#security_group_rules}.
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#security_groups ComputeQuotasetV2#security_groups}.
        :param server_group_members: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#server_group_members ComputeQuotasetV2#server_group_members}.
        :param server_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#server_groups ComputeQuotasetV2#server_groups}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#timeouts ComputeQuotasetV2#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ComputeQuotasetV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2349e5e7d8a1030bd08ad0d6851cb8d6e6beda5f4cb63eb17eab4a57cab4c54a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument cores", value=cores, expected_type=type_hints["cores"])
            check_type(argname="argument fixed_ips", value=fixed_ips, expected_type=type_hints["fixed_ips"])
            check_type(argname="argument floating_ips", value=floating_ips, expected_type=type_hints["floating_ips"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument injected_file_content_bytes", value=injected_file_content_bytes, expected_type=type_hints["injected_file_content_bytes"])
            check_type(argname="argument injected_file_path_bytes", value=injected_file_path_bytes, expected_type=type_hints["injected_file_path_bytes"])
            check_type(argname="argument injected_files", value=injected_files, expected_type=type_hints["injected_files"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument key_pairs", value=key_pairs, expected_type=type_hints["key_pairs"])
            check_type(argname="argument metadata_items", value=metadata_items, expected_type=type_hints["metadata_items"])
            check_type(argname="argument ram", value=ram, expected_type=type_hints["ram"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument security_group_rules", value=security_group_rules, expected_type=type_hints["security_group_rules"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument server_group_members", value=server_group_members, expected_type=type_hints["server_group_members"])
            check_type(argname="argument server_groups", value=server_groups, expected_type=type_hints["server_groups"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_id": project_id,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if cores is not None:
            self._values["cores"] = cores
        if fixed_ips is not None:
            self._values["fixed_ips"] = fixed_ips
        if floating_ips is not None:
            self._values["floating_ips"] = floating_ips
        if id is not None:
            self._values["id"] = id
        if injected_file_content_bytes is not None:
            self._values["injected_file_content_bytes"] = injected_file_content_bytes
        if injected_file_path_bytes is not None:
            self._values["injected_file_path_bytes"] = injected_file_path_bytes
        if injected_files is not None:
            self._values["injected_files"] = injected_files
        if instances is not None:
            self._values["instances"] = instances
        if key_pairs is not None:
            self._values["key_pairs"] = key_pairs
        if metadata_items is not None:
            self._values["metadata_items"] = metadata_items
        if ram is not None:
            self._values["ram"] = ram
        if region is not None:
            self._values["region"] = region
        if security_group_rules is not None:
            self._values["security_group_rules"] = security_group_rules
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if server_group_members is not None:
            self._values["server_group_members"] = server_group_members
        if server_groups is not None:
            self._values["server_groups"] = server_groups
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#project_id ComputeQuotasetV2#project_id}.'''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cores(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#cores ComputeQuotasetV2#cores}.'''
        result = self._values.get("cores")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fixed_ips(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#fixed_ips ComputeQuotasetV2#fixed_ips}.'''
        result = self._values.get("fixed_ips")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def floating_ips(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#floating_ips ComputeQuotasetV2#floating_ips}.'''
        result = self._values.get("floating_ips")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#id ComputeQuotasetV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def injected_file_content_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#injected_file_content_bytes ComputeQuotasetV2#injected_file_content_bytes}.'''
        result = self._values.get("injected_file_content_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def injected_file_path_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#injected_file_path_bytes ComputeQuotasetV2#injected_file_path_bytes}.'''
        result = self._values.get("injected_file_path_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def injected_files(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#injected_files ComputeQuotasetV2#injected_files}.'''
        result = self._values.get("injected_files")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instances(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#instances ComputeQuotasetV2#instances}.'''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def key_pairs(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#key_pairs ComputeQuotasetV2#key_pairs}.'''
        result = self._values.get("key_pairs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metadata_items(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#metadata_items ComputeQuotasetV2#metadata_items}.'''
        result = self._values.get("metadata_items")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ram(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#ram ComputeQuotasetV2#ram}.'''
        result = self._values.get("ram")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#region ComputeQuotasetV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_rules(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#security_group_rules ComputeQuotasetV2#security_group_rules}.'''
        result = self._values.get("security_group_rules")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#security_groups ComputeQuotasetV2#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def server_group_members(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#server_group_members ComputeQuotasetV2#server_group_members}.'''
        result = self._values.get("server_group_members")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def server_groups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#server_groups ComputeQuotasetV2#server_groups}.'''
        result = self._values.get("server_groups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeQuotasetV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#timeouts ComputeQuotasetV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeQuotasetV2Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeQuotasetV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.computeQuotasetV2.ComputeQuotasetV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeQuotasetV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#create ComputeQuotasetV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#delete ComputeQuotasetV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#update ComputeQuotasetV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b86d3ac89566cf07d11f095ddab60aa6064bb21391bd04186892528865ac8f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#create ComputeQuotasetV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#delete ComputeQuotasetV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_quotaset_v2#update ComputeQuotasetV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeQuotasetV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeQuotasetV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeQuotasetV2.ComputeQuotasetV2TimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a2e000e68967b8239f2e9e949415ce8406387d2ecded27e100221973d2d1aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e733a260c72988e579fffa9b16fff8694880cd3fe4d41780938c6b0550d9ebfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf91cca2ca5869211cd4585e4231d1675e47135fc113a19aa3cc9bf3e515f4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ddc3788321f4cdd59dc6f7e6f0937ba968f706fe956e9d9ced59971efc0631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeQuotasetV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeQuotasetV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeQuotasetV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cd170db0def43ed6dd036f997f18ec1cfc3f519049ae0fee287053393a3cb2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeQuotasetV2",
    "ComputeQuotasetV2Config",
    "ComputeQuotasetV2Timeouts",
    "ComputeQuotasetV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__831c2b1427dce070f5c5b7c29624875452e9b1cdd3280f53ead27c723bcff5f6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    project_id: builtins.str,
    cores: typing.Optional[jsii.Number] = None,
    fixed_ips: typing.Optional[jsii.Number] = None,
    floating_ips: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    injected_file_content_bytes: typing.Optional[jsii.Number] = None,
    injected_file_path_bytes: typing.Optional[jsii.Number] = None,
    injected_files: typing.Optional[jsii.Number] = None,
    instances: typing.Optional[jsii.Number] = None,
    key_pairs: typing.Optional[jsii.Number] = None,
    metadata_items: typing.Optional[jsii.Number] = None,
    ram: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    security_group_rules: typing.Optional[jsii.Number] = None,
    security_groups: typing.Optional[jsii.Number] = None,
    server_group_members: typing.Optional[jsii.Number] = None,
    server_groups: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ComputeQuotasetV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fd454a8c40b20beb2400622fa25031f51a11afd079215f6e925f96b573ce41(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83e173e0e970247848d23050d0bcb56d439d808e9c7c695443e2daa7005f41d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6487be82210eceb375aaa7f4cd112b429ffc5f487cac17bb5499911ce839880b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98754d6662308c79b390006b45b5ccb3b9ba907f6b2e9b30f093707eb83d2895(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12bd3679c3f6ae27741a6656e642101d5c920a51cdd25e2cd76c662fc62a5843(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b38ad8bf6e76a4f76e4d0c6a2125c79f2fb16607c8ad8d9c273e8612825cf8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26bdca1360cfa26b531de30dbd09147be1a32210b748e4fe8e4080484f3d4f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87268e107ba705b93a15a63d9453287887df70b6b60eea4712929d01a9a8a0f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a376a9331f29a5743a1fc66ba9c1fdf2e900778bb809d7677e4bb9682bd802(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9be5f16c53490d8d8c7a9748023f19ab11499ebd40be6d440944c5ccdc59288(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d0c13d078d0c565cfc6767783a6cb6ec1df7e79b581970514d768199846b5c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3da6e4ca6161848cb4e8d0574360f771bc44350b0a73d0cf223b0a75cdbbadc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43cbae62eab20b6be3b7711723210761277c7d49e24298a2e7f48e321f93d0df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8735030f6725bf6733ac4089256cdff5c10469a14c18b8efa5cfc8bad94f29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8615c0a92963bc58a312ba208f16343e1ddca7c1d07d855c1de54bab41318ea6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f977ec660ae55ae8cb291fab73c5d5e279b82beac502822eb29cb159892b1902(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24716f7fb1d1d5dfcd3b8223ab844e5fd0fd854ee996ce78a146db2cd779c14a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263ab170bffa0bcd464de99af06150188d1bb6c02b1d60c599a523fb131e2904(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2349e5e7d8a1030bd08ad0d6851cb8d6e6beda5f4cb63eb17eab4a57cab4c54a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project_id: builtins.str,
    cores: typing.Optional[jsii.Number] = None,
    fixed_ips: typing.Optional[jsii.Number] = None,
    floating_ips: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    injected_file_content_bytes: typing.Optional[jsii.Number] = None,
    injected_file_path_bytes: typing.Optional[jsii.Number] = None,
    injected_files: typing.Optional[jsii.Number] = None,
    instances: typing.Optional[jsii.Number] = None,
    key_pairs: typing.Optional[jsii.Number] = None,
    metadata_items: typing.Optional[jsii.Number] = None,
    ram: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    security_group_rules: typing.Optional[jsii.Number] = None,
    security_groups: typing.Optional[jsii.Number] = None,
    server_group_members: typing.Optional[jsii.Number] = None,
    server_groups: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ComputeQuotasetV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b86d3ac89566cf07d11f095ddab60aa6064bb21391bd04186892528865ac8f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a2e000e68967b8239f2e9e949415ce8406387d2ecded27e100221973d2d1aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e733a260c72988e579fffa9b16fff8694880cd3fe4d41780938c6b0550d9ebfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf91cca2ca5869211cd4585e4231d1675e47135fc113a19aa3cc9bf3e515f4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ddc3788321f4cdd59dc6f7e6f0937ba968f706fe956e9d9ced59971efc0631(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd170db0def43ed6dd036f997f18ec1cfc3f519049ae0fee287053393a3cb2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeQuotasetV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
