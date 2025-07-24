# Makefile for Game API C++ Library

# Compiler settings
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -Wpedantic -O2
DEBUGFLAGS = -g -O0 -DDEBUG
INCLUDES = -I.

# Build directory
BUILD_DIR = build

# Library settings
LIB_NAME = game_api
STATIC_LIB = lib$(LIB_NAME).a
SHARED_LIB = lib$(LIB_NAME).so

# Source and header files
SOURCES = game_client.cpp varient.cpp
HEADERS = constants.h structures.h game_client.h serialization.h varient.h
OBJECTS = $(SOURCES:%.cpp=$(BUILD_DIR)/%.o)

# Example
EXAMPLE_SRC = example.cpp
EXAMPLE_BIN = game_client_example

# Targets
.PHONY: all static shared example clean install debug

all: static shared example

static: $(STATIC_LIB)

shared: $(SHARED_LIB)

example: $(EXAMPLE_BIN)

debug: CXXFLAGS += $(DEBUGFLAGS)
debug: all

# Create build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Build static library
$(STATIC_LIB): $(OBJECTS)
	ar rcs $@ $^
	ranlib $@

# Build shared library
$(SHARED_LIB): $(OBJECTS)
	$(CXX) -shared -fPIC -o $@ $^

# Build example
$(EXAMPLE_BIN): $(EXAMPLE_SRC) $(STATIC_LIB)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $< -L. -l$(LIB_NAME)

# Compile object files
$(BUILD_DIR)/%.o: %.cpp $(HEADERS) | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -fPIC -c $< -o $@

# Install libraries and headers
install: $(STATIC_LIB) $(SHARED_LIB)
	sudo mkdir -p /usr/local/lib
	sudo mkdir -p /usr/local/include/game_api
	sudo cp $(STATIC_LIB) $(SHARED_LIB) /usr/local/lib/
	sudo cp $(HEADERS) /usr/local/include/game_api/
	sudo ldconfig

# Uninstall
uninstall:
	sudo rm -f /usr/local/lib/$(STATIC_LIB)
	sudo rm -f /usr/local/lib/$(SHARED_LIB)
	sudo rm -rf /usr/local/include/game_api
	sudo ldconfig

# Clean build files
clean:
	rm -f $(OBJECTS) $(STATIC_LIB) $(SHARED_LIB) $(EXAMPLE_BIN)
	rm -rf $(BUILD_DIR)

# Help target
help:
	@echo "Available targets:"
	@echo "  all      - Build static library, shared library, and example"
	@echo "  static   - Build static library only"
	@echo "  shared   - Build shared library only"
	@echo "  example  - Build example executable"
	@echo "  debug    - Build with debug flags"
	@echo "  install  - Install libraries and headers to system"
	@echo "  uninstall- Remove installed files"
	@echo "  clean    - Remove all build files"
	@echo "  help     - Show this help message"

# Dependencies
$(BUILD_DIR)/game_client.o: game_client.cpp game_client.h structures.h constants.h
