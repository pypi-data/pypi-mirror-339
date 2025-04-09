import asyncio
import os
import sys
import logging
from typing import Any
import httpx

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verify environment variables
API_TOKEN = os.getenv("YALA_EVENTS_API_TOKEN")
BASE_URL = os.getenv("BASE_URL")

if not API_TOKEN:
    logger.error("YALA_EVENTS_API_TOKEN environment variable not set")
    sys.exit(1)

server = Server("Yala Events Server")

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

async def make_api_request(method: str, url: str, json: dict = None, params: dict = None) -> dict[str, Any] | None:
    """Make a request to the yala.events API with error handling."""
    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Making {method} request to {url}")
            response = await client.request(
                method=method,
                url=url,
                headers=HEADERS,
                json=json,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"API error: {e.response.status_code} - {e.response.text}")
            return {"error": f"API error: {e.response.status_code} - {e.response.text}"}
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available resources from yala.events."""
    data = await make_api_request("GET", f"{BASE_URL}/api/events")
    if not data or "data" not in data:
        return []
    
    return [
        types.Resource(
            uri=AnyUrl(f"event://yala/{event['id']}"),
            name=event['title'],
            description=f"Event on {event['startDateTime']}",
            mimeType="application/json",
        )
        for event in data["data"]
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read a specific event's details by its URI."""
    if uri.scheme != "event":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")
    
    event_id = uri.path.lstrip("/")
    data = await make_api_request("GET", f"{BASE_URL}/api/events/{event_id}")
    
    if not data or "data" not in data:
        raise ValueError(f"Event not found: {event_id}")
    
    event = data["data"]
    return "\n".join([
        f"Title: {event['title']}",
        f"ID: {event['id']}",
        f"Date: {event['startDateTime']}",
        f"Content: {event['content']}"
    ])

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available tools for managing yala.events."""
    return [
        types.Tool(name="list-events", description="List events with optional date filter",
            inputSchema={"type": "object", "properties": {"date": {"type": "string"}}}),
        types.Tool(name="create-event", description="Create a new event",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"}, "content": {"type": "string"}, "date": {"type": "string"},
                    "organization_id": {"type": "integer"}, "type_id": {"type": "integer"},
                    "category_id": {"type": "integer"}, "format_id": {"type": "integer"},
                    "covers": {"type": "array", "items": {"type": "string"}}, "is_private": {"type": "boolean"}
                },
                "required": ["title", "content", "date", "organization_id", "type_id", "category_id", "format_id", "covers", "is_private"]
            }),
        types.Tool(name="get-event-details", description="Get details of a specific event",
            inputSchema={"type": "object", "properties": {"event_id": {"type": "integer"}}, "required": ["event_id"]}),
        types.Tool(name="get-organizations", description="List all organizations"),  # No arguments, omit inputSchema
        types.Tool(name="list-histories", description="List history records",
            inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}, "page": {"type": "integer"}}}),
        types.Tool(name="list-modules", description="List modules with optional search",
            inputSchema={"type": "object", "properties": {"search": {"type": "string"}}}),
        types.Tool(name="create-module", description="Create a new module",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
        types.Tool(name="update-module", description="Update an existing module",
            inputSchema={"type": "object", "properties": {"module_id": {"type": "integer"}, "name": {"type": "string"}},
                        "required": ["module_id", "name"]}),
        types.Tool(name="delete-module", description="Delete a module",
            inputSchema={"type": "object", "properties": {"module_id": {"type": "integer"}}, "required": ["module_id"]}),
        types.Tool(name="get-module-histories", description="Get history records for modules",
            inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}, "page": {"type": "integer"}}}),
        types.Tool(name="list-permissions", description="List permissions with optional search",
            inputSchema={"type": "object", "properties": {"search": {"type": "string"}}}),
        types.Tool(name="create-permission", description="Create a new permission",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
        types.Tool(name="update-permission", description="Update an existing permission",
            inputSchema={"type": "object", "properties": {"permission_id": {"type": "integer"}, "name": {"type": "string"}},
                        "required": ["permission_id", "name"]}),
        types.Tool(name="delete-permission", description="Delete a permission",
            inputSchema={"type": "object", "properties": {"permission_id": {"type": "integer"}}, "required": ["permission_id"]}),
        types.Tool(name="get-permission-histories", description="Get history records for permissions",
            inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}, "page": {"type": "integer"}}}),
        types.Tool(name="list-roles", description="List roles with optional search",
            inputSchema={"type": "object", "properties": {"search": {"type": "string"}}}),
        types.Tool(name="create-role", description="Create a new role with permissions",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, 
                        "permissions_per_module": {"type": "array", "items": {"type": "object"}}},
                        "required": ["name", "permissions_per_module"]}),
        types.Tool(name="update-role", description="Update an existing role",
            inputSchema={"type": "object", "properties": {"role_id": {"type": "integer"}, "name": {"type": "string"},
                        "permissions_per_module": {"type": "array", "items": {"type": "object"}}},
                        "required": ["role_id", "name", "permissions_per_module"]}),
        types.Tool(name="delete-role", description="Delete a role",
            inputSchema={"type": "object", "properties": {"role_id": {"type": "integer"}}, "required": ["role_id"]}),
        types.Tool(name="get-role-histories", description="Get history records for roles",
            inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}, "page": {"type": "integer"}}}),
        types.Tool(name="list-favorites-events", description="List favorite events"),  # No arguments, omit inputSchema
        types.Tool(name="create-favorite-event", description="Add an event to favorites",
            inputSchema={"type": "object", "properties": {"event_id": {"type": "integer"}, "user_id": {"type": "integer"}},
                        "required": ["event_id", "user_id"]}),
        types.Tool(name="update-favorite-event", description="Update a favorite event",
            inputSchema={"type": "object", "properties": {"favorite_id": {"type": "integer"}, "event_id": {"type": "integer"},
                        "user_id": {"type": "integer"}}, "required": ["favorite_id", "event_id", "user_id"]}),
        types.Tool(name="delete-favorite-event", description="Remove an event from favorites",
            inputSchema={"type": "object", "properties": {"favorite_id": {"type": "integer"}}, "required": ["favorite_id"]}),
        types.Tool(name="get-favorites-events-histories", description="Get history records for favorite events",
            inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}, "page": {"type": "integer"}}}),
        types.Tool(name="list-personal-access-tokens", description="List personal access tokens",
            inputSchema={"type": "object", "properties": {"search": {"type": "string"}}}),
        types.Tool(name="create-personal-access-token", description="Create a new personal access token",
            inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "expire": {"type": "boolean"},
                        "expire_at": {"type": "string"}}, "required": ["name", "expire"]}),
        types.Tool(name="update-personal-access-token", description="Update a personal access token",
            inputSchema={"type": "object", "properties": {"token_id": {"type": "integer"}, "name": {"type": "string"},
                        "expire": {"type": "boolean"}, "expire_at": {"type": "string"}},
                        "required": ["token_id", "name", "expire"]}),
        types.Tool(name="delete-personal-access-token", description="Delete a personal access token",
            inputSchema={"type": "object", "properties": {"token_id": {"type": "integer"}}, "required": ["token_id"]}),
        types.Tool(name="get-personal-access-token-histories", description="Get history records for personal access tokens",
            inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}, "page": {"type": "integer"}}}),
        types.Tool(name="list-public-organizations", description="List public organizations for SEO",
            inputSchema={"type": "object", "properties": {"search": {"type": "string"}}}),
        types.Tool(name="get-app-version", description="Get the application version information"),  # No arguments, omit inputSchema
        types.Tool(name="health-check", description="Perform a health check on the application")  # No arguments, omit inputSchema
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests for yala.events."""
    if name == "list-events":
        params = {"date": arguments.get("date")} if arguments and "date" in arguments else {}
        data = await make_api_request("GET", f"{BASE_URL}/api/events", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No events found")]
        events = [f"Event: {e['title']} | Date: {e['startDateTime']} | ID: {e['id']}" for e in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(events))]

    elif name == "create-event":
        if not arguments: raise ValueError("Missing arguments")
        payload = {
            "title": arguments.get("title"), "content": arguments.get("content"), "startDateTime": arguments.get("date"),
            "organizationId": arguments.get("organization_id"), "typeId": arguments.get("type_id"),
            "categoryId": arguments.get("category_id"), "formatId": arguments.get("format_id"),
            "covers": arguments.get("covers"), "isPrivate": arguments.get("is_private")
        }
        data = await make_api_request("POST", f"{BASE_URL}/api/events", json=payload)
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        event = data["data"]
        await server.request_context.session.send_resource_list_changed()
        return [types.TextContent(type="text", text=f"Event created: {event['title']} (ID: {event['id']})")]

    elif name == "get-event-details":
        if not arguments or "event_id" not in arguments: raise ValueError("Missing event_id")
        data = await make_api_request("GET", f"{BASE_URL}/api/events/{arguments['event_id']}")
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Event not found')}")
        event = data["data"]
        details = [f"Title: {event['title']}", f"ID: {event['id']}", f"Date: {event['startDateTime']}", f"Content: {event['content']}"]
        return [types.TextContent(type="text", text="\n".join(details))]

    elif name == "get-organizations":
        data = await make_api_request("GET", f"{BASE_URL}/api/organizations")
        if not data or "data" not in data: return [types.TextContent(type="text", text="No organizations found")]
        orgs = [f"Organization: {org['name']} | ID: {org['id']}" for org in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(orgs))]

    elif name == "list-histories":
        params = {k: arguments[k] for k in ["limit", "page"] if arguments and k in arguments}
        data = await make_api_request("GET", f"{BASE_URL}/api/histories", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No histories found")]
        histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']} | Date: {h['createdAt']}" for h in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(histories))]

    elif name == "list-modules":
        params = {"search": arguments.get("search")} if arguments and "search" in arguments else {}
        data = await make_api_request("GET", f"{BASE_URL}/api/modules", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No modules found")]
        modules = [f"Module: {m['name']} | ID: {m['id']}" for m in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(modules))]

    elif name == "create-module":
        if not arguments or "name" not in arguments: raise ValueError("Missing name")
        data = await make_api_request("POST", f"{BASE_URL}/api/modules", json={"name": arguments["name"]})
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        module = data["data"]
        return [types.TextContent(type="text", text=f"Module created: {module['name']} (ID: {module['id']})")]

    elif name == "update-module":
        if not arguments or not all(k in arguments for k in ["module_id", "name"]): raise ValueError("Missing arguments")
        data = await make_api_request("PUT", f"{BASE_URL}/api/modules/{arguments['module_id']}", json={"name": arguments["name"]})
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        module = data["data"]
        return [types.TextContent(type="text", text=f"Module updated: {module['name']} (ID: {module['id']})")]

    elif name == "delete-module":
        if not arguments or "module_id" not in arguments: raise ValueError("Missing module_id")
        data = await make_api_request("DELETE", f"{BASE_URL}/api/modules/{arguments['module_id']}")
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        return [types.TextContent(type="text", text=f"Module deleted (ID: {arguments['module_id']})")]

    elif name == "get-module-histories":
        params = {k: arguments[k] for k in ["limit", "page"] if arguments and k in arguments}
        data = await make_api_request("GET", f"{BASE_URL}/api/modules/histories", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No module histories found")]
        histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']}" for h in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(histories))]

    elif name == "list-permissions":
        params = {"search": arguments.get("search")} if arguments and "search" in arguments else {}
        data = await make_api_request("GET", f"{BASE_URL}/api/permissions", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No permissions found")]
        perms = [f"Permission: {p['name']} | ID: {p['id']}" for p in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(perms))]

    elif name == "create-permission":
        if not arguments or "name" not in arguments: raise ValueError("Missing name")
        data = await make_api_request("POST", f"{BASE_URL}/api/permissions", json={"name": arguments["name"]})
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        perm = data["data"]
        return [types.TextContent(type="text", text=f"Permission created: {perm['name']} (ID: {perm['id']})")]

    elif name == "update-permission":
        if not arguments or not all(k in arguments for k in ["permission_id", "name"]): raise ValueError("Missing arguments")
        data = await make_api_request("PUT", f"{BASE_URL}/api/permissions/{arguments['permission_id']}", json={"name": arguments["name"]})
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        perm = data["data"]
        return [types.TextContent(type="text", text=f"Permission updated: {perm['name']} (ID: {perm['id']})")]

    elif name == "delete-permission":
        if not arguments or "permission_id" not in arguments: raise ValueError("Missing permission_id")
        data = await make_api_request("DELETE", f"{BASE_URL}/api/permissions/{arguments['permission_id']}")
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        return [types.TextContent(type="text", text=f"Permission deleted (ID: {arguments['permission_id']})")]

    elif name == "get-permission-histories":
        params = {k: arguments[k] for k in ["limit", "page"] if arguments and k in arguments}
        data = await make_api_request("GET", f"{BASE_URL}/api/permissions/histories", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No permission histories found")]
        histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']}" for h in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(histories))]

    elif name == "list-roles":
        params = {"search": arguments.get("search")} if arguments and "search" in arguments else {}
        data = await make_api_request("GET", f"{BASE_URL}/api/roles", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No roles found")]
        roles = [f"Role: {r['name']} | ID: {r['id']} | Users: {r['_count']['users']}" for r in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(roles))]

    elif name == "create-role":
        if not arguments or not all(k in arguments for k in ["name", "permissions_per_module"]): raise ValueError("Missing arguments")
        payload = {"name": arguments["name"], "permissionsPerModule": arguments["permissions_per_module"]}
        data = await make_api_request("POST", f"{BASE_URL}/api/roles", json=payload)
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        role = data["data"]
        return [types.TextContent(type="text", text=f"Role created: {role['name']} (ID: {role['id']})")]

    elif name == "update-role":
        if not arguments or not all(k in arguments for k in ["role_id", "name", "permissions_per_module"]): raise ValueError("Missing arguments")
        payload = {"name": arguments["name"], "permissionsPerModule": arguments["permissions_per_module"]}
        data = await make_api_request("PUT", f"{BASE_URL}/api/roles/{arguments['role_id']}", json=payload)
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        role = data["data"]
        return [types.TextContent(type="text", text=f"Role updated: {role['name']} (ID: {role['id']})")]

    elif name == "delete-role":
        if not arguments or "role_id" not in arguments: raise ValueError("Missing role_id")
        data = await make_api_request("DELETE", f"{BASE_URL}/api/roles/{arguments['role_id']}")
        if not data or "data" not in data: raise ValueError(f"Failed:igm {data.get('error', 'Unknown error')}")
        return [types.TextContent(type="text", text=f"Role deleted (ID: {arguments['role_id']})")]

    elif name == "get-role-histories":
        params = {k: arguments[k] for k in ["limit", "page"] if arguments and k in arguments}
        data = await make_api_request("GET", f"{BASE_URL}/api/roles/histories", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No role histories found")]
        histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']}" for h in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(histories))]

    elif name == "list-favorites-events":
        data = await make_api_request("GET", f"{BASE_URL}/api/favorites-events")
        if not data or "data" not in data: return [types.TextContent(type="text", text="No favorite events found")]
        favorites = [f"Event: {f['event']['title']} | User: {f['user']['firstName']} {f['user']['lastName']} | ID: {f['id']}" for f in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(favorites))]

    elif name == "create-favorite-event":
        if not arguments or not all(k in arguments for k in ["event_id", "user_id"]): raise ValueError("Missing arguments")
        payload = {"eventId": arguments["event_id"], "userId": arguments["user_id"]}
        data = await make_api_request("POST", f"{BASE_URL}/api/favorites-events", json=payload)
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        favorite = data["data"]
        return [types.TextContent(type="text", text=f"Favorite created for event ID: {favorite['eventId']}")]

    elif name == "update-favorite-event":
        if not arguments or not all(k in arguments for k in ["favorite_id", "event_id", "user_id"]): raise ValueError("Missing arguments")
        payload = {"eventId": arguments["event_id"], "userId": arguments["user_id"]}
        data = await make_api_request("PUT", f"{BASE_URL}/api/favorites-events/{arguments['favorite_id']}", json=payload)
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        return [types.TextContent(type="text", text=f"Favorite updated (ID: {arguments['favorite_id']})")]

    elif name == "delete-favorite-event":
        if not arguments or "favorite_id" not in arguments: raise ValueError("Missing favorite_id")
        data = await make_api_request("DELETE", f"{BASE_URL}/api/favorites-events/{arguments['favorite_id']}")
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        return [types.TextContent(type="text", text=f"Favorite deleted (ID: {arguments['favorite_id']})")]

    elif name == "get-favorites-events-histories":
        params = {k合约: arguments[k] for k in ["limit", "page"] if arguments and k in arguments}
        data = await make_api_request("GET", f"{BASE_URL}/api/favorites-events/histories", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No favorites histories found")]
        histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']}" for h in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(histories))]

    elif name == "list-personal-access-tokens":
        params = {"search": arguments.get("search")} if arguments and "search" in arguments else {}
        data = await make_api_request("GET", f"{BASE_URL}/api/personals-accesses-tokens", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No tokens found")]
        tokens = [f"Name: {t['name']} | ID: {t['id']} | Expires: {t.get('expireAt', 'Never')}" for t in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(tokens))]

    elif name == "create-personal-access-token":
        if not arguments or not all(k in arguments for k in ["name", "expire"]): raise ValueError("Missing arguments")
        payload = {"name": arguments["name"], "expire": arguments["expire"]}
        if "expire_at" in arguments: payload["expireAt"] = arguments["expire_at"]
        data = await make_api_request("POST", f"{BASE_URL}/api/personals-accesses-tokens", json=payload)
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        return [types.TextContent(type="text", text=f"Token created: {data['data']}")]

    elif name == "update-personal-access-token":
        if not arguments or not all(k in arguments for k in ["token_id", "name", "expire"]): raise ValueError("Missing arguments")
        payload = {"name": arguments["name"], "expire": arguments["expire"]}
        if "expire_at" in arguments: payload["expireAt"] = arguments["expire_at"]
        data = await make_api_request("PUT", f"{BASE_URL}/api/personals-accesses-tokens/{arguments['token_id']}", json=payload)
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        token = data["data"]
        return [types.TextContent(type="text", text=f"Token updated: {token['name']} (ID: {token['id']})")]

    elif name == "delete-personal-access-token":
        if not arguments or "token_id" not in arguments: raise ValueError("Missing token_id")
        data = await make_api_request("DELETE", f"{BASE_URL}/api/personals-accesses-tokens/{arguments['token_id']}")
        if not data or "data" not in data: raise ValueError(f"Failed: {data.get('error', 'Unknown error')}")
        return [types.TextContent(type="text", text=f"Token deleted (ID: {arguments['token_id']})")]

    elif name == "get-personal-access-token-histories":
        params = {k: arguments[k] for k in ["limit", "page"] if arguments and k in arguments}
        data = await make_api_request("GET", f"{BASE_URL}/api/personals-accesses-tokens/histories", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No token histories found")]
        histories = [f"ID: {h['id']} | Module: {h['module']} | Action: {h['action']}" for h in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(histories))]

    elif name == "list-public-organizations":
        params = {"search": arguments.get("search")} if arguments and "search" in arguments else {}
        data = await make_api_request("GET", f"{BASE_URL}/api/seo/organizations/public", params=params)
        if not data or "data" not in data: return [types.TextContent(type="text", text="No public organizations found")]
        orgs = [f"Name: {o['name']} | ID: {o['id']} | Slug: {o['slug']}" for o in data["data"]]
        return [types.TextContent(type="text", text="\n---\n".join(orgs))]

    elif name == "get-app-version":
        data = await make_api_request("GET", f"{BASE_URL}/app/info/version")
        if not data: return [types.TextContent(type="text", text="Unable to fetch version information")]
        return [types.TextContent(type="text", text=f"App Name: {data['name']} | Version: {data['version']}")]

    elif name == "health-check":
        data = await make_api_request("GET", f"{BASE_URL}/app/info/health-check")
        if not data: return [types.TextContent(type="text", text="Health check failed")]
        return [types.TextContent(type="text", text="Application is healthy")]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="Yala Events Server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )