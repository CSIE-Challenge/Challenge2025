#pragma once

#include <utility>
#include <string>
#include <unordered_map>

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

const std::unordered_map<int, std::string> StatusCodeToString = {
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

} // namespace GameAPI
