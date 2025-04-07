# Insilico Medicine AWS SDK

Insilico-aws is a python package for interacting with Insilico Medicine's products deployed on AWS.
Please check the `examples` directory for more details.

The package is optional if you are proficient user of the Sagemaker API you might prefer `sagemaker.Session` direct usage.
 

## Installation

```bash
pip install insilico-aws
```

## Quick Start

Check the example [Jupyter notebooks](insilico_aws/examples) to get started:

```bash
python -c "import insilico_aws; insilico_aws.load_examples(overwrite=False)"
```

This will create `examples` directory in the current workspace.

Before using the package make sure you have configured AWS credentials,
the default region can be overwritten by the client parameter:

```python
from insilico_aws import AlgorithmClient
client = AlgorithmClient(algorithm='<name>', region_name='us-east-1')
```

Or use a Product Arn (can be found in your subscription details):

```python
from insilico_aws import AlgorithmClient
client = AlgorithmClient(algorithm='<name>', arn='<arn>')
```

## Support

Please contact us via `info@insilico.com`
