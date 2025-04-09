r'''
# `openstack_images_image_v2`

Refer to the Terraform Registry for docs: [`openstack_images_image_v2`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2).
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


class ImagesImageV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.imagesImageV2.ImagesImageV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2 openstack_images_image_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        container_format: builtins.str,
        disk_format: builtins.str,
        name: builtins.str,
        decompress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        image_cache_path: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        image_source_password: typing.Optional[builtins.str] = None,
        image_source_url: typing.Optional[builtins.str] = None,
        image_source_username: typing.Optional[builtins.str] = None,
        local_file_path: typing.Optional[builtins.str] = None,
        min_disk_gb: typing.Optional[jsii.Number] = None,
        min_ram_mb: typing.Optional[jsii.Number] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        protected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ImagesImageV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        verify_checksum: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        visibility: typing.Optional[builtins.str] = None,
        web_download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2 openstack_images_image_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param container_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#container_format ImagesImageV2#container_format}.
        :param disk_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#disk_format ImagesImageV2#disk_format}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#name ImagesImageV2#name}.
        :param decompress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#decompress ImagesImageV2#decompress}.
        :param hidden: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#hidden ImagesImageV2#hidden}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#id ImagesImageV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_cache_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_cache_path ImagesImageV2#image_cache_path}.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_id ImagesImageV2#image_id}.
        :param image_source_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_source_password ImagesImageV2#image_source_password}.
        :param image_source_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_source_url ImagesImageV2#image_source_url}.
        :param image_source_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_source_username ImagesImageV2#image_source_username}.
        :param local_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#local_file_path ImagesImageV2#local_file_path}.
        :param min_disk_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#min_disk_gb ImagesImageV2#min_disk_gb}.
        :param min_ram_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#min_ram_mb ImagesImageV2#min_ram_mb}.
        :param properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#properties ImagesImageV2#properties}.
        :param protected: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#protected ImagesImageV2#protected}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#region ImagesImageV2#region}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#tags ImagesImageV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#timeouts ImagesImageV2#timeouts}
        :param verify_checksum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#verify_checksum ImagesImageV2#verify_checksum}.
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#visibility ImagesImageV2#visibility}.
        :param web_download: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#web_download ImagesImageV2#web_download}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43aee1393827bdfe227acda7387e3af2ad999cac4326bfc6f0ee598c51815283)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ImagesImageV2Config(
            container_format=container_format,
            disk_format=disk_format,
            name=name,
            decompress=decompress,
            hidden=hidden,
            id=id,
            image_cache_path=image_cache_path,
            image_id=image_id,
            image_source_password=image_source_password,
            image_source_url=image_source_url,
            image_source_username=image_source_username,
            local_file_path=local_file_path,
            min_disk_gb=min_disk_gb,
            min_ram_mb=min_ram_mb,
            properties=properties,
            protected=protected,
            region=region,
            tags=tags,
            timeouts=timeouts,
            verify_checksum=verify_checksum,
            visibility=visibility,
            web_download=web_download,
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
        '''Generates CDKTF code for importing a ImagesImageV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ImagesImageV2 to import.
        :param import_from_id: The id of the existing ImagesImageV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ImagesImageV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690469b60b4320a033507062193da6a353505fd25cdf43104a7b4b197d2da49c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#create ImagesImageV2#create}.
        '''
        value = ImagesImageV2Timeouts(create=create)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDecompress")
    def reset_decompress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDecompress", []))

    @jsii.member(jsii_name="resetHidden")
    def reset_hidden(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHidden", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageCachePath")
    def reset_image_cache_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageCachePath", []))

    @jsii.member(jsii_name="resetImageId")
    def reset_image_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageId", []))

    @jsii.member(jsii_name="resetImageSourcePassword")
    def reset_image_source_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageSourcePassword", []))

    @jsii.member(jsii_name="resetImageSourceUrl")
    def reset_image_source_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageSourceUrl", []))

    @jsii.member(jsii_name="resetImageSourceUsername")
    def reset_image_source_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageSourceUsername", []))

    @jsii.member(jsii_name="resetLocalFilePath")
    def reset_local_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalFilePath", []))

    @jsii.member(jsii_name="resetMinDiskGb")
    def reset_min_disk_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinDiskGb", []))

    @jsii.member(jsii_name="resetMinRamMb")
    def reset_min_ram_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinRamMb", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetProtected")
    def reset_protected(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtected", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVerifyChecksum")
    def reset_verify_checksum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyChecksum", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

    @jsii.member(jsii_name="resetWebDownload")
    def reset_web_download(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebDownload", []))

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
    @jsii.member(jsii_name="checksum")
    def checksum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checksum"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="sizeBytes")
    def size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeBytes"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ImagesImageV2TimeoutsOutputReference":
        return typing.cast("ImagesImageV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="containerFormatInput")
    def container_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="decompressInput")
    def decompress_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "decompressInput"))

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
    @jsii.member(jsii_name="imageCachePathInput")
    def image_cache_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageCachePathInput"))

    @builtins.property
    @jsii.member(jsii_name="imageIdInput")
    def image_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="imageSourcePasswordInput")
    def image_source_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageSourcePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="imageSourceUrlInput")
    def image_source_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageSourceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="imageSourceUsernameInput")
    def image_source_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageSourceUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="localFilePathInput")
    def local_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="minDiskGbInput")
    def min_disk_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minDiskGbInput"))

    @builtins.property
    @jsii.member(jsii_name="minRamMbInput")
    def min_ram_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minRamMbInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="protectedInput")
    def protected_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "protectedInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ImagesImageV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ImagesImageV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyChecksumInput")
    def verify_checksum_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyChecksumInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="webDownloadInput")
    def web_download_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "webDownloadInput"))

    @builtins.property
    @jsii.member(jsii_name="containerFormat")
    def container_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerFormat"))

    @container_format.setter
    def container_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93caa8dcccc97bf7c33a29f9d7bc511409b518eedf78fba5783ede7348c4bcd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="decompress")
    def decompress(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "decompress"))

    @decompress.setter
    def decompress(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f8ef8e891bd870b575148b28a174fa458e03023bcdd65818af28ed84152cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "decompress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskFormat")
    def disk_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskFormat"))

    @disk_format.setter
    def disk_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf37f67929276a460a8027ceead028b60532aa570dc9f230fa7bbe048a614e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a4c4277069d6e1ae412883da2d7c184b7528fb5499936a518fdecec3346aba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hidden", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2684140ba527958d8f740677155fe34ece236af10aa9d7f235bc9b4d327c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageCachePath")
    def image_cache_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageCachePath"))

    @image_cache_path.setter
    def image_cache_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed5e20f1305839e344a16f18db948d86ac0c358e9be9abc63adab2b5dd25212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageCachePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageId"))

    @image_id.setter
    def image_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270b0ae65febbac689fb6823f5bcc2def13336cd8cde7c3f1b04bb9ee3cf136a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageSourcePassword")
    def image_source_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageSourcePassword"))

    @image_source_password.setter
    def image_source_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eccdcc2b147afeb575886fdbe117ae7de0138d66de8c2afcf64625fc39e2ebb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageSourcePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageSourceUrl")
    def image_source_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageSourceUrl"))

    @image_source_url.setter
    def image_source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e611a49bc35a3db2fa9c053e2602e8218ef20145442b3b10138857c6805092d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageSourceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageSourceUsername")
    def image_source_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageSourceUsername"))

    @image_source_username.setter
    def image_source_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a991b60e18129c32512a50a1552b431ec595e280eb10a41ca1cfd6e2320a0378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageSourceUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localFilePath")
    def local_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localFilePath"))

    @local_file_path.setter
    def local_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda0c66e735967d7a8044b7a02826bd00f5e7276993d70f08bbe64bdafa43f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minDiskGb")
    def min_disk_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minDiskGb"))

    @min_disk_gb.setter
    def min_disk_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28db1d29af0181989402349e069a8ed2778c013aeb93eeb213b068310b0ef3c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minDiskGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minRamMb")
    def min_ram_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minRamMb"))

    @min_ram_mb.setter
    def min_ram_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211e388814df7825fd1211281590176400e37b379af89561abbf0be3667ccfc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minRamMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e0f1f9bb51b7e1651678988ae2bd31651a51512c93cbe99b6fb026eb636332a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709a4052dec973a13b263c947c81dbb4ec986fdb04f28a525407b9eff44e54ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protected")
    def protected(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "protected"))

    @protected.setter
    def protected(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed1dbfa8db43e7734bab2370cafcf6624cd6a81d582b74f754be1a45ae77a620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protected", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9701feaefd17aaa2fdca288e574110740795a8bd6a1b44cd8a02a184740393b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b7e57b1be0aab8d01eb8820b4aebf061c3d552d7c6145cf4a19735bdb6cca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verifyChecksum")
    def verify_checksum(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyChecksum"))

    @verify_checksum.setter
    def verify_checksum(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c06b070af7183247534d210770994ffeac314de77d05b82b9547d095fa7775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyChecksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf29fa4dde4f9bcba16d64787020a25688927aba3c19fb8e412b2e6c58208d7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webDownload")
    def web_download(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "webDownload"))

    @web_download.setter
    def web_download(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b97256140f7ae7d69a2ba73160f392d2f8018f725ca132c48d37634301051e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webDownload", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.imagesImageV2.ImagesImageV2Config",
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
        "name": "name",
        "decompress": "decompress",
        "hidden": "hidden",
        "id": "id",
        "image_cache_path": "imageCachePath",
        "image_id": "imageId",
        "image_source_password": "imageSourcePassword",
        "image_source_url": "imageSourceUrl",
        "image_source_username": "imageSourceUsername",
        "local_file_path": "localFilePath",
        "min_disk_gb": "minDiskGb",
        "min_ram_mb": "minRamMb",
        "properties": "properties",
        "protected": "protected",
        "region": "region",
        "tags": "tags",
        "timeouts": "timeouts",
        "verify_checksum": "verifyChecksum",
        "visibility": "visibility",
        "web_download": "webDownload",
    },
)
class ImagesImageV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        container_format: builtins.str,
        disk_format: builtins.str,
        name: builtins.str,
        decompress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        image_cache_path: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        image_source_password: typing.Optional[builtins.str] = None,
        image_source_url: typing.Optional[builtins.str] = None,
        image_source_username: typing.Optional[builtins.str] = None,
        local_file_path: typing.Optional[builtins.str] = None,
        min_disk_gb: typing.Optional[jsii.Number] = None,
        min_ram_mb: typing.Optional[jsii.Number] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        protected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ImagesImageV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        verify_checksum: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        visibility: typing.Optional[builtins.str] = None,
        web_download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param container_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#container_format ImagesImageV2#container_format}.
        :param disk_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#disk_format ImagesImageV2#disk_format}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#name ImagesImageV2#name}.
        :param decompress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#decompress ImagesImageV2#decompress}.
        :param hidden: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#hidden ImagesImageV2#hidden}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#id ImagesImageV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_cache_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_cache_path ImagesImageV2#image_cache_path}.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_id ImagesImageV2#image_id}.
        :param image_source_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_source_password ImagesImageV2#image_source_password}.
        :param image_source_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_source_url ImagesImageV2#image_source_url}.
        :param image_source_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_source_username ImagesImageV2#image_source_username}.
        :param local_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#local_file_path ImagesImageV2#local_file_path}.
        :param min_disk_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#min_disk_gb ImagesImageV2#min_disk_gb}.
        :param min_ram_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#min_ram_mb ImagesImageV2#min_ram_mb}.
        :param properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#properties ImagesImageV2#properties}.
        :param protected: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#protected ImagesImageV2#protected}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#region ImagesImageV2#region}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#tags ImagesImageV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#timeouts ImagesImageV2#timeouts}
        :param verify_checksum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#verify_checksum ImagesImageV2#verify_checksum}.
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#visibility ImagesImageV2#visibility}.
        :param web_download: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#web_download ImagesImageV2#web_download}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ImagesImageV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3cb10a1f62720dd2fecd1f062f0c3d038499964734b5e6945940db4eb07218e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument container_format", value=container_format, expected_type=type_hints["container_format"])
            check_type(argname="argument disk_format", value=disk_format, expected_type=type_hints["disk_format"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument decompress", value=decompress, expected_type=type_hints["decompress"])
            check_type(argname="argument hidden", value=hidden, expected_type=type_hints["hidden"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_cache_path", value=image_cache_path, expected_type=type_hints["image_cache_path"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument image_source_password", value=image_source_password, expected_type=type_hints["image_source_password"])
            check_type(argname="argument image_source_url", value=image_source_url, expected_type=type_hints["image_source_url"])
            check_type(argname="argument image_source_username", value=image_source_username, expected_type=type_hints["image_source_username"])
            check_type(argname="argument local_file_path", value=local_file_path, expected_type=type_hints["local_file_path"])
            check_type(argname="argument min_disk_gb", value=min_disk_gb, expected_type=type_hints["min_disk_gb"])
            check_type(argname="argument min_ram_mb", value=min_ram_mb, expected_type=type_hints["min_ram_mb"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument protected", value=protected, expected_type=type_hints["protected"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument verify_checksum", value=verify_checksum, expected_type=type_hints["verify_checksum"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
            check_type(argname="argument web_download", value=web_download, expected_type=type_hints["web_download"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_format": container_format,
            "disk_format": disk_format,
            "name": name,
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
        if decompress is not None:
            self._values["decompress"] = decompress
        if hidden is not None:
            self._values["hidden"] = hidden
        if id is not None:
            self._values["id"] = id
        if image_cache_path is not None:
            self._values["image_cache_path"] = image_cache_path
        if image_id is not None:
            self._values["image_id"] = image_id
        if image_source_password is not None:
            self._values["image_source_password"] = image_source_password
        if image_source_url is not None:
            self._values["image_source_url"] = image_source_url
        if image_source_username is not None:
            self._values["image_source_username"] = image_source_username
        if local_file_path is not None:
            self._values["local_file_path"] = local_file_path
        if min_disk_gb is not None:
            self._values["min_disk_gb"] = min_disk_gb
        if min_ram_mb is not None:
            self._values["min_ram_mb"] = min_ram_mb
        if properties is not None:
            self._values["properties"] = properties
        if protected is not None:
            self._values["protected"] = protected
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if verify_checksum is not None:
            self._values["verify_checksum"] = verify_checksum
        if visibility is not None:
            self._values["visibility"] = visibility
        if web_download is not None:
            self._values["web_download"] = web_download

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
    def container_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#container_format ImagesImageV2#container_format}.'''
        result = self._values.get("container_format")
        assert result is not None, "Required property 'container_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#disk_format ImagesImageV2#disk_format}.'''
        result = self._values.get("disk_format")
        assert result is not None, "Required property 'disk_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#name ImagesImageV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def decompress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#decompress ImagesImageV2#decompress}.'''
        result = self._values.get("decompress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hidden(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#hidden ImagesImageV2#hidden}.'''
        result = self._values.get("hidden")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#id ImagesImageV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_cache_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_cache_path ImagesImageV2#image_cache_path}.'''
        result = self._values.get("image_cache_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_id ImagesImageV2#image_id}.'''
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_source_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_source_password ImagesImageV2#image_source_password}.'''
        result = self._values.get("image_source_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_source_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_source_url ImagesImageV2#image_source_url}.'''
        result = self._values.get("image_source_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_source_username(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#image_source_username ImagesImageV2#image_source_username}.'''
        result = self._values.get("image_source_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_file_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#local_file_path ImagesImageV2#local_file_path}.'''
        result = self._values.get("local_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_disk_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#min_disk_gb ImagesImageV2#min_disk_gb}.'''
        result = self._values.get("min_disk_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_ram_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#min_ram_mb ImagesImageV2#min_ram_mb}.'''
        result = self._values.get("min_ram_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#properties ImagesImageV2#properties}.'''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def protected(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#protected ImagesImageV2#protected}.'''
        result = self._values.get("protected")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#region ImagesImageV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#tags ImagesImageV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ImagesImageV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#timeouts ImagesImageV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ImagesImageV2Timeouts"], result)

    @builtins.property
    def verify_checksum(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#verify_checksum ImagesImageV2#verify_checksum}.'''
        result = self._values.get("verify_checksum")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#visibility ImagesImageV2#visibility}.'''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_download(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#web_download ImagesImageV2#web_download}.'''
        result = self._values.get("web_download")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagesImageV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.imagesImageV2.ImagesImageV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create"},
)
class ImagesImageV2Timeouts:
    def __init__(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#create ImagesImageV2#create}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d6ee65d95fea30cc8faf83e455c56c023a52020fec338491cc8dedc8227b8bd)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/images_image_v2#create ImagesImageV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagesImageV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagesImageV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.imagesImageV2.ImagesImageV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__938f7d4afc1b217a18da834a241563dc22754bc211e11b8fe1b60fd20e2aa581)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad6bfad9753d5d6a75b15309ede4a4258978fd6bd1c8a8574d6b2d1040321fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagesImageV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagesImageV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagesImageV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8984a2d2463dd5c07cfe54ed853070eb1efb22fc9288f7ff09792f567beacc3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ImagesImageV2",
    "ImagesImageV2Config",
    "ImagesImageV2Timeouts",
    "ImagesImageV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__43aee1393827bdfe227acda7387e3af2ad999cac4326bfc6f0ee598c51815283(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    container_format: builtins.str,
    disk_format: builtins.str,
    name: builtins.str,
    decompress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    image_cache_path: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    image_source_password: typing.Optional[builtins.str] = None,
    image_source_url: typing.Optional[builtins.str] = None,
    image_source_username: typing.Optional[builtins.str] = None,
    local_file_path: typing.Optional[builtins.str] = None,
    min_disk_gb: typing.Optional[jsii.Number] = None,
    min_ram_mb: typing.Optional[jsii.Number] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    protected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ImagesImageV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    verify_checksum: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    visibility: typing.Optional[builtins.str] = None,
    web_download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__690469b60b4320a033507062193da6a353505fd25cdf43104a7b4b197d2da49c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93caa8dcccc97bf7c33a29f9d7bc511409b518eedf78fba5783ede7348c4bcd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f8ef8e891bd870b575148b28a174fa458e03023bcdd65818af28ed84152cd8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf37f67929276a460a8027ceead028b60532aa570dc9f230fa7bbe048a614e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4c4277069d6e1ae412883da2d7c184b7528fb5499936a518fdecec3346aba8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2684140ba527958d8f740677155fe34ece236af10aa9d7f235bc9b4d327c1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed5e20f1305839e344a16f18db948d86ac0c358e9be9abc63adab2b5dd25212(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270b0ae65febbac689fb6823f5bcc2def13336cd8cde7c3f1b04bb9ee3cf136a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccdcc2b147afeb575886fdbe117ae7de0138d66de8c2afcf64625fc39e2ebb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e611a49bc35a3db2fa9c053e2602e8218ef20145442b3b10138857c6805092d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a991b60e18129c32512a50a1552b431ec595e280eb10a41ca1cfd6e2320a0378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda0c66e735967d7a8044b7a02826bd00f5e7276993d70f08bbe64bdafa43f9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28db1d29af0181989402349e069a8ed2778c013aeb93eeb213b068310b0ef3c9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211e388814df7825fd1211281590176400e37b379af89561abbf0be3667ccfc1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0f1f9bb51b7e1651678988ae2bd31651a51512c93cbe99b6fb026eb636332a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709a4052dec973a13b263c947c81dbb4ec986fdb04f28a525407b9eff44e54ba(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1dbfa8db43e7734bab2370cafcf6624cd6a81d582b74f754be1a45ae77a620(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9701feaefd17aaa2fdca288e574110740795a8bd6a1b44cd8a02a184740393b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b7e57b1be0aab8d01eb8820b4aebf061c3d552d7c6145cf4a19735bdb6cca4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c06b070af7183247534d210770994ffeac314de77d05b82b9547d095fa7775(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf29fa4dde4f9bcba16d64787020a25688927aba3c19fb8e412b2e6c58208d7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b97256140f7ae7d69a2ba73160f392d2f8018f725ca132c48d37634301051e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3cb10a1f62720dd2fecd1f062f0c3d038499964734b5e6945940db4eb07218e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    container_format: builtins.str,
    disk_format: builtins.str,
    name: builtins.str,
    decompress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    image_cache_path: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    image_source_password: typing.Optional[builtins.str] = None,
    image_source_url: typing.Optional[builtins.str] = None,
    image_source_username: typing.Optional[builtins.str] = None,
    local_file_path: typing.Optional[builtins.str] = None,
    min_disk_gb: typing.Optional[jsii.Number] = None,
    min_ram_mb: typing.Optional[jsii.Number] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    protected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ImagesImageV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    verify_checksum: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    visibility: typing.Optional[builtins.str] = None,
    web_download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6ee65d95fea30cc8faf83e455c56c023a52020fec338491cc8dedc8227b8bd(
    *,
    create: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938f7d4afc1b217a18da834a241563dc22754bc211e11b8fe1b60fd20e2aa581(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad6bfad9753d5d6a75b15309ede4a4258978fd6bd1c8a8574d6b2d1040321fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8984a2d2463dd5c07cfe54ed853070eb1efb22fc9288f7ff09792f567beacc3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagesImageV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
