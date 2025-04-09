r'''
# `openstack_blockstorage_quotaset_v3`

Refer to the Terraform Registry for docs: [`openstack_blockstorage_quotaset_v3`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3).
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


class BlockstorageQuotasetV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.blockstorageQuotasetV3.BlockstorageQuotasetV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3 openstack_blockstorage_quotaset_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        project_id: builtins.str,
        backup_gigabytes: typing.Optional[jsii.Number] = None,
        backups: typing.Optional[jsii.Number] = None,
        gigabytes: typing.Optional[jsii.Number] = None,
        groups: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        per_volume_gigabytes: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        snapshots: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["BlockstorageQuotasetV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        volumes: typing.Optional[jsii.Number] = None,
        volume_type_quota: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3 openstack_blockstorage_quotaset_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#project_id BlockstorageQuotasetV3#project_id}.
        :param backup_gigabytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#backup_gigabytes BlockstorageQuotasetV3#backup_gigabytes}.
        :param backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#backups BlockstorageQuotasetV3#backups}.
        :param gigabytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#gigabytes BlockstorageQuotasetV3#gigabytes}.
        :param groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#groups BlockstorageQuotasetV3#groups}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#id BlockstorageQuotasetV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param per_volume_gigabytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#per_volume_gigabytes BlockstorageQuotasetV3#per_volume_gigabytes}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#region BlockstorageQuotasetV3#region}.
        :param snapshots: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#snapshots BlockstorageQuotasetV3#snapshots}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#timeouts BlockstorageQuotasetV3#timeouts}
        :param volumes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#volumes BlockstorageQuotasetV3#volumes}.
        :param volume_type_quota: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#volume_type_quota BlockstorageQuotasetV3#volume_type_quota}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce10dcf65ca5bf56eecba31cf29a58656ab4f4e1e300c0cde9fe3afe13355e8f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BlockstorageQuotasetV3Config(
            project_id=project_id,
            backup_gigabytes=backup_gigabytes,
            backups=backups,
            gigabytes=gigabytes,
            groups=groups,
            id=id,
            per_volume_gigabytes=per_volume_gigabytes,
            region=region,
            snapshots=snapshots,
            timeouts=timeouts,
            volumes=volumes,
            volume_type_quota=volume_type_quota,
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
        '''Generates CDKTF code for importing a BlockstorageQuotasetV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BlockstorageQuotasetV3 to import.
        :param import_from_id: The id of the existing BlockstorageQuotasetV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BlockstorageQuotasetV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9801825abbdf40360fe9e0b9941e65e3553eb751e4d6384312f45d0c8147bca7)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#create BlockstorageQuotasetV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#delete BlockstorageQuotasetV3#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#update BlockstorageQuotasetV3#update}.
        '''
        value = BlockstorageQuotasetV3Timeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBackupGigabytes")
    def reset_backup_gigabytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupGigabytes", []))

    @jsii.member(jsii_name="resetBackups")
    def reset_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackups", []))

    @jsii.member(jsii_name="resetGigabytes")
    def reset_gigabytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGigabytes", []))

    @jsii.member(jsii_name="resetGroups")
    def reset_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroups", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPerVolumeGigabytes")
    def reset_per_volume_gigabytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerVolumeGigabytes", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSnapshots")
    def reset_snapshots(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshots", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @jsii.member(jsii_name="resetVolumeTypeQuota")
    def reset_volume_type_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeTypeQuota", []))

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
    def timeouts(self) -> "BlockstorageQuotasetV3TimeoutsOutputReference":
        return typing.cast("BlockstorageQuotasetV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backupGigabytesInput")
    def backup_gigabytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupGigabytesInput"))

    @builtins.property
    @jsii.member(jsii_name="backupsInput")
    def backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupsInput"))

    @builtins.property
    @jsii.member(jsii_name="gigabytesInput")
    def gigabytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gigabytesInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsInput")
    def groups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "groupsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="perVolumeGigabytesInput")
    def per_volume_gigabytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "perVolumeGigabytesInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotsInput")
    def snapshots_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BlockstorageQuotasetV3Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BlockstorageQuotasetV3Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeQuotaInput")
    def volume_type_quota_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "volumeTypeQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="backupGigabytes")
    def backup_gigabytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupGigabytes"))

    @backup_gigabytes.setter
    def backup_gigabytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6c66151892396adab5809df0568b1faa1a1270153e49472080e80375b5835c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupGigabytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backups")
    def backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backups"))

    @backups.setter
    def backups(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5448b4c22813fa52f23ddefd3aec9df1c2cc802f84ce4ae24eadcaf4cfee1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gigabytes")
    def gigabytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gigabytes"))

    @gigabytes.setter
    def gigabytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4380eabf4ec82dc73847beb76c9d93e261177f564f12de41841fd72ecf47ac90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gigabytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dffd17394d55da7fd16eca34b3f4c84bd36ec2d565974f7daeb2202b033c5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b777152b8bc1d7d70122011bc816e87c93b47acd84cd1a7247782f1c6788ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perVolumeGigabytes")
    def per_volume_gigabytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "perVolumeGigabytes"))

    @per_volume_gigabytes.setter
    def per_volume_gigabytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9892c3392a7e8daa2cf1673f9c9faaab9a700ddc797e9ed7c0760351f8f9fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perVolumeGigabytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d66de2fa03358c2c29db02332229327882271983f41e6d2e7915a41130b6155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__004be0d77f0988e94c5312ffe77b515fcf9ec7dc5ceb641763c4ca94dc5f5765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshots")
    def snapshots(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshots"))

    @snapshots.setter
    def snapshots(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd1198bc2936f67d515d4c1f691ef8186ac6d1b30482079cf8378ea4a3a8a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshots", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumes"))

    @volumes.setter
    def volumes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be4f8213286e66142ad1cdfef5df49a986afb997811b6019d96ae1514f98098f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeTypeQuota")
    def volume_type_quota(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "volumeTypeQuota"))

    @volume_type_quota.setter
    def volume_type_quota(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2942eb8503ddab62b794b3c218e1e1f310a31b6c51d1c8f81fcbed548b328790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeTypeQuota", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.blockstorageQuotasetV3.BlockstorageQuotasetV3Config",
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
        "backup_gigabytes": "backupGigabytes",
        "backups": "backups",
        "gigabytes": "gigabytes",
        "groups": "groups",
        "id": "id",
        "per_volume_gigabytes": "perVolumeGigabytes",
        "region": "region",
        "snapshots": "snapshots",
        "timeouts": "timeouts",
        "volumes": "volumes",
        "volume_type_quota": "volumeTypeQuota",
    },
)
class BlockstorageQuotasetV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backup_gigabytes: typing.Optional[jsii.Number] = None,
        backups: typing.Optional[jsii.Number] = None,
        gigabytes: typing.Optional[jsii.Number] = None,
        groups: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        per_volume_gigabytes: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        snapshots: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["BlockstorageQuotasetV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        volumes: typing.Optional[jsii.Number] = None,
        volume_type_quota: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#project_id BlockstorageQuotasetV3#project_id}.
        :param backup_gigabytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#backup_gigabytes BlockstorageQuotasetV3#backup_gigabytes}.
        :param backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#backups BlockstorageQuotasetV3#backups}.
        :param gigabytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#gigabytes BlockstorageQuotasetV3#gigabytes}.
        :param groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#groups BlockstorageQuotasetV3#groups}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#id BlockstorageQuotasetV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param per_volume_gigabytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#per_volume_gigabytes BlockstorageQuotasetV3#per_volume_gigabytes}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#region BlockstorageQuotasetV3#region}.
        :param snapshots: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#snapshots BlockstorageQuotasetV3#snapshots}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#timeouts BlockstorageQuotasetV3#timeouts}
        :param volumes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#volumes BlockstorageQuotasetV3#volumes}.
        :param volume_type_quota: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#volume_type_quota BlockstorageQuotasetV3#volume_type_quota}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = BlockstorageQuotasetV3Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f1390045deded11d467e9d8a8c50a3262617077ba7686764f3050824290328)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument backup_gigabytes", value=backup_gigabytes, expected_type=type_hints["backup_gigabytes"])
            check_type(argname="argument backups", value=backups, expected_type=type_hints["backups"])
            check_type(argname="argument gigabytes", value=gigabytes, expected_type=type_hints["gigabytes"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument per_volume_gigabytes", value=per_volume_gigabytes, expected_type=type_hints["per_volume_gigabytes"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument snapshots", value=snapshots, expected_type=type_hints["snapshots"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument volume_type_quota", value=volume_type_quota, expected_type=type_hints["volume_type_quota"])
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
        if backup_gigabytes is not None:
            self._values["backup_gigabytes"] = backup_gigabytes
        if backups is not None:
            self._values["backups"] = backups
        if gigabytes is not None:
            self._values["gigabytes"] = gigabytes
        if groups is not None:
            self._values["groups"] = groups
        if id is not None:
            self._values["id"] = id
        if per_volume_gigabytes is not None:
            self._values["per_volume_gigabytes"] = per_volume_gigabytes
        if region is not None:
            self._values["region"] = region
        if snapshots is not None:
            self._values["snapshots"] = snapshots
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if volumes is not None:
            self._values["volumes"] = volumes
        if volume_type_quota is not None:
            self._values["volume_type_quota"] = volume_type_quota

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#project_id BlockstorageQuotasetV3#project_id}.'''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_gigabytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#backup_gigabytes BlockstorageQuotasetV3#backup_gigabytes}.'''
        result = self._values.get("backup_gigabytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#backups BlockstorageQuotasetV3#backups}.'''
        result = self._values.get("backups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gigabytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#gigabytes BlockstorageQuotasetV3#gigabytes}.'''
        result = self._values.get("gigabytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def groups(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#groups BlockstorageQuotasetV3#groups}.'''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#id BlockstorageQuotasetV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def per_volume_gigabytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#per_volume_gigabytes BlockstorageQuotasetV3#per_volume_gigabytes}.'''
        result = self._values.get("per_volume_gigabytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#region BlockstorageQuotasetV3#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshots(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#snapshots BlockstorageQuotasetV3#snapshots}.'''
        result = self._values.get("snapshots")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BlockstorageQuotasetV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#timeouts BlockstorageQuotasetV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BlockstorageQuotasetV3Timeouts"], result)

    @builtins.property
    def volumes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#volumes BlockstorageQuotasetV3#volumes}.'''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type_quota(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#volume_type_quota BlockstorageQuotasetV3#volume_type_quota}.'''
        result = self._values.get("volume_type_quota")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockstorageQuotasetV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.blockstorageQuotasetV3.BlockstorageQuotasetV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BlockstorageQuotasetV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#create BlockstorageQuotasetV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#delete BlockstorageQuotasetV3#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#update BlockstorageQuotasetV3#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31211b1e861a70c35fe6407f5c403601b1f6b25b4cd91c52fcdb7c192decf87)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#create BlockstorageQuotasetV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#delete BlockstorageQuotasetV3#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_quotaset_v3#update BlockstorageQuotasetV3#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockstorageQuotasetV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BlockstorageQuotasetV3TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.blockstorageQuotasetV3.BlockstorageQuotasetV3TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0396c1062a30df8fead7184b42dd3d86f4be2492b5c531d769902aa84551cbb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__969ecf729f4f1d3c961e98b44d1e5f2b7819f2281a66d68e862b1ce4a44e61b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0ae5008ac8021903b8227ae81bc34544f7c7dfc0446bf48e7c5d42f3eba649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12061d3f5ecd0c6d5211f17c80ae6d68dfe85c034053ae3f0072610b9484f44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockstorageQuotasetV3Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockstorageQuotasetV3Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockstorageQuotasetV3Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__019b1d31535b5d1c5ce6692faa8239c148bdc3c0cd5d8b9df1ae0c90590cc557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BlockstorageQuotasetV3",
    "BlockstorageQuotasetV3Config",
    "BlockstorageQuotasetV3Timeouts",
    "BlockstorageQuotasetV3TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ce10dcf65ca5bf56eecba31cf29a58656ab4f4e1e300c0cde9fe3afe13355e8f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    project_id: builtins.str,
    backup_gigabytes: typing.Optional[jsii.Number] = None,
    backups: typing.Optional[jsii.Number] = None,
    gigabytes: typing.Optional[jsii.Number] = None,
    groups: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    per_volume_gigabytes: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    snapshots: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[BlockstorageQuotasetV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    volumes: typing.Optional[jsii.Number] = None,
    volume_type_quota: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__9801825abbdf40360fe9e0b9941e65e3553eb751e4d6384312f45d0c8147bca7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6c66151892396adab5809df0568b1faa1a1270153e49472080e80375b5835c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5448b4c22813fa52f23ddefd3aec9df1c2cc802f84ce4ae24eadcaf4cfee1e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4380eabf4ec82dc73847beb76c9d93e261177f564f12de41841fd72ecf47ac90(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dffd17394d55da7fd16eca34b3f4c84bd36ec2d565974f7daeb2202b033c5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b777152b8bc1d7d70122011bc816e87c93b47acd84cd1a7247782f1c6788ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9892c3392a7e8daa2cf1673f9c9faaab9a700ddc797e9ed7c0760351f8f9fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d66de2fa03358c2c29db02332229327882271983f41e6d2e7915a41130b6155(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004be0d77f0988e94c5312ffe77b515fcf9ec7dc5ceb641763c4ca94dc5f5765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd1198bc2936f67d515d4c1f691ef8186ac6d1b30482079cf8378ea4a3a8a44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4f8213286e66142ad1cdfef5df49a986afb997811b6019d96ae1514f98098f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2942eb8503ddab62b794b3c218e1e1f310a31b6c51d1c8f81fcbed548b328790(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f1390045deded11d467e9d8a8c50a3262617077ba7686764f3050824290328(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project_id: builtins.str,
    backup_gigabytes: typing.Optional[jsii.Number] = None,
    backups: typing.Optional[jsii.Number] = None,
    gigabytes: typing.Optional[jsii.Number] = None,
    groups: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    per_volume_gigabytes: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    snapshots: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[BlockstorageQuotasetV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    volumes: typing.Optional[jsii.Number] = None,
    volume_type_quota: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31211b1e861a70c35fe6407f5c403601b1f6b25b4cd91c52fcdb7c192decf87(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0396c1062a30df8fead7184b42dd3d86f4be2492b5c531d769902aa84551cbb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969ecf729f4f1d3c961e98b44d1e5f2b7819f2281a66d68e862b1ce4a44e61b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0ae5008ac8021903b8227ae81bc34544f7c7dfc0446bf48e7c5d42f3eba649(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12061d3f5ecd0c6d5211f17c80ae6d68dfe85c034053ae3f0072610b9484f44e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__019b1d31535b5d1c5ce6692faa8239c148bdc3c0cd5d8b9df1ae0c90590cc557(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockstorageQuotasetV3Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
