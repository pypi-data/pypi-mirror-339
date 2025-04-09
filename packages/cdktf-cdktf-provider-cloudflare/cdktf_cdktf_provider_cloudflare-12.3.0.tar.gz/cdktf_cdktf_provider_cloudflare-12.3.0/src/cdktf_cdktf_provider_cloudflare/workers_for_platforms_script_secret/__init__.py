r'''
# `cloudflare_workers_for_platforms_script_secret`

Refer to the Terraform Registry for docs: [`cloudflare_workers_for_platforms_script_secret`](https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret).
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


class WorkersForPlatformsScriptSecret(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersForPlatformsScriptSecret.WorkersForPlatformsScriptSecret",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret cloudflare_workers_for_platforms_script_secret}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_id: builtins.str,
        dispatch_namespace: builtins.str,
        name: builtins.str,
        script_name: builtins.str,
        text: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret cloudflare_workers_for_platforms_script_secret} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: Identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#account_id WorkersForPlatformsScriptSecret#account_id}
        :param dispatch_namespace: Name of the Workers for Platforms dispatch namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#dispatch_namespace WorkersForPlatformsScriptSecret#dispatch_namespace}
        :param name: The name of this secret, this is what will be used to access it inside the Worker. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#name WorkersForPlatformsScriptSecret#name}
        :param script_name: Name of the script, used in URLs and route configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#script_name WorkersForPlatformsScriptSecret#script_name}
        :param text: The value of the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#text WorkersForPlatformsScriptSecret#text}
        :param type: The type of secret to put. Available values: "secret_text". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#type WorkersForPlatformsScriptSecret#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718861c8a87bf3783f709f7cbb409002e9bee5ca3cf516ce4ba48c8c598ebc25)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = WorkersForPlatformsScriptSecretConfig(
            account_id=account_id,
            dispatch_namespace=dispatch_namespace,
            name=name,
            script_name=script_name,
            text=text,
            type=type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a WorkersForPlatformsScriptSecret resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WorkersForPlatformsScriptSecret to import.
        :param import_from_id: The id of the existing WorkersForPlatformsScriptSecret that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WorkersForPlatformsScriptSecret to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5415122af543381e813b46ed58917e7d68ad436f957c0655b8a940095c08349e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dispatchNamespaceInput")
    def dispatch_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dispatchNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptNameInput")
    def script_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptNameInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7776413886a97c146b9cb640a1a6097518e02bf84fa902efb68a0daa45cc41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dispatchNamespace")
    def dispatch_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dispatchNamespace"))

    @dispatch_namespace.setter
    def dispatch_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3de3ecb5a5bca9b4e3fcbc0fa8b41d7b7b962fbac4a2467cc9402aea434d87e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dispatchNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd0bb26cce95f20745660344fb37904b7355e3c95f90e6f53fe1c470ec15735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptName")
    def script_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scriptName"))

    @script_name.setter
    def script_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f697323259b9404a352a7e40534d518e762524dd44b0343ab98f9b7feadae42e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5cfe0d8057d7ab8459ebb5e44a952cbad3407bf75de46fd0db41f5da738402d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c66aca7ea4b00c6c13c2d9154d1f6b514f32e8b389bb2e2fa87aed461c0f0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersForPlatformsScriptSecret.WorkersForPlatformsScriptSecretConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_id": "accountId",
        "dispatch_namespace": "dispatchNamespace",
        "name": "name",
        "script_name": "scriptName",
        "text": "text",
        "type": "type",
    },
)
class WorkersForPlatformsScriptSecretConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_id: builtins.str,
        dispatch_namespace: builtins.str,
        name: builtins.str,
        script_name: builtins.str,
        text: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: Identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#account_id WorkersForPlatformsScriptSecret#account_id}
        :param dispatch_namespace: Name of the Workers for Platforms dispatch namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#dispatch_namespace WorkersForPlatformsScriptSecret#dispatch_namespace}
        :param name: The name of this secret, this is what will be used to access it inside the Worker. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#name WorkersForPlatformsScriptSecret#name}
        :param script_name: Name of the script, used in URLs and route configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#script_name WorkersForPlatformsScriptSecret#script_name}
        :param text: The value of the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#text WorkersForPlatformsScriptSecret#text}
        :param type: The type of secret to put. Available values: "secret_text". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#type WorkersForPlatformsScriptSecret#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b80575003aaf62a5a97e7e2fbc1bfcde8244194a5383f2f74ad3628f5076f8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument dispatch_namespace", value=dispatch_namespace, expected_type=type_hints["dispatch_namespace"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument script_name", value=script_name, expected_type=type_hints["script_name"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "dispatch_namespace": dispatch_namespace,
            "name": name,
            "script_name": script_name,
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
        if text is not None:
            self._values["text"] = text
        if type is not None:
            self._values["type"] = type

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
    def account_id(self) -> builtins.str:
        '''Identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#account_id WorkersForPlatformsScriptSecret#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dispatch_namespace(self) -> builtins.str:
        '''Name of the Workers for Platforms dispatch namespace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#dispatch_namespace WorkersForPlatformsScriptSecret#dispatch_namespace}
        '''
        result = self._values.get("dispatch_namespace")
        assert result is not None, "Required property 'dispatch_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this secret, this is what will be used to access it inside the Worker.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#name WorkersForPlatformsScriptSecret#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def script_name(self) -> builtins.str:
        '''Name of the script, used in URLs and route configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#script_name WorkersForPlatformsScriptSecret#script_name}
        '''
        result = self._values.get("script_name")
        assert result is not None, "Required property 'script_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''The value of the secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#text WorkersForPlatformsScriptSecret#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of secret to put. Available values: "secret_text".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/5.3.0/docs/resources/workers_for_platforms_script_secret#type WorkersForPlatformsScriptSecret#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersForPlatformsScriptSecretConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "WorkersForPlatformsScriptSecret",
    "WorkersForPlatformsScriptSecretConfig",
]

publication.publish()

def _typecheckingstub__718861c8a87bf3783f709f7cbb409002e9bee5ca3cf516ce4ba48c8c598ebc25(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_id: builtins.str,
    dispatch_namespace: builtins.str,
    name: builtins.str,
    script_name: builtins.str,
    text: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__5415122af543381e813b46ed58917e7d68ad436f957c0655b8a940095c08349e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7776413886a97c146b9cb640a1a6097518e02bf84fa902efb68a0daa45cc41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3de3ecb5a5bca9b4e3fcbc0fa8b41d7b7b962fbac4a2467cc9402aea434d87e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd0bb26cce95f20745660344fb37904b7355e3c95f90e6f53fe1c470ec15735(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f697323259b9404a352a7e40534d518e762524dd44b0343ab98f9b7feadae42e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5cfe0d8057d7ab8459ebb5e44a952cbad3407bf75de46fd0db41f5da738402d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c66aca7ea4b00c6c13c2d9154d1f6b514f32e8b389bb2e2fa87aed461c0f0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b80575003aaf62a5a97e7e2fbc1bfcde8244194a5383f2f74ad3628f5076f8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    dispatch_namespace: builtins.str,
    name: builtins.str,
    script_name: builtins.str,
    text: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
