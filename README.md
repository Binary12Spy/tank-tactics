# tank-tactics

## Goal

The goal of this repository is to develop TankTactics, as covered by [PeopleMakeGames](https://www.youtube.com/@PeopleMakeGames) in [this video](https://www.youtube.com/watch?v=aOYbR-Q_4Hs). This implementation will be open-source, allowing individuals to host their own servers or play on a potential future central public server.

## Planned Features

- **Player Movement**: Players can move to adjacent, unoccupied squares on the grid.
- **Shooting Mechanism**: Players can shoot others within their range, reducing their health.
- **Health Management**: Players can add hearts to their health to increase their survivability.
- **Range Upgrade**: Players can upgrade their shooting range to target opponents from a greater distance.
- **Gifting System**: Players can gift hearts or action points to others within their range.
- **Revival Mechanism**: Dead players can be revived by receiving hearts from other players.
- **Dead Players Jury**: Dead players form a jury to vote and haunt a living player, preventing them from receiving action points for a day.
- **Random Heart Spawn**: Hearts spawn randomly on the field once a day, providing opportunities for players to gain additional health.
- **Game End Conditions**: The game ends when a clear 1st, 2nd, and 3rd place can be determined. The final 4 players must agree on the placing.
- **Secret Action Points**: Action points are kept secret from other players, adding a layer of strategy and deception.
- **Web-based Interface**: The game will have a web-based interface for easy access and interaction.

## Technology Stack

- **Frontend**: Angular
  - Interactive and responsive UI
  - HTTP client for REST API interactions
  - WebSocket support for real-time updates

- **Backend**: Python with FastAPI
  - REST API for player actions and game state management
  - WebSocket endpoints for real-time communication
  - Asynchronous handling for efficient performance

## Roadmap

### Base Functionality
- [ ] Initialize game grid and player positions
- [ ] Implement player movement
- [ ] Implement shooting mechanism
- [ ] Implement health management (adding hearts)
- [ ] Implement action points (AP) system
- [ ] Implement range upgrade functionality
- [ ] Implement basic game state management

### Extended Features
- [ ] Implement gifting system (AP)
- [ ] Implement revival mechanism for dead players (?)
- [ ] Implement dead players jury
- [ ] Implement game end conditions and ranking system
- [ ] Ensure secret action points are maintained

### Modularity and Extensibility
- [ ] Design modular architecture for easy rule extension
- [ ] Implement dynamic rule loading from configuration
- [ ] Provide clear API endpoints for actions and game state updates
- [ ] Implement event-driven architecture for game events
- [ ] Create detailed documentation for setting up and extending the game
