r'''
# TypeScript AWS CDK solution for setup a developer platform at AWS

This is TypeScript CDK constructs project to create an open source developer platform at AWS

## How it Works

This project uses projen for TypeScript sources, tooling and testing.
Just execute `npx projen help` to see what you can do.

**Current status:** Under development

## How to start

You will need to have Typescript 5.8 or newer version and Yarn installed.
This will also install AWS cdk command by calling `npm install -g aws-cdk`.

... Yada yada

main DevCloudConstruct

# cdk-dev-cloud-constructs

[![](https://constructs.dev/favicon.ico) Construct Hub](https://constructs.dev/packages/@bitbauer/cdk-dev-cloud-constructs)

---


## Table of Contents

* [Installation](#installation)
* [License](#license)

## Installation

TypeScript/JavaScript:

```bash
npm i cdk-dev-cloud-constructs
```

Python:

```bash
pip install cdk-dev-cloud-constructs
```

## License

`cdk-pipeline-for-terraform` is distributed under the terms of the [MIT](https://opensource.org/license/mit/) license.

# replace this
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

from ._jsii import *


class Hello(metaclass=jsii.JSIIMeta, jsii_type="cdk-dev-cloud-constructs.Hello"):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="sayHello")
    def say_hello(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "sayHello", []))


__all__ = [
    "Hello",
]

publication.publish()
