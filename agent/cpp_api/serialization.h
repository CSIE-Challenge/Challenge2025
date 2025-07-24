#pragma once

#include <cstddef>
#include <stdexcept>
#include <vector>
#include <string>
#include <cstdint>
#include <cstring>
#include "structures.h"

namespace GameAPI {

enum class ContainerTypeKind : int {
    NONE = 0b00,
    BUILTIN = 0b01,
    CLASS_NAME = 0b10,
    SCRIPT = 0b11
};

/**
 * @brief Godot-compatible serialization utilities
 * Based on Godot Engine's marshalls.cpp
 */
class GodotSerializer {
public:
    // Encoding functions (little-endian)
    static void encode_uint32(uint32_t value, uint8_t* buffer) {
        buffer[0] = value & 0xFF;
        buffer[1] = (value >> 8) & 0xFF;
        buffer[2] = (value >> 16) & 0xFF;
        buffer[3] = (value >> 24) & 0xFF;
    }
    
    static void encode_uint64(uint64_t value, uint8_t* buffer) {
        encode_uint32(value & 0xFFFFFFFF, buffer);
        encode_uint32(value >> 32, buffer + 4);
    }
    
    static void encode_float(float value, uint8_t* buffer) {
        union { float f; uint32_t i; } u;
        u.f = value;
        encode_uint32(u.i, buffer);
    }
    
    static void encode_double(double value, uint8_t* buffer) {
        union { double d; uint64_t i; } u;
        u.d = value;
        encode_uint64(u.i, buffer);
    }
    
    // Decoding functions (little-endian)
    static uint32_t decode_uint32(const uint8_t* buffer) {
        return buffer[0] | (buffer[1] << 8) | (buffer[2] << 16) | (buffer[3] << 24);
    }
    
    static uint64_t decode_uint64(const uint8_t* buffer) {
        uint32_t low = decode_uint32(buffer);
        uint32_t high = decode_uint32(buffer + 4);
        return static_cast<uint64_t>(low) | (static_cast<uint64_t>(high) << 32);
    }
    
    static float decode_float(const uint8_t* buffer) {
        union { float f; uint32_t i; } u;
        u.i = decode_uint32(buffer);
        return u.f;
    }
    
    static double decode_double(const uint8_t* buffer) {
        union { double d; uint64_t i; } u;
        u.i = decode_uint64(buffer);
        return u.d;
    }
    
    // Helper functions for buffer operations
    static void push_int32(std::vector<uint8_t>& buffer, int32_t value) {
        size_t old_size = buffer.size();
        buffer.resize(old_size + 4);
        encode_uint32(static_cast<uint32_t>(value), &buffer[old_size]);
    }
    
    static void push_int64(std::vector<uint8_t>& buffer, int64_t value) {
        size_t old_size = buffer.size();
        buffer.resize(old_size + 8);
        encode_uint64(static_cast<uint64_t>(value), &buffer[old_size]);
    }
    
    static void push_float(std::vector<uint8_t>& buffer, float value) {
        size_t old_size = buffer.size();
        buffer.resize(old_size + 4);
        encode_float(value, &buffer[old_size]);
    }
    
    static void push_double(std::vector<uint8_t>& buffer, double value) {
        size_t old_size = buffer.size();
        buffer.resize(old_size + 8);
        encode_double(value, &buffer[old_size]);
    }
    
    // String encoding (following Godot's format)
    static void push_string(std::vector<uint8_t>& buffer, const std::string& str) {
        // Push string length
        push_int32(buffer, static_cast<int32_t>(str.size()));
        
        // Push string data
        buffer.insert(buffer.end(), str.begin(), str.end());
        
        // Add padding to align to 4-byte boundary
        while (buffer.size() % 4 != 0) {
            buffer.push_back(0);
        }
    }
    
    // Reading functions with offset management
    static int32_t read_int32(const std::vector<uint8_t>& data, size_t& offset) {
        if (offset + 4 > data.size()) {
            throw std::runtime_error("Not enough data to read int32");
        }
        int32_t value = static_cast<int32_t>(decode_uint32(&data[offset]));
        offset += 4;
        return value;
    }
    
    static int64_t read_int64(const std::vector<uint8_t>& data, size_t& offset) {
        if (offset + 8 > data.size()) {
            throw std::runtime_error("Not enough data to read int64");
        }
        int64_t value = static_cast<int64_t>(decode_uint64(&data[offset]));
        offset += 8;
        return value;
    }
    
    static float read_float(const std::vector<uint8_t>& data, size_t& offset) {
        if (offset + 4 > data.size()) {
            throw std::runtime_error("Not enough data to read float");
        }
        float value = decode_float(&data[offset]);
        offset += 4;
        return value;
    }
    
    static double read_double(const std::vector<uint8_t>& data, size_t& offset) {
        if (offset + 8 > data.size()) {
            throw std::runtime_error("Not enough data to read double");
        }
        double value = decode_double(&data[offset]);
        offset += 8;
        return value;
    }
    
    static std::string read_string(const std::vector<uint8_t>& data, size_t& offset) {
        int32_t length = read_int32(data, offset);
        
        if (offset + length > data.size()) {
            throw std::runtime_error("Not enough data to read string");
        }
        
        std::string result(reinterpret_cast<const char*>(&data[offset]), length);
        offset += length;
        
        // Skip padding
        while (offset % 4 != 0 && offset < data.size()) {
            offset++;
        }
        
        return result;
    }

    static void read_container_type(int container_type_kind, size_t &offset) {
        switch (static_cast<ContainerTypeKind>(container_type_kind)) {
            case ContainerTypeKind::NONE:
                break;
            case ContainerTypeKind::BUILTIN:
                offset += 4;
                break;
            default:
                throw std::runtime_error("Unable to deserialize: unsupported container type: " + std::to_string(container_type_kind));
        }
    }
    
    // High-level serialization functions
    static std::vector<uint8_t> serialize(bool value) {
        std::vector<uint8_t> result;
        push_int32(result, 1); // BOOL type
        push_int32(result, value ? 1 : 0);
        return result;
    }
    
    static std::vector<uint8_t> serialize(int32_t value) {
        std::vector<uint8_t> result;
        push_int32(result, 2); // INT type
        push_int32(result, value);
        return result;
    }
    
    static std::vector<uint8_t> serialize(int64_t value) {
        std::vector<uint8_t> result;
        if (value > INT32_MAX || value < INT32_MIN) {
            push_int32(result, 2 | (1 << 16)); // INT type with 64-bit flag
            push_int64(result, value);
        } else {
            push_int32(result, 2); // INT type
            push_int32(result, static_cast<int32_t>(value));
        }
        return result;
    }
    
    static std::vector<uint8_t> serialize(float value) {
        std::vector<uint8_t> result;
        push_int32(result, 3); // FLOAT type
        push_float(result, value);
        return result;
    }
    
    static std::vector<uint8_t> serialize(double value) {
        std::vector<uint8_t> result;
        float f = static_cast<float>(value);
        if (static_cast<double>(f) != value) {
            push_int32(result, 3 | (1 << 16)); // FLOAT type with 64-bit flag
            push_double(result, value);
        } else {
            push_int32(result, 3); // FLOAT type
            push_float(result, f);
        }
        return result;
    }
    
    static std::vector<uint8_t> serialize(const std::string& value) {
        std::vector<uint8_t> result;
        push_int32(result, 4); // STRING type
        push_string(result, value);
        return result;
    }
    
    static std::vector<uint8_t> serialize(const Vector2& value) {
        std::vector<uint8_t> result;
        push_int32(result, 6); // VECTOR2I type
        push_int32(result, value.x);
        push_int32(result, value.y);
        return result;
    }
    
    // Deserialization functions for backwards compatibility
    static int deserialize_int(const std::vector<uint8_t>& data, size_t& offset) {
        return read_int32(data, offset);
    }
    
    static std::string deserialize_string(const std::vector<uint8_t>& data, size_t& offset) {
        return read_string(data, offset);
    }
};

} // namespace GameAPI
