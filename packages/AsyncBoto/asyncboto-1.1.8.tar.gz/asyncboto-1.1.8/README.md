# Welcome to AsyncBoto

AsyncBoto is a Python library that provides an asynchronous interface similar to the Boto3 library, allowing you to interact with AWS services in a non-blocking manner.
This can be particularly useful for applications that require high concurrency or need to perform multiple AWS operations simultaneously.
This library is built on top of aiohttp and is designed to be easy to use, efficient, and compatible with the latest AWS services.

## Features
- Asynchronous API: Built on top of aiohttp, allowing for non-blocking I/O operations.
- Familiar Interface: Similar to Boto3, making it easy for existing Boto3 users to transition.
- Support for Multiple AWS Services: Interact with various AWS services such as S3, DynamoDB, and more.
- Automatic Retries: Built-in support for automatic retries on failed requests.
- Session Management: Manage AWS sessions and credentials easily.
- Customizable: Easily extendable and customizable to fit your needs.
- Full typing support: Every request/response is fully typed using pydantic models.

## Installation
You can install AsyncBoto using pip:

```bash
pip install AsyncBoto
```

or using uv
```bash
uv pip install AsyncBoto
```