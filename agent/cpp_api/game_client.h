#pragma once
#include <vector>
#include <string>
#include <memory>
#include <functional>
#include "constants.h"
#include "structures.h"

namespace GameAPI {
class GodotDictionary;

/**
 * @brief WebSocket-based game client for interacting with the game server
 */
class GameClient {
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

    // Easter Egg Commands (implement as needed)
    std::string pixelcat();
    std::string ntu_student_id_card();
    void metal_pipe();
    void spam(const std::string& message, int size = 48, const std::string& color = "#ffffff");
    void super_star();
    void turbo_on();
    int get_the_radiant_core_of_stellar_faith();
    void set_the_radiant_core_of_stellar_faith(int value);
    bool boo();
};

} // namespace GameAPI
