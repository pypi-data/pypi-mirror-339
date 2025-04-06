# Payload42

PAYLOAD: Payload Abstraction Yields Layered Ordered Annotated Data

The `payload42` module provides the reference implementation of Payload42, a
type-length-value (TLV) encoding scheme designed for misuse-resistant
serialization in network protocols.

# What is Payload42?

Payload42 is type length value (TLV) encoding scheme designed to be misuse
resistant when used for serializing data sent by network protocols.

## Status of `payload42` implementing Payload42

This is pre-release software, under active development.

# How to use Payload42?

Python applications using network communication can encode messages using the
provided pure functions, producing structured, self-synchronizing payloads and
corresponding misuse-resistant decoders.
