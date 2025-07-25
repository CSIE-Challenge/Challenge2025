#include "api.hpp"
#include <iostream>
#include <thread>
#include <chrono>

using namespace GameAPI;

int main() {
    try {
        std::cout << "=== C++ Game API Comprehensive Test ===" << std::endl;
        
        // Create game client with your token
        GameClient client(7749, "50ef3715"); // Replace with your actual token
        
        std::cout << "\n--- Connection & Authentication ---" << std::endl;
        std::cout << "[Example] Connected to game server successfully!" << std::endl;
        
        // Wait for game to start
        std::cout << "\n--- Game Status ---" << std::endl;
        std::cout << "Waiting for game to start..." << std::endl;
        while (client.get_game_status() != GameStatus::RUNNING) {
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
        std::cout << "[Example] Game is now RUNNING!" << std::endl;
        
        // Test basic info APIs
        std::cout << "\n--- Game Information APIs ---" << std::endl;
        int current_wave = client.get_current_wave();
        float remain_time = client.get_remain_time();
        float time_to_next_wave = client.get_time_until_next_wave();
        
        std::cout << "Current wave: " << current_wave << std::endl;
        std::cout << "Remaining time: " << remain_time << "s" << std::endl;
        std::cout << "Time until next wave: " << time_to_next_wave << "s" << std::endl;
        
        // Test terrain APIs
        std::cout << "\n--- Terrain APIs ---" << std::endl;
        auto terrain = client.get_all_terrain();
        std::cout << "Map size: " << terrain.size() << "x" << (terrain.empty() ? 0 : terrain[0].size()) << std::endl;
        
        // Test specific terrain position
        Vector2 test_pos(5, 5);
        TerrainType terrain_type = client.get_terrain(test_pos);
        std::cout << "Terrain at (5,5): " << static_cast<int>(terrain_type) << std::endl;
        
        // Test money and income APIs
        std::cout << "\n--- Economy APIs ---" << std::endl;
        int my_money = client.get_money(true);
        int opp_money = client.get_money(false);
        int my_income = client.get_income(true);
        int opp_income = client.get_income(false);
        
        std::cout << "My money: " << my_money << " | Opponent money: " << opp_money << std::endl;
        std::cout << "My income: " << my_income << " | Opponent income: " << opp_income << std::endl;
        
        // Test score APIs
        int my_score = client.get_scores(true);
        int opp_score = client.get_scores(false);
        std::cout << "My score: " << my_score << " | Opponent score: " << opp_score << std::endl;
        
        // Test path APIs
        std::cout << "\n--- Path APIs ---" << std::endl;
        auto my_path = client.get_system_path(false);  // Ground path
        auto my_air_path = client.get_system_path(true);   // Air path
        auto opp_path = client.get_opponent_path(false);
        auto opp_air_path = client.get_opponent_path(true);
        
        std::cout << "System ground path length: " << my_path.size() << std::endl;
        std::cout << "System air path length: " << my_air_path.size() << std::endl;
        std::cout << "Opponent ground path length: " << opp_path.size() << std::endl;
        std::cout << "Opponent air path length: " << opp_air_path.size() << std::endl;
        
        // Test tower APIs
        std::cout << "\n--- Tower APIs ---" << std::endl;
        auto my_towers = client.get_all_towers(true);
        auto opp_towers = client.get_all_towers(false);
        std::cout << "My towers: " << my_towers.size() << " | Opponent towers: " << opp_towers.size() << std::endl;
        
        // Test tower placement if we have money
        if (my_money >= 100) {
            try {
                Vector2 tower_pos(6, 6);
                client.place_tower(TowerType::FIRE_MARIO, "1", tower_pos);
                std::cout << "[Example] Successfully placed tower at (6,6)" << std::endl;
                
                // Test getting specific tower info
                Tower placed_tower = client.get_tower(true, tower_pos);
                std::cout << "Placed tower level: " << placed_tower.level_a << "/" << placed_tower.level_b << std::endl;
                
                // Test tower strategy setting
                client.set_strategy(tower_pos, TargetStrategy::FIRST);
                std::cout << "[Example] Set tower strategy to FIRST" << std::endl;
                
            } catch (const ApiException& e) {
                std::cout << "✗ Tower placement failed: " << e.what() << std::endl;
            }
        } else {
            std::cout << "Skipping tower placement (insufficient money: " << my_money << ")" << std::endl;
        }
        
        // Test enemy APIs
        std::cout << "\n--- Enemy APIs ---" << std::endl;
        auto my_enemies = client.get_all_enemies(true);
        auto opp_enemies = client.get_all_enemies(false);
        std::cout << "My enemies: " << my_enemies.size() << " | Opponent enemies: " << opp_enemies.size() << std::endl;
        
        // Print first enemy details if any exist
        if (!my_enemies.empty()) {
            const Enemy& enemy = my_enemies[0];
            std::cout << "First enemy - Type: " << static_cast<int>(enemy.type) 
                      << ", Health: " << enemy.health << "/" << enemy.max_health 
                      << ", Position: (" << enemy.position.x << "," << enemy.position.y << ")" << std::endl;
        }
        
        // Test unit spawning and cooldowns
        std::cout << "\n--- Unit Management APIs ---" << std::endl;
        float koopa_cooldown = client.get_unit_cooldown(EnemyType::KOOPA);
        float goomba_cooldown = client.get_unit_cooldown(EnemyType::GOOMBA);
        std::cout << "KOOPA cooldown: " << koopa_cooldown << "s" << std::endl;
        std::cout << "GOOMBA cooldown: " << goomba_cooldown << "s" << std::endl;
        
        // Try spawning a unit if cooldown allows
        if (koopa_cooldown <= 0.1f) {
            try {
                client.spawn_unit(EnemyType::KOOPA);
                std::cout << "[Example] Successfully spawned KOOPA" << std::endl;
            } catch (const ApiException& e) {
                std::cout << "✗ KOOPA spawn failed: " << e.what() << std::endl;
            }
        } else {
            std::cout << "Skipping KOOPA spawn (cooldown: " << koopa_cooldown << "s)" << std::endl;
        }
        
        // Test spell APIs
        std::cout << "\n--- Spell APIs ---" << std::endl;
        float poison_cd = client.get_spell_cooldown(true, SpellType::POISON);
        float double_income_cd = client.get_spell_cooldown(true, SpellType::DOUBLE_INCOME);
        float teleport_cd = client.get_spell_cooldown(true, SpellType::TELEPORT);
        
        std::cout << "POISON cooldown: " << poison_cd << "s" << std::endl;
        std::cout << "DOUBLE_INCOME cooldown: " << double_income_cd << "s" << std::endl;
        std::cout << "TELEPORT cooldown: " << teleport_cd << "s" << std::endl;
        
        // Try casting a spell if available
        if (poison_cd <= 0.1f && !opp_enemies.empty()) {
            try {
                Vector2 target_pos = opp_enemies[0].position;
                client.cast_spell(SpellType::POISON, target_pos);
                std::cout << "[Example] Successfully cast POISON at (" << target_pos.x << "," << target_pos.y << ")" << std::endl;
            } catch (const ApiException& e) {
                std::cout << "✗ POISON cast failed: " << e.what() << std::endl;
            }
        } else {
            std::cout << "Skipping POISON cast (cooldown: " << poison_cd << "s or no targets)" << std::endl;
        }
        
        // Test chat APIs
        std::cout << "\n--- Chat APIs ---" << std::endl;
        client.set_name("CppTestBot");
        client.set_chat_name_color("ff6600"); // Orange color
        client.send_chat("C++ API test completed successfully!");
        std::cout << "[Example] Sent chat message" << std::endl;
        
        // Get chat history
        auto chat_history = client.get_chat_history(5);
        std::cout << "Recent chat messages: " << chat_history.size() << std::endl;
        
        // Test developer APIs
        std::cout << "\n--- Developer APIs ---" << std::endl;
        auto devs = client.get_devs();
        std::cout << "Developers: ";
        for (size_t i = 0; i < devs.size(); i++) {
            std::cout << devs[i];
            if (i < devs.size() - 1) std::cout << ", ";
        }
        std::cout << std::endl;
        
        // Test easter egg APIs (be careful with these!)
        std::cout << "\n--- Easter Egg APIs ---" << std::endl;
        try {
            std::string pixelcat_result = client.pixelcat();
            std::cout << "Pixelcat response length: " << pixelcat_result.length() << std::endl;
        } catch (const std::exception& e) {
            std::cout << "Pixelcat failed: " << e.what() << std::endl;
        }
        
        try {
            bool boo_result = client.boo();
            std::cout << "Boo result: " << (boo_result ? "true" : "false") << std::endl;
        } catch (const std::exception& e) {
            std::cout << "Boo failed: " << e.what() << std::endl;
        }
        
        
        client.disconnect();
        std::cout << "\n[Example] Disconnected from game server." << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
