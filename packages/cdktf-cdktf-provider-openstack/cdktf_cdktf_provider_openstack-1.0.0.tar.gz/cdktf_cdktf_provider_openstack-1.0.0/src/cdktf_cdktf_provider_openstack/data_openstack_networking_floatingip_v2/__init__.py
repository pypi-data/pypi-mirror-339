r'''
# `data_openstack_networking_floatingip_v2`

Refer to the Terraform Registry for docs: [`data_openstack_networking_floatingip_v2`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2).
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


class DataOpenstackNetworkingFloatingipV2(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.dataOpenstackNetworkingFloatingipV2.DataOpenstackNetworkingFloatingipV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2 openstack_networking_floatingip_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        address: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        fixed_ip: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        pool: typing.Optional[builtins.str] = None,
        port_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2 openstack_networking_floatingip_v2} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#address DataOpenstackNetworkingFloatingipV2#address}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#description DataOpenstackNetworkingFloatingipV2#description}.
        :param fixed_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#fixed_ip DataOpenstackNetworkingFloatingipV2#fixed_ip}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#id DataOpenstackNetworkingFloatingipV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pool: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#pool DataOpenstackNetworkingFloatingipV2#pool}.
        :param port_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#port_id DataOpenstackNetworkingFloatingipV2#port_id}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#region DataOpenstackNetworkingFloatingipV2#region}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#status DataOpenstackNetworkingFloatingipV2#status}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#tags DataOpenstackNetworkingFloatingipV2#tags}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#tenant_id DataOpenstackNetworkingFloatingipV2#tenant_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83160c3e12aa0f0c92922f4a5d7f81fb56ef588e1457edb4933dfbb49ff8ea88)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpenstackNetworkingFloatingipV2Config(
            address=address,
            description=description,
            fixed_ip=fixed_ip,
            id=id,
            pool=pool,
            port_id=port_id,
            region=region,
            status=status,
            tags=tags,
            tenant_id=tenant_id,
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
        '''Generates CDKTF code for importing a DataOpenstackNetworkingFloatingipV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpenstackNetworkingFloatingipV2 to import.
        :param import_from_id: The id of the existing DataOpenstackNetworkingFloatingipV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpenstackNetworkingFloatingipV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417b5299da3131b3456548965a39090d527cce10c7f7c60d19cda0b7b36edb3b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFixedIp")
    def reset_fixed_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedIp", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPool")
    def reset_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPool", []))

    @jsii.member(jsii_name="resetPortId")
    def reset_port_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

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
    @jsii.member(jsii_name="allTags")
    def all_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allTags"))

    @builtins.property
    @jsii.member(jsii_name="dnsDomain")
    def dns_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsDomain"))

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedIpInput")
    def fixed_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedIpInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="poolInput")
    def pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolInput"))

    @builtins.property
    @jsii.member(jsii_name="portIdInput")
    def port_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575306edc57753e6baa2cb7ca2055adb9a3a6788f274ebee23550ad793c50ab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3929fa69b74a537519afbd434de423e09c86ab827da4257d0d9aecec229bd7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedIp")
    def fixed_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedIp"))

    @fixed_ip.setter
    def fixed_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbe9d20899afc2e10f3c57038bf693e1af85bd97f37d9d075b63d1139c8fc53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599a47bb91b936f52c8c953cbbb6043374b3081ac99594476755de5c01ce6b99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pool")
    def pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pool"))

    @pool.setter
    def pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978ee2974418068a40909ba857abdfc5c0056a5c20a4f51a946b6d02213aaa42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portId")
    def port_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portId"))

    @port_id.setter
    def port_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e5774328f59ce0ef49a2765539deb4efc24a4721f71a6419eae62bdff66f39d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016418d6beb437596048ad740fad6c0ce2213bfa1d871cb8ac0b21a5e15d3182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b01a2a65bc534f1b958780937dd7a7b5997edd10a2b5603b68e35960ca0589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69155ecafdea1a065630f11e73f838d4b26968738999aa80634075fc840d3263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ad667b7ba93947e45fcd1dbfbdeab184ecbbb02b6dfd141455f38ec8fd34a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.dataOpenstackNetworkingFloatingipV2.DataOpenstackNetworkingFloatingipV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "address": "address",
        "description": "description",
        "fixed_ip": "fixedIp",
        "id": "id",
        "pool": "pool",
        "port_id": "portId",
        "region": "region",
        "status": "status",
        "tags": "tags",
        "tenant_id": "tenantId",
    },
)
class DataOpenstackNetworkingFloatingipV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        address: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        fixed_ip: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        pool: typing.Optional[builtins.str] = None,
        port_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#address DataOpenstackNetworkingFloatingipV2#address}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#description DataOpenstackNetworkingFloatingipV2#description}.
        :param fixed_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#fixed_ip DataOpenstackNetworkingFloatingipV2#fixed_ip}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#id DataOpenstackNetworkingFloatingipV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pool: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#pool DataOpenstackNetworkingFloatingipV2#pool}.
        :param port_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#port_id DataOpenstackNetworkingFloatingipV2#port_id}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#region DataOpenstackNetworkingFloatingipV2#region}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#status DataOpenstackNetworkingFloatingipV2#status}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#tags DataOpenstackNetworkingFloatingipV2#tags}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#tenant_id DataOpenstackNetworkingFloatingipV2#tenant_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dbe54173a19dc4600112092574ce40c849e24ff54ce62b91058d6ebae0654d6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument fixed_ip", value=fixed_ip, expected_type=type_hints["fixed_ip"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pool", value=pool, expected_type=type_hints["pool"])
            check_type(argname="argument port_id", value=port_id, expected_type=type_hints["port_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if address is not None:
            self._values["address"] = address
        if description is not None:
            self._values["description"] = description
        if fixed_ip is not None:
            self._values["fixed_ip"] = fixed_ip
        if id is not None:
            self._values["id"] = id
        if pool is not None:
            self._values["pool"] = pool
        if port_id is not None:
            self._values["port_id"] = port_id
        if region is not None:
            self._values["region"] = region
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id

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
    def address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#address DataOpenstackNetworkingFloatingipV2#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#description DataOpenstackNetworkingFloatingipV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#fixed_ip DataOpenstackNetworkingFloatingipV2#fixed_ip}.'''
        result = self._values.get("fixed_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#id DataOpenstackNetworkingFloatingipV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pool(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#pool DataOpenstackNetworkingFloatingipV2#pool}.'''
        result = self._values.get("pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#port_id DataOpenstackNetworkingFloatingipV2#port_id}.'''
        result = self._values.get("port_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#region DataOpenstackNetworkingFloatingipV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#status DataOpenstackNetworkingFloatingipV2#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#tags DataOpenstackNetworkingFloatingipV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_floatingip_v2#tenant_id DataOpenstackNetworkingFloatingipV2#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpenstackNetworkingFloatingipV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpenstackNetworkingFloatingipV2",
    "DataOpenstackNetworkingFloatingipV2Config",
]

publication.publish()

def _typecheckingstub__83160c3e12aa0f0c92922f4a5d7f81fb56ef588e1457edb4933dfbb49ff8ea88(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    address: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    fixed_ip: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    pool: typing.Optional[builtins.str] = None,
    port_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__417b5299da3131b3456548965a39090d527cce10c7f7c60d19cda0b7b36edb3b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575306edc57753e6baa2cb7ca2055adb9a3a6788f274ebee23550ad793c50ab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3929fa69b74a537519afbd434de423e09c86ab827da4257d0d9aecec229bd7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbe9d20899afc2e10f3c57038bf693e1af85bd97f37d9d075b63d1139c8fc53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599a47bb91b936f52c8c953cbbb6043374b3081ac99594476755de5c01ce6b99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978ee2974418068a40909ba857abdfc5c0056a5c20a4f51a946b6d02213aaa42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5774328f59ce0ef49a2765539deb4efc24a4721f71a6419eae62bdff66f39d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016418d6beb437596048ad740fad6c0ce2213bfa1d871cb8ac0b21a5e15d3182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b01a2a65bc534f1b958780937dd7a7b5997edd10a2b5603b68e35960ca0589(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69155ecafdea1a065630f11e73f838d4b26968738999aa80634075fc840d3263(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ad667b7ba93947e45fcd1dbfbdeab184ecbbb02b6dfd141455f38ec8fd34a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbe54173a19dc4600112092574ce40c849e24ff54ce62b91058d6ebae0654d6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    address: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    fixed_ip: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    pool: typing.Optional[builtins.str] = None,
    port_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
