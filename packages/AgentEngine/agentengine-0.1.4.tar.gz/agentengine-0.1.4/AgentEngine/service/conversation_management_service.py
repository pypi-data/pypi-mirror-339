import logging
import argparse
import uvicorn
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

from AgentEngine.database.conversation_db import (
    create_conversation,
    create_conversation_message,
    create_message_units,
    get_conversation_list,
    rename_conversation,
    delete_conversation,
    get_conversation_history
)


# 定义请求和响应模型
class MessageUnit(BaseModel):
    type: str
    content: str


class MessageRequest(BaseModel):
    conversation_id: int  # 修改为整数类型，匹配数据库自增ID
    message_idx: int      # 修改为整数类型
    role: str
    message: List[MessageUnit]


class ConversationRequest(BaseModel):
    title: str = "新对话"


class ConversationResponse(BaseModel):
    code: int = 0  # 修改默认值为0
    message: str = "success"
    data: Any


class RenameRequest(BaseModel):
    conversation_id: int
    name: str


def create_conversation_management_app(enable_cors: bool = True) -> FastAPI:
    app = FastAPI(title="Conversation Management Service")
    
    # 配置 CORS
    if enable_cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.put("/conversation/create", response_model=ConversationResponse)
    async def create_new_conversation(request: ConversationRequest):
        """
        创建新的对话
        
        Args:
            request: ConversationRequest对象，包含：
                - title: 对话标题，默认为"新对话"
        
        Returns:
            ConversationResponse对象，包含：
                - conversation_id: 对话ID
                - conversation_title: 对话标题
                - create_time: 创建时间戳（毫秒）
                - update_time: 更新时间戳（毫秒）
        """
        try:
            conversation_data = create_conversation(request.title)
            
            return ConversationResponse(
                code=0,
                message="success",
                data=conversation_data
            )
            
        except Exception as e:
            logging.error(f"创建对话失败: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/conversation/save", response_model=ConversationResponse)
    async def save_message(request: MessageRequest):
        """
        保存一条新的消息记录
        
        Args:
            request: MessageRequest对象，包含：
                - conversation_id: 必填，对话ID（整数类型）
                - message_idx: 消息索引（整数类型）
                - role: 消息角色
                - message: 消息单元列表
        
        Returns:
            ConversationResponse对象：
                - code: 0 表示成功
                - data: true 表示保存成功
                - message: "success" 成功信息
        """
        try:
            message_data = request.model_dump()
            
            # 验证conversation_id
            conversation_id = message_data.get('conversation_id')
            if not conversation_id:
                raise HTTPException(
                    status_code=400, 
                    detail="必须提供conversation_id，请先调用/conversation/create创建对话"
                )
            
            # 创建消息记录
            message_id = create_conversation_message(message_data)
            
            # 创建消息单元记录
            create_message_units(message_data['message'], message_id, conversation_id)
            
            return ConversationResponse(
                code=0,
                message="success",
                data=True
            )
            
        except Exception as e:
            logging.error(f"保存消息失败: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/conversation/list", response_model=ConversationResponse)
    async def list_conversations():
        """
        获取所有对话列表
        
        Returns:
            ConversationResponse对象：
                - code: 0 表示成功
                - data: 对话列表，每个对话包含：
                    - conversation_id: 对话ID
                    - conversation_title: 对话标题
                    - create_time: 创建时间戳（毫秒）
                    - update_time: 更新时间戳（毫秒）
                - message: "success" 成功信息
        """
        try:
            conversations = get_conversation_list()
            
            return ConversationResponse(
                code=0,
                message="success",
                data=conversations
            )
            
        except Exception as e:
            logging.error(f"获取对话列表失败: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/conversation/rename", response_model=ConversationResponse)
    async def rename_conversation_title(request: RenameRequest):
        """
        重命名对话
        
        Args:
            request: RenameRequest对象，包含：
                - conversation_id: 对话ID（整数类型）
                - name: 新的对话标题
        
        Returns:
            ConversationResponse对象：
                - code: 0 表示成功
                - data: true 表示重命名成功
                - message: "success" 成功信息
        """
        try:
            success = rename_conversation(request.conversation_id, request.name)
            
            if not success:
                raise HTTPException(
                    status_code=404,
                    detail=f"对话 {request.conversation_id} 不存在或已删除"
                )
            
            return ConversationResponse(
                code=0,
                message="success",
                data=True
            )
            
        except Exception as e:
            logging.error(f"重命名对话失败: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=str(e))

    @app.delete("/conversation/{conversation_id}", response_model=ConversationResponse)
    async def delete_conversation_by_id(conversation_id: int):
        """
        删除指定的对话
        
        Args:
            conversation_id: 要删除的对话ID（整数类型）
        
        Returns:
            ConversationResponse对象：
                - code: 0 表示成功
                - data: true 表示删除成功
                - message: "success" 成功信息
        """
        try:
            success = delete_conversation(conversation_id)
            
            if not success:
                raise HTTPException(
                    status_code=404,
                    detail=f"对话 {conversation_id} 不存在或已删除"
                )
            
            return ConversationResponse(
                code=0,
                message="success",
                data=True
            )
            
        except Exception as e:
            logging.error(f"删除对话失败: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/conversation/{conversation_id}", response_model=ConversationResponse)
    async def get_conversation_history_by_id(conversation_id: int):
        """
        获取指定对话的完整历史记录
        
        Args:
            conversation_id: 对话ID（整数类型）
        
        Returns:
            ConversationResponse对象：
                - code: 0 表示成功
                - data: 包含完整对话历史的列表，每个对话包含：
                    - conversation_id: 对话ID
                    - create_time: 创建时间戳（毫秒）
                    - message: 消息列表，每条消息包含：
                        - role: 消息角色
                        - message: 消息单元列表，每个单元包含：
                            - type: 单元类型
                            - content: 单元内容
                - message: "success" 成功信息
        """
        try:
            history = get_conversation_history(conversation_id)
            
            if not history:
                raise HTTPException(
                    status_code=404,
                    detail=f"对话 {conversation_id} 不存在或已删除"
                )
            
            return ConversationResponse(
                code=0,
                message="success",
                data=[history]  # 包装在列表中以匹配期望的格式
            )
            
        except Exception as e:
            logging.error(f"获取对话历史失败: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=str(e))

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='运行对话管理服务')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='服务器主机地址')
    parser.add_argument('--port', type=int, default=8005, help='服务器端口')
    parser.add_argument('--no-cors', action='store_true', help='禁用 CORS 中间件')
    args = parser.parse_args()
    
    print(f"Starting conversation management service")
    print(f"Host: {args.host}, Port: {args.port}")
    print(f"CORS middleware: {'disabled' if args.no_cors else 'enabled'}")
    
    app = create_conversation_management_app(
        enable_cors=not args.no_cors
    )
    
    uvicorn.run(app, host=args.host, port=args.port) 