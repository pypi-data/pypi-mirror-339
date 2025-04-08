import logging
import httpx
from typing import Dict, Any, List, Optional
from mcp.types import TextContent

from agentmail import AsyncAgentMail
from agentmail.core.api_error import ApiError

logger = logging.getLogger("agentmail_mcp")

client = None

def setup_client(user_api_key: Optional[str] = None):
    """Setup the API client with authentication."""
    global client
    
    # headers = {}
    # if api_key:
    #     headers["Authorization"] = f"Bearer {api_key}"
    
    # client = httpx.AsyncClient(
    #     base_url="https://api.agentmail.to/v0",
    #     headers=headers,
    #     timeout=30.0
    # )
    # return client

    # SDK variation
    client = AsyncAgentMail(
        api_key= user_api_key,
    )
    return client

async def make_api_request(method: str, path: str, **kwargs) -> Dict[str, Any]:
    """Make a request to the AgentMail API"""
    global client
    if client is None:
        error_msg = "Client not initialized. Please call setup_client() first."
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}

    auth_header = client.headers.get("Authorization", "None")
    if auth_header.startswith("Bearer "):
        masked_token = auth_header[:10] + "..." + auth_header[-5:] if len(auth_header) > 15 else "Bearer [token]"
        logger.info(f"Using Authorization: {masked_token}")
    
    try:
        logger.info(f"Making API request: {method.upper()} {path}")
        if method.lower() == "get":
            response = await client.get(path, **kwargs)
        elif method.lower() == "post":
            response = await client.post(path, **kwargs)
        elif method.lower() == "put":
            response = await client.put(path, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        logger.info(f"API response status: {response.status_code}")
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"API response: {result}")
        
        # Check if response is empty or has no meaningful content
        if not result or (isinstance(result, dict) and not any(result.values())):
            return {"message": "The API returned an empty result", "data": result, "status": "success"}
            
        return result
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error: {e.response.status_code} - {e.response.text}"
        logger.error(f"API request error ({method} {path}): {error_msg}")
        return {"error": error_msg, "status": "failed", "status_code": e.response.status_code}
    except httpx.RequestError as e:
        error_msg = f"Request error: {str(e)}"
        logger.error(f"API request error ({method} {path}): {error_msg}")
        return {"error": error_msg, "status": "failed"}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"API request error ({method} {path}): {error_msg}")
        return {"error": error_msg, "status": "failed"}

def register_tools(mcp):
    """Register all email tools with the MCP server."""
    
    # Inbox operations
    @mcp.tool(description="List all inboxes")
    async def list_inboxes(limit: Optional[int] = None, last_key: Optional[str] = None) -> str:
        """
        List all inboxes.
        
        Args:
            limit: Maximum number of inboxes to return
            last_key: Pagination key for retrieving the next set of results
        """
        try:
            result = await client.inboxes.list(limit=limit, last_key=last_key)
        except ApiError as e:
            print(e.status_code)
            print(e.body)
            return f"Error listing inboxes: {e}"

        return str(result)
        
        # if "error" in result:
        #     return f"Error listing inboxes: {result['error']}"
        
        # # Check if we got inboxes or an empty list
        # if "data" in result and isinstance(result["data"], list):
        #     if not result["data"]:
        #         return "No inboxes found. You may need to create an inbox first."
        #     return f"Found {len(result['data'])} inboxes: {result}"
        
        # return str(result)
    
    @mcp.tool(description="Get inbox by ID")
    async def get_inbox(inbox_id: str) -> str:
        """
        Get inbox by ID.
        
        Args:
            inbox_id: ID of the inbox to retrieve
        """
        # result = await make_api_request("GET", f"/inboxes/{inbox_id}")

        # SDK variation
        try:
            result = await client.inboxes.get(inbox_id)
        except ApiError as e:
            return f"Error getting inbox: {e}"
        
        return str(result)
    
    @mcp.tool(description="Create a new inbox")
    async def create_inbox(username: Optional[str] = None, domain: Optional[str] = None, display_name: Optional[str] = None) -> str:
        """
        Create a new inbox. Use default username, domain, and display name unless otherwise specified.
        
        Args:
            username: Email username (optional)
            domain: Email domain (optional)
            display_name: Display name for the inbox (optional)
        """
        # payload = {}
        # if username:
        #     payload["username"] = username
        # if domain:
        #     payload["domain"] = domain
        # if display_name:
        #     payload["display_name"] = display_name
            
        # result = await make_api_request("POST", "/inboxes", json=payload)

        result = await client.inboxes.create(username=username, domain=domain, display_name=display_name)

        return str(result)
    
    # Thread operations
    @mcp.tool(description="List threads by inbox ID")
    async def list_threads(inbox_id: str, limit: Optional[int] = None, last_key: Optional[str] = None, labels: Optional[List[str]] = None) -> str:
        """
        List threads by inbox ID.
        
        Args:
            inbox_id: ID of the inbox
            limit: Maximum number of threads to return
            last_key: Pagination key for retrieving the next set of results
            labels: Filter threads by these labels
        """
        try:
            result = await client.threads.list(inbox_id=inbox_id, limit=limit, last_key=last_key, labels=labels)
        except ApiError as e:
            return f"Error listing threads: {e}"
        
        return str(result)
    
    @mcp.tool(description="Get thread by ID")
    async def get_thread(inbox_id: str, thread_id: str) -> str:
        """
        Get thread by ID.
        
        Args:
            inbox_id: ID of the inbox
            thread_id: ID of the thread to retrieve
        """

        try:
            result = await client.threads.get(inbox_id=inbox_id, thread_id=thread_id)
        except ApiError as e:
            return f"Error getting thread: {e}"
        return str(result)
    
    # Message operations
    @mcp.tool(description="List messages")
    async def list_messages(inbox_id: str, limit: Optional[int] = None, last_key: Optional[str] = None, labels: Optional[List[str]] = None) -> str:
        """
        List messages in an inbox.
        
        Args:
            inbox_id: ID of the inbox
            limit: Maximum number of messages to return
            last_key: Pagination key for retrieving the next set of results
            labels: Filter messages by these labels
        """
        try:
            result = await client.messages.list(inbox_id=inbox_id, limit=limit, last_key=last_key, labels=labels)
        except ApiError as e:
            return f"Error listing messages: {e}"
        
        return str(result)
            
   
    
    @mcp.tool(description="Get message by ID")
    async def get_message(inbox_id: str, message_id: str) -> str:
        """
        Get message by ID.
        
        Args:
            message_id: ID of the message to retrieve
        """
        # result = await make_api_request("GET", f"/inboxes/{inbox_id}/messages/{message_id}")
        # return str(result)

        try:
            result = await client.messages.get(inbox_id=inbox_id, message_id=message_id)
        except ApiError as e:
            return f"Error getting message: {e}"
        
        return str(result)
    
    @mcp.tool(description="Send a message")
    async def send_message(
        inbox_id: str, 
        to: List[str], 
        subject: str, 
        text: str, 
        cc: Optional[List[str]] = None, 
        bcc: Optional[List[str]] = None, 
        html: Optional[str] = None
    ) -> str:
        """
        Send a message.
        
        Args:
            inbox_id: ID of the sending inbox
            to: Recipient email addresses
            subject: Email subject
            body: Email body content
            cc: CC recipients
            bcc: BCC recipients
            html: HTML email body (optional)
        """

        try: 
            result = await client.messages.send(inbox_id=inbox_id, to=to, subject=subject, text=text, cc=cc, bcc=bcc, html=html)
        except ApiError as e:
            return f"Error sending message: {e}"
        
        return str(result)
    
    @mcp.tool(description="Reply to a message")
    async def reply_to_message(
        inbox_id: str,
        message_id: str,
        to: Optional[List[str]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        text: Optional[str] = None,
        html: Optional[str] = None
    ) -> str:
        """
        Reply to a message.
        
        Args:
            inbox_id: ID of the inbox
            message_id: ID of the message to reply to
            to: List of recipient email addresses (optional)
            cc: List of CC recipient email addresses (optional)
            bcc: List of BCC recipient email addresses (optional)
            text: Plain text content of the reply (optional)
            html: HTML content of the reply (optional)
        """
        try:
            result = await client.messages.reply(
                inbox_id=inbox_id,
                message_id=message_id,
                to=to,
                cc=cc,
                bcc=bcc,
                text=text,
                html=html
            )
        except ApiError as e:
            return f"Error replying to message: {e}"
        
        return str(result)
    
    # # Attachment operations
    # @mcp.tool(description="Get attachment by ID")
    # async def get_attachment(inbox_id: str, message_id: str, attachment_id: str) -> str:
    #     """
    #     Get attachment by ID.
        
    #     Args:
    #         attachment_id: ID of the attachment to retrieve
    #     """
    #     # result = await make_api_request("GET", f"/inboxes/{inbox_id}/messages/{message_id}/attachments/{attachment_id}")
    #     # return str(result)
    #     try:
    #         result = await client.get_attachment(inbox_id=inbox_id, message_id=message_id, attachment_id=attachment_id)
    #     except ApiError as e:
    #         return f"Error getting attachment: {e}"
        
    #     return str(result)
    
    logger.info("Email tools registered")

    
    return {
        "list_inboxes": list_inboxes,
        "get_inbox": get_inbox,
        "create_inbox": create_inbox,
        "list_threads": list_threads,
        "get_thread": get_thread,
        "list_messages": list_messages,
        "get_message": get_message,
        "send_message": send_message,
        "reply_to_message": reply_to_message,
        # "get_attachment": get_attachment
    }