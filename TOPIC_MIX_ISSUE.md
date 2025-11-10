# Description

Reusing Vehicle example to reproduce an issue where 2 publishers write 1MB messages to 2 different topics. A subscriber is configured to read only from the first topic but we see it eventually receives messages from the second topic too.

Expected behavior: the subscriber only recieves messages from the topic it subscribes to.

Changes:
- Added `examples/vehicle/main.py`: instanitaties and runs 2 publishers and 1 subscriber to reproduce the issue
- Extended Vehicle idl by adding a data buffer field (`types.sequence[types.uint8]`)

Observations:
- Lowering the `Vehicle.data` payload from 1MB to 1KB doesn't trigger the issue
- Additional error hit:
```
  File "/usr/local/lib/python3.12/dist-packages/cyclonedds/idl/_support.py", line 142, in read_multi
    v = struct.unpack_from(self._endian + pack, buffer=self._bytes, offset=self._pos)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
struct.error: unpack_from requires a buffer of at least 1048624 bytes for unpacking 1048576 bytes at offset 48 (actual buffer size is 48)
```

# How to run

Minimal docker image for reproducing the issue:
- Installs CycloneDSS + CycloneDDS python (both at 0.10.5)
- Runs `example/vehicle/main,py` described on previous section

```
docker build -f topic-mix-issue.Dockerfile -t cyclonedds_repro . && docker run -it cyclonedds_repro
```

Example stdout output:

```
-----------------------------
Publishing to topics:
 - topic/vehicle1
 - topic/vehicle2
Subscribing to topic: topic/vehicle1
-----------------------------
Wait for data...
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
[!!!] Unexpected topic name [!!!]: topic/vehicle2, expected: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
[!!!] Unexpected topic name [!!!]: topic/vehicle2, expected: topic/vehicle1
[!!!] Unexpected topic name [!!!]: topic/vehicle2, expected: topic/vehicle1
Received message from topic: topic/vehicle1
Received message from topic: topic/vehicle1
```
