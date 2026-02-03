from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
from datetime import datetime, timezone
import json

router = APIRouter()

# Store active WebSocket connections per user
active_connections: Dict[int, Set[WebSocket]] = {}


class ConnectionManager:
    """Manages WebSocket connections for real-time sync"""
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Connect a new WebSocket client"""
        await websocket.accept()
        if user_id not in active_connections:
            active_connections[user_id] = set()
        active_connections[user_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """Disconnect a WebSocket client"""
        if user_id in active_connections:
            active_connections[user_id].discard(websocket)
            if not active_connections[user_id]:
                del active_connections[user_id]
    
    async def broadcast_to_user(self, user_id: int, message: dict):
        """Broadcast a message to all connections for a specific user"""
        if user_id in active_connections:
            disconnected = []
            for connection in active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Error sending to connection: {e}")
                    disconnected.append(connection)
            
            # Clean up disconnected clients
            for connection in disconnected:
                self.disconnect(connection, user_id)
    
    async def broadcast_data_change(self, user_id: int, resource_type: str, action: str, data: dict = None):
        """Notify all clients about a data change"""
        message = {
            "type": "data_change",
            "resource": resource_type,
            "action": action,  # created, updated, deleted
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.broadcast_to_user(user_id, message)


manager = ConnectionManager()


@router.websocket("/ws/sync/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """WebSocket endpoint for real-time synchronization"""
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Receive messages from client (ping/pong, etc.)
            data = await websocket.receive_text()
            
            # Echo back or handle commands
            if data == "ping":
                await websocket.send_text("pong")
            else:
                # Handle other client messages if needed
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


# Helper function to trigger sync notifications
async def notify_data_change(user_id: int, resource_type: str, action: str, data: dict = None):
    """
    Call this function after creating/updating/deleting data to notify all connected clients
    
    Example:
        await notify_data_change(user_id=1, resource_type="transaction", action="created", data={"id": 123})
    """
    await manager.broadcast_data_change(user_id, resource_type, action, data)
