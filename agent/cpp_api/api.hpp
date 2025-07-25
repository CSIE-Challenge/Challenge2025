#pragma once

#include <iostream>
#include <vector>
#include <string>
#include <utility>
#include <unordered_map>
#include <memory>
#include <variant>
#include <exception>
#include <thread>
#include <regex>
#include <chrono>
#include <stdexcept>
#include <algorithm>
#include <cstdint>
#include <cctype>
#include <cerrno>
#include <cstring>

#if defined(__linux__) || defined(__unix__) || defined(__APPLE__) || defined (__MACH__)
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netdb.h>
#elif defined(_WIN32) || defined(_WIN64)
// TODO
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#pragma comment(lib, "ws2_32.lib")
#else
#error "Unsupported platform"
#endif

// ****************************************************************************
// *                                                                          *
// *                         Constants and Enums                              *
// *                                                                          *
// ****************************************************************************
namespace GameAPI {

enum class CommandType {
    GET_ALL_TERRAIN = 1,
    GET_SCORES = 2,
    GET_CURRENT_WAVE = 3,
    GET_REMAIN_TIME = 4,
    GET_TIME_UNTIL_NEXT_WAVE = 5,
    GET_MONEY = 6,
    GET_INCOME = 7,
    GET_GAME_STATUS = 8,
    GET_TERRAIN = 9,
    GET_SYSTEM_PATH = 10,
    GET_OPPONENT_PATH = 11,
    PLACE_TOWER = 101,
    GET_ALL_TOWERS = 102,
    GET_TOWER = 103,
    SELL_TOWER = 104,
    SET_STRATEGY = 105,
    SPAWN_UNIT = 201,
    GET_UNIT_COOLDOWN = 202,
    GET_ALL_ENEMIES = 203,
    CAST_SPELL = 301,
    GET_SPELL_COOLDOWN = 302,
    SEND_CHAT = 401,
    GET_CHAT_HISTORY = 402,
    SET_CHAT_NAME_COLOR = 403,
    PIXELCAT = 501,
    GET_DEVS = 502,
    SET_NAME = 503,
    DISCONNECT = 601,
    NTU_STUDENT_ID_CARD = 602,
    METAL_PIPE = 603,
    SPAM = 604,
    SUPER_STAR = 605,
    TURBO_ON = 606,
    GET_THE_RADIANT_CORE_OF_STELLAR_FAITH = 607,
    SET_THE_RADIANT_CORE_OF_STELLAR_FAITH = 608,
    BOO = 609
};

enum class GameStatus {
    PREPARING = 0,
    RUNNING = 1,
    PAUSED = 2
};

enum class TerrainType {
    OUT_OF_BOUNDS = 0,
    EMPTY = 1,
    ROAD = 2,
    OBSTACLE = 3
};

enum class TowerType {
    FIRE_MARIO = 1,
    ICE_LUIGI = 2,
    DONKEY_KONG = 3,
    FORT = 4,
    SHY_GUY = 5
};

enum class EnemyType {
    BUZZY_BEETLE = 0,
    GOOMBA = 1,
    KOOPA_JR = 2,
    KOOPA_PARATROOPA = 3,
    KOOPA = 4,
    SPINY_SHELL = 5,
    WIGGLER = 6
};

enum class StatusCode : int {
    OK = 200,
    ILLFORMED_COMMAND = 400,
    AUTH_FAIL = 401,
    ILLEGAL_ARGUMENT = 402,
    COMMAND_ERR = 403,
    NOT_FOUND = 404,
    TOO_FREQUENT = 405,
    NOT_STARTED = 406,
    PAUSED = 407,
    INSUFFICIENT_QUOTA = 408,
    INTERNAL_ERR = 500,
    CLIENT_ERR = 501
};

const std::unordered_map<int, std::string> STATUS_CODE_TO_STRING = {
    {static_cast<int>(StatusCode::OK), "OK"},
    {static_cast<int>(StatusCode::ILLFORMED_COMMAND), "Ill-formed command"},
    {static_cast<int>(StatusCode::AUTH_FAIL), "Authentication failed"},
    {static_cast<int>(StatusCode::ILLEGAL_ARGUMENT), "Illegal argument"},
    {static_cast<int>(StatusCode::COMMAND_ERR), "Command error"},
    {static_cast<int>(StatusCode::NOT_FOUND), "Not found"},
    {static_cast<int>(StatusCode::TOO_FREQUENT), "Too frequent requests"},
    {static_cast<int>(StatusCode::NOT_STARTED), "Game not started"},
    {static_cast<int>(StatusCode::PAUSED), "Game paused"},
    {static_cast<int>(StatusCode::INSUFFICIENT_QUOTA), "Insufficient quota"},
    {static_cast<int>(StatusCode::INTERNAL_ERR), "Internal error"},
    {static_cast<int>(StatusCode::CLIENT_ERR), "Client error"}
};

enum class ChatSource {
    SYSTEM = 0,
    PLAYER = 1,
    OPPONENT = 2
};

enum class SpellType {
    POISON = 0,
    DOUBLE_INCOME = 1,
    TELEPORT = 2
};

enum class TargetStrategy {
    FIRST = 0,
    LAST = 1,
    CLOSEST = 2
};

}

// ****************************************************************************
// *                                                                          *
// *                       Structures and Classes                             *
// *                                                                          *
// ****************************************************************************
namespace GameAPI {

/**
 * @brief Two-dimensional vector with integer coordinates
 */
struct Vector2 {
    int x;
    int y;

    Vector2() : x(0), y(0) {}
    Vector2(int x, int y) : x(x), y(y) {}
    
    std::string toString() const {
        return "(" + std::to_string(x) + ", " + std::to_string(y) + ")";
    }
    
    bool operator==(const Vector2& other) const {
        return x == other.x && y == other.y;
    }
    
    bool operator!=(const Vector2& other) const {
        return !(*this == other);
    }
};

/**
 * @brief Exception thrown when API call fails
 */
class ApiException : public std::exception {
private:
    CommandType source_fn;
    StatusCode code;
    std::string message;
    std::string what_message;

public:
    ApiException(CommandType source_fn, StatusCode code, const std::string& what)
        : source_fn(source_fn), code(code), message(what) {
        what_message = "API call " + std::to_string(static_cast<int>(source_fn)) + 
                      " fails with status code " + std::to_string(static_cast<int>(code)) + 
                      ": " + what;
    }

    const char* what() const noexcept {
        return what_message.c_str();
    }

    CommandType getSourceFunction() const { return source_fn; }
    StatusCode getStatusCode() const { return code; }
    const std::string& getMessage() const { return message; }
};

/**
 * @brief Information about a tower
 */
struct Tower {
    TowerType type;
    Vector2 position;
    int level_a;
    int level_b;
    bool aim;
    bool anti_air;
    int reload;
    int range;
    int damage;
    std::string bullet_effect;

    Tower() : type(TowerType::FIRE_MARIO), position(0, 0), level_a(1), level_b(1),
              aim(false), anti_air(false), reload(0), range(0), damage(0),
              bullet_effect("none") {}

    Tower(TowerType type, const Vector2& position, int level_a, int level_b,
          bool aim, bool anti_air, int reload, int range, int damage,
          const std::string& bullet_effect)
        : type(type), position(position), level_a(level_a), level_b(level_b),
          aim(aim), anti_air(anti_air), reload(reload), range(range),
          damage(damage), bullet_effect(bullet_effect) {}
};

/**
 * @brief Information about an enemy unit
 */
struct Enemy {
    EnemyType type;
    Vector2 position;
    double progress_ratio;
    int income_impact;
    int health;
    int max_health;
    int damage;
    int max_speed;
    bool flying;
    double knockback_resist;
    int kill_reward;
    
    // Constructor matching Python API fields
    Enemy(EnemyType type, const Vector2& position, double progress_ratio, int income_impact, int health, int max_health, int damage, int max_speed, bool flying, double knockback_resist, int kill_reward)
        : type(type), position(position), progress_ratio(progress_ratio), income_impact(income_impact), health(health), max_health(max_health), damage(damage), max_speed(max_speed), flying(flying), knockback_resist(knockback_resist), kill_reward(kill_reward) {}
};

/**
 * @brief Chat message structure
 */
struct ChatMessage {
    ChatSource source;
    std::string sender_name;
    std::string content;
    std::string color;

    ChatMessage() : source(ChatSource::SYSTEM), sender_name(""), content(""), color("") {}

    ChatMessage(ChatSource source, const std::string& sender_name,
                const std::string& content, const std::string& color)
        : source(source), sender_name(sender_name), content(content), color(color) {}
};

}


// ****************************************************************************
// *                                                                          *
// *                         Serialization Utilities                          *
// *                                                                          *
// ****************************************************************************
namespace GameAPI {

enum class ContainerTypeKind : int {
    NONE = 0b00,
    BUILTIN = 0b01,
    CLASS_NAME = 0b10,
    SCRIPT = 0b11
};

/**
 * @brief Godot-compatible serialization utilities
 */
class GodotSerializer {
public:
    static void encode_uint32(uint32_t value, uint8_t *buffer) {
        buffer[0] = value & 0xFF;
        buffer[1] = (value >> 8) & 0xFF;
        buffer[2] = (value >> 16) & 0xFF;
        buffer[3] = (value >> 24) & 0xFF;
    }

    static void encode_uint64(uint64_t value, uint8_t *buffer) {
        encode_uint32(value & 0xFFFFFFFF, buffer);
        encode_uint32(value >> 32, buffer + 4);
    }

    static void encode_float(float value, uint8_t *buffer) {
        union { float f; uint32_t i; } u;
        u.f = value;
        encode_uint32(u.i, buffer);
    }

    static void encode_double(double value, uint8_t *buffer) {
        union { double d; uint64_t i; } u;
        u.d = value;
        encode_uint64(u.i, buffer);
    }

    static uint32_t decode_uint32(const uint8_t *buffer) {
        return buffer[0] | (buffer[1] << 8) | (buffer[2] << 16) | (buffer[3] << 24);
    }

    static uint64_t decode_uint64(const uint8_t *buffer) {
        uint32_t low = decode_uint32(buffer);
        uint32_t high = decode_uint32(buffer + 4);
        return static_cast<uint64_t>(low) | (static_cast<uint64_t>(high) << 32);
    }

    static float decode_float(const uint8_t *buffer) {
        union { float f; uint32_t i; } u;
        u.i = decode_uint32(buffer);
        return u.f;
    }

    static double decode_double(const uint8_t *buffer) {
        union { double d; uint64_t i; } u;
        u.i = decode_uint64(buffer);
        return u.d;
    }
    
    // Helper functions for buffer operations
    static void push_int32(std::vector<uint8_t> &buffer, int32_t value) {
        size_t old_size = buffer.size();
        buffer.resize(old_size + 4);
        encode_uint32(static_cast<uint32_t>(value), &buffer[old_size]);
    }

    static void push_int64(std::vector<uint8_t> &buffer, int64_t value) {
        size_t old_size = buffer.size();
        buffer.resize(old_size + 8);
        encode_uint64(static_cast<uint64_t>(value), &buffer[old_size]);
    }

    static void push_float(std::vector<uint8_t> &buffer, float value) {
        size_t old_size = buffer.size();
        buffer.resize(old_size + 4);
        encode_float(value, &buffer[old_size]);
    }

    static void push_double(std::vector<uint8_t> &buffer, double value) {
        size_t old_size = buffer.size();
        buffer.resize(old_size + 8);
        encode_double(value, &buffer[old_size]);
    }
    
    static void push_string(std::vector<uint8_t> &buffer, const std::string &str) {
        push_int32(buffer, static_cast<int32_t>(str.size()));
        buffer.insert(buffer.end(), str.begin(), str.end());
        while (buffer.size() % 4 != 0) {
            buffer.push_back(0);
        }
    }

    static int32_t read_int32(const std::vector<uint8_t> &data, size_t &offset) {
        if (offset + 4 > data.size()) {
            throw std::runtime_error("Not enough data to read int32");
        }
        int32_t value = static_cast<int32_t>(decode_uint32(&data[offset]));
        offset += 4;
        return value;
    }

    static int64_t read_int64(const std::vector<uint8_t> &data, size_t &offset) {
        if (offset + 8 > data.size()) {
            throw std::runtime_error("Not enough data to read int64");
        }
        int64_t value = static_cast<int64_t>(decode_uint64(&data[offset]));
        offset += 8;
        return value;
    }

    static float read_float(const std::vector<uint8_t> &data, size_t &offset) {
        if (offset + 4 > data.size()) {
            throw std::runtime_error("Not enough data to read float");
        }
        float value = decode_float(&data[offset]);
        offset += 4;
        return value;
    }

    static double read_double(const std::vector<uint8_t> &data, size_t &offset) {
        if (offset + 8 > data.size()) {
            throw std::runtime_error("Not enough data to read double");
        }
        double value = decode_double(&data[offset]);
        offset += 8;
        return value;
    }

    static std::string read_string(const std::vector<uint8_t> &data, size_t &offset) {
        int32_t length = read_int32(data, offset);
        
        if (offset + length > data.size()) {
            throw std::runtime_error("Not enough data to read string");
        }
        
        std::string result(reinterpret_cast<const char*>(&data[offset]), length);
        offset += length;
        
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

}

// ****************************************************************************
// *                                                                          *
// *                         Godot Variant Classes                            *
// *                                                                          *
// ****************************************************************************
namespace GameAPI {

constexpr uint64_t HEADER_TYPE_MASK = 0xFF;
constexpr uint64_t HEADER_DATA_FLAG_64 = 1 << 16;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_ARRAY_MASK = 0b11 << 16;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_ARRAY_SHIFT = 16;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_DICTIONARY_KEY_MASK = 0b11 << 16;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_DICTIONARY_KEY_SHIFT = 16;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_DICTIONARY_VALUE_MASK = 0b11 << 18;
constexpr uint64_t HEADER_DATA_FIELD_TYPED_DICTIONARY_VALUE_SHIFT = 18;

class GodotArray;
class GodotDictionary;
using GodotVariant = std::variant<int64_t, double, std::string, Vector2, GodotArray, GodotDictionary>;

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

class GodotVector2 {
public:
    GodotVector2(const Vector2& v) : value(v) {}
    GodotVector2(int x, int y) : value(x, y) {}
    
    std::vector<uint8_t> serialize() const {
        std::vector<uint8_t> result;
        GodotSerializer::push_int32(result, static_cast<int32_t>(TypeCode::VECTOR2I_TYPE));
        GodotSerializer::push_int32(result, value.x);
        GodotSerializer::push_int32(result, value.y);
        return result;
    }
    
    TypeCode getType() const { return TypeCode::VECTOR2I_TYPE; }
    const Vector2& getValue() const { return value; }
    
private:
    Vector2 value;
};

class GodotArray {
public:
    GodotArray() {}
    GodotArray(const GodotArray &other) {
        value = other.value;
    }
    GodotArray(const std::vector<GodotVariant>& elements) {
        for (const auto &elem : elements) {
            value.push_back(elem);
        }
    }
    
    std::vector<uint8_t> serialize() const {
        std::vector<uint8_t> result;
        GodotSerializer::push_int32(result, static_cast<int32_t>(TypeCode::ARRAY_TYPE));
        GodotSerializer::push_int32(result, static_cast<int32_t>(value.size()));
        
        for (const auto& elem : value) {
            auto elem_data = elem->serialize();
            result.insert(result.end(), elem_data.begin(), elem_data.end());
        }
        
        return result;
    }
    
    TypeCode getType() const { return TypeCode::ARRAY_TYPE; }
    
    void push_back(std::unique_ptr<GodotVariant> variant) {
        value.push_back(std::move(variant));
    }
    
    size_t size() const { return value.size(); }
    const GodotVariant& at(size_t index) const { return *value.at(index); }
    const std::vector<std::unique_ptr<GodotVariant>>& getValue() const { return value; }
    
private:
    std::vector<GodotVariant> value;
};

class GodotDictionary {
public:
    GodotDictionary() {}
    
    std::vector<uint8_t> serialize() const {
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
    
    TypeCode getType() const { return TypeCode::DICTIONARY_TYPE; }
    
    void insert(GodotVariant key, GodotVariant val) {
        value.emplace_back(std::move(key), std::move(val));
    }
    
    size_t size() const { return value.size(); }
    const std::vector<std::pair<GodotVariant, GodotVariant>>& getValue() const {
        return value;
    }
    
private:
    std::vector<std::pair<GodotVariant, GodotVariant>> value;
};

GodotVariant deserialize(const std::vector<uint8_t> &data, size_t &offset) {
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

std::vector<uint8_t> serialize(const GodotVariant &variant) {
    // TODO
}

}

// ****************************************************************************
// *                                                                          *
// *                         Game Client API                                  *
// *                                                                          *
// ****************************************************************************
namespace GameAPI {
/**
 * @brief WebSocket-based game client for interacting with the game server
 */
class GameClient {
public:
    /**
     * @brief Construct a new Game Client object
     * 
     * @param port Server port number
     * @param token Authentication token (8-digit hex string)
     * @param server_domain Server domain (default: "localhost")
     * @param command_timeout_msec Command timeout in milliseconds (default: 1000)
     * @param retry_count Number of retries for failed commands (default: 3)
     */
    GameClient(int port, const std::string& token, 
               const std::string& server_domain = "localhost",
               int command_timeout_msec = 1000, int retry_count = 3);
    
    /**
     * @brief Destroy the Game Client object
     */
    ~GameClient();

    // Game Status and Information
    /**
     * @brief Get current game status
     * @return GameStatus Current game status
     */
    GameStatus get_game_status();

    /**
     * @brief Get all terrain types on the map
     * @return std::vector<std::vector<TerrainType>> 2D grid of terrain types
     */
    std::vector<std::vector<TerrainType>> get_all_terrain();

    /**
     * @brief Get terrain type at specific position
     * @param position Position to check
     * @return TerrainType Terrain type at the position
     */
    TerrainType get_terrain(const Vector2& position);

    /**
     * @brief Get player or opponent score
     * @param owned true for player score, false for opponent score
     * @return int Score value
     */
    int get_scores(bool owned);

    /**
     * @brief Get current wave number
     * @return int Current wave number
     */
    int get_current_wave();

    /**
     * @brief Get remaining time in current wave
     * @return float Remaining time in seconds
     */
    float get_remain_time();

    /**
     * @brief Get time until next wave starts
     * @return float Time until next wave in seconds
     */
    float get_time_until_next_wave();

    /**
     * @brief Get current money amount
     * @param owned True for player's money, false for opponent's money
     * @return int Current money
     */
    int get_money(bool owned = true);

    /**
     * @brief Get player or opponent income per second
     * @param owned true for player income, false for opponent income
     * @return int Income per second
     */
    int get_income(bool owned);

    /**
     * @brief Get system path for units
     * @param flying Whether to get path for flying units
     * @return std::vector<Vector2> List of positions forming the path
     */
    std::vector<Vector2> get_system_path(bool flying = false);

    /**
     * @brief Get opponent's path for units
     * @param flying Whether to get path for flying units
     * @return std::vector<Vector2> List of positions forming the path
     */
    std::vector<Vector2> get_opponent_path(bool flying = false);

    // Tower Management
    /**
     * @brief Place a tower at specified position
     * @param tower_type Type of tower to place
     * @param level Tower level ("1", "2a", "2b", "3a", "3b")
     * @param position Position to place the tower
     */
    void place_tower(TowerType tower_type, const std::string& level, const Vector2& position);

    /**
     * @brief Get all towers on player or opponent map
     * @param owned true for player towers, false for opponent towers
     * @return std::vector<Tower> List of all towers
     */
    std::vector<Tower> get_all_towers(bool owned);

    /**
     * @brief Get tower at specific position
     * @param owned true for player tower, false for opponent tower
     * @param position Position to check
     * @return Tower Tower at the position (throws ApiException if no tower exists)
     */
    Tower get_tower(bool owned, const Vector2& position);

    /**
     * @brief Sell tower at specified position
     * @param position Position of tower to sell
     */
    void sell_tower(const Vector2& position);

    /**
     * @brief Set targeting strategy for tower
     * @param position Position of the tower
     * @param strategy Target strategy to set
     */
    void set_strategy(const Vector2& position, TargetStrategy strategy);

    // Enemy and Unit Management
    /**
     * @brief Spawn a unit
     * @param enemy_type Type of enemy unit to spawn
     */
    void spawn_unit(EnemyType enemy_type);

    /**
     * @brief Get cooldown time for unit spawning
     * @param enemy_type Type of enemy unit
     * @return float Cooldown time in seconds
     */
    float get_unit_cooldown(EnemyType enemy_type);

    /**
     * @brief Get all enemy units currently on player or opponent map
     * @param owned true for player enemies, false for opponent enemies
     * @return std::vector<Enemy> List of all enemies
     */
    std::vector<Enemy> get_all_enemies(bool owned);

    // Spell System
    /**
     * @brief Cast a spell at specified position
     * @param spell_type Type of spell to cast
     * @param position Target position for the spell
     */
    void cast_spell(SpellType spell_type, const Vector2& position);

    /**
     * @brief Get cooldown time for spell casting
     * @param owned true for player cooldown, false for opponent cooldown
     * @param spell_type Type of spell
     * @return float Cooldown time in seconds
     */
    float get_spell_cooldown(bool owned, SpellType spell_type);

    // Chat System
    /**
     * @brief Send a chat message
     * @param message Message content to send
     */
    void send_chat(const std::string& message);

    /**
     * @brief Get chat message history
     * @param num Number of messages to retrieve (default 15)
     * @return std::vector<ChatMessage> List of chat messages
     */
    std::vector<ChatMessage> get_chat_history(int num = 15);

    /**
     * @brief Set chat name color
     * @param color Hex color string (e.g., "ff0000" for red)
     */
    void set_chat_name_color(const std::string& color);

    /**
     * @brief Set player name
     * @param name Player name to set
     */
    void set_name(const std::string& name);

    // Special Commands
    /**
     * @brief Disconnect from the server
     */
    void disconnect();

    /**
     * @brief Get list of developers
     * @return std::vector<std::string> List of developer names
     */
    std::vector<std::string> get_devs();

    
    std::string pixelcat();
    std::string ntu_student_id_card();
    void metal_pipe();
    void spam(const std::string& message, int size = 48, const std::string& color = "#ffffff");
    void super_star();
    void turbo_on();
    int get_the_radiant_core_of_stellar_faith();
    void set_the_radiant_core_of_stellar_faith(int value);
    bool boo();
private:
    std::string server_url;
    std::string server_domain;
    std::string token;
    int port;
    int sent_command_count;
    long long last_command;
    
    static const int COMMAND_RATE_LIMIT_MSEC = 10;
    
    // Socket connection
    int socket_fd;
    bool connected;
    
    // Internal helper methods
    void ws_connect();
    bool ws_authenticate();
    void ws_send_data(const std::vector<uint8_t>& data);
    std::vector<uint8_t> ws_recv_data();
    void wait_for_next_command();
    std::vector<uint8_t> serialize_command(CommandType cmd, const std::vector<uint8_t>& args);
    std::vector<uint8_t> deserialize_response(const std::vector<uint8_t>& response, CommandType cmd);
    
    // Helper functions
    Tower parse_tower_from_dictionary(const GodotDictionary* tower_dict_ptr);
    Enemy parse_enemy_from_dictionary(const GodotDictionary* enemy_dict_ptr);
    
    // Command sending
    std::vector<uint8_t> send_command(CommandType cmd);
    std::vector<uint8_t> send_command(CommandType cmd, const std::vector<uint8_t>& args);
    
    // WebSocket helpers
    std::string create_websocket_handshake();
    bool validate_websocket_response(const std::string& response);
    void send_websocket_frame(const std::vector<uint8_t>& payload);
    void send_websocket_text_frame(const std::string& text);
    std::vector<uint8_t> receive_websocket_frame();

};

GameClient::GameClient(int port, const std::string& token, 
                      const std::string& server_domain,
                      int command_timeout_msec, int retry_count)
    : server_domain(server_domain), token(token), port(port),
      sent_command_count(0), last_command(0), socket_fd(-1), connected(false) {
    
    // Validate parameters
    if (port < 0 || port >= 65536) {
        throw std::invalid_argument("Port must be between 0 and 65535");
    }
    
    if (!std::regex_match(token, std::regex("[0-9a-fA-F]{8}"))) {
        throw std::invalid_argument("Token must be an 8-digit hexadecimal number");
    }
    
    if (command_timeout_msec < COMMAND_RATE_LIMIT_MSEC) {
        throw std::invalid_argument("Command timeout must be at least " + 
                                   std::to_string(COMMAND_RATE_LIMIT_MSEC) + " ms");
    }
    
    if (retry_count <= 0) {
        throw std::invalid_argument("Retry count must be positive");
    }
    
    server_url = "ws://" + server_domain + ":" + std::to_string(port);
    
    // Convert token to lowercase  
    this->token = token;
    std::transform(this->token.begin(), this->token.end(), this->token.begin(), 
                   [](unsigned char c){ return std::tolower(c); });
    
    ws_connect();
}

GameClient::~GameClient() {
    if (connected && socket_fd >= 0) {
        disconnect();
        close(socket_fd);
    }
}

void GameClient::ws_connect() {
    std::cout << "Connecting to " << server_url << std::endl;
    
    // Create socket
    socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd < 0) {
        throw std::runtime_error("Failed to create socket");
    }
    
    // Resolve hostname
    struct hostent* host = gethostbyname(server_domain.c_str());
    if (host == nullptr) {
        close(socket_fd);
        throw std::runtime_error("Failed to resolve hostname: " + server_domain);
    }
    
    // Setup server address
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    memcpy(&server_addr.sin_addr.s_addr, host->h_addr, host->h_length);
    
    // Connect to server
    if (connect(socket_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        close(socket_fd);
        throw std::runtime_error("Failed to connect to " + server_domain + ":" + std::to_string(port));
    }
    
    // Perform WebSocket handshake
    std::string handshake = create_websocket_handshake();
    if (send(socket_fd, handshake.c_str(), handshake.length(), 0) < 0) {
        close(socket_fd);
        throw std::runtime_error("Failed to send WebSocket handshake");
    }
    
    // Read handshake response
    char buffer[4096];
    ssize_t bytes_read = recv(socket_fd, buffer, sizeof(buffer) - 1, 0);
    if (bytes_read <= 0) {
        close(socket_fd);
        throw std::runtime_error("Failed to receive WebSocket handshake response");
    }
    
    buffer[bytes_read] = '\0';
    std::string response(buffer);
    
    if (!validate_websocket_response(response)) {
        close(socket_fd);
        throw std::runtime_error("Invalid WebSocket handshake response");
    }
    
    connected = true;
    
    if (!ws_authenticate()) {
        throw std::runtime_error("Authentication failed. Is the token correct?");
    }
    
    std::cout << "Connected to " << server_url << std::endl;
}

bool GameClient::ws_authenticate() {
    std::cout << "Authenticating connection" << std::endl;
    
    try {
        // Send token as plain text WebSocket frame (not binary)
        send_websocket_text_frame(token);
        
        // Receive authentication response
        std::vector<uint8_t> response = receive_websocket_frame();
        std::string response_str(response.begin(), response.end());
        
        std::cout << "Server says: " << response_str << std::endl;
        return response_str == "Connection OK. Have Fun!";
        
    } catch (const std::exception& e) {
        std::cerr << "Authentication error: " << e.what() << std::endl;
        return false;
    }
}

void GameClient::ws_send_data(const std::vector<uint8_t>& data) {
    send_websocket_frame(data);
}

std::vector<uint8_t> GameClient::ws_recv_data() {
    return receive_websocket_frame();
}

void GameClient::wait_for_next_command() {
    long long current_time = std::chrono::high_resolution_clock::now().time_since_epoch().count();
    long long time_to_wait = COMMAND_RATE_LIMIT_MSEC * 1000000 - (current_time - last_command);
    
    if (time_to_wait > 0) {
        std::this_thread::sleep_for(std::chrono::nanoseconds(time_to_wait));
    }
}

std::vector<uint8_t> GameClient::serialize_command(CommandType cmd, const std::vector<uint8_t>& args) {
    // Create command array: [request_id, command_id, ...args]
    sent_command_count++;
    
    // Create a GodotArray with proper structure
    GodotArray command_array;
    
    // Add request ID
    command_array.push_back(std::make_unique<GodotInt>(sent_command_count));
    
    // Add command ID  
    command_array.push_back(std::make_unique<GodotInt>(static_cast<int>(cmd)));
    
    // Add arguments if any
    if (!args.empty()) {
        // Try to deserialize individual arguments from the concatenated byte array
        // This is a workaround for the current method signature
        size_t offset = 0;
        while (offset < args.size()) {
            try {
                auto arg_variant = GodotVariant::deserialize(args, offset);
                command_array.push_back(std::move(arg_variant));
            } catch (const std::exception& e) {
                std::cerr << "Warning: Could not deserialize command argument at offset " << offset << ": " << e.what() << std::endl;
                break;
            }
        }
    }
    
    return command_array.serialize();
}

std::vector<uint8_t> GameClient::deserialize_response(const std::vector<uint8_t>& response, CommandType cmd) {
    size_t offset = 0;
    
    // Deserialize the response array
    auto response_variant = GodotVariant::deserialize(response, offset);
    auto *array_ptr = dynamic_cast<const GodotArray*>(response_variant.get());
    
    if (!array_ptr || array_ptr->size() < 2) {
        throw std::runtime_error("Invalid response format: expected array with [int, StatusCode, value]");
    }
    
    // Get the first integer (index 0) - not currently used but part of format
    auto *first_int = dynamic_cast<const GodotInt*>(&array_ptr->at(0));
    if (!first_int) {
        throw std::runtime_error("Invalid response format: first element must be integer");
    }
    
    // Get status code (second element at index 1)
    auto *status_variant = dynamic_cast<const GodotInt*>(&array_ptr->at(1));
    if (!status_variant) {
        throw std::runtime_error("Invalid response format: status code must be integer");
    }
    
    StatusCode status_code = static_cast<StatusCode>(status_variant->getValue());
    
    // Check status code
    if (status_code != StatusCode::OK) {
        std::string error_msg = "API call failed with status code " + std::to_string(static_cast<int>(status_code));
        
        // Add status code description if available
        auto status_iter = StatusCodeToString.find(static_cast<int>(status_code));
        if (status_iter != StatusCodeToString.end()) {
            error_msg += ": " + status_iter->second;
        }
        
        if (array_ptr->size() >= 3) {
            try {
                auto *error_variant = dynamic_cast<const GodotString*>(&array_ptr->at(2));
                if (error_variant) {
                    error_msg += ": " + error_variant->getValue();
                }
            } catch (std::exception &e) {
                std::cerr << "Error deserializing error message: " << e.what() << std::endl;
            }
        }
        throw ApiException(cmd, static_cast<StatusCode>(status_code), error_msg);
    }
    
    // Return the value part (third element at index 2) serialized
    if (array_ptr->size() >= 3) {
        return array_ptr->at(2).serialize();
    }
    
    return std::vector<uint8_t>();
}

std::vector<uint8_t> GameClient::send_command(CommandType cmd) {
    return send_command(cmd, std::vector<uint8_t>());
}

std::vector<uint8_t> GameClient::send_command(CommandType cmd, const std::vector<uint8_t>& args) {
    wait_for_next_command();
    
    // Serialize command
    std::vector<uint8_t> command_data = serialize_command(cmd, args);
    
    // Send command
    ws_send_data(command_data);
    last_command = std::chrono::high_resolution_clock::now().time_since_epoch().count();
    
    // Receive response
    std::vector<uint8_t> response = ws_recv_data();
    
    // Deserialize and return response data
    return deserialize_response(response, cmd);
}

// Game Status and Information
GameStatus GameClient::get_game_status() {
    try {
        std::vector<uint8_t> response = send_command(CommandType::GET_GAME_STATUS);
        if (response.empty()) {
            return GameStatus::PREPARING;
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        int status = variant->getValue<int>();
        return static_cast<GameStatus>(status);
    } catch (const std::exception& e) {
        std::cerr << "Error deserializing game status: " << e.what() << std::endl;
        return GameStatus::PREPARING;
    }
}

std::vector<std::vector<TerrainType>> GameClient::get_all_terrain() {
    try {
        std::vector<uint8_t> response = send_command(CommandType::GET_ALL_TERRAIN);
        if (response.empty()) {
            throw std::runtime_error("Failed to get terrain data: empty response");
        }

        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        
        // Expect an array of arrays
        auto *outer_array = dynamic_cast<const GodotArray*>(variant.get());
        if (!outer_array) {
            throw std::runtime_error("Invalid response format: expected array of arrays");
        }

        std::vector<std::vector<TerrainType>> terrain;
        terrain.reserve(outer_array->size());
        
        for (size_t row = 0; row < outer_array->size(); row++) {
            auto *inner_array = dynamic_cast<const GodotArray*>(&outer_array->at(row));
            if (!inner_array) {
                throw std::runtime_error("Invalid response format: expected array");
            }
            std::vector<TerrainType> row_data;
            row_data.reserve(inner_array->size());
            
            for (size_t col = 0; col < inner_array->size(); col++) {
                auto *terrain_int = dynamic_cast<const GodotInt*>(&inner_array->at(col));
                if (terrain_int) {
                    row_data.push_back(static_cast<TerrainType>(terrain_int->getValue()));
                } else {
                    throw std::runtime_error("Expected int for terrain type");
                }
            }
            terrain.push_back(std::move(row_data));
        }
        
        return terrain;
    } catch (const std::exception &e) {
        std::cerr << "Error retrieving terrain data: " << e.what() << std::endl;
        return std::vector<std::vector<TerrainType>>();
    }
}

TerrainType GameClient::get_terrain(const Vector2& position) {
    try {
        // Serialize position argument
        auto position_data = GodotSerializer::serialize(position);
        std::vector<uint8_t> response = send_command(CommandType::GET_TERRAIN, position_data);
        
        if (response.empty()) {
            return TerrainType::OUT_OF_BOUNDS;
        }
        
        size_t offset = 0;
        int terrain_value = GodotSerializer::deserialize_int(response, offset);
        return static_cast<TerrainType>(terrain_value);
    } catch (const std::exception&) {
        return TerrainType::OUT_OF_BOUNDS;
    }
}

int GameClient::get_scores(bool owned) {
    try {
        // Serialize owned parameter
        auto owned_data = GodotSerializer::serialize(owned);
        std::vector<uint8_t> response = send_command(CommandType::GET_SCORES, owned_data);
        
        if (response.empty()) {
            throw std::runtime_error("Failed to get scores: empty response");
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<int>();
    } catch (const std::exception &e) {
        std::cerr << "Error deserializing scores: " << e.what() << std::endl;
        return -1;
    }
}

int GameClient::get_current_wave() {
    try {
        std::vector<uint8_t> response = send_command(CommandType::GET_CURRENT_WAVE);
        if (response.empty()) {
            return 0;
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<int>();
    } catch (const std::exception&) {
        return 0;
    }
}

float GameClient::get_remain_time() {
    try {
        std::vector<uint8_t> response = send_command(CommandType::GET_REMAIN_TIME);
        if (response.empty()) {
            return 0.0f;
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<float>();
        
    } catch (const std::exception& e) {
        std::cerr << "Error deserializing remain time: " << e.what() << std::endl;
        return 0.0f;
    }
}

float GameClient::get_time_until_next_wave() {
    try {
        std::vector<uint8_t> response = send_command(CommandType::GET_TIME_UNTIL_NEXT_WAVE);
        if (response.empty()) {
            return 0.0f;
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<float>();
    } catch (const std::exception&) {
        return 0.0f;
    }
}

int GameClient::get_money(bool owned) {
    try {
        // Serialize owned parameter
        auto owned_data = GodotSerializer::serialize(owned);
        std::vector<uint8_t> response = send_command(CommandType::GET_MONEY, owned_data);
        
        if (response.empty()) {
            return 0;
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<int>();
    } catch (const std::exception&) {
        return 0;
    }
}

int GameClient::get_income(bool owned) {
    try {
        // Serialize owned parameter
        auto owned_data = GodotSerializer::serialize(owned);
        std::vector<uint8_t> response = send_command(CommandType::GET_INCOME, owned_data);
        
        if (response.empty()) {
            return 0;
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<int>();
    } catch (const std::exception&) {
        return 0;
    }
}

std::vector<Vector2> GameClient::get_system_path(bool flying) {
    try {
        // Serialize flying argument
        auto flying_data = GodotSerializer::serialize(flying);
        std::vector<uint8_t> response = send_command(CommandType::GET_SYSTEM_PATH, flying_data);
        
        if (response.empty()) {
            throw std::runtime_error("Failed to get system path: empty response");
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        
        // The response should be an array of Vector2 positions
        auto *array_ptr = dynamic_cast<const GodotArray*>(variant.get());
        if (!array_ptr) {
            throw std::runtime_error("Invalid response format: expected array of Vector2 positions");
        }
        
        std::vector<Vector2> path;
        path.reserve(array_ptr->size());
        
        for (size_t i = 0; i < array_ptr->size(); i++) {
            auto *vector_variant = dynamic_cast<const GodotVector2*>(&array_ptr->at(i));
            if (vector_variant) {
                path.push_back(vector_variant->getValue());
            } else {
                path.push_back(Vector2(0, 0));
            }
        }
        
        return path;
    } catch (const std::exception &e) {
        std::cerr << "Error retrieving system path: " << e.what() << std::endl;
        return std::vector<Vector2>();
    }
}

std::vector<Vector2> GameClient::get_opponent_path(bool flying) {
    try {
        // Serialize flying argument
        auto flying_data = GodotSerializer::serialize(flying);
        std::vector<uint8_t> response = send_command(CommandType::GET_OPPONENT_PATH, flying_data);
        
        if (response.empty()) {
            return std::vector<Vector2>();
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        
        // The response should be an array of Vector2 positions
        auto *array_ptr = dynamic_cast<const GodotArray*>(variant.get());
        if (!array_ptr) {
            return std::vector<Vector2>();
        }
        
        std::vector<Vector2> path;
        path.reserve(array_ptr->size());
        
        for (size_t i = 0; i < array_ptr->size(); i++) {
            auto *vector_variant = dynamic_cast<const GodotVector2*>(&array_ptr->at(i));
            if (vector_variant) {
                path.push_back(vector_variant->getValue());
            } else {
                path.push_back(Vector2(0, 0));
            }
        }
        
        return path;
    } catch (const std::exception&) {
        return std::vector<Vector2>();
    }
}

// Tower Management
void GameClient::place_tower(TowerType tower_type, const std::string& level, const Vector2& position) {
    try {
        // Serialize arguments
        auto tower_type_data = GodotSerializer::serialize(static_cast<int>(tower_type));
        auto level_data = GodotSerializer::serialize(level);
        auto position_data = GodotSerializer::serialize(position);
        
        std::vector<uint8_t> args;
        args.insert(args.end(), tower_type_data.begin(), tower_type_data.end());
        args.insert(args.end(), level_data.begin(), level_data.end());
        args.insert(args.end(), position_data.begin(), position_data.end());
        
        send_command(CommandType::PLACE_TOWER, args);
    } catch (const std::exception&) {
        // Tower placement failed - exception already thrown by send_command
    }
}

std::vector<Tower> GameClient::get_all_towers(bool owned) {
    try {
        // Serialize owned parameter
        auto owned_data = GodotSerializer::serialize(owned);
        std::vector<uint8_t> response = send_command(CommandType::GET_ALL_TOWERS, owned_data);
        
        if (response.empty()) {
            throw std::runtime_error("Failed to get towers: empty response");
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        
        // The response should be an array of tower objects
        auto *array_ptr = dynamic_cast<const GodotArray*>(variant.get());
        if (!array_ptr) {
            throw std::runtime_error("Invalid response format: expected array of towers");
        }
        
        std::vector<Tower> towers;
        towers.reserve(array_ptr->size());
        
        for (size_t i = 0; i < array_ptr->size(); i++) {
            // Each tower should be a dictionary/object with fields
            auto* tower_dict_ptr = dynamic_cast<const GodotDictionary*>(&array_ptr->at(i));
            if (tower_dict_ptr) {
                towers.push_back(parse_tower_from_dictionary(tower_dict_ptr));
            } else {
                throw std::runtime_error("Invalid tower format in response");
            }
        }
        
        return towers;
    } catch (const std::exception &e) {
        std::cerr << "Error retrieving towers: " << e.what() << std::endl;
        return std::vector<Tower>();
    }
}

Tower GameClient::parse_tower_from_dictionary(const GodotDictionary* tower_dict_ptr) {
    if (!tower_dict_ptr) {
        throw std::runtime_error("Error: tower dictionary is null");
    }
    
    const auto& tower_dict_raw = tower_dict_ptr->getValue();
    std::map<std::string, const GodotVariant*> tower_dict;
    for (const auto &[key, val] : tower_dict_raw) {
        tower_dict[key->getValue<std::string>()] = val.get();
    }
    
    try {
        // Extract Tower fields from dictionary - all fields are required
        if (tower_dict.find("type") == tower_dict.end()) {
            throw std::runtime_error("Missing required field 'type' in tower dictionary");
        }
        
        // Extract type - try int first, then float
        auto* type_variant = tower_dict.at("type");
        TowerType type;
        try {
            type = static_cast<TowerType>(type_variant->getValue<int>());
        } catch (const std::exception&) {
            try {
                // Server might send as float, convert to int
                type = static_cast<TowerType>(static_cast<int>(type_variant->getValue<float>()));
            } catch (const std::exception& e) {
                throw std::runtime_error("Field 'type' cannot be converted to int or float: " + std::string(e.what()));
            }
        }
        
        // Extract position (should be a dictionary with x, y)
        if (tower_dict.find("position") == tower_dict.end()) {
            throw std::runtime_error("Missing required field 'position' in tower dictionary");
        }
        auto* pos_dict_ptr = dynamic_cast<const GodotDictionary*>(tower_dict.at("position"));
        if (!pos_dict_ptr) {
            throw std::runtime_error("Field 'position' is not a dictionary");
        }
        
        const auto& pos_dict_raw = pos_dict_ptr->getValue();
        std::map<std::string, const GodotVariant*> pos_dict;
        for (const auto &[key, val] : pos_dict_raw) {
            pos_dict[key->getValue<std::string>()] = val.get();
        }
        
        if (pos_dict.find("x") == pos_dict.end() || pos_dict.find("y") == pos_dict.end()) {
            throw std::runtime_error("Missing x or y coordinates in position dictionary");
        }
        
        // Helper lambda to get int value that might be stored as float
        auto getIntValue = [](const GodotVariant* variant) -> int {
            try {
                return variant->getValue<int>();
            } catch (const std::exception&) {
                return static_cast<int>(variant->getValue<float>());
            }
        };
        
        Vector2 position(0, 0);
        try {
            position = Vector2(getIntValue(pos_dict.at("x")), getIntValue(pos_dict.at("y")));
        } catch (const std::exception& e) {
            throw std::runtime_error("Position coordinates cannot be converted to int: " + std::string(e.what()));
        }
        
        // Extract other required fields with flexible type handling
        if (tower_dict.find("level_a") == tower_dict.end()) {
            throw std::runtime_error("Missing required field 'level_a' in tower dictionary");
        }
        int level_a;
        try {
            level_a = getIntValue(tower_dict.at("level_a"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'level_a' cannot be converted to int: " + std::string(e.what()));
        }
        
        if (tower_dict.find("level_b") == tower_dict.end()) {
            throw std::runtime_error("Missing required field 'level_b' in tower dictionary");
        }
        int level_b;
        try {
            level_b = getIntValue(tower_dict.at("level_b"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'level_b' cannot be converted to int: " + std::string(e.what()));
        }
        
        if (tower_dict.find("aim") == tower_dict.end()) {
            throw std::runtime_error("Missing required field 'aim' in tower dictionary");
        }
        bool aim;
        try {
            aim = tower_dict.at("aim")->getValue<bool>();
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'aim' cannot be converted to bool: " + std::string(e.what()));
        }
        
        if (tower_dict.find("anti_air") == tower_dict.end()) {
            throw std::runtime_error("Missing required field 'anti_air' in tower dictionary");
        }
        bool anti_air;
        try {
            anti_air = tower_dict.at("anti_air")->getValue<bool>();
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'anti_air' cannot be converted to bool: " + std::string(e.what()));
        }
        
        if (tower_dict.find("reload") == tower_dict.end()) {
            throw std::runtime_error("Missing required field 'reload' in tower dictionary");
        }
        int reload;
        try {
            reload = getIntValue(tower_dict.at("reload"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'reload' cannot be converted to int: " + std::string(e.what()));
        }
        
        if (tower_dict.find("range") == tower_dict.end()) {
            throw std::runtime_error("Missing required field 'range' in tower dictionary");
        }
        int range;
        try {
            range = getIntValue(tower_dict.at("range"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'range' cannot be converted to int: " + std::string(e.what()));
        }
        
        if (tower_dict.find("damage") == tower_dict.end()) {
            throw std::runtime_error("Missing required field 'damage' in tower dictionary");
        }
        int damage;
        try {
            damage = getIntValue(tower_dict.at("damage"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'damage' cannot be converted to int: " + std::string(e.what()));
        }
        
        if (tower_dict.find("bullet_effect") == tower_dict.end()) {
            throw std::runtime_error("Missing required field 'bullet_effect' in tower dictionary");
        }
        std::string bullet_effect;
        try {
            bullet_effect = tower_dict.at("bullet_effect")->getValue<std::string>();
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'bullet_effect' cannot be converted to string: " + std::string(e.what()));
        }
        
        return Tower(type, position, level_a, level_b, aim, anti_air, reload, range, damage, bullet_effect);
    } catch (const std::exception& e) {
        std::cerr << "Error parsing tower from dictionary: " << e.what() << std::endl;
        throw; // Re-throw the original exception with proper error details
    }
}

Enemy GameClient::parse_enemy_from_dictionary(const GodotDictionary* enemy_dict_ptr) {
    if (!enemy_dict_ptr) {
        throw std::runtime_error("Error: enemy dictionary is null");
    }
    
    const auto& enemy_dict_raw = enemy_dict_ptr->getValue();
    std::map<std::string, const GodotVariant*> enemy_dict;
    for (const auto &[key, val] : enemy_dict_raw) {
        enemy_dict[key->getValue<std::string>()] = val.get();
    }
    
    try {
        // Helper lambda to get int value that might be stored as float
        auto getIntValue = [](const GodotVariant* variant) -> int {
            try {
                return variant->getValue<int>();
            } catch (const std::exception&) {
                return static_cast<int>(variant->getValue<float>());
            }
        };
        
        // Helper lambda to get double value that might be stored as float
        auto getDoubleValue = [](const GodotVariant* variant) -> double {
            try {
                return variant->getValue<double>();
            } catch (const std::exception&) {
                return static_cast<double>(variant->getValue<float>());
            }
        };
        
        // Extract Enemy fields from dictionary - all fields are required
        if (enemy_dict.find("type") == enemy_dict.end()) {
            throw std::runtime_error("Missing required field 'type' in enemy dictionary");
        }
        EnemyType type;
        try {
            type = static_cast<EnemyType>(getIntValue(enemy_dict.at("type")));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'type' cannot be converted to int: " + std::string(e.what()));
        }
        
        // Extract position (should be a dictionary with x, y)
        if (enemy_dict.find("position") == enemy_dict.end()) {
            throw std::runtime_error("Missing required field 'position' in enemy dictionary");
        }
        auto* pos_dict_ptr = dynamic_cast<const GodotDictionary*>(enemy_dict.at("position"));
        if (!pos_dict_ptr) {
            throw std::runtime_error("Field 'position' is not a dictionary");
        }
        
        const auto& pos_dict_raw = pos_dict_ptr->getValue();
        std::map<std::string, const GodotVariant*> pos_dict;
        for (const auto &[key, val] : pos_dict_raw) {
            pos_dict[key->getValue<std::string>()] = val.get();
        }
        
        if (pos_dict.find("x") == pos_dict.end() || pos_dict.find("y") == pos_dict.end()) {
            throw std::runtime_error("Missing x or y coordinates in position dictionary");
        }
        Vector2 position(0, 0);
        try {
            position = Vector2(getIntValue(pos_dict.at("x")), getIntValue(pos_dict.at("y")));
        } catch (const std::exception& e) {
            throw std::runtime_error("Position coordinates cannot be converted to int: " + std::string(e.what()));
        }
        
        // Extract other required fields with flexible type handling
        if (enemy_dict.find("health") == enemy_dict.end()) {
            throw std::runtime_error("Missing required field 'health' in enemy dictionary");
        }
        int health;
        try {
            health = getIntValue(enemy_dict.at("health"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'health' cannot be converted to int: " + std::string(e.what()));
        }
        
        if (enemy_dict.find("max_health") == enemy_dict.end()) {
            throw std::runtime_error("Missing required field 'max_health' in enemy dictionary");
        }
        int max_health;
        try {
            max_health = getIntValue(enemy_dict.at("max_health"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'max_health' cannot be converted to int: " + std::string(e.what()));
        }
        
        if (enemy_dict.find("flying") == enemy_dict.end()) {
            throw std::runtime_error("Missing required field 'flying' in enemy dictionary");
        }
        bool flying;
        try {
            flying = enemy_dict.at("flying")->getValue<bool>();
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'flying' cannot be converted to bool: " + std::string(e.what()));
        }
        
        if (enemy_dict.find("knockback_resist") == enemy_dict.end()) {
            throw std::runtime_error("Missing required field 'knockback_resist' in enemy dictionary");
        }
        double knockback_resist;
        try {
            // Try to get as double first, fallback to bool conversion
            try {
                knockback_resist = getDoubleValue(enemy_dict.at("knockback_resist"));
            } catch (const std::exception&) {
                // If it fails, try as bool and convert to double
                bool knockback_resist_bool = enemy_dict.at("knockback_resist")->getValue<bool>();
                knockback_resist = knockback_resist_bool ? 1.0 : 0.0;
            }
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'knockback_resist' cannot be converted to double or bool: " + std::string(e.what()));
        }
        
        // Extract fields that match the Python API structure
        if (enemy_dict.find("progress_ratio") == enemy_dict.end()) {
            throw std::runtime_error("Missing required field 'progress_ratio' in enemy dictionary");
        }
        double progress_ratio;
        try {
            progress_ratio = getDoubleValue(enemy_dict.at("progress_ratio"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'progress_ratio' cannot be converted to double: " + std::string(e.what()));
        }
        
        if (enemy_dict.find("income_impact") == enemy_dict.end()) {
            throw std::runtime_error("Missing required field 'income_impact' in enemy dictionary");
        }
        int income_impact;
        try {
            income_impact = getIntValue(enemy_dict.at("income_impact"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'income_impact' cannot be converted to int: " + std::string(e.what()));
        }
        
        if (enemy_dict.find("damage") == enemy_dict.end()) {
            throw std::runtime_error("Missing required field 'damage' in enemy dictionary");
        }
        int damage;
        try {
            damage = getIntValue(enemy_dict.at("damage"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'damage' cannot be converted to int: " + std::string(e.what()));
        }
        
        if (enemy_dict.find("max_speed") == enemy_dict.end()) {
            throw std::runtime_error("Missing required field 'max_speed' in enemy dictionary");
        }
        int max_speed;
        try {
            max_speed = getIntValue(enemy_dict.at("max_speed"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'max_speed' cannot be converted to int: " + std::string(e.what()));
        }
        
        if (enemy_dict.find("kill_reward") == enemy_dict.end()) {
            throw std::runtime_error("Missing required field 'kill_reward' in enemy dictionary");
        }
        int kill_reward;
        try {
            kill_reward = getIntValue(enemy_dict.at("kill_reward"));
        } catch (const std::exception& e) {
            throw std::runtime_error("Field 'kill_reward' cannot be converted to int: " + std::string(e.what()));
        }
        
        // Use the constructor that matches Python API fields
        return Enemy(type, position, progress_ratio, income_impact, health, max_health, damage, max_speed, flying, knockback_resist, kill_reward);
    } catch (const std::exception& e) {
        std::cerr << "Error parsing enemy from dictionary: " << e.what() << std::endl;
        throw; // Re-throw the original exception with proper error details
    }
}

Tower GameClient::get_tower(bool owned, const Vector2& position) {
    try {
        // Serialize arguments
        auto owned_data = GodotSerializer::serialize(owned);
        auto position_data = GodotSerializer::serialize(position);
        
        std::vector<uint8_t> args;
        args.insert(args.end(), owned_data.begin(), owned_data.end());
        args.insert(args.end(), position_data.begin(), position_data.end());
        
        std::vector<uint8_t> response = send_command(CommandType::GET_TOWER, args);
        
        if (response.empty()) {
            throw std::runtime_error("Error: no response");
        }
        
        size_t offset = 0;
        auto tower_var = GodotVariant::deserialize(response, offset);
        auto tower_dict_ptr = dynamic_cast<const GodotDictionary*>(tower_var.get());
        if (!tower_dict_ptr) {
            throw std::runtime_error("Error: not a dictionary");
        }
        
        return parse_tower_from_dictionary(tower_dict_ptr);
    } catch (const std::exception&) {
        return Tower();
    }
}

void GameClient::sell_tower(const Vector2& position) {
    try {
        // Serialize position argument
        auto position_data = GodotSerializer::serialize(position);
        send_command(CommandType::SELL_TOWER, position_data);
    } catch (const std::exception&) {
        // Sell tower failed - exception already thrown by send_command
    }
}

void GameClient::set_strategy(const Vector2& position, TargetStrategy strategy) {
    try {
        // Serialize arguments
        auto position_data = GodotSerializer::serialize(position);
        auto strategy_data = GodotSerializer::serialize(static_cast<int>(strategy));
        
        std::vector<uint8_t> args;
        args.insert(args.end(), position_data.begin(), position_data.end());
        args.insert(args.end(), strategy_data.begin(), strategy_data.end());
        
        send_command(CommandType::SET_STRATEGY, args);
    } catch (const std::exception&) {
        // Set strategy failed - exception already thrown by send_command
    }
}

// Enemy and Unit Management
void GameClient::spawn_unit(EnemyType enemy_type) {
    try {
        // Serialize enemy type argument
        auto enemy_type_data = GodotSerializer::serialize(static_cast<int>(enemy_type));
        send_command(CommandType::SPAWN_UNIT, enemy_type_data);
    } catch (const std::exception&) {
        // Spawn unit failed - exception already thrown by send_command
    }
}

float GameClient::get_unit_cooldown(EnemyType enemy_type) {
    try {
        // Serialize enemy type argument
        auto enemy_type_data = GodotSerializer::serialize(static_cast<int>(enemy_type));
        std::vector<uint8_t> response = send_command(CommandType::GET_UNIT_COOLDOWN, enemy_type_data);
        
        if (response.empty()) {
            return 0.0f;
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<float>();
    } catch (const std::exception&) {
        return 0.0f;
    }
}

std::vector<Enemy> GameClient::get_all_enemies(bool owned) {
    try {
        // Serialize owned parameter
        auto owned_data = GodotSerializer::serialize(owned);
        std::vector<uint8_t> response = send_command(CommandType::GET_ALL_ENEMIES, owned_data);

        if (response.empty()) {
            return std::vector<Enemy>();
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        
        // The response should be an array of enemy objects
        auto *array_ptr = dynamic_cast<const GodotArray*>(variant.get());
        if (!array_ptr) {
            return std::vector<Enemy>();
        }
        
        std::vector<Enemy> enemies;
        enemies.reserve(array_ptr->size());
        
        for (size_t i = 0; i < array_ptr->size(); i++) {
            // Each enemy should be a dictionary/object with fields
            auto* enemy_dict_ptr = dynamic_cast<const GodotDictionary*>(&array_ptr->at(i));
            if (enemy_dict_ptr) {
                enemies.push_back(parse_enemy_from_dictionary(enemy_dict_ptr));
            } else {
                throw std::runtime_error("Invalid enemy format in response");
            }
        }
        return enemies;
    } catch (const std::exception& e) {
        std::cerr << "DEBUG: Exception in get_all_enemies: " << e.what() << std::endl;
        return std::vector<Enemy>();
    }
}

// Spell System
void GameClient::cast_spell(SpellType spell_type, const Vector2& position) {
    try {
        // Serialize arguments
        auto spell_type_data = GodotSerializer::serialize(static_cast<int>(spell_type));
        auto position_data = GodotSerializer::serialize(position);
        
        std::vector<uint8_t> args;
        args.insert(args.end(), spell_type_data.begin(), spell_type_data.end());
        args.insert(args.end(), position_data.begin(), position_data.end());
        
        send_command(CommandType::CAST_SPELL, args);
    } catch (const std::exception&) {
        // Cast spell failed - exception already thrown by send_command
    }
}

float GameClient::get_spell_cooldown(bool owned, SpellType spell_type) {
    try {
        // Serialize arguments
        auto owned_data = GodotSerializer::serialize(owned);
        auto spell_type_data = GodotSerializer::serialize(static_cast<int>(spell_type));
        
        std::vector<uint8_t> args;
        args.insert(args.end(), owned_data.begin(), owned_data.end());
        args.insert(args.end(), spell_type_data.begin(), spell_type_data.end());
        
        std::vector<uint8_t> response = send_command(CommandType::GET_SPELL_COOLDOWN, args);
        
        if (response.empty()) {
            return 0.0f;
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<float>();
    } catch (const std::exception&) {
        return 0.0f;
    }
}

// Chat System
void GameClient::send_chat(const std::string& message) {
    try {
        auto message_data = GodotSerializer::serialize(message);
        send_command(CommandType::SEND_CHAT, message_data);
    } catch (const std::exception&) {
        // Chat send failed
    }
}

std::vector<ChatMessage> GameClient::get_chat_history(int num) {
    try {
        // Serialize num parameter
        auto num_data = GodotSerializer::serialize(num);
        std::vector<uint8_t> response = send_command(CommandType::GET_CHAT_HISTORY, num_data);
        
        if (response.empty()) {
            return std::vector<ChatMessage>();
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        
        // The response should be an array of chat message objects
        auto *array_ptr = dynamic_cast<const GodotArray*>(variant.get());
        if (!array_ptr) {
            return std::vector<ChatMessage>();
        }
        
        std::vector<ChatMessage> messages;
        messages.reserve(array_ptr->size());
        
        for (size_t i = 0; i < array_ptr->size(); i++) {
            // Each message should be a dictionary/object with fields
            // For now, return basic chat messages - proper dictionary parsing would be needed for full implementation
            messages.push_back(ChatMessage());
        }
        
        return messages;
    } catch (const std::exception&) {
        return std::vector<ChatMessage>();
    }
}

void GameClient::set_chat_name_color(const std::string& color) {
    try {
        auto color_data = GodotSerializer::serialize(color);
        send_command(CommandType::SET_CHAT_NAME_COLOR, color_data);
    } catch (const std::exception&) {
        // Set color failed
    }
}

void GameClient::set_name(const std::string& name) {
    try {
        auto name_data = GodotSerializer::serialize(name);
        send_command(CommandType::SET_NAME, name_data);
    } catch (const std::exception&) {
        // Set name failed
    }
}

// Special Commands
void GameClient::disconnect() {
    wait_for_next_command();
    
    if (connected && socket_fd >= 0) {
        connected = false;
        close(socket_fd);
        socket_fd = -1;
    }
}

std::vector<std::string> GameClient::get_devs() {
    try {
        std::vector<uint8_t> response = send_command(CommandType::GET_DEVS);
        if (response.empty()) {
            return std::vector<std::string>();
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        
        // The response should be an array of strings
        auto *array_ptr = dynamic_cast<const GodotArray*>(variant.get());
        if (!array_ptr) {
            return std::vector<std::string>();
        }
        
        std::vector<std::string> devs;
        devs.reserve(array_ptr->size());
        
        for (size_t i = 0; i < array_ptr->size(); i++) {
            const auto& element = array_ptr->at(i);
            if (auto *str_ptr = dynamic_cast<const GodotString*>(&element)) {
                devs.push_back(str_ptr->getValue());
            } else {
                devs.push_back(""); // Default empty string on error
            }
        }
        
        return devs;
    } catch (const std::exception&) {
        return std::vector<std::string>();
    }
}

// Easter Egg Commands
std::string GameClient::pixelcat() {
    try {
        std::vector<uint8_t> response = send_command(CommandType::PIXELCAT);
        if (response.empty()) {
            return "";
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<std::string>();
    } catch (const std::exception&) {
        return "";
    }
}

std::string GameClient::ntu_student_id_card() {
    try {
        std::vector<uint8_t> response = send_command(CommandType::NTU_STUDENT_ID_CARD);
        if (response.empty()) {
            return "";
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<std::string>();
    } catch (const std::exception&) {
        return "";
    }
}

void GameClient::metal_pipe() {
    try {
        send_command(CommandType::METAL_PIPE);
    } catch (const std::exception&) {
        // Metal pipe failed
    }
}

void GameClient::spam(const std::string& message, int size, const std::string& color) {
    try {
        // Serialize arguments
        auto message_data = GodotSerializer::serialize(message);
        auto size_data = GodotSerializer::serialize(size);
        auto color_data = GodotSerializer::serialize(color);
        
        std::vector<uint8_t> args;
        args.insert(args.end(), message_data.begin(), message_data.end());
        args.insert(args.end(), size_data.begin(), size_data.end());
        args.insert(args.end(), color_data.begin(), color_data.end());
        
        send_command(CommandType::SPAM, args);
    } catch (const std::exception&) {
        // Spam failed
    }
}

void GameClient::super_star() {
    try {
        send_command(CommandType::SUPER_STAR);
    } catch (const std::exception&) {
        // Super star failed
    }
}

void GameClient::turbo_on() {
    try {
        send_command(CommandType::TURBO_ON);
    } catch (const std::exception&) {
        // Turbo on failed
    }
}

int GameClient::get_the_radiant_core_of_stellar_faith() {
    try {
        std::vector<uint8_t> response = send_command(CommandType::GET_THE_RADIANT_CORE_OF_STELLAR_FAITH);
        if (response.empty()) {
            return -1;
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<int>();
    } catch (const std::exception&) {
        return -1;
    }
}

void GameClient::set_the_radiant_core_of_stellar_faith(int value) {
    try {
        auto value_data = GodotSerializer::serialize(value);
        send_command(CommandType::SET_THE_RADIANT_CORE_OF_STELLAR_FAITH, value_data);
    } catch (const std::exception&) {
        // Set radiant core failed
    }
}

bool GameClient::boo() {
    try {
        std::vector<uint8_t> response = send_command(CommandType::BOO);
        if (response.empty()) {
            return false;
        }
        
        size_t offset = 0;
        auto variant = GodotVariant::deserialize(response, offset);
        return variant->getValue<bool>();
    } catch (const std::exception&) {
        return false;
    }
}

// WebSocket helper methods
std::string GameClient::create_websocket_handshake() {
    std::string handshake = 
        "GET / HTTP/1.1\r\n"
        "Host: " + server_domain + ":" + std::to_string(port) + "\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "\r\n";
    return handshake;
}

bool GameClient::validate_websocket_response(const std::string& response) {
    return response.find("101 Switching Protocols") != std::string::npos &&
           response.find("Upgrade: websocket") != std::string::npos;
}

void GameClient::send_websocket_frame(const std::vector<uint8_t>& payload) {
    if (!connected || socket_fd < 0) {
        throw std::runtime_error("Not connected to server");
    }
    
    std::vector<uint8_t> frame;
    
    // WebSocket frame format: FIN=1, opcode=2 (binary), mask=1
    frame.push_back(0x82); // FIN + binary opcode
    
    uint64_t payload_len = payload.size();
    if (payload_len < 126) {
        frame.push_back(0x80 | payload_len); // Mask bit + length
    } else if (payload_len < 65536) {
        frame.push_back(0x80 | 126); // Mask bit + extended length indicator
        frame.push_back((payload_len >> 8) & 0xFF);
        frame.push_back(payload_len & 0xFF);
    } else {
        frame.push_back(0x80 | 127); // Mask bit + extended length indicator
        for (int i = 7; i >= 0; i--) {
            frame.push_back((payload_len >> (i * 8)) & 0xFF);
        }
    }
    
    // Add masking key (simple static key for now)
    uint8_t mask[4] = {0x12, 0x34, 0x56, 0x78};
    frame.insert(frame.end(), mask, mask + 4);
    
    // Add masked payload
    for (size_t i = 0; i < payload.size(); i++) {
        frame.push_back(payload[i] ^ mask[i % 4]);
    }
    
    if (send(socket_fd, frame.data(), frame.size(), 0) < 0) {
        throw std::runtime_error("Failed to send WebSocket frame");
    }
}

void GameClient::send_websocket_text_frame(const std::string& text) {
    if (!connected || socket_fd < 0) {
        throw std::runtime_error("Not connected to server");
    }
    
    std::vector<uint8_t> frame;
    
    // WebSocket frame format: FIN=1, opcode=1 (text), mask=1
    frame.push_back(0x81); // FIN + text opcode
    
    uint64_t payload_len = text.size();
    if (payload_len < 126) {
        frame.push_back(0x80 | payload_len); // Mask bit + length
    } else if (payload_len < 65536) {
        frame.push_back(0x80 | 126); // Mask bit + extended length indicator
        frame.push_back((payload_len >> 8) & 0xFF);
        frame.push_back(payload_len & 0xFF);
    } else {
        frame.push_back(0x80 | 127); // Mask bit + extended length indicator
        for (int i = 7; i >= 0; i--) {
            frame.push_back((payload_len >> (i * 8)) & 0xFF);
        }
    }
    
    // Add masking key (simple static key for now)
    uint8_t mask[4] = {0x12, 0x34, 0x56, 0x78};
    frame.insert(frame.end(), mask, mask + 4);
    
    // Add masked payload
    for (size_t i = 0; i < text.size(); i++) {
        frame.push_back(text[i] ^ mask[i % 4]);
    }
    
    if (send(socket_fd, frame.data(), frame.size(), 0) < 0) {
        throw std::runtime_error("Failed to send WebSocket text frame");
    }
}

std::vector<uint8_t> GameClient::receive_websocket_frame() {
    if (!connected || socket_fd < 0) {
        throw std::runtime_error("Not connected to server");
    }
    
    // Helper function to receive exact number of bytes with retry logic
    auto recv_exact = [this](void* buffer, size_t len) -> bool {
        char* buf = static_cast<char*>(buffer);
        size_t total_received = 0;
        
        while (total_received < len) {
            ssize_t received = recv(socket_fd, buf + total_received, len - total_received, 0);
            
            if (received > 0) {
                total_received += received;
            } else if (received == 0) {
                throw std::runtime_error("Server closed connection");
            } else {
                // Check for temporary errors that we can retry
                if (errno == EINTR || errno == EAGAIN || errno == EWOULDBLOCK) {
                    // Temporary error, continue trying
                    std::this_thread::sleep_for(std::chrono::milliseconds(1));
                    continue;
                } else {
                    throw std::runtime_error("Network error during receive: " + std::string(strerror(errno)));
                }
            }
        }
        return true;
    };
    
    try {
        // Set socket timeout to prevent hanging
        struct timeval timeout;
        timeout.tv_sec = 10; // Increased timeout
        timeout.tv_usec = 0;
        
        if (setsockopt(socket_fd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout)) < 0) {
            std::cerr << "Warning: Could not set socket timeout" << std::endl;
        }
        
        // Read WebSocket frame header (2 bytes minimum)
        char header[2];
        recv_exact(header, 2);
        
        // Parse WebSocket frame header
        bool fin __attribute__((unused)) = (header[0] & 0x80) != 0;
        uint8_t opcode __attribute__((unused)) = header[0] & 0x0F;
        bool masked = (header[1] & 0x80) != 0;
        uint64_t payload_len = header[1] & 0x7F;
        
        // Handle extended payload length
        if (payload_len == 126) {
            uint8_t len_bytes[2];
            recv_exact(len_bytes, 2);
            payload_len = (static_cast<uint16_t>(len_bytes[0]) << 8) | 
                          static_cast<uint16_t>(len_bytes[1]);
        } else if (payload_len == 127) {
            uint8_t len_bytes[8];
            recv_exact(len_bytes, 8);
            payload_len = 0;
            for (int i = 0; i < 8; i++) {
                payload_len = (payload_len << 8) | static_cast<uint64_t>(len_bytes[i]);
            }
        }
        
        // Sanity check on payload length
        if (payload_len > 10 * 1024 * 1024) { // 10MB limit
            throw std::runtime_error("Payload too large: " + std::to_string(payload_len) + " bytes");
        }
        
        // Read masking key if present
        uint8_t mask[4] = {0};
        if (masked) {
            recv_exact(mask, 4);
        }
        
        // Read payload
        std::vector<uint8_t> payload(payload_len);
        if (payload_len > 0) {
            recv_exact(payload.data(), payload_len);
            
            // Unmask payload if needed
            if (masked) {
                for (size_t i = 0; i < payload_len; i++) {
                    payload[i] ^= mask[i % 4];
                }
            }
        }
        
        return payload;
        
    } catch (const std::runtime_error& e) {
        std::cerr << "WebSocket receive error: " << e.what() << std::endl;
        throw;
    }
}

}

