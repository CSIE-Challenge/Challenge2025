#include "varient.h"
#include "serialization.h"
#include <stdexcept>

namespace GameAPI {

std::unique_ptr<GodotVariant> GodotVariant::deserialize(const std::vector<uint8_t>& data, size_t& offset) {
    if (offset + 4 > data.size()) {
        throw std::runtime_error("Not enough data to read variant header");
    }
    
    int32_t header = GodotSerializer::read_int32(data, offset);
    TypeCode typecode = static_cast<TypeCode>(header & HEADER_TYPE_MASK);
    
    switch (typecode) {
        case TypeCode::NULL_TYPE:
            return std::make_unique<GodotNull>();
            
        case TypeCode::BOOL_TYPE: {
            int32_t value = GodotSerializer::read_int32(data, offset);
            return std::make_unique<GodotBool>(value == 1);
        }
        
        case TypeCode::INT_TYPE: {
            int32_t value = GodotSerializer::read_int32(data, offset);
            if (header & HEADER_DATA_FLAG_64) {
                int32_t hi = GodotSerializer::read_int32(data, offset);
                int64_t full_value = (static_cast<int64_t>(hi) << 32) | static_cast<uint32_t>(value);
                return std::make_unique<GodotInt>(full_value);
            } else {
                return std::make_unique<GodotInt>(value);
            }
        }
        
        case TypeCode::FLOAT_TYPE: {
            if (header & HEADER_DATA_FLAG_64) {
                uint64_t ieee_integer = 0;
                for (int i = 0; i < 8; i++) {
                    if (offset >= data.size()) throw std::runtime_error("Not enough data for float64");
                    ieee_integer = ieee_integer * 256 + data[offset + 7 - i];
                }
                offset += 8;
                union { double d; uint64_t i; } u;
                u.i = ieee_integer;
                return std::make_unique<GodotFloat>(u.d);
            } else {
                int32_t raw_value = GodotSerializer::read_int32(data, offset);
                union { float f; uint32_t i; } u;
                u.i = static_cast<uint32_t>(raw_value);
                return std::make_unique<GodotFloat>(u.f);
            }
        }
        
        case TypeCode::STRING_TYPE: {
            std::string value = GodotSerializer::read_string(data, offset);
            return std::make_unique<GodotString>(value);
        }
        
        case TypeCode::VECTOR2I_TYPE: {
            int32_t x = GodotSerializer::read_int32(data, offset);
            int32_t y = GodotSerializer::read_int32(data, offset);
            return std::make_unique<GodotVector2>(Vector2(x, y));
        }
        
        case TypeCode::ARRAY_TYPE: {
            int container_type_kind = (header & HEADER_DATA_FIELD_TYPED_ARRAY_MASK)
                    >> HEADER_DATA_FIELD_TYPED_ARRAY_SHIFT;
            GodotSerializer::read_container_type(container_type_kind, offset);
            
            int32_t count = GodotSerializer::read_int32(data, offset) & 0x7FFFFFFF;
            auto array = std::make_unique<GodotArray>();
            
            for (int32_t i = 0; i < count; i++) {
                array->push_back(deserialize(data, offset));
            }
            
            return array;
        }
        
        case TypeCode::DICTIONARY_TYPE: {
            // Skip container type info
            int key_type_kind = (header >> 16) & 0x3;
            int value_type_kind = (header >> 18) & 0x3;
            GodotSerializer::read_container_type(key_type_kind, offset);
            GodotSerializer::read_container_type(value_type_kind, offset);
            
            int32_t count = GodotSerializer::read_int32(data, offset) & 0x7FFFFFFF;
            auto dict = std::make_unique<GodotDictionary>();
            
            for (int32_t i = 0; i < count; i++) {
                auto key = deserialize(data, offset);
                auto value = deserialize(data, offset);
                dict->insert(std::move(key), std::move(value));
            }
            
            return dict;
        }
        
        default:
            throw std::runtime_error("Unsupported type code: " + std::to_string(static_cast<int>(typecode)));
    }
}

} // namespace GameAPI
