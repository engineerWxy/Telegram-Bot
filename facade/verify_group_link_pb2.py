# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: verify_group_link.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'verify_group_link.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import facade.base_pb2 as base__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17verify_group_link.proto\x1a\nbase.proto\"Z\n\x16VerifyGroupLinkRequest\x12\x0e\n\x06sassId\x18\x01 \x01(\t\x12\x1d\n\tgroupType\x18\x02 \x01(\x0e\x32\n.GroupType\x12\x11\n\tgroupLink\x18\x03 \x01(\t*$\n\tGroupType\x12\x0b\n\x07private\x10\x00\x12\n\n\x06public\x10\x01\x32I\n\nVerifyLink\x12;\n\x0fverifyGroupLink\x12\x17.VerifyGroupLinkRequest\x1a\x0f.CommonResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'verify_group_link_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GROUPTYPE']._serialized_start=131
  _globals['_GROUPTYPE']._serialized_end=167
  _globals['_VERIFYGROUPLINKREQUEST']._serialized_start=39
  _globals['_VERIFYGROUPLINKREQUEST']._serialized_end=129
  _globals['_VERIFYLINK']._serialized_start=169
  _globals['_VERIFYLINK']._serialized_end=242
# @@protoc_insertion_point(module_scope)
