# Pixy Official PythonSDK

Pixy is a GenAI plform to generate multi-media resources. This SDK provides a super simple and integrated interface to generate images, videos and subtitles using the Pixy API.

## Installation

```bash
pip install pixy-sdk
```

## Usage

This SDK can be used in two ways:

1. **Naive**: Conducting tasks using the `PixyClient` class; this way, operations are simple and straightforward, sacrificing flexibility.

2. **Advanced**: Methods of the `PixyClient` rely on a set of functions, available at the `utils` [module](core/utils); using these functions directly increases the flexibility, however this approach can get more complex.

## Documentation

For each module of the SDK, we have prepaired exlusive documentation pages, as below:

1. [`client`](documentation/client): This module provides the `PixyClient` class; if you are considering taking the Naive approach (as described above) to use the SDK, you should start here.

2. [`schemas`](documentation/schemas): To avoid data validation issues, we define and use custom data classes as schemas; on this page, we go through each of them individually.

3. [`utils`](documentation/utils): To provide advanced users with more control over the SDK, the whole functionality of the SDK is also available outside of the `PixyClient` class; on this page, we go through each of them individually.