# Matrix-Roomba

[![Support Private.coffee!](https://shields.private.coffee/badge/private.coffee-support%20us!-pink?logo=coffeescript)](https://private.coffee)
[![PyPI](https://shields.private.coffee/pypi/v/matrix-roomba)](https://pypi.org/project/matrix-roomba/)
[![PyPI - Python Version](https://shields.private.coffee/pypi/pyversions/matrix-roomba)](https://pypi.org/project/matrix-roomba/)
[![PyPI - License](https://shields.private.coffee/pypi/l/matrix-roomba)](https://pypi.org/project/matrix-roomba/)
[![Latest Git Commit](https://shields.private.coffee/gitea/last-commit/privatecoffee/matrix-roomba?gitea_url=https://git.private.coffee)](https://git.private.coffee/privatecoffee/matrix-roomba)

Roomba is a moderation bot for Matrix, designed to help manage rooms and enforce content policies. The bot can block/unblock rooms, shut down rooms, and notify users of shutdowns. It integrates with Synapse's administrative API and supports optional encryption through Pantalaimon.

## Installation

```bash
pip install matrix-roomba
```

## Configuration

The following configuration options are available:

```yaml
homeserver: "https://matrix.example.com"
user_id: "@roomba:example.com"
access_token: "YOUR_ACCESS_TOKEN"
moderation_room_id: "!moderation_room_id:example.com"

# Debug mode - set to true for verbose logging
debug: false

# If your moderation room is encrypted, use Pantalaimon:
pantalaimon:
  homeserver: "http://localhost:8010"
  access_token: "YOUR_PANTALAIMON_ACCESS_TOKEN"
```

Ensure that the bot user is an admin on the homeserver, as it needs to be able to moderate rooms. Also add the user to the moderation room before starting the bot.

We recommend using pantalaimon as a proxy, because the bot itself does not support end-to-end encryption.

### Debug Mode

You can enable debug mode in two ways:

1. Set `debug: true` in your config.yaml file for persistent debug logging
2. Use the `!roomba debug` command in the moderation room to toggle debug mode at runtime

When debug mode is enabled, the bot will output detailed logs about:

- API requests and responses
- Room and user information
- Command processing
- Matrix client operations

This is useful for troubleshooting issues with the bot or understanding its behavior.

## Usage

1. Start the bot:

```bash
roomba
```

2. Send a message to the moderation room to get a list of available commands:

```
!roomba
```

### Commands

In the moderation room, send commands to manage rooms:

- Block a room: !roomba block <room_id>
- Unblock a room: !roomba unblock <room_id>
- Shutdown a room: !roomba shutdown <room_id> [--purge]
- For help: !roomba

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
