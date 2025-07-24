#pragma once
#include <string>
#include "constants.h"

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

} // namespace GameAPI
