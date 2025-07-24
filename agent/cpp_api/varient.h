#pragma once

#include <cstdint>
#include <vector>
#include <string>
#include <memory>
#include <map>
#include "serialization.h"
#include "structures.h"

namespace GameAPI {

constexpr uint64_t HEADER_TYPE_MASK = 0xFF;
constexpr uint64_t HEADER_DATA_FLAG_64 = 1 << 16;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_ARRAY_MASK = 0b11 << 16;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_ARRAY_SHIFT = 16;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_DICTIONARY_KEY_MASK = 0b11 << 16;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_DICTIONARY_KEY_SHIFT = 16;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_DICTIONARY_VALUE_MASK = 0b11 << 18;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_DICTIONARY_VALUE_SHIFT = 18;

class GodotVariant {
public:
    enum class TypeCode : uint8_t {
        NULL_TYPE = 0,
        BOOL_TYPE = 1,
        INT_TYPE = 2,
        FLOAT_TYPE = 3,
        STRING_TYPE = 4,
        VECTOR2I_TYPE = 6,
        DICTIONARY_TYPE = 27,
        ARRAY_TYPE = 28
    };

    virtual ~GodotVariant() = default;
    virtual std::vector<uint8_t> serialize() const = 0;
    virtual TypeCode getType() const = 0;
    
    // Static factory methods for deserialization
    static std::unique_ptr<GodotVariant> deserialize(const std::vector<uint8_t>& data, size_t& offset);
    
    // Template methods for getting values
    template<typename T>
    T getValue() const;
};

class GodotNull : public GodotVariant {
public:
    GodotNull() {}
    
    std::vector<uint8_t> serialize() const override {
        std::vector<uint8_t> result;
        GodotSerializer::push_int32(result, static_cast<int32_t>(TypeCode::NULL_TYPE));
        return result;
    }
    
    TypeCode getType() const override { return TypeCode::NULL_TYPE; }
};

class GodotBool : public GodotVariant {
public:
    GodotBool(bool v) : value(v) {}
    
    std::vector<uint8_t> serialize() const override {
        std::vector<uint8_t> result;
        GodotSerializer::push_int32(result, static_cast<int32_t>(TypeCode::BOOL_TYPE));
        GodotSerializer::push_int32(result, value ? 1 : 0);
        return result;
    }
    
    TypeCode getType() const override { return TypeCode::BOOL_TYPE; }
    bool getValue() const { return value; }
    
private:
    bool value;
};

class GodotInt : public GodotVariant {
public:
    GodotInt(int64_t v) : value(v) {}
    GodotInt(int v) : value(static_cast<int64_t>(v)) {}
    
    std::vector<uint8_t> serialize() const override {
        std::vector<uint8_t> result;
        
        uint32_t header = static_cast<uint32_t>(TypeCode::INT_TYPE);
        
        // Check if value fits in 32-bit range
        if (value > INT32_MAX || value < INT32_MIN) {
            // 64-bit integer serialization
            header |= HEADER_DATA_FLAG_64;
            GodotSerializer::push_int32(result, static_cast<int32_t>(header));
            GodotSerializer::push_int64(result, value);
        } else {
            // 32-bit integer serialization
            GodotSerializer::push_int32(result, static_cast<int32_t>(header));
            GodotSerializer::push_int32(result, static_cast<int32_t>(value));
        }
        
        return result;
    }
    
    TypeCode getType() const override { return TypeCode::INT_TYPE; }
    int64_t getValue() const { return value; }
    
private:
    int64_t value;
};

class GodotFloat : public GodotVariant {
public:
    GodotFloat(double v) : value(v) {}
    GodotFloat(float v) : value(static_cast<double>(v)) {}
    
    std::vector<uint8_t> serialize() const override {
        std::vector<uint8_t> result;
        
        uint32_t header = static_cast<uint32_t>(TypeCode::FLOAT_TYPE);
        float f = static_cast<float>(value);
        
        if (static_cast<double>(f) != value) {
            // Need 64-bit precision
            header |= HEADER_DATA_FLAG_64;
            GodotSerializer::push_int32(result, static_cast<int32_t>(header));
            GodotSerializer::push_double(result, value);
        } else {
            // 32-bit precision is sufficient
            GodotSerializer::push_int32(result, static_cast<int32_t>(header));
            GodotSerializer::push_float(result, f);
        }
        
        return result;
    }
    
    TypeCode getType() const override { return TypeCode::FLOAT_TYPE; }
    double getValue() const { return value; }
    float getValueAsFloat() const { return static_cast<float>(value); }
    
private:
    double value;
};

class GodotString : public GodotVariant {
public:
    GodotString(const std::string& v) : value(v) {}
    GodotString(const char* v) : value(v) {}
    
    std::vector<uint8_t> serialize() const override {
        std::vector<uint8_t> result;
        GodotSerializer::push_int32(result, static_cast<int32_t>(TypeCode::STRING_TYPE));
        GodotSerializer::push_string(result, value);
        return result;
    }
    
    TypeCode getType() const override { return TypeCode::STRING_TYPE; }
    const std::string& getValue() const { return value; }
    
private:
    std::string value;
};

class GodotVector2 : public GodotVariant {
public:
    GodotVector2(const Vector2& v) : value(v) {}
    GodotVector2(int x, int y) : value(x, y) {}
    
    std::vector<uint8_t> serialize() const override {
        std::vector<uint8_t> result;
        GodotSerializer::push_int32(result, static_cast<int32_t>(TypeCode::VECTOR2I_TYPE));
        GodotSerializer::push_int32(result, value.x);
        GodotSerializer::push_int32(result, value.y);
        return result;
    }
    
    TypeCode getType() const override { return TypeCode::VECTOR2I_TYPE; }
    const Vector2& getValue() const { return value; }
    
private:
    Vector2 value;
};

class GodotArray : public GodotVariant {
public:
    GodotArray() {}
    GodotArray(const std::vector<std::unique_ptr<GodotVariant>>& elements) {
        for (const auto& elem : elements) {
            value.push_back(std::unique_ptr<GodotVariant>(elem.get()));
        }
    }
    
    std::vector<uint8_t> serialize() const override {
        std::vector<uint8_t> result;
        GodotSerializer::push_int32(result, static_cast<int32_t>(TypeCode::ARRAY_TYPE));
        GodotSerializer::push_int32(result, static_cast<int32_t>(value.size()));
        
        for (const auto& elem : value) {
            auto elem_data = elem->serialize();
            result.insert(result.end(), elem_data.begin(), elem_data.end());
        }
        
        return result;
    }
    
    TypeCode getType() const override { return TypeCode::ARRAY_TYPE; }
    
    void push_back(std::unique_ptr<GodotVariant> variant) {
        value.push_back(std::move(variant));
    }
    
    size_t size() const { return value.size(); }
    const GodotVariant& at(size_t index) const { return *value.at(index); }
    const std::vector<std::unique_ptr<GodotVariant>>& getValue() const { return value; }
    
private:
    std::vector<std::unique_ptr<GodotVariant>> value;
};

class GodotDictionary : public GodotVariant {
public:
    GodotDictionary() {}
    
    std::vector<uint8_t> serialize() const override {
        std::vector<uint8_t> result;
        GodotSerializer::push_int32(result, static_cast<int32_t>(TypeCode::DICTIONARY_TYPE));
        GodotSerializer::push_int32(result, static_cast<int32_t>(value.size()));
        
        for (const auto& pair : value) {
            auto key_data = pair.first->serialize();
            auto val_data = pair.second->serialize();
            result.insert(result.end(), key_data.begin(), key_data.end());
            result.insert(result.end(), val_data.begin(), val_data.end());
        }
        
        return result;
    }
    
    TypeCode getType() const override { return TypeCode::DICTIONARY_TYPE; }
    
    void insert(std::unique_ptr<GodotVariant> key, std::unique_ptr<GodotVariant> val) {
        value.emplace_back(std::move(key), std::move(val));
    }
    
    size_t size() const { return value.size(); }
    const std::vector<std::pair<std::unique_ptr<GodotVariant>, std::unique_ptr<GodotVariant>>>& getValue() const { 
        return value; 
    }
    
private:
    std::vector<std::pair<std::unique_ptr<GodotVariant>, std::unique_ptr<GodotVariant>>> value;
};

// Template specializations for getValue
template<>
inline bool GodotVariant::getValue<bool>() const {
    if (auto* v = dynamic_cast<const GodotBool*>(this)) {
        return v->getValue();
    }
    throw std::runtime_error("Invalid type conversion to bool");
}

template<>
inline int GodotVariant::getValue<int>() const {
    if (auto* v = dynamic_cast<const GodotInt*>(this)) {
        return static_cast<int>(v->getValue());
    }
    throw std::runtime_error("Invalid type conversion to int");
}

template<>
inline int64_t GodotVariant::getValue<int64_t>() const {
    if (auto* v = dynamic_cast<const GodotInt*>(this)) {
        return v->getValue();
    }
    throw std::runtime_error("Invalid type conversion to int64_t");
}

template<>
inline float GodotVariant::getValue<float>() const {
    if (auto* v = dynamic_cast<const GodotFloat*>(this)) {
        return v->getValueAsFloat();
    }
    throw std::runtime_error("Invalid type conversion to float");
}

template<>
inline double GodotVariant::getValue<double>() const {
    if (auto* v = dynamic_cast<const GodotFloat*>(this)) {
        return v->getValue();
    }
    throw std::runtime_error("Invalid type conversion to double");
}

template<>
inline std::string GodotVariant::getValue<std::string>() const {
    if (auto* v = dynamic_cast<const GodotString*>(this)) {
        return v->getValue();
    }
    throw std::runtime_error("Invalid type conversion to string");
}

template<>
inline Vector2 GodotVariant::getValue<Vector2>() const {
    if (auto* v = dynamic_cast<const GodotVector2*>(this)) {
        return v->getValue();
    }
    throw std::runtime_error("Invalid type conversion to Vector2");
}

} // namespace GameAPI
