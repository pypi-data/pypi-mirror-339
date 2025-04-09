# server.py
import os
from http.client import responses

import requests
from typing import Dict, Any

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Home Assistant")


def execute_service(service: str, payload: Dict[str, str]):
    host = os.getenv("HASS_HOST")
    token = os.getenv("HASS_TOKEN")

    url = f"https://{host}/api/services/{service}"
    headers = {
        "Authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response


@mcp.tool(
    name="call_xiaoai",
    description="Xiao Mi Smart Voice Home Assistant, You can use natural language to directive it / "
                "小米家的小爱同学，您的智能语音家居助手，您可以使用自然语言去命令它",
)
def call_xiaoai(command: str) -> str:
    entity_id = os.getenv("HASS_XIAOAI_ENTITY_ID")
    payload = {
        "entity_id": entity_id,
        "execute": True,
        "silent": True,
        "text": command,
    }
    response = execute_service("xiaomi_miot/intelligent_speaker", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="Turn On Light in your home",
)
def turn_on_light(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id
    }

    response = execute_service("light/turn_on", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="Turn Off Light in your home",
)
def turn_off_light(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id
    }

    response = execute_service("light/turn_off", payload)
    response.raise_for_status()
    return "OK"

@mcp.tool(
    description="Turn On Climate in your home",
)
def turn_on_climate(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service("climate/turn_on", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="Turn Off Climate in your home",
)
def turn_off_climate(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service("climate/turn_off", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="Turn On Switch in your home",
)
def turn_on_switch(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service("switch/turn_on", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="Turn Off Switch in your home",
)
def turn_off_switch(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service("switch/turn_off", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="Get the state of entity"
)
def get_state_of_entity(entity_id: str) -> str:
    host = os.getenv("HASS_HOST")
    token = os.getenv("HASS_TOKEN")

    url = f"https://{host}/api/states/{entity_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


@mcp.resource(
    "entity://{entity_id}",
)
def get_state_of_entity_resource(entity_id: str) -> str:
    """Get the state of entity"""
    return get_state_of_entity(entity_id)


def main():
    mcp.run()
