// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.28.1
// 	protoc        v3.12.4
// source: vacancy.proto

package protobuf

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type ListRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields
}

func (x *ListRequest) Reset() {
	*x = ListRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_vacancy_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *ListRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*ListRequest) ProtoMessage() {}

func (x *ListRequest) ProtoReflect() protoreflect.Message {
	mi := &file_vacancy_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use ListRequest.ProtoReflect.Descriptor instead.
func (*ListRequest) Descriptor() ([]byte, []int) {
	return file_vacancy_proto_rawDescGZIP(), []int{0}
}

type Vacancy struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Id          int32  `protobuf:"varint,1,opt,name=id,proto3" json:"id,omitempty"`
	SectId      int32  `protobuf:"varint,2,opt,name=sect_id,json=sectId,proto3" json:"sect_id,omitempty"`
	Name        string `protobuf:"bytes,3,opt,name=name,proto3" json:"name,omitempty"`
	Description string `protobuf:"bytes,4,opt,name=description,proto3" json:"description,omitempty"`
	IsActive    bool   `protobuf:"varint,5,opt,name=is_active,json=isActive,proto3" json:"is_active,omitempty"`
	Token       string `protobuf:"bytes,6,opt,name=token,proto3" json:"token,omitempty"`
}

func (x *Vacancy) Reset() {
	*x = Vacancy{}
	if protoimpl.UnsafeEnabled {
		mi := &file_vacancy_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Vacancy) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Vacancy) ProtoMessage() {}

func (x *Vacancy) ProtoReflect() protoreflect.Message {
	mi := &file_vacancy_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Vacancy.ProtoReflect.Descriptor instead.
func (*Vacancy) Descriptor() ([]byte, []int) {
	return file_vacancy_proto_rawDescGZIP(), []int{1}
}

func (x *Vacancy) GetId() int32 {
	if x != nil {
		return x.Id
	}
	return 0
}

func (x *Vacancy) GetSectId() int32 {
	if x != nil {
		return x.SectId
	}
	return 0
}

func (x *Vacancy) GetName() string {
	if x != nil {
		return x.Name
	}
	return ""
}

func (x *Vacancy) GetDescription() string {
	if x != nil {
		return x.Description
	}
	return ""
}

func (x *Vacancy) GetIsActive() bool {
	if x != nil {
		return x.IsActive
	}
	return false
}

func (x *Vacancy) GetToken() string {
	if x != nil {
		return x.Token
	}
	return ""
}

type ListResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Vacancies []*Vacancy `protobuf:"bytes,1,rep,name=vacancies,proto3" json:"vacancies,omitempty"`
}

func (x *ListResponse) Reset() {
	*x = ListResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_vacancy_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *ListResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*ListResponse) ProtoMessage() {}

func (x *ListResponse) ProtoReflect() protoreflect.Message {
	mi := &file_vacancy_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use ListResponse.ProtoReflect.Descriptor instead.
func (*ListResponse) Descriptor() ([]byte, []int) {
	return file_vacancy_proto_rawDescGZIP(), []int{2}
}

func (x *ListResponse) GetVacancies() []*Vacancy {
	if x != nil {
		return x.Vacancies
	}
	return nil
}

type GetRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Id   int32  `protobuf:"varint,1,opt,name=id,proto3" json:"id,omitempty"`
	Name string `protobuf:"bytes,2,opt,name=name,proto3" json:"name,omitempty"`
}

func (x *GetRequest) Reset() {
	*x = GetRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_vacancy_proto_msgTypes[3]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *GetRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GetRequest) ProtoMessage() {}

func (x *GetRequest) ProtoReflect() protoreflect.Message {
	mi := &file_vacancy_proto_msgTypes[3]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GetRequest.ProtoReflect.Descriptor instead.
func (*GetRequest) Descriptor() ([]byte, []int) {
	return file_vacancy_proto_rawDescGZIP(), []int{3}
}

func (x *GetRequest) GetId() int32 {
	if x != nil {
		return x.Id
	}
	return 0
}

func (x *GetRequest) GetName() string {
	if x != nil {
		return x.Name
	}
	return ""
}

type CreateRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	SectId      int32  `protobuf:"varint,1,opt,name=sect_id,json=sectId,proto3" json:"sect_id,omitempty"`
	Description string `protobuf:"bytes,2,opt,name=description,proto3" json:"description,omitempty"`
}

func (x *CreateRequest) Reset() {
	*x = CreateRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_vacancy_proto_msgTypes[4]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *CreateRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*CreateRequest) ProtoMessage() {}

func (x *CreateRequest) ProtoReflect() protoreflect.Message {
	mi := &file_vacancy_proto_msgTypes[4]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use CreateRequest.ProtoReflect.Descriptor instead.
func (*CreateRequest) Descriptor() ([]byte, []int) {
	return file_vacancy_proto_rawDescGZIP(), []int{4}
}

func (x *CreateRequest) GetSectId() int32 {
	if x != nil {
		return x.SectId
	}
	return 0
}

func (x *CreateRequest) GetDescription() string {
	if x != nil {
		return x.Description
	}
	return ""
}

var File_vacancy_proto protoreflect.FileDescriptor

var file_vacancy_proto_rawDesc = []byte{
	0x0a, 0x0d, 0x76, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x79, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12,
	0x07, 0x76, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x79, 0x22, 0x0d, 0x0a, 0x0b, 0x4c, 0x69, 0x73, 0x74,
	0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x22, 0x9b, 0x01, 0x0a, 0x07, 0x56, 0x61, 0x63, 0x61,
	0x6e, 0x63, 0x79, 0x12, 0x0e, 0x0a, 0x02, 0x69, 0x64, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52,
	0x02, 0x69, 0x64, 0x12, 0x17, 0x0a, 0x07, 0x73, 0x65, 0x63, 0x74, 0x5f, 0x69, 0x64, 0x18, 0x02,
	0x20, 0x01, 0x28, 0x05, 0x52, 0x06, 0x73, 0x65, 0x63, 0x74, 0x49, 0x64, 0x12, 0x12, 0x0a, 0x04,
	0x6e, 0x61, 0x6d, 0x65, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x6e, 0x61, 0x6d, 0x65,
	0x12, 0x20, 0x0a, 0x0b, 0x64, 0x65, 0x73, 0x63, 0x72, 0x69, 0x70, 0x74, 0x69, 0x6f, 0x6e, 0x18,
	0x04, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0b, 0x64, 0x65, 0x73, 0x63, 0x72, 0x69, 0x70, 0x74, 0x69,
	0x6f, 0x6e, 0x12, 0x1b, 0x0a, 0x09, 0x69, 0x73, 0x5f, 0x61, 0x63, 0x74, 0x69, 0x76, 0x65, 0x18,
	0x05, 0x20, 0x01, 0x28, 0x08, 0x52, 0x08, 0x69, 0x73, 0x41, 0x63, 0x74, 0x69, 0x76, 0x65, 0x12,
	0x14, 0x0a, 0x05, 0x74, 0x6f, 0x6b, 0x65, 0x6e, 0x18, 0x06, 0x20, 0x01, 0x28, 0x09, 0x52, 0x05,
	0x74, 0x6f, 0x6b, 0x65, 0x6e, 0x22, 0x3e, 0x0a, 0x0c, 0x4c, 0x69, 0x73, 0x74, 0x52, 0x65, 0x73,
	0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x2e, 0x0a, 0x09, 0x76, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x69,
	0x65, 0x73, 0x18, 0x01, 0x20, 0x03, 0x28, 0x0b, 0x32, 0x10, 0x2e, 0x76, 0x61, 0x63, 0x61, 0x6e,
	0x63, 0x79, 0x2e, 0x56, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x79, 0x52, 0x09, 0x76, 0x61, 0x63, 0x61,
	0x6e, 0x63, 0x69, 0x65, 0x73, 0x22, 0x30, 0x0a, 0x0a, 0x47, 0x65, 0x74, 0x52, 0x65, 0x71, 0x75,
	0x65, 0x73, 0x74, 0x12, 0x0e, 0x0a, 0x02, 0x69, 0x64, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52,
	0x02, 0x69, 0x64, 0x12, 0x12, 0x0a, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x18, 0x02, 0x20, 0x01, 0x28,
	0x09, 0x52, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x22, 0x4a, 0x0a, 0x0d, 0x43, 0x72, 0x65, 0x61, 0x74,
	0x65, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x17, 0x0a, 0x07, 0x73, 0x65, 0x63, 0x74,
	0x5f, 0x69, 0x64, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52, 0x06, 0x73, 0x65, 0x63, 0x74, 0x49,
	0x64, 0x12, 0x20, 0x0a, 0x0b, 0x64, 0x65, 0x73, 0x63, 0x72, 0x69, 0x70, 0x74, 0x69, 0x6f, 0x6e,
	0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0b, 0x64, 0x65, 0x73, 0x63, 0x72, 0x69, 0x70, 0x74,
	0x69, 0x6f, 0x6e, 0x32, 0xce, 0x01, 0x0a, 0x09, 0x56, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x69, 0x65,
	0x73, 0x12, 0x32, 0x0a, 0x06, 0x43, 0x72, 0x65, 0x61, 0x74, 0x65, 0x12, 0x16, 0x2e, 0x76, 0x61,
	0x63, 0x61, 0x6e, 0x63, 0x79, 0x2e, 0x43, 0x72, 0x65, 0x61, 0x74, 0x65, 0x52, 0x65, 0x71, 0x75,
	0x65, 0x73, 0x74, 0x1a, 0x10, 0x2e, 0x76, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x79, 0x2e, 0x56, 0x61,
	0x63, 0x61, 0x6e, 0x63, 0x79, 0x12, 0x33, 0x0a, 0x04, 0x4c, 0x69, 0x73, 0x74, 0x12, 0x14, 0x2e,
	0x76, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x79, 0x2e, 0x4c, 0x69, 0x73, 0x74, 0x52, 0x65, 0x71, 0x75,
	0x65, 0x73, 0x74, 0x1a, 0x15, 0x2e, 0x76, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x79, 0x2e, 0x4c, 0x69,
	0x73, 0x74, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x2c, 0x0a, 0x03, 0x47, 0x65,
	0x74, 0x12, 0x13, 0x2e, 0x76, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x79, 0x2e, 0x47, 0x65, 0x74, 0x52,
	0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x10, 0x2e, 0x76, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x79,
	0x2e, 0x56, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x79, 0x12, 0x2a, 0x0a, 0x04, 0x45, 0x64, 0x69, 0x74,
	0x12, 0x10, 0x2e, 0x76, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x79, 0x2e, 0x56, 0x61, 0x63, 0x61, 0x6e,
	0x63, 0x79, 0x1a, 0x10, 0x2e, 0x76, 0x61, 0x63, 0x61, 0x6e, 0x63, 0x79, 0x2e, 0x56, 0x61, 0x63,
	0x61, 0x6e, 0x63, 0x79, 0x42, 0x0d, 0x5a, 0x0b, 0x2e, 0x2e, 0x2f, 0x70, 0x72, 0x6f, 0x74, 0x6f,
	0x62, 0x75, 0x66, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_vacancy_proto_rawDescOnce sync.Once
	file_vacancy_proto_rawDescData = file_vacancy_proto_rawDesc
)

func file_vacancy_proto_rawDescGZIP() []byte {
	file_vacancy_proto_rawDescOnce.Do(func() {
		file_vacancy_proto_rawDescData = protoimpl.X.CompressGZIP(file_vacancy_proto_rawDescData)
	})
	return file_vacancy_proto_rawDescData
}

var file_vacancy_proto_msgTypes = make([]protoimpl.MessageInfo, 5)
var file_vacancy_proto_goTypes = []interface{}{
	(*ListRequest)(nil),   // 0: vacancy.ListRequest
	(*Vacancy)(nil),       // 1: vacancy.Vacancy
	(*ListResponse)(nil),  // 2: vacancy.ListResponse
	(*GetRequest)(nil),    // 3: vacancy.GetRequest
	(*CreateRequest)(nil), // 4: vacancy.CreateRequest
}
var file_vacancy_proto_depIdxs = []int32{
	1, // 0: vacancy.ListResponse.vacancies:type_name -> vacancy.Vacancy
	4, // 1: vacancy.Vacancies.Create:input_type -> vacancy.CreateRequest
	0, // 2: vacancy.Vacancies.List:input_type -> vacancy.ListRequest
	3, // 3: vacancy.Vacancies.Get:input_type -> vacancy.GetRequest
	1, // 4: vacancy.Vacancies.Edit:input_type -> vacancy.Vacancy
	1, // 5: vacancy.Vacancies.Create:output_type -> vacancy.Vacancy
	2, // 6: vacancy.Vacancies.List:output_type -> vacancy.ListResponse
	1, // 7: vacancy.Vacancies.Get:output_type -> vacancy.Vacancy
	1, // 8: vacancy.Vacancies.Edit:output_type -> vacancy.Vacancy
	5, // [5:9] is the sub-list for method output_type
	1, // [1:5] is the sub-list for method input_type
	1, // [1:1] is the sub-list for extension type_name
	1, // [1:1] is the sub-list for extension extendee
	0, // [0:1] is the sub-list for field type_name
}

func init() { file_vacancy_proto_init() }
func file_vacancy_proto_init() {
	if File_vacancy_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_vacancy_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*ListRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_vacancy_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Vacancy); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_vacancy_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*ListResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_vacancy_proto_msgTypes[3].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*GetRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_vacancy_proto_msgTypes[4].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*CreateRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_vacancy_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   5,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_vacancy_proto_goTypes,
		DependencyIndexes: file_vacancy_proto_depIdxs,
		MessageInfos:      file_vacancy_proto_msgTypes,
	}.Build()
	File_vacancy_proto = out.File
	file_vacancy_proto_rawDesc = nil
	file_vacancy_proto_goTypes = nil
	file_vacancy_proto_depIdxs = nil
}
