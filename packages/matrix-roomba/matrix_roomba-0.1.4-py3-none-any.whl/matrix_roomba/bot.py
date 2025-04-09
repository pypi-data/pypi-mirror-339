import nio
import asyncio
import aiohttp
import yaml
import logging
import sys


class RoombaBot:
    def __init__(
        self,
        homeserver,
        user_id,
        access_token,
        moderation_room_id,
        pantalaimon_homeserver=None,
        pantalaimon_token=None,
        shutdown_title=None,
        shutdown_message=None,
        debug=False,
    ):
        """Initialize the bot.

        Args:
            homeserver (str): The homeserver URL.
            user_id (str): The user ID of the bot.
            access_token (str): The access token of the bot.
            moderation_room_id (str): The room ID of the moderation room.
            pantalaimon_homeserver (str, optional): The homeserver URL of the Pantalaimon instance. Defaults to None, which means no Pantalaimon.
            pantalaimon_token (str, optional): The access token of the Pantalaimon instance. Defaults to None. Required if pantalaimon_homeserver is set.
            shutdown_title (str, optional): The title of the shutdown message. Defaults to None.
            shutdown_message (str, optional): The message of the shutdown message. Defaults to None.
            debug (bool, optional): Whether to enable debug mode. Defaults to False.
        """
        self.homeserver = homeserver
        self.access_token = access_token
        self.debug = debug

        self.shutdown_title = shutdown_title or "Content Violation Notification"
        self.shutdown_message = shutdown_message or (
            "A room you were a member of has been shutdown on this server due to content violations. Please review our Terms of Service."
        )

        if pantalaimon_homeserver and pantalaimon_token:
            self.client = nio.AsyncClient(pantalaimon_homeserver)
            self.client.access_token = pantalaimon_token

        else:
            self.client = nio.AsyncClient(homeserver)
            self.client.access_token = access_token

        self.client.user_id = user_id

        self.moderation_room_id = moderation_room_id
        self.logger = logging.getLogger(__name__)

        # Set log level based on debug mode
        log_level = logging.DEBUG if debug else logging.INFO
        self.logger.setLevel(log_level)

        # Configure console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)

        # Create a more detailed formatter for debug mode
        if debug:
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
            )
        else:
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        handler.setFormatter(formatter)

        # Remove existing handlers to avoid duplicates
        if self.logger.handlers:
            self.logger.handlers.clear()

        self.logger.addHandler(handler)

        if debug:
            self.logger.debug("Debug mode enabled - verbose logging activated")
            self.logger.debug(f"Initialized with homeserver: {homeserver}")
            self.logger.debug(f"User ID: {user_id}")
            self.logger.debug(f"Moderation room: {moderation_room_id}")
            if pantalaimon_homeserver:
                self.logger.debug(f"Using Pantalaimon at: {pantalaimon_homeserver}")

    async def start(self):
        """Start the bot."""
        self.logger.info("Starting Matrix-Roomba bot")
        if self.debug:
            self.logger.debug("Performing initial sync...")

        sync_response = await self.client.sync(timeout=30000)

        if self.debug:
            self.logger.debug(
                f"Initial sync complete, response type: {type(sync_response).__name__}"
            )
            if hasattr(sync_response, "rooms"):
                joined_rooms = (
                    len(sync_response.rooms.join)
                    if hasattr(sync_response.rooms, "join")
                    else 0
                )
                self.logger.debug(f"Joined rooms: {joined_rooms}")

                if self.moderation_room_id in sync_response.rooms.join:
                    self.logger.debug(
                        f"Successfully found moderation room {self.moderation_room_id} in joined rooms"
                    )
                else:
                    self.logger.warning(
                        f"Moderation room {self.moderation_room_id} not found in joined rooms!"
                    )

        self.client.add_event_callback(self.message_callback, nio.RoomMessageText)
        self.logger.info("Bot started, listening for commands...")
        await self.client.sync_forever(timeout=30000)

    async def message_callback(self, room, event):
        """Callback for when a message is received in a room.

        Args:
            room (nio.room.Room): The room the message was received in.
            event (nio.events.room_events.RoomMessageText): The message event.
        """
        if room.room_id != self.moderation_room_id:
            if self.debug:
                self.logger.debug(
                    f"Ignoring message in room {room.room_id} (not moderation room)"
                )
            return

        if self.debug:
            self.logger.debug(f"Received message in moderation room: '{event.body}'")
            self.logger.debug(f"Message sender: {event.sender}")
            self.logger.debug(f"Event ID: {event.event_id}")

        if event.body.startswith("!roomba block"):
            room_ids = event.body.split()[2:]
            self.logger.info(f"Blocking rooms: {', '.join(room_ids)}")
            for room_id in room_ids:
                if room_id.startswith("#"):
                    if self.debug:
                        self.logger.debug(f"Resolving room alias {room_id}")
                    room_id = await self.resolve_room_alias(room_id)

                await self.block_room(room_id, True)

        elif event.body.startswith("!roomba unblock"):
            room_ids = event.body.split()[2:]
            self.logger.info(f"Unblocking rooms: {', '.join(room_ids)}")
            for room_id in room_ids:
                if room_id.startswith("#"):
                    if self.debug:
                        self.logger.debug(f"Resolving room alias {room_id}")
                    room_id = await self.resolve_room_alias(room_id)

                await self.block_room(room_id, False)

        elif event.body.startswith("!roomba roominfo"):
            room_id = event.body.split()[2]
            self.logger.info(f"Getting room info for: {room_id}")
            if room_id.startswith("#"):
                if self.debug:
                    self.logger.debug(f"Resolving room alias {room_id}")
                room_id = await self.resolve_room_alias(room_id)

            await self.get_room_info(room_id)

        elif event.body.startswith("!roomba shutdown"):
            parts = event.body.split()

            if "--purge" in parts:
                parts.remove("--purge")
                purge = True
                if self.debug:
                    self.logger.debug("Purge option enabled for shutdown")
            else:
                purge = False

            room_ids = parts[2:]
            self.logger.info(
                f"Shutting down rooms: {', '.join(room_ids)} (purge={purge})"
            )
            for room_id in room_ids:
                if room_id.startswith("#"):
                    if self.debug:
                        self.logger.debug(f"Resolving room alias {room_id}")
                    room_id = await self.resolve_room_alias(room_id)

                await self.shutdown_room(room_id, purge)

        elif event.body.startswith("!roomba lock"):
            user_ids = event.body.split()[2:]
            self.logger.info(f"Locking users: {', '.join(user_ids)}")
            for user_id in user_ids:
                await self.lock_user(user_id, True)

        elif event.body.startswith("!roomba unlock"):
            user_ids = event.body.split()[2:]
            self.logger.info(f"Unlocking users: {', '.join(user_ids)}")
            for user_id in user_ids:
                await self.lock_user(user_id, False)

        elif event.body.startswith("!roomba debug"):
            # Toggle debug mode command
            self.debug = not self.debug
            log_level = logging.DEBUG if self.debug else logging.INFO
            self.logger.setLevel(log_level)
            for handler in self.logger.handlers:
                handler.setLevel(log_level)

            await self.send_message(
                self.moderation_room_id,
                f"Debug mode {'enabled' if self.debug else 'disabled'}.",
            )
            self.logger.info(f"Debug mode {'enabled' if self.debug else 'disabled'}")

        elif event.body and event.body.split()[0] == "!roomba":
            help_message = (
                "Available commands:\n"
                "- !roomba block <room_id> - Block a room\n"
                "- !roomba unblock <room_id> - Unblock a room\n"
                "- !roomba roominfo <room_id> - Get information about a room\n"
                "- !roomba shutdown <room_id> [--purge] - Shutdown a room (optionally purge)\n"
                "- !roomba lock <user_id> - Lock a user\n"
                "- !roomba unlock <user_id> - Unlock a user\n"
                "- !roomba debug - Toggle debug mode"
            )
            await self.send_message(self.moderation_room_id, help_message)

        await self.client.room_read_markers(
            self.moderation_room_id, event.event_id, event.event_id
        )

    async def resolve_room_alias(self, room_alias):
        """Resolve a room alias to a room ID.

        Args:
            room_alias (str): The room alias to resolve.

        Returns:
            str: The room ID of the resolved room alias.
        """
        if self.debug:
            self.logger.debug(f"Resolving room alias: {room_alias}")

        response = await self.client.room_resolve_alias(room_alias)

        if isinstance(response, nio.RoomResolveAliasResponse):
            if self.debug:
                self.logger.debug(f"Resolved {room_alias} to {response.room_id}")
            return response.room_id
        else:
            if self.debug:
                self.logger.debug(f"Failed to resolve {room_alias}: {response}")
            return room_alias

    async def block_room(self, room_id, block):
        """Block or unblock a room.

        Args:
            room_id (str): The room ID to block or unblock.
            block (bool): Whether to block or unblock the room.
        """
        url = f"{self.homeserver}/_synapse/admin/v1/rooms/{room_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        body = {"block": block}

        if self.debug:
            self.logger.debug(
                f"Making API call to {'block' if block else 'unblock'} room {room_id}"
            )
            self.logger.debug(f"URL: {url}/block")
            self.logger.debug(f"Headers: {headers}")
            self.logger.debug(f"Body: {body}")

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if self.debug:
                    self.logger.debug(f"GET {url} response status: {resp.status}")

                if resp.status == 200:
                    room_data = await resp.json()
                    room_name = room_data.get("name")

                    if self.debug:
                        self.logger.debug(f"Room data: {room_data}")
                else:
                    if self.debug:
                        self.logger.debug(
                            f"Failed to get room info: {await resp.text()}"
                        )
                    room_name = None

            async with session.put(f"{url}/block", headers=headers, json=body) as resp:
                if self.debug:
                    self.logger.debug(f"PUT {url}/block response status: {resp.status}")
                    response_text = await resp.text()
                    self.logger.debug(f"Response body: {response_text}")

                if resp.status == 200:
                    response = await resp.json()
                    self.logger.info(
                        f"Room {room_id}{f' ({room_name})' if room_name else ''} {'blocked' if block else 'unblocked'} successfully"
                    )
                    local_users = await self.get_local_users(room_id)
                    await self.send_message(
                        self.moderation_room_id,
                        f"Room {room_id} {'blocked' if block else 'unblocked'} successfully. Local users: {', '.join(local_users)}",
                    )
                else:
                    self.logger.error(
                        f"Failed to {'block' if block else 'unblock'} room {room_id}: {resp.status}"
                    )
                    await self.send_message(
                        self.moderation_room_id,
                        f"Failed to {'block' if block else 'unblock'} room {room_id}.",
                    )

    async def get_room_info(self, room_id):
        """Fetch and print basic info and local users of a room.

        Args:
            room_id (str): The room ID to get information about.
        """
        url = f"{self.homeserver}/_synapse/admin/v1/rooms/{room_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        if self.debug:
            self.logger.debug(f"Fetching room info for {room_id}")
            self.logger.debug(f"URL: {url}")
            self.logger.debug(f"Headers: {headers}")

        # Get room information
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if self.debug:
                    self.logger.debug(f"GET {url} response status: {resp.status}")

                if resp.status == 200:
                    room_info = await resp.json()
                    if self.debug:
                        self.logger.debug(f"Room info response: {room_info}")

                    room_name = room_info.get("name", "Unknown Room")
                    creation_ts = room_info.get("creation_ts", "Unknown Timestamp")
                else:
                    error_text = await resp.text()
                    self.logger.error(
                        f"Failed to fetch room info for {room_id}: {resp.status} - {error_text}"
                    )
                    if self.debug:
                        self.logger.debug(f"Error response: {error_text}")

                    await self.send_message(
                        self.moderation_room_id,
                        f"Failed to fetch room information for {room_id}.",
                    )
                    return

        # Get local users
        local_users = await self.get_local_users(room_id)

        # Format and send the response message
        message = (
            f"Room Info for {room_id}:\n"
            f"- Name: {room_name}\n"
            f"- Creation Timestamp: {creation_ts}\n"
            f"- Local Users: {', '.join(local_users) if local_users else 'None'}"
        )

        if self.debug:
            self.logger.debug(f"Sending room info message: {message}")

        await self.send_message(self.moderation_room_id, message)

    async def get_local_users(self, room_id):
        """Get the local users in a room.

        Args:
            room_id (str): The room ID to get the local users from.

        Returns:
            list: The list of local users in the room.
        """
        members_url = f"{self.homeserver}/_matrix/client/r0/rooms/{room_id}/members"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        if self.debug:
            self.logger.debug(f"Fetching members for room {room_id}")
            self.logger.debug(f"URL: {members_url}")

        local_users = []

        async with aiohttp.ClientSession() as session:
            async with session.get(members_url, headers=headers) as resp:
                if self.debug:
                    self.logger.debug(f"Members API response status: {resp.status}")

                if resp.status == 200:
                    members = await resp.json()
                    if self.debug:
                        self.logger.debug(
                            f"Found {len(members.get('chunk', []))} members in room"
                        )

                    for member in members.get("chunk", []):
                        user_id = member.get("user_id")
                        if user_id and user_id.endswith(
                            self.client.user_id.split(":")[1]
                        ):
                            local_users.append(user_id)
                else:
                    error_text = await resp.text()
                    if self.debug:
                        self.logger.debug(f"Failed to get room members: {error_text}")

        if self.debug:
            self.logger.debug(f"Found {len(local_users)} local users in room {room_id}")

        return local_users

    async def shutdown_room(self, room_id, purge=True):
        """Shutdown and optionally purge a room.

        Args:
            room_id (str): The room ID to shut down.
            purge (bool, optional): Whether to purge the room. Defaults to True.
        """
        url = f"{self.homeserver}/_synapse/admin/v2/rooms/{room_id}"
        v1_url = f"{self.homeserver}/_synapse/admin/v1/rooms/{room_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        body = {
            "new_room_user_id": self.client.user_id,
            "room_name": self.shutdown_title,
            "message": self.shutdown_message,
            "block": True,
            "purge": purge,
        }

        if self.debug:
            self.logger.debug(f"Shutting down room {room_id} (purge={purge})")
            self.logger.debug(f"URL: {url}")
            self.logger.debug(f"Headers: {headers}")
            self.logger.debug(f"Request body: {body}")

        local_users = await self.get_local_users(room_id)
        if self.debug:
            self.logger.debug(f"Local users in room {room_id}: {local_users}")

        async with aiohttp.ClientSession() as session:
            # First get room info to include room name in logs
            async with session.get(v1_url, headers=headers) as resp:
                if self.debug:
                    self.logger.debug(f"GET {v1_url} response status: {resp.status}")

                if resp.status == 200:
                    room_data = await resp.json()
                    room_name = room_data.get("name")
                    if self.debug:
                        self.logger.debug(f"Room data: {room_data}")
                else:
                    if self.debug:
                        self.logger.debug(
                            f"Failed to get room info: {await resp.text()}"
                        )
                    room_name = None

            # Now perform the shutdown
            async with session.delete(url, headers=headers, json=body) as resp:
                if self.debug:
                    self.logger.debug(f"DELETE {url} response status: {resp.status}")
                    response_text = await resp.text()
                    self.logger.debug(f"Response body: {response_text}")

                if resp.status == 200:
                    response = await resp.json()
                    delete_id = response.get("delete_id")
                    self.logger.info(
                        f"Room {room_id}{f' ({room_name})' if room_name else ''} shutdown initiated successfully: delete_id={delete_id}"
                    )
                    await self.send_message(
                        self.moderation_room_id,
                        f"Room {room_id}{f' ({room_name})' if room_name else ''} shutdown initiated successfully. Delete ID: {delete_id}. Local users: {', '.join(local_users)}",
                    )
                else:
                    error_text = await resp.text()
                    self.logger.error(
                        f"Failed to shutdown room {room_id}: {resp.status} - {error_text}"
                    )
                    await self.send_message(
                        self.moderation_room_id,
                        f"Failed to shutdown room {room_id}. Error: {resp.status}",
                    )

    async def lock_user(self, user_id, locked=True):
        """Lock or unlock a user.

        Args:
            user_id (str): The user ID to lock.
            locked (bool, optional): Whether to lock (True) or unlock (False) the user. Defaults to True.
        """
        url = f"{self.homeserver}/_synapse/admin/v2/users/{user_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        payload = {"locked": locked}

        if self.debug:
            self.logger.debug(f"{'Locking' if locked else 'Unlocking'} user {user_id}")
            self.logger.debug(f"URL: {url}")
            self.logger.debug(f"Headers: {headers}")
            self.logger.debug(f"Payload: {payload}")

        async with aiohttp.ClientSession() as session:
            # Get user's joined rooms for reporting
            joined_rooms_url = (
                f"{self.homeserver}/_synapse/admin/v1/users/{user_id}/joined_rooms"
            )
            if self.debug:
                self.logger.debug(f"Fetching joined rooms for user {user_id}")
                self.logger.debug(f"URL: {joined_rooms_url}")

            async with session.get(joined_rooms_url, headers=headers) as resp:
                if self.debug:
                    self.logger.debug(
                        f"GET {joined_rooms_url} response status: {resp.status}"
                    )

                if resp.status == 200:
                    joined_rooms_data = await resp.json()
                    joined_rooms = joined_rooms_data.get("joined_rooms", [])
                    if self.debug:
                        self.logger.debug(
                            f"User is in {len(joined_rooms)} rooms: {joined_rooms}"
                        )
                else:
                    error_text = await resp.text()
                    if self.debug:
                        self.logger.debug(f"Failed to get joined rooms: {error_text}")
                    joined_rooms = []

            # Perform the lock/unlock action
            async with session.put(url, headers=headers, json=payload) as resp:
                if self.debug:
                    self.logger.debug(f"PUT {url} response status: {resp.status}")
                    response_text = await resp.text()
                    self.logger.debug(f"Response body: {response_text}")

                if resp.status == 200:
                    self.logger.info(
                        f"User {user_id} {'locked' if locked else 'unlocked'} successfully"
                    )

                    message = f"User {user_id} {'locked' if locked else 'unlocked'} successfully."

                    if joined_rooms:
                        message += "\n\nJoined rooms:\n"

                        for room_id in joined_rooms:
                            room_url = (
                                f"{self.homeserver}/_synapse/admin/v1/rooms/{room_id}"
                            )
                            if self.debug:
                                self.logger.debug(f"Fetching room info for {room_id}")

                            async with session.get(
                                room_url, headers=headers
                            ) as room_resp:
                                if self.debug:
                                    self.logger.debug(
                                        f"GET {room_url} response status: {room_resp.status}"
                                    )

                                if room_resp.status == 200:
                                    room_data = await room_resp.json()
                                    room_name = room_data.get("name")
                                    if self.debug:
                                        self.logger.debug(f"Room data: {room_data}")
                                else:
                                    if self.debug:
                                        self.logger.debug(
                                            f"Failed to get room info: {await room_resp.text()}"
                                        )
                                    room_name = None

                            message += (
                                f"\n- {room_id}{f' ({room_name})' if room_name else ''}"
                            )

                    await self.send_message(self.moderation_room_id, message)
                else:
                    error_text = await resp.text()
                    self.logger.error(
                        f"Failed to {'lock' if locked else 'unlock'} user {user_id}: {resp.status} - {error_text}"
                    )
                    await self.send_message(
                        self.moderation_room_id,
                        f"Failed to {'lock' if locked else 'unlock'} user {user_id}. Error: {resp.status}",
                    )

    async def send_message(self, room_id, message):
        """Send a message to a room.

        Args:
            room_id (str): The room ID to send the message to.
            message (str): The message to send.
        """
        content = {"msgtype": "m.text", "body": message}

        if self.debug:
            self.logger.debug(f"Sending message to {room_id}")
            self.logger.debug(
                f"Message content: {message[:100]}{'...' if len(message) > 100 else ''}"
            )

        response = await self.client.room_send(
            room_id, message_type="m.room.message", content=content
        )

        if self.debug:
            self.logger.debug(f"Send message response: {response}")


async def main_async():
    # Load configuration from config.yaml
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    homeserver = config["homeserver"]
    user_id = config["user_id"]
    access_token = config["access_token"]
    moderation_room_id = config["moderation_room_id"]
    debug = config.get("debug", False)

    # Set up root logger for startup logs
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting Matrix-Roomba")
    logger.info(f"Debug mode: {'enabled' if debug else 'disabled'}")

    if "pantalaimon" in config:
        pantalaimon_homeserver = config["pantalaimon"]["homeserver"]
        pantalaimon_token = config["pantalaimon"]["access_token"]
        logger.info("Using Pantalaimon for E2EE support")
    else:
        pantalaimon_homeserver = None
        pantalaimon_token = None
        logger.info("No Pantalaimon configuration found")

    if "shutdown" in config:
        shutdown_title = config["shutdown"].get("title")
        shutdown_message = config["shutdown"].get("message")
        logger.info("Using custom shutdown messages")
    else:
        shutdown_title = None
        shutdown_message = None
        logger.info("Using default shutdown messages")

    # Create and start the bot
    bot = RoombaBot(
        homeserver,
        user_id,
        access_token,
        moderation_room_id,
        pantalaimon_homeserver,
        pantalaimon_token,
        shutdown_title,
        shutdown_message,
        debug,
    )
    await bot.start()


def main():
    try:
        asyncio.get_event_loop().run_until_complete(main_async())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
