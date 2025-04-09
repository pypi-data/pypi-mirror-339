r'''
# `data_openstack_dns_zone_v2`

Refer to the Terraform Registry for docs: [`data_openstack_dns_zone_v2`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2).
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


class DataOpenstackDnsZoneV2(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.dataOpenstackDnsZoneV2.DataOpenstackDnsZoneV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2 openstack_dns_zone_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        all_projects: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        created_at: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        masters: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        pool_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        serial: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        transferred_at: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        updated_at: typing.Optional[builtins.str] = None,
        version: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2 openstack_dns_zone_v2} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param all_projects: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#all_projects DataOpenstackDnsZoneV2#all_projects}.
        :param attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#attributes DataOpenstackDnsZoneV2#attributes}.
        :param created_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#created_at DataOpenstackDnsZoneV2#created_at}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#description DataOpenstackDnsZoneV2#description}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#email DataOpenstackDnsZoneV2#email}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#id DataOpenstackDnsZoneV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param masters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#masters DataOpenstackDnsZoneV2#masters}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#name DataOpenstackDnsZoneV2#name}.
        :param pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#pool_id DataOpenstackDnsZoneV2#pool_id}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#project_id DataOpenstackDnsZoneV2#project_id}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#region DataOpenstackDnsZoneV2#region}.
        :param serial: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#serial DataOpenstackDnsZoneV2#serial}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#status DataOpenstackDnsZoneV2#status}.
        :param transferred_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#transferred_at DataOpenstackDnsZoneV2#transferred_at}.
        :param ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#ttl DataOpenstackDnsZoneV2#ttl}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#type DataOpenstackDnsZoneV2#type}.
        :param updated_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#updated_at DataOpenstackDnsZoneV2#updated_at}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#version DataOpenstackDnsZoneV2#version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__268f31c782998a35a4ba363a8ee8557ddb96ee5c4962cc6166acb86d60d0fec7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpenstackDnsZoneV2Config(
            all_projects=all_projects,
            attributes=attributes,
            created_at=created_at,
            description=description,
            email=email,
            id=id,
            masters=masters,
            name=name,
            pool_id=pool_id,
            project_id=project_id,
            region=region,
            serial=serial,
            status=status,
            transferred_at=transferred_at,
            ttl=ttl,
            type=type,
            updated_at=updated_at,
            version=version,
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
        '''Generates CDKTF code for importing a DataOpenstackDnsZoneV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpenstackDnsZoneV2 to import.
        :param import_from_id: The id of the existing DataOpenstackDnsZoneV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpenstackDnsZoneV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7dd06afc91c4fc9dd0afc4940b66ba1fc7c522b910100a86c5bc8fc9649286)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAllProjects")
    def reset_all_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllProjects", []))

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetCreatedAt")
    def reset_created_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedAt", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMasters")
    def reset_masters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasters", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPoolId")
    def reset_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPoolId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSerial")
    def reset_serial(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSerial", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTransferredAt")
    def reset_transferred_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransferredAt", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUpdatedAt")
    def reset_updated_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatedAt", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

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
    @jsii.member(jsii_name="allProjectsInput")
    def all_projects_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="createdAtInput")
    def created_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdAtInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mastersInput")
    def masters_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "mastersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="poolIdInput")
    def pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serialInput")
    def serial_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serialInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="transferredAtInput")
    def transferred_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transferredAtInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="updatedAtInput")
    def updated_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updatedAtInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="allProjects")
    def all_projects(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allProjects"))

    @all_projects.setter
    def all_projects(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ada8e07650d53a0d63a5aa0e604fd031e442b5255db092f7bc6e92885048e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea5234dddac8bbd6cd897c23dbeccb2a6a212ce4e0a3f0f9ddcdf332461ff554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @created_at.setter
    def created_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b454c39a23f82c84809eee589b0cee3ee84c7be2b481efde7b9a14a59ff7d038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a12cc50d08bafe9fdc7d1175faf65b54e545370c7216badff63c96ab43f016c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a2991d05f41bb0a5b7a326352ce7dba7df2c77b4f447af139fe49adc3a6e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca844b124caeca02ea955956ff0389b5312112dcd1f8d351a05162459b32387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masters")
    def masters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "masters"))

    @masters.setter
    def masters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9180bbf8d68824c8e618ccc8b5b68131af31ea329cf68451fd812b01c6d3ff3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c5511f7425bb27537a6cec1a021ff8b4da32c72f4134545706ce6659b68080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="poolId")
    def pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolId"))

    @pool_id.setter
    def pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7dd0550c442ee678b57abcad4731622ac9b507d8f2f2a32acdba9fe603214f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe9106cccf15da777cf5fbbbbaee25ec756f3311948bbb3d9a77d9d9381620c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5143c1460e8feae7286d19ffdceeef90596a9f93d7522a6f72c1e172ef1c80b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serial")
    def serial(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serial"))

    @serial.setter
    def serial(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7032847420ff116de54aa853cec89962ebb773ff3121693676b3d40b6bab521a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serial", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169d607d774fc28bec7421fb307928f07152070e01f433be88609ee22375b754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transferredAt")
    def transferred_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transferredAt"))

    @transferred_at.setter
    def transferred_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2c667a171498d0dfa8f3ac04b2a7c13fa931328b7052a3528b3480b5cc58dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transferredAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe6d3c12bfe99a7712ac85112c04aa601c82d8d4b1c1adc8d49944e53f52090d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c460b8bae148a28c734452f6ff6a73dc2023a8ea1c0352aa58ef744612aa56e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @updated_at.setter
    def updated_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffdcf5e48e82a889d138b3ac5fc8405dd46130d1e77e124c16c9afc936ae7d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatedAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @version.setter
    def version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e02506b0fdcbc9aad40c034238cad8e043adc0c82e46c256c637426f9d9d554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.dataOpenstackDnsZoneV2.DataOpenstackDnsZoneV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "all_projects": "allProjects",
        "attributes": "attributes",
        "created_at": "createdAt",
        "description": "description",
        "email": "email",
        "id": "id",
        "masters": "masters",
        "name": "name",
        "pool_id": "poolId",
        "project_id": "projectId",
        "region": "region",
        "serial": "serial",
        "status": "status",
        "transferred_at": "transferredAt",
        "ttl": "ttl",
        "type": "type",
        "updated_at": "updatedAt",
        "version": "version",
    },
)
class DataOpenstackDnsZoneV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        all_projects: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        created_at: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        masters: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        pool_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        serial: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        transferred_at: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        updated_at: typing.Optional[builtins.str] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param all_projects: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#all_projects DataOpenstackDnsZoneV2#all_projects}.
        :param attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#attributes DataOpenstackDnsZoneV2#attributes}.
        :param created_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#created_at DataOpenstackDnsZoneV2#created_at}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#description DataOpenstackDnsZoneV2#description}.
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#email DataOpenstackDnsZoneV2#email}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#id DataOpenstackDnsZoneV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param masters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#masters DataOpenstackDnsZoneV2#masters}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#name DataOpenstackDnsZoneV2#name}.
        :param pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#pool_id DataOpenstackDnsZoneV2#pool_id}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#project_id DataOpenstackDnsZoneV2#project_id}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#region DataOpenstackDnsZoneV2#region}.
        :param serial: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#serial DataOpenstackDnsZoneV2#serial}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#status DataOpenstackDnsZoneV2#status}.
        :param transferred_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#transferred_at DataOpenstackDnsZoneV2#transferred_at}.
        :param ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#ttl DataOpenstackDnsZoneV2#ttl}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#type DataOpenstackDnsZoneV2#type}.
        :param updated_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#updated_at DataOpenstackDnsZoneV2#updated_at}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#version DataOpenstackDnsZoneV2#version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61af23fa06bd2a3cc4e81342c57d787ea4851df79d6bbcf1571c437b50f76a43)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument all_projects", value=all_projects, expected_type=type_hints["all_projects"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument masters", value=masters, expected_type=type_hints["masters"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pool_id", value=pool_id, expected_type=type_hints["pool_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument serial", value=serial, expected_type=type_hints["serial"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument transferred_at", value=transferred_at, expected_type=type_hints["transferred_at"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
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
        if all_projects is not None:
            self._values["all_projects"] = all_projects
        if attributes is not None:
            self._values["attributes"] = attributes
        if created_at is not None:
            self._values["created_at"] = created_at
        if description is not None:
            self._values["description"] = description
        if email is not None:
            self._values["email"] = email
        if id is not None:
            self._values["id"] = id
        if masters is not None:
            self._values["masters"] = masters
        if name is not None:
            self._values["name"] = name
        if pool_id is not None:
            self._values["pool_id"] = pool_id
        if project_id is not None:
            self._values["project_id"] = project_id
        if region is not None:
            self._values["region"] = region
        if serial is not None:
            self._values["serial"] = serial
        if status is not None:
            self._values["status"] = status
        if transferred_at is not None:
            self._values["transferred_at"] = transferred_at
        if ttl is not None:
            self._values["ttl"] = ttl
        if type is not None:
            self._values["type"] = type
        if updated_at is not None:
            self._values["updated_at"] = updated_at
        if version is not None:
            self._values["version"] = version

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
    def all_projects(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#all_projects DataOpenstackDnsZoneV2#all_projects}.'''
        result = self._values.get("all_projects")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#attributes DataOpenstackDnsZoneV2#attributes}.'''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def created_at(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#created_at DataOpenstackDnsZoneV2#created_at}.'''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#description DataOpenstackDnsZoneV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#email DataOpenstackDnsZoneV2#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#id DataOpenstackDnsZoneV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def masters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#masters DataOpenstackDnsZoneV2#masters}.'''
        result = self._values.get("masters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#name DataOpenstackDnsZoneV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#pool_id DataOpenstackDnsZoneV2#pool_id}.'''
        result = self._values.get("pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#project_id DataOpenstackDnsZoneV2#project_id}.'''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#region DataOpenstackDnsZoneV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serial(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#serial DataOpenstackDnsZoneV2#serial}.'''
        result = self._values.get("serial")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#status DataOpenstackDnsZoneV2#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transferred_at(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#transferred_at DataOpenstackDnsZoneV2#transferred_at}.'''
        result = self._values.get("transferred_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#ttl DataOpenstackDnsZoneV2#ttl}.'''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#type DataOpenstackDnsZoneV2#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#updated_at DataOpenstackDnsZoneV2#updated_at}.'''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/dns_zone_v2#version DataOpenstackDnsZoneV2#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpenstackDnsZoneV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpenstackDnsZoneV2",
    "DataOpenstackDnsZoneV2Config",
]

publication.publish()

def _typecheckingstub__268f31c782998a35a4ba363a8ee8557ddb96ee5c4962cc6166acb86d60d0fec7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    all_projects: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    created_at: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    masters: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    pool_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    serial: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    transferred_at: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__ab7dd06afc91c4fc9dd0afc4940b66ba1fc7c522b910100a86c5bc8fc9649286(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ada8e07650d53a0d63a5aa0e604fd031e442b5255db092f7bc6e92885048e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5234dddac8bbd6cd897c23dbeccb2a6a212ce4e0a3f0f9ddcdf332461ff554(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b454c39a23f82c84809eee589b0cee3ee84c7be2b481efde7b9a14a59ff7d038(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a12cc50d08bafe9fdc7d1175faf65b54e545370c7216badff63c96ab43f016c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a2991d05f41bb0a5b7a326352ce7dba7df2c77b4f447af139fe49adc3a6e04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca844b124caeca02ea955956ff0389b5312112dcd1f8d351a05162459b32387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9180bbf8d68824c8e618ccc8b5b68131af31ea329cf68451fd812b01c6d3ff3e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c5511f7425bb27537a6cec1a021ff8b4da32c72f4134545706ce6659b68080(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7dd0550c442ee678b57abcad4731622ac9b507d8f2f2a32acdba9fe603214f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe9106cccf15da777cf5fbbbbaee25ec756f3311948bbb3d9a77d9d9381620c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5143c1460e8feae7286d19ffdceeef90596a9f93d7522a6f72c1e172ef1c80b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7032847420ff116de54aa853cec89962ebb773ff3121693676b3d40b6bab521a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169d607d774fc28bec7421fb307928f07152070e01f433be88609ee22375b754(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2c667a171498d0dfa8f3ac04b2a7c13fa931328b7052a3528b3480b5cc58dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6d3c12bfe99a7712ac85112c04aa601c82d8d4b1c1adc8d49944e53f52090d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c460b8bae148a28c734452f6ff6a73dc2023a8ea1c0352aa58ef744612aa56e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffdcf5e48e82a889d138b3ac5fc8405dd46130d1e77e124c16c9afc936ae7d18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e02506b0fdcbc9aad40c034238cad8e043adc0c82e46c256c637426f9d9d554(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61af23fa06bd2a3cc4e81342c57d787ea4851df79d6bbcf1571c437b50f76a43(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    all_projects: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    created_at: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    masters: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    pool_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    serial: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    transferred_at: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
