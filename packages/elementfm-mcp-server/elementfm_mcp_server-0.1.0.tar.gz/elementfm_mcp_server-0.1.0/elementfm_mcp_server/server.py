# server.py
from mcp.server.fastmcp import FastMCP
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
import requests
import sys

# Set default frontend URL
FRONTEND_ROOT_URL = os.getenv('FRONTEND_ROOT_URL', 'https://app.element.fm')

# Create an MCP server
mcp = FastMCP("elementfm-mcp-server")

# Pydantic models for request/response types
class Workspace(BaseModel):
    id: str
    name: str

class Show(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    artwork_url: Optional[str] = None

class Episode(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    audio_url: Optional[str] = None
    show_id: str

# Workspace endpoints
@mcp.tool()
def list_workspaces() -> List[Workspace]:
    """List all workspaces"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
        
    # Make request to frontend API
    response = requests.get(
        f"{FRONTEND_ROOT_URL}/api/workspaces",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to list of Workspace objects
    workspaces_data = response.json()
    return [Workspace(**workspace) for workspace in workspaces_data]

@mcp.tool()
def create_workspace(name: str) -> Workspace:
    """Create a new workspace"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Implementation will be added
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"name": name}
    )
    response.raise_for_status()
    
    # Convert response data to Workspace object
    workspace_data = response.json()
    return Workspace(**workspace_data)

@mcp.tool()
def get_workspace_by_id(workspace_id: str) -> Workspace:
    """Get a workspace by ID"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Implementation will be added
    # Make request to frontend API
    response = requests.get(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to Workspace object
    workspace_data = response.json()
    return Workspace(**workspace_data)

# Show endpoints
@mcp.tool()
def list_shows() -> List[Show]:
    """List all shows"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.get(
        f"{FRONTEND_ROOT_URL}/api/shows",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()

    # Convert response data to list of Show objects
    shows_data = response.json()
    return [Show(**show) for show in shows_data]

@mcp.tool()
def create_show(title: str, description: Optional[str] = None) -> Show:
    """Create a new show"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/shows",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"title": title, "description": description}
    )
    response.raise_for_status()

    # Convert response data to Show object
    show_data = response.json()
    return Show(**show_data)

@mcp.tool()
def get_show_by_id(show_id: str) -> Show:
    """Get a show by ID"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.get(
        f"{FRONTEND_ROOT_URL}/api/shows/{show_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to Show object
    show_data = response.json()
    return Show(**show_data)

@mcp.tool()
def update_show(workspace_id: str, show_id: str, title: Optional[str] = None, 
                description: Optional[str] = None, author: Optional[str] = None, link: Optional[str] = None, language: Optional[str] = None, copyright: Optional[str] = None, category: Optional[str] = None, funding_url: Optional[str] = None, funding_text: Optional[str] = None, email: Optional[str] = None, explicit: Optional[bool] = None) -> Show:
    """Update a show"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.patch(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "name": title,
            "author": author, 
            "description": description,
            "explicit": explicit,
            "link": link,
            "language": language, 
            "copyright": copyright,
            "category": category,
            "funding_url": funding_url,
            "funding_text": funding_text,
            "email": email
        }
    )
    response.raise_for_status()
    
    # Convert response data to Show object
    show_data = response.json()
    return Show(**show_data)

# Episode endpoints
@mcp.tool()
def list_episodes(workspace_id: str, show_id: str) -> List[Episode]:
    """List all episodes for a show"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.get(
            f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to list of Episode objects
    episodes_data = response.json()
    return [Episode(**episode) for episode in episodes_data]

@mcp.tool()
def create_episode(workspace_id: str, show_id: str, title: str, 
                  description: Optional[str] = None) -> Episode:
    """Create a new episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"title": title, "show_id": show_id, "description": description}
    )
    response.raise_for_status()
    
    # Convert response data to Episode object
    episode_data = response.json()
    return Episode(**episode_data)

@mcp.tool()
def get_episode_by_id(workspace_id: str, show_id: str, episode_id: str) -> Episode:
    """Get an episode by ID"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.get(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to Episode object
    episode_data = response.json()
    return Episode(**episode_data)

@mcp.tool()
def update_episode(workspace_id: str, show_id: str, episode_id: str, title: Optional[str] = None,
                  description: Optional[str] = None) -> Episode:
    """Update an episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.patch(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"title": title, "description": description}
    )
    response.raise_for_status()
    
    # Convert response data to Episode object
    episode_data = response.json()
    return Episode(**episode_data)

@mcp.tool()
def publish_episode(workspace_id: str, show_id: str, episode_id: str) -> Dict[str, Any]:
    """Publish an episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}/publish",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to Episode object
    episode_data = response.json()
    return Episode(**episode_data)


# AI features
@mcp.tool()
def transcribe_audio(workspace_id: str, show_id: str, episode_id: str) -> Dict[str, Any]:
    """Transcribe audio for an episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}/transcribe",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to Episode object
    episode_data = response.json()
    return Episode(**episode_data)

@mcp.tool()
def generate_ai_chapters(workspace_id: str, show_id: str, episode_id: str) -> Dict[str, Any]:
    """Generate AI chapters for an episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}/autochapter",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to Episode object
    episode_data = response.json()
    return Episode(**episode_data)

@mcp.tool()
def generate_ai_show_notes(workspace_id: str, show_id: str, episode_id: str) -> Dict[str, Any]:
    """Generate AI show notes for an episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}/summarize",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to Episode object
    episode_data = response.json()
    return Episode(**episode_data)

# Workspace invitation endpoints
@mcp.tool()
def list_invitations() -> List[Dict[str, Any]]:
    """List workspace invitations"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.get(
        f"{FRONTEND_ROOT_URL}/api/workspaces/invitations",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to list of invitations
    invitations_data = response.json()
    return [Dict[str, Any](**invitation) for invitation in invitations_data]

@mcp.tool()
def send_workspace_invite(workspace_id: str, invitee_email: str) -> Dict[str, Any]:
    """Send a workspace invitation"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/invite",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"invitee_email": invitee_email}
    )
    response.raise_for_status()
    
    # Convert response data to invitation object
    invitation_data = response.json()
    return Dict[str, Any](**invitation_data)

@mcp.tool()
def accept_invite(invitation_id: str, invitee_email: str) -> Dict[str, Any]:
    """Accept a workspace invitation"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.patch(
        f"{FRONTEND_ROOT_URL}/api/workspaces/invitations/{invitation_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"invitee_email": invitee_email}
    )
    response.raise_for_status()
    
    # Convert response data to invitation object
    invitation_data = response.json()
    return Dict[str, Any](**invitation_data)

# Recipient endpoints
@mcp.tool()
def create_recipient(workspace_id: str, name: str, wallet_address: str) -> Dict[str, Any]:
    """Create a new recipient"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/recipients",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "name": name,
            "wallet_address": wallet_address
        }
    )
    response.raise_for_status()
    
    # Convert response data to recipient object
    recipient_data = response.json()
    return Dict[str, Any](**recipient_data)

@mcp.tool()
def search_workspace(workspace_id: str, query: str) -> Dict[str, Any]:
    """Search within a workspace"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    
    # Make request to frontend API
    response = requests.get(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/search",
        headers={"Authorization": f"Bearer {api_key}"},
        params={"q": query}
    )
    response.raise_for_status()
    
    # Return search results
    return response.json()

def main():
    """Entry point for the MCP server"""
    import sys
    t = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    if t not in ["stdio", "sse"]:
        t = "stdio"
    print(f"Running MCP server with transport: {t}")
    mcp.run(transport=t)

if __name__ == "__main__":
    main()