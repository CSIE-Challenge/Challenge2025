#include "game_client.h"
#include <iostream>
#include <thread>
#include <chrono>

using namespace GameAPI;

int main() {
    try {
        // Create game client with your token
        GameClient client(7749, "50ef3715"); // Replace with your actual token
        
        std::cout << "Waiting for game to start..." << std::endl;
        
        // Wait for game to start
        while (client.get_game_status() != GameStatus::RUNNING) {
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
        
        std::cout << "Game started!" << std::endl;
        
        // Set player name and chat color
        client.set_name("CppBot");
        client.set_chat_name_color("00ff00"); // Green color
        
        // Send a greeting message
        client.send_chat("Hello from C++!");
        
        // Get terrain information
        auto terrain = client.get_all_terrain();
        std::cout << "Map size: " << terrain.size() << "x" << (terrain.empty() ? 0 : terrain[0].size()) << std::endl;
        
        // Get current money
        int money = client.get_money();
        std::cout << "Current money: " << money << std::endl;
        
        // Example: Place a tower if we have enough money
        if (money >= 100) { // Assuming towers cost around 100
            try {
                Vector2 tower_pos(5, 5); // Example position
                client.place_tower(TowerType::FIRE_MARIO, "1", tower_pos);
                std::cout << "Placed tower at " << tower_pos.toString() << std::endl;
            } catch (const ApiException& e) {
                std::cout << "Failed to place tower: " << e.what() << std::endl;
            }
        }
        
        // Get all towers
        auto towers = client.get_all_towers(true);
        std::cout << "Number of towers: " << towers.size() << std::endl;
        
        auto enemies = client.get_all_enemies(true);
        std::cout << "Number of enemies: " << enemies.size() << std::endl;

        // Disconnect gracefully
        client.disconnect();
        std::cout << "Disconnected from game server." << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
