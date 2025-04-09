r'''
# `data_openstack_images_image_ids_v2`

Refer to the Terraform Registry for docs: [`data_openstack_images_image_ids_v2`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2).
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


class DataOpenstackImagesImageIdsV2(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.dataOpenstackImagesImageIdsV2.DataOpenstackImagesImageIdsV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2 openstack_images_image_ids_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        container_format: typing.Optional[builtins.str] = None,
        disk_format: typing.Optional[builtins.str] = None,
        hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        member_status: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_regex: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        size_max: typing.Optional[jsii.Number] = None,
        size_min: typing.Optional[jsii.Number] = None,
        sort: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        visibility: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2 openstack_images_image_ids_v2} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param container_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#container_format DataOpenstackImagesImageIdsV2#container_format}.
        :param disk_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#disk_format DataOpenstackImagesImageIdsV2#disk_format}.
        :param hidden: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#hidden DataOpenstackImagesImageIdsV2#hidden}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#id DataOpenstackImagesImageIdsV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param member_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#member_status DataOpenstackImagesImageIdsV2#member_status}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#name DataOpenstackImagesImageIdsV2#name}.
        :param name_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#name_regex DataOpenstackImagesImageIdsV2#name_regex}.
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#owner DataOpenstackImagesImageIdsV2#owner}.
        :param properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#properties DataOpenstackImagesImageIdsV2#properties}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#region DataOpenstackImagesImageIdsV2#region}.
        :param size_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#size_max DataOpenstackImagesImageIdsV2#size_max}.
        :param size_min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#size_min DataOpenstackImagesImageIdsV2#size_min}.
        :param sort: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#sort DataOpenstackImagesImageIdsV2#sort}.
        :param tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#tag DataOpenstackImagesImageIdsV2#tag}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#tags DataOpenstackImagesImageIdsV2#tags}.
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#visibility DataOpenstackImagesImageIdsV2#visibility}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac4f9e1911a7b98947f2dadbecf15ee2bad62a3119baf1b9462b87b40087afe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpenstackImagesImageIdsV2Config(
            container_format=container_format,
            disk_format=disk_format,
            hidden=hidden,
            id=id,
            member_status=member_status,
            name=name,
            name_regex=name_regex,
            owner=owner,
            properties=properties,
            region=region,
            size_max=size_max,
            size_min=size_min,
            sort=sort,
            tag=tag,
            tags=tags,
            visibility=visibility,
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
        '''Generates CDKTF code for importing a DataOpenstackImagesImageIdsV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpenstackImagesImageIdsV2 to import.
        :param import_from_id: The id of the existing DataOpenstackImagesImageIdsV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpenstackImagesImageIdsV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__764c76f1424f948c88ea3650c0ae7c24776345d2f0fa0d6beaf9bfba95e01957)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetContainerFormat")
    def reset_container_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerFormat", []))

    @jsii.member(jsii_name="resetDiskFormat")
    def reset_disk_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskFormat", []))

    @jsii.member(jsii_name="resetHidden")
    def reset_hidden(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHidden", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMemberStatus")
    def reset_member_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberStatus", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNameRegex")
    def reset_name_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameRegex", []))

    @jsii.member(jsii_name="resetOwner")
    def reset_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwner", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSizeMax")
    def reset_size_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeMax", []))

    @jsii.member(jsii_name="resetSizeMin")
    def reset_size_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeMin", []))

    @jsii.member(jsii_name="resetSort")
    def reset_sort(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSort", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

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
    @jsii.member(jsii_name="ids")
    def ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ids"))

    @builtins.property
    @jsii.member(jsii_name="containerFormatInput")
    def container_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="diskFormatInput")
    def disk_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="hiddenInput")
    def hidden_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hiddenInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="memberStatusInput")
    def member_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memberStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameRegexInput")
    def name_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeMaxInput")
    def size_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeMinInput")
    def size_min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeMinInput"))

    @builtins.property
    @jsii.member(jsii_name="sortInput")
    def sort_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="containerFormat")
    def container_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerFormat"))

    @container_format.setter
    def container_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96b81c9e574ada1a895eb2a2bc0d7aecadccb217d5464c7be264cba025816a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskFormat")
    def disk_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskFormat"))

    @disk_format.setter
    def disk_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7365307fa58e8efb423ae82a31a92e583f5ff2e6135dcb018014638e8d048ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hidden")
    def hidden(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hidden"))

    @hidden.setter
    def hidden(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67fb578f98fc8d69117300cc73be32249511c8bee10f4bc11930cb0ecad5cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hidden", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238442c7ded31d518b008ff88c49a940b546682bb6154e1b33f1e282afc9085e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memberStatus")
    def member_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memberStatus"))

    @member_status.setter
    def member_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b441b6a973537784dc012fb717d1637d9e4cd52a864404caecdc1714a0aa39be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd30a84bdd2af606906b7e7b2166f83f8b4695f0f6391b19a09f6bffd26c341e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameRegex")
    def name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameRegex"))

    @name_regex.setter
    def name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf216b672d395f52efe0cc697877133f97acfbc0793bdb3b2fbf5f9c8ef64a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc364201bbf89a405771cbffb33f46074be620e68ef886318e2a63c2c5a1a15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965b014cb9015c29d7655610bb7a663916954730bd5cfad02bd37bd4f0ead064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1cff6992b16ad3dfb99df9c7c305b0e4a12398051617775d2690606e62b411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeMax")
    def size_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeMax"))

    @size_max.setter
    def size_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb563beebfc9d1e75f9a4b9e7741aa0e8ca2e6e021bed2172c20e22bc08967a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeMax", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeMin")
    def size_min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeMin"))

    @size_min.setter
    def size_min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ce708919826050b5a7407af01d0bb7b00a12d2685a2a4a5f71d9a1c9258024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeMin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sort")
    def sort(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sort"))

    @sort.setter
    def sort(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23a043035a387dde163e2bc29568ba41061dd889d3fe622534b79f3cff139c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae72ec4d3772f319939f6291ac30e09aeff6555f938e64039c8bccd38b9015ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5f317f064eebbfaf01f86be1108662753506f22e9cf34214752bda15e6d90a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5968cc3e589bce6b3067769a2f93ee8cdffe7b33eb3d042cb552150788cf2213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.dataOpenstackImagesImageIdsV2.DataOpenstackImagesImageIdsV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "container_format": "containerFormat",
        "disk_format": "diskFormat",
        "hidden": "hidden",
        "id": "id",
        "member_status": "memberStatus",
        "name": "name",
        "name_regex": "nameRegex",
        "owner": "owner",
        "properties": "properties",
        "region": "region",
        "size_max": "sizeMax",
        "size_min": "sizeMin",
        "sort": "sort",
        "tag": "tag",
        "tags": "tags",
        "visibility": "visibility",
    },
)
class DataOpenstackImagesImageIdsV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        container_format: typing.Optional[builtins.str] = None,
        disk_format: typing.Optional[builtins.str] = None,
        hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        member_status: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_regex: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        size_max: typing.Optional[jsii.Number] = None,
        size_min: typing.Optional[jsii.Number] = None,
        sort: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        visibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param container_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#container_format DataOpenstackImagesImageIdsV2#container_format}.
        :param disk_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#disk_format DataOpenstackImagesImageIdsV2#disk_format}.
        :param hidden: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#hidden DataOpenstackImagesImageIdsV2#hidden}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#id DataOpenstackImagesImageIdsV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param member_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#member_status DataOpenstackImagesImageIdsV2#member_status}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#name DataOpenstackImagesImageIdsV2#name}.
        :param name_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#name_regex DataOpenstackImagesImageIdsV2#name_regex}.
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#owner DataOpenstackImagesImageIdsV2#owner}.
        :param properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#properties DataOpenstackImagesImageIdsV2#properties}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#region DataOpenstackImagesImageIdsV2#region}.
        :param size_max: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#size_max DataOpenstackImagesImageIdsV2#size_max}.
        :param size_min: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#size_min DataOpenstackImagesImageIdsV2#size_min}.
        :param sort: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#sort DataOpenstackImagesImageIdsV2#sort}.
        :param tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#tag DataOpenstackImagesImageIdsV2#tag}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#tags DataOpenstackImagesImageIdsV2#tags}.
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#visibility DataOpenstackImagesImageIdsV2#visibility}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8499d8d9a19701df858828bd39d1298a1d6cf3afcb8a7b392e6efa8fe85c1221)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument container_format", value=container_format, expected_type=type_hints["container_format"])
            check_type(argname="argument disk_format", value=disk_format, expected_type=type_hints["disk_format"])
            check_type(argname="argument hidden", value=hidden, expected_type=type_hints["hidden"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument member_status", value=member_status, expected_type=type_hints["member_status"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_regex", value=name_regex, expected_type=type_hints["name_regex"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument size_max", value=size_max, expected_type=type_hints["size_max"])
            check_type(argname="argument size_min", value=size_min, expected_type=type_hints["size_min"])
            check_type(argname="argument sort", value=sort, expected_type=type_hints["sort"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
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
        if container_format is not None:
            self._values["container_format"] = container_format
        if disk_format is not None:
            self._values["disk_format"] = disk_format
        if hidden is not None:
            self._values["hidden"] = hidden
        if id is not None:
            self._values["id"] = id
        if member_status is not None:
            self._values["member_status"] = member_status
        if name is not None:
            self._values["name"] = name
        if name_regex is not None:
            self._values["name_regex"] = name_regex
        if owner is not None:
            self._values["owner"] = owner
        if properties is not None:
            self._values["properties"] = properties
        if region is not None:
            self._values["region"] = region
        if size_max is not None:
            self._values["size_max"] = size_max
        if size_min is not None:
            self._values["size_min"] = size_min
        if sort is not None:
            self._values["sort"] = sort
        if tag is not None:
            self._values["tag"] = tag
        if tags is not None:
            self._values["tags"] = tags
        if visibility is not None:
            self._values["visibility"] = visibility

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
    def container_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#container_format DataOpenstackImagesImageIdsV2#container_format}.'''
        result = self._values.get("container_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#disk_format DataOpenstackImagesImageIdsV2#disk_format}.'''
        result = self._values.get("disk_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hidden(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#hidden DataOpenstackImagesImageIdsV2#hidden}.'''
        result = self._values.get("hidden")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#id DataOpenstackImagesImageIdsV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#member_status DataOpenstackImagesImageIdsV2#member_status}.'''
        result = self._values.get("member_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#name DataOpenstackImagesImageIdsV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#name_regex DataOpenstackImagesImageIdsV2#name_regex}.'''
        result = self._values.get("name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#owner DataOpenstackImagesImageIdsV2#owner}.'''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#properties DataOpenstackImagesImageIdsV2#properties}.'''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#region DataOpenstackImagesImageIdsV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#size_max DataOpenstackImagesImageIdsV2#size_max}.'''
        result = self._values.get("size_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def size_min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#size_min DataOpenstackImagesImageIdsV2#size_min}.'''
        result = self._values.get("size_min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sort(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#sort DataOpenstackImagesImageIdsV2#sort}.'''
        result = self._values.get("sort")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#tag DataOpenstackImagesImageIdsV2#tag}.'''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#tags DataOpenstackImagesImageIdsV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/images_image_ids_v2#visibility DataOpenstackImagesImageIdsV2#visibility}.'''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpenstackImagesImageIdsV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpenstackImagesImageIdsV2",
    "DataOpenstackImagesImageIdsV2Config",
]

publication.publish()

def _typecheckingstub__6ac4f9e1911a7b98947f2dadbecf15ee2bad62a3119baf1b9462b87b40087afe(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    container_format: typing.Optional[builtins.str] = None,
    disk_format: typing.Optional[builtins.str] = None,
    hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    member_status: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_regex: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    size_max: typing.Optional[jsii.Number] = None,
    size_min: typing.Optional[jsii.Number] = None,
    sort: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    visibility: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__764c76f1424f948c88ea3650c0ae7c24776345d2f0fa0d6beaf9bfba95e01957(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b81c9e574ada1a895eb2a2bc0d7aecadccb217d5464c7be264cba025816a42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7365307fa58e8efb423ae82a31a92e583f5ff2e6135dcb018014638e8d048ca9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67fb578f98fc8d69117300cc73be32249511c8bee10f4bc11930cb0ecad5cb6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238442c7ded31d518b008ff88c49a940b546682bb6154e1b33f1e282afc9085e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b441b6a973537784dc012fb717d1637d9e4cd52a864404caecdc1714a0aa39be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd30a84bdd2af606906b7e7b2166f83f8b4695f0f6391b19a09f6bffd26c341e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf216b672d395f52efe0cc697877133f97acfbc0793bdb3b2fbf5f9c8ef64a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc364201bbf89a405771cbffb33f46074be620e68ef886318e2a63c2c5a1a15a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965b014cb9015c29d7655610bb7a663916954730bd5cfad02bd37bd4f0ead064(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1cff6992b16ad3dfb99df9c7c305b0e4a12398051617775d2690606e62b411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb563beebfc9d1e75f9a4b9e7741aa0e8ca2e6e021bed2172c20e22bc08967a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ce708919826050b5a7407af01d0bb7b00a12d2685a2a4a5f71d9a1c9258024(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23a043035a387dde163e2bc29568ba41061dd889d3fe622534b79f3cff139c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae72ec4d3772f319939f6291ac30e09aeff6555f938e64039c8bccd38b9015ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5f317f064eebbfaf01f86be1108662753506f22e9cf34214752bda15e6d90a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5968cc3e589bce6b3067769a2f93ee8cdffe7b33eb3d042cb552150788cf2213(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8499d8d9a19701df858828bd39d1298a1d6cf3afcb8a7b392e6efa8fe85c1221(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container_format: typing.Optional[builtins.str] = None,
    disk_format: typing.Optional[builtins.str] = None,
    hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    member_status: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_regex: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    size_max: typing.Optional[jsii.Number] = None,
    size_min: typing.Optional[jsii.Number] = None,
    sort: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    visibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
