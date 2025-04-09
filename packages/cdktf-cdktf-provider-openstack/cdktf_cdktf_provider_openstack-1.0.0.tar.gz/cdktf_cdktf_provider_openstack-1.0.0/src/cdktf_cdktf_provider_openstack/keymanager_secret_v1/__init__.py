r'''
# `openstack_keymanager_secret_v1`

Refer to the Terraform Registry for docs: [`openstack_keymanager_secret_v1`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1).
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


class KeymanagerSecretV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.keymanagerSecretV1.KeymanagerSecretV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1 openstack_keymanager_secret_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        acl: typing.Optional[typing.Union["KeymanagerSecretV1Acl", typing.Dict[builtins.str, typing.Any]]] = None,
        algorithm: typing.Optional[builtins.str] = None,
        bit_length: typing.Optional[jsii.Number] = None,
        expiration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        payload: typing.Optional[builtins.str] = None,
        payload_content_encoding: typing.Optional[builtins.str] = None,
        payload_content_type: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KeymanagerSecretV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1 openstack_keymanager_secret_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param acl: acl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#acl KeymanagerSecretV1#acl}
        :param algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#algorithm KeymanagerSecretV1#algorithm}.
        :param bit_length: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#bit_length KeymanagerSecretV1#bit_length}.
        :param expiration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#expiration KeymanagerSecretV1#expiration}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#id KeymanagerSecretV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#metadata KeymanagerSecretV1#metadata}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#mode KeymanagerSecretV1#mode}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#name KeymanagerSecretV1#name}.
        :param payload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#payload KeymanagerSecretV1#payload}.
        :param payload_content_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#payload_content_encoding KeymanagerSecretV1#payload_content_encoding}.
        :param payload_content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#payload_content_type KeymanagerSecretV1#payload_content_type}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#region KeymanagerSecretV1#region}.
        :param secret_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#secret_type KeymanagerSecretV1#secret_type}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#timeouts KeymanagerSecretV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2239baf16431f9c18f180f25edad6e03c4b8dd449e9e36298ee9e59976649055)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KeymanagerSecretV1Config(
            acl=acl,
            algorithm=algorithm,
            bit_length=bit_length,
            expiration=expiration,
            id=id,
            metadata=metadata,
            mode=mode,
            name=name,
            payload=payload,
            payload_content_encoding=payload_content_encoding,
            payload_content_type=payload_content_type,
            region=region,
            secret_type=secret_type,
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
        '''Generates CDKTF code for importing a KeymanagerSecretV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KeymanagerSecretV1 to import.
        :param import_from_id: The id of the existing KeymanagerSecretV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KeymanagerSecretV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c91f88be4e9b0c13b17f4b5b125a5643d355f0e69d116ad86ede31adebd1e1d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAcl")
    def put_acl(
        self,
        *,
        read: typing.Optional[typing.Union["KeymanagerSecretV1AclRead", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param read: read block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#read KeymanagerSecretV1#read}
        '''
        value = KeymanagerSecretV1Acl(read=read)

        return typing.cast(None, jsii.invoke(self, "putAcl", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#create KeymanagerSecretV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#delete KeymanagerSecretV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#update KeymanagerSecretV1#update}.
        '''
        value = KeymanagerSecretV1Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAcl")
    def reset_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcl", []))

    @jsii.member(jsii_name="resetAlgorithm")
    def reset_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlgorithm", []))

    @jsii.member(jsii_name="resetBitLength")
    def reset_bit_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBitLength", []))

    @jsii.member(jsii_name="resetExpiration")
    def reset_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPayload")
    def reset_payload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayload", []))

    @jsii.member(jsii_name="resetPayloadContentEncoding")
    def reset_payload_content_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayloadContentEncoding", []))

    @jsii.member(jsii_name="resetPayloadContentType")
    def reset_payload_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayloadContentType", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecretType")
    def reset_secret_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretType", []))

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
    @jsii.member(jsii_name="acl")
    def acl(self) -> "KeymanagerSecretV1AclOutputReference":
        return typing.cast("KeymanagerSecretV1AclOutputReference", jsii.get(self, "acl"))

    @builtins.property
    @jsii.member(jsii_name="allMetadata")
    def all_metadata(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "allMetadata"))

    @builtins.property
    @jsii.member(jsii_name="contentTypes")
    def content_types(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "contentTypes"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="creatorId")
    def creator_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creatorId"))

    @builtins.property
    @jsii.member(jsii_name="secretRef")
    def secret_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretRef"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KeymanagerSecretV1TimeoutsOutputReference":
        return typing.cast("KeymanagerSecretV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="aclInput")
    def acl_input(self) -> typing.Optional["KeymanagerSecretV1Acl"]:
        return typing.cast(typing.Optional["KeymanagerSecretV1Acl"], jsii.get(self, "aclInput"))

    @builtins.property
    @jsii.member(jsii_name="algorithmInput")
    def algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "algorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="bitLengthInput")
    def bit_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bitLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationInput")
    def expiration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadContentEncodingInput")
    def payload_content_encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadContentEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadContentTypeInput")
    def payload_content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadContentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadInput")
    def payload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretTypeInput")
    def secret_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KeymanagerSecretV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KeymanagerSecretV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @algorithm.setter
    def algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d732afe0f07b30a84c82aac97b73e318429b36ba5dee85e9cfcc2cf75240c0cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bitLength")
    def bit_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bitLength"))

    @bit_length.setter
    def bit_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560288e5f7c2ac4e849cb7282a64bc3d09101fca9784d303a7a147eecbba1369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bitLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiration"))

    @expiration.setter
    def expiration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4f9a77ecfc38d3798c4e65b45de62bb9d3cea1c9d52156b2a4f77586c3831d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e646e11f398291af7ead265dd41e1f9c152787161f58b805860280eac7f8eadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975f7c6aa5f0759fb0d2e388a8682d2449ba993ffed307944a2720271216d8f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae9f7401dcf79cbcc796269a4a0c755936098ef017f8950b1147536d009091a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5291d0ff65776186b751fd5bc780e0351721bd2a9da6db147579a07cd9e9ef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payload")
    def payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payload"))

    @payload.setter
    def payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf50b5debab9fe074fe0de16e068ab124f6118e56665cb9f23052e925bac85f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payloadContentEncoding")
    def payload_content_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payloadContentEncoding"))

    @payload_content_encoding.setter
    def payload_content_encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb8ee889d745632cbeb298049ff55aacf96cb7aa1771716cc87d866af009f901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadContentEncoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payloadContentType")
    def payload_content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payloadContentType"))

    @payload_content_type.setter
    def payload_content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ed014d75f3544bf779010b12a8c8e11b2f8e063dcb4a83bca17e625389f372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadContentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccbe04f024f8c67c8e70de7774f3cb089dc12e1a13b552a67001b55c9e3dcc49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02950621155535edbaba4e9de95770dc3d71634825605c8710ff9970bdca838c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.keymanagerSecretV1.KeymanagerSecretV1Acl",
    jsii_struct_bases=[],
    name_mapping={"read": "read"},
)
class KeymanagerSecretV1Acl:
    def __init__(
        self,
        *,
        read: typing.Optional[typing.Union["KeymanagerSecretV1AclRead", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param read: read block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#read KeymanagerSecretV1#read}
        '''
        if isinstance(read, dict):
            read = KeymanagerSecretV1AclRead(**read)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d4b90a6cf696e5c4b7b8e5a2d7fcd3dc2d97388eed720d7220b3da8a280484)
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def read(self) -> typing.Optional["KeymanagerSecretV1AclRead"]:
        '''read block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#read KeymanagerSecretV1#read}
        '''
        result = self._values.get("read")
        return typing.cast(typing.Optional["KeymanagerSecretV1AclRead"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeymanagerSecretV1Acl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeymanagerSecretV1AclOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.keymanagerSecretV1.KeymanagerSecretV1AclOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36a3618ad755893fc2658c3191836aa7fc9bf894f250de79a32e9730fb1d6efb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRead")
    def put_read(
        self,
        *,
        project_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param project_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#project_access KeymanagerSecretV1#project_access}.
        :param users: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#users KeymanagerSecretV1#users}.
        '''
        value = KeymanagerSecretV1AclRead(project_access=project_access, users=users)

        return typing.cast(None, jsii.invoke(self, "putRead", [value]))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> "KeymanagerSecretV1AclReadOutputReference":
        return typing.cast("KeymanagerSecretV1AclReadOutputReference", jsii.get(self, "read"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional["KeymanagerSecretV1AclRead"]:
        return typing.cast(typing.Optional["KeymanagerSecretV1AclRead"], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KeymanagerSecretV1Acl]:
        return typing.cast(typing.Optional[KeymanagerSecretV1Acl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[KeymanagerSecretV1Acl]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6eaa7727365f5723b71e99a034e9d052a8cf37ed52b43ffd144d4021071fc39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.keymanagerSecretV1.KeymanagerSecretV1AclRead",
    jsii_struct_bases=[],
    name_mapping={"project_access": "projectAccess", "users": "users"},
)
class KeymanagerSecretV1AclRead:
    def __init__(
        self,
        *,
        project_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param project_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#project_access KeymanagerSecretV1#project_access}.
        :param users: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#users KeymanagerSecretV1#users}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f207fcd5f24a11c917d3cc3f3b039e19440ac13d2bae2621b5b3d7544b2ee199)
            check_type(argname="argument project_access", value=project_access, expected_type=type_hints["project_access"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if project_access is not None:
            self._values["project_access"] = project_access
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def project_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#project_access KeymanagerSecretV1#project_access}.'''
        result = self._values.get("project_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#users KeymanagerSecretV1#users}.'''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeymanagerSecretV1AclRead(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeymanagerSecretV1AclReadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.keymanagerSecretV1.KeymanagerSecretV1AclReadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4925d0a6473c3635cd1e837148d3279ec5bbbaf7f7904fb9db7c49aee4bdf8bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProjectAccess")
    def reset_project_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectAccess", []))

    @jsii.member(jsii_name="resetUsers")
    def reset_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsers", []))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="projectAccessInput")
    def project_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "projectAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="usersInput")
    def users_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="projectAccess")
    def project_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "projectAccess"))

    @project_access.setter
    def project_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d37d2009708dc4c3791c0ab861acf65f5fb383689cd7803aabb49dced5d57f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6de7834b98535d8646f7ffcbd7c2d3be19ecc254655e9fc556e7da199bc1f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KeymanagerSecretV1AclRead]:
        return typing.cast(typing.Optional[KeymanagerSecretV1AclRead], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[KeymanagerSecretV1AclRead]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21553ac7cd7128a6040e6448b714cec35768d944b53ef0ad547363f234d206a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.keymanagerSecretV1.KeymanagerSecretV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "acl": "acl",
        "algorithm": "algorithm",
        "bit_length": "bitLength",
        "expiration": "expiration",
        "id": "id",
        "metadata": "metadata",
        "mode": "mode",
        "name": "name",
        "payload": "payload",
        "payload_content_encoding": "payloadContentEncoding",
        "payload_content_type": "payloadContentType",
        "region": "region",
        "secret_type": "secretType",
        "timeouts": "timeouts",
    },
)
class KeymanagerSecretV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        acl: typing.Optional[typing.Union[KeymanagerSecretV1Acl, typing.Dict[builtins.str, typing.Any]]] = None,
        algorithm: typing.Optional[builtins.str] = None,
        bit_length: typing.Optional[jsii.Number] = None,
        expiration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        payload: typing.Optional[builtins.str] = None,
        payload_content_encoding: typing.Optional[builtins.str] = None,
        payload_content_type: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        secret_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KeymanagerSecretV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param acl: acl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#acl KeymanagerSecretV1#acl}
        :param algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#algorithm KeymanagerSecretV1#algorithm}.
        :param bit_length: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#bit_length KeymanagerSecretV1#bit_length}.
        :param expiration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#expiration KeymanagerSecretV1#expiration}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#id KeymanagerSecretV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#metadata KeymanagerSecretV1#metadata}.
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#mode KeymanagerSecretV1#mode}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#name KeymanagerSecretV1#name}.
        :param payload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#payload KeymanagerSecretV1#payload}.
        :param payload_content_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#payload_content_encoding KeymanagerSecretV1#payload_content_encoding}.
        :param payload_content_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#payload_content_type KeymanagerSecretV1#payload_content_type}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#region KeymanagerSecretV1#region}.
        :param secret_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#secret_type KeymanagerSecretV1#secret_type}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#timeouts KeymanagerSecretV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(acl, dict):
            acl = KeymanagerSecretV1Acl(**acl)
        if isinstance(timeouts, dict):
            timeouts = KeymanagerSecretV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5fa3c2f1773fbc8e8d0e36181d0dea87908732a68a0353668ca77ff4e112f73)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument acl", value=acl, expected_type=type_hints["acl"])
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
            check_type(argname="argument bit_length", value=bit_length, expected_type=type_hints["bit_length"])
            check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument payload_content_encoding", value=payload_content_encoding, expected_type=type_hints["payload_content_encoding"])
            check_type(argname="argument payload_content_type", value=payload_content_type, expected_type=type_hints["payload_content_type"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument secret_type", value=secret_type, expected_type=type_hints["secret_type"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
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
        if acl is not None:
            self._values["acl"] = acl
        if algorithm is not None:
            self._values["algorithm"] = algorithm
        if bit_length is not None:
            self._values["bit_length"] = bit_length
        if expiration is not None:
            self._values["expiration"] = expiration
        if id is not None:
            self._values["id"] = id
        if metadata is not None:
            self._values["metadata"] = metadata
        if mode is not None:
            self._values["mode"] = mode
        if name is not None:
            self._values["name"] = name
        if payload is not None:
            self._values["payload"] = payload
        if payload_content_encoding is not None:
            self._values["payload_content_encoding"] = payload_content_encoding
        if payload_content_type is not None:
            self._values["payload_content_type"] = payload_content_type
        if region is not None:
            self._values["region"] = region
        if secret_type is not None:
            self._values["secret_type"] = secret_type
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
    def acl(self) -> typing.Optional[KeymanagerSecretV1Acl]:
        '''acl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#acl KeymanagerSecretV1#acl}
        '''
        result = self._values.get("acl")
        return typing.cast(typing.Optional[KeymanagerSecretV1Acl], result)

    @builtins.property
    def algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#algorithm KeymanagerSecretV1#algorithm}.'''
        result = self._values.get("algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bit_length(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#bit_length KeymanagerSecretV1#bit_length}.'''
        result = self._values.get("bit_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def expiration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#expiration KeymanagerSecretV1#expiration}.'''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#id KeymanagerSecretV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#metadata KeymanagerSecretV1#metadata}.'''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#mode KeymanagerSecretV1#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#name KeymanagerSecretV1#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#payload KeymanagerSecretV1#payload}.'''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload_content_encoding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#payload_content_encoding KeymanagerSecretV1#payload_content_encoding}.'''
        result = self._values.get("payload_content_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload_content_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#payload_content_type KeymanagerSecretV1#payload_content_type}.'''
        result = self._values.get("payload_content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#region KeymanagerSecretV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#secret_type KeymanagerSecretV1#secret_type}.'''
        result = self._values.get("secret_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KeymanagerSecretV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#timeouts KeymanagerSecretV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KeymanagerSecretV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeymanagerSecretV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.keymanagerSecretV1.KeymanagerSecretV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class KeymanagerSecretV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#create KeymanagerSecretV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#delete KeymanagerSecretV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#update KeymanagerSecretV1#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980dcbd5a1500b734b3c24ba0729c9932f5ef4fad9760ceb7a0e62beec5821e2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#create KeymanagerSecretV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#delete KeymanagerSecretV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/keymanager_secret_v1#update KeymanagerSecretV1#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeymanagerSecretV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeymanagerSecretV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.keymanagerSecretV1.KeymanagerSecretV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f18db6d56fc6ac1854540f6469141cb52ed608be47f3fd5079893251d07d53e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b34c819b57b94965e92ab33917e1ff6bda8244b5230667806cb3cef61050dca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2492620996451f148723aca84dc88705d6a16273eb8a0c5a50b101dcea027cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567b7bae913e4dd878c332e913dde05fc1164d243c85e3c9c7440c4e64a8788c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeymanagerSecretV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeymanagerSecretV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeymanagerSecretV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf7f7d6afb2e1a0d20e7c8e516803491fb06938e75038440f5c24ed164caf76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KeymanagerSecretV1",
    "KeymanagerSecretV1Acl",
    "KeymanagerSecretV1AclOutputReference",
    "KeymanagerSecretV1AclRead",
    "KeymanagerSecretV1AclReadOutputReference",
    "KeymanagerSecretV1Config",
    "KeymanagerSecretV1Timeouts",
    "KeymanagerSecretV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2239baf16431f9c18f180f25edad6e03c4b8dd449e9e36298ee9e59976649055(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    acl: typing.Optional[typing.Union[KeymanagerSecretV1Acl, typing.Dict[builtins.str, typing.Any]]] = None,
    algorithm: typing.Optional[builtins.str] = None,
    bit_length: typing.Optional[jsii.Number] = None,
    expiration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mode: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    payload: typing.Optional[builtins.str] = None,
    payload_content_encoding: typing.Optional[builtins.str] = None,
    payload_content_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    secret_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KeymanagerSecretV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4c91f88be4e9b0c13b17f4b5b125a5643d355f0e69d116ad86ede31adebd1e1d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d732afe0f07b30a84c82aac97b73e318429b36ba5dee85e9cfcc2cf75240c0cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560288e5f7c2ac4e849cb7282a64bc3d09101fca9784d303a7a147eecbba1369(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4f9a77ecfc38d3798c4e65b45de62bb9d3cea1c9d52156b2a4f77586c3831d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e646e11f398291af7ead265dd41e1f9c152787161f58b805860280eac7f8eadb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975f7c6aa5f0759fb0d2e388a8682d2449ba993ffed307944a2720271216d8f8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae9f7401dcf79cbcc796269a4a0c755936098ef017f8950b1147536d009091a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5291d0ff65776186b751fd5bc780e0351721bd2a9da6db147579a07cd9e9ef3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf50b5debab9fe074fe0de16e068ab124f6118e56665cb9f23052e925bac85f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8ee889d745632cbeb298049ff55aacf96cb7aa1771716cc87d866af009f901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ed014d75f3544bf779010b12a8c8e11b2f8e063dcb4a83bca17e625389f372(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbe04f024f8c67c8e70de7774f3cb089dc12e1a13b552a67001b55c9e3dcc49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02950621155535edbaba4e9de95770dc3d71634825605c8710ff9970bdca838c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d4b90a6cf696e5c4b7b8e5a2d7fcd3dc2d97388eed720d7220b3da8a280484(
    *,
    read: typing.Optional[typing.Union[KeymanagerSecretV1AclRead, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a3618ad755893fc2658c3191836aa7fc9bf894f250de79a32e9730fb1d6efb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6eaa7727365f5723b71e99a034e9d052a8cf37ed52b43ffd144d4021071fc39(
    value: typing.Optional[KeymanagerSecretV1Acl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f207fcd5f24a11c917d3cc3f3b039e19440ac13d2bae2621b5b3d7544b2ee199(
    *,
    project_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4925d0a6473c3635cd1e837148d3279ec5bbbaf7f7904fb9db7c49aee4bdf8bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d37d2009708dc4c3791c0ab861acf65f5fb383689cd7803aabb49dced5d57f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6de7834b98535d8646f7ffcbd7c2d3be19ecc254655e9fc556e7da199bc1f5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21553ac7cd7128a6040e6448b714cec35768d944b53ef0ad547363f234d206a(
    value: typing.Optional[KeymanagerSecretV1AclRead],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5fa3c2f1773fbc8e8d0e36181d0dea87908732a68a0353668ca77ff4e112f73(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    acl: typing.Optional[typing.Union[KeymanagerSecretV1Acl, typing.Dict[builtins.str, typing.Any]]] = None,
    algorithm: typing.Optional[builtins.str] = None,
    bit_length: typing.Optional[jsii.Number] = None,
    expiration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mode: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    payload: typing.Optional[builtins.str] = None,
    payload_content_encoding: typing.Optional[builtins.str] = None,
    payload_content_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    secret_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KeymanagerSecretV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980dcbd5a1500b734b3c24ba0729c9932f5ef4fad9760ceb7a0e62beec5821e2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18db6d56fc6ac1854540f6469141cb52ed608be47f3fd5079893251d07d53e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34c819b57b94965e92ab33917e1ff6bda8244b5230667806cb3cef61050dca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2492620996451f148723aca84dc88705d6a16273eb8a0c5a50b101dcea027cf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567b7bae913e4dd878c332e913dde05fc1164d243c85e3c9c7440c4e64a8788c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf7f7d6afb2e1a0d20e7c8e516803491fb06938e75038440f5c24ed164caf76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KeymanagerSecretV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
