from typing import Dict, List, Any, Optional
import psycopg2.extras
from datetime import datetime
from .client import db_client

def create_conversation(conversation_title: str) -> Dict[str, Any]:
    """
    创建新的对话记录
    
    Args:
        conversation_title: 对话标题
        
    Returns:
        Dict[str, Any]: 包含新创建对话完整信息的字典
    """
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        sql = """
            INSERT INTO agent_engine.conversation_record_t 
            (conversation_title, delete_flag, create_time, update_time)
            VALUES (%s, 'N', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            RETURNING conversation_id, conversation_title, 
                    EXTRACT(EPOCH FROM create_time) * 1000 as create_time,
                    EXTRACT(EPOCH FROM update_time) * 1000 as update_time
        """
        
        cursor.execute(sql, (conversation_title,))
        record = cursor.fetchone()
        conn.commit()
        
        # 转换为字典并确保时间戳为整数
        result = dict(record)
        result['create_time'] = int(result['create_time'])
        result['update_time'] = int(result['update_time'])
        return result
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        db_client.close_connection(conn)

def create_conversation_message(message_data: Dict[str, Any]) -> int:
    """
    创建对话消息记录
    
    Args:
        message_data: 包含消息数据的字典，必须包含以下字段：
            - conversation_id: 对话ID（整数类型）
            - message_idx: 消息索引（整数类型）
            - role: 消息角色
            
    Returns:
        int: 新创建的消息ID（自增ID）
    """
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor()
        
        # 确保conversation_id是整数类型
        conversation_id = int(message_data['conversation_id'])
        message_idx = int(message_data['message_idx'])
        
        sql = """
            INSERT INTO agent_engine.conversation_message_t 
            (conversation_id, message_index, message_role, delete_flag, create_time, update_time)
            VALUES (%s, %s, %s, 'N', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            RETURNING message_id
        """
        
        cursor.execute(sql, (
            conversation_id,  # 确保是整数
            message_idx,      # 确保是整数
            message_data['role']
        ))
        
        message_id = cursor.fetchone()[0]  # 获取返回的ID（整数类型）
        conn.commit()
        return message_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        db_client.close_connection(conn)

def create_message_units(message_units: List[Dict[str, Any]], message_id: int, conversation_id: int) -> bool:
    """
    批量创建消息单元记录
    
    Args:
        message_units: 消息单元列表，每个单元包含:
            - type: 单元类型
            - content: 单元内容
        message_id: 消息ID（整数类型）
        conversation_id: 对话ID（整数类型）
        
    Returns:
        bool: 操作是否成功
    """
    if not message_units:
        return True  # 没有消息单元，视为成功
        
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor()
        
        # 确保ID是整数类型
        message_id = int(message_id)
        conversation_id = int(conversation_id)
        
        sql = """
            INSERT INTO agent_engine.conversation_message_unit_t 
            (message_id, conversation_id, unit_index, unit_type, unit_content, 
             delete_flag, create_time, update_time)
            VALUES (%s, %s, %s, %s, %s, 'N', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        
        # 批量插入所有消息单元
        values = [
            (message_id, conversation_id, idx, unit['type'], unit['content'])
            for idx, unit in enumerate(message_units)
        ]
        
        psycopg2.extras.execute_batch(cursor, sql, values)
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        db_client.close_connection(conn)

def get_conversation(conversation_id: int) -> Optional[Dict[str, Any]]:
    """
    获取对话详情
    
    Args:
        conversation_id: 对话ID（整数类型）
        
    Returns:
        Optional[Dict[str, Any]]: 对话详情，如果不存在则返回None
    """
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # 确保conversation_id是整数类型
        conversation_id = int(conversation_id)
        
        sql = """
            SELECT * FROM agent_engine.conversation_record_t
            WHERE conversation_id = %s AND delete_flag = 'N'
        """
        
        cursor.execute(sql, (conversation_id,))
        record = cursor.fetchone()
        
        if record:
            return dict(record)
        return None
    except Exception as e:
        raise e
    finally:
        db_client.close_connection(conn)

def get_conversation_messages(conversation_id: int) -> List[Dict[str, Any]]:
    """
    获取对话的所有消息
    
    Args:
        conversation_id: 对话ID（整数类型）
        
    Returns:
        List[Dict[str, Any]]: 消息列表，按message_index排序
    """
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # 确保conversation_id是整数类型
        conversation_id = int(conversation_id)
        
        sql = """
            SELECT * FROM agent_engine.conversation_message_t
            WHERE conversation_id = %s AND delete_flag = 'N'
            ORDER BY message_index
        """
        
        cursor.execute(sql, (conversation_id,))
        records = cursor.fetchall()
        return [dict(record) for record in records]
    except Exception as e:
        raise e
    finally:
        db_client.close_connection(conn)

def get_message_units(message_id: int) -> List[Dict[str, Any]]:
    """
    获取消息的所有单元
    
    Args:
        message_id: 消息ID（整数类型）
        
    Returns:
        List[Dict[str, Any]]: 消息单元列表，按unit_index排序
    """
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # 确保message_id是整数类型
        message_id = int(message_id)
        
        sql = """
            SELECT * FROM agent_engine.conversation_message_unit_t
            WHERE message_id = %s AND delete_flag = 'N'
            ORDER BY unit_index
        """
        
        cursor.execute(sql, (message_id,))
        records = cursor.fetchall()
        return [dict(record) for record in records]
    except Exception as e:
        raise e
    finally:
        db_client.close_connection(conn)

def get_conversation_list() -> List[Dict[str, Any]]:
    """
    获取所有未删除的对话列表，按创建时间倒序排序
    
    Returns:
        List[Dict[str, Any]]: 对话列表，每个对话包含id、标题和时间戳信息
    """
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        sql = """
            SELECT 
                conversation_id,
                conversation_title,
                EXTRACT(EPOCH FROM create_time) * 1000 as create_time,
                EXTRACT(EPOCH FROM update_time) * 1000 as update_time
            FROM agent_engine.conversation_record_t
            WHERE delete_flag = 'N'
            ORDER BY create_time DESC
        """
        
        cursor.execute(sql)
        records = cursor.fetchall()
        
        # 转换为字典列表并确保时间戳为整数
        result = []
        for record in records:
            conversation = dict(record)
            conversation['create_time'] = int(conversation['create_time'])
            conversation['update_time'] = int(conversation['update_time'])
            result.append(conversation)
            
        return result
    except Exception as e:
        raise e
    finally:
        db_client.close_connection(conn)

def rename_conversation(conversation_id: int, new_title: str) -> bool:
    """
    重命名对话
    
    Args:
        conversation_id: 对话ID（整数类型）
        new_title: 新的对话标题
        
    Returns:
        bool: 操作是否成功
    """
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor()
        
        sql = """
            UPDATE agent_engine.conversation_record_t
            SET conversation_title = %s, update_time = CURRENT_TIMESTAMP
            WHERE conversation_id = %s AND delete_flag = 'N'
        """
        
        cursor.execute(sql, (new_title, conversation_id))
        affected_rows = cursor.rowcount
        conn.commit()
        
        return affected_rows > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        db_client.close_connection(conn)

def delete_conversation(conversation_id: int) -> bool:
    """
    删除对话（软删除）
    
    Args:
        conversation_id: 对话ID（整数类型）
        
    Returns:
        bool: 操作是否成功
    """
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor()
        
        # 软删除对话记录及其关联的消息和消息单元
        sql_conversation = """
            UPDATE agent_engine.conversation_record_t
            SET delete_flag = 'Y', update_time = CURRENT_TIMESTAMP
            WHERE conversation_id = %s AND delete_flag = 'N'
        """
        
        sql_messages = """
            UPDATE agent_engine.conversation_message_t
            SET delete_flag = 'Y', update_time = CURRENT_TIMESTAMP
            WHERE conversation_id = %s AND delete_flag = 'N'
        """
        
        sql_units = """
            UPDATE agent_engine.conversation_message_unit_t
            SET delete_flag = 'Y', update_time = CURRENT_TIMESTAMP
            WHERE conversation_id = %s AND delete_flag = 'N'
        """
        
        # 执行删除操作
        cursor.execute(sql_conversation, (conversation_id,))
        affected_rows = cursor.rowcount
        
        # 如果对话存在，则删除关联的消息和消息单元
        if affected_rows > 0:
            cursor.execute(sql_messages, (conversation_id,))
            cursor.execute(sql_units, (conversation_id,))
            
        conn.commit()
        return affected_rows > 0
        
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        db_client.close_connection(conn)

def get_conversation_history(conversation_id: int) -> Optional[Dict[str, Any]]:
    """
    获取完整的对话历史，包括所有消息和消息单元
    
    Args:
        conversation_id: 对话ID（整数类型）
        
    Returns:
        Optional[Dict[str, Any]]: 完整的对话历史，如果不存在则返回None
    """
    conn = None
    try:
        conn = db_client.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # 获取对话基本信息
        sql_conversation = """
            SELECT 
                conversation_id,
                EXTRACT(EPOCH FROM create_time) * 1000 as create_time
            FROM agent_engine.conversation_record_t
            WHERE conversation_id = %s AND delete_flag = 'N'
        """
        
        cursor.execute(sql_conversation, (conversation_id,))
        conversation = cursor.fetchone()
        
        if not conversation:
            return None
            
        # 获取所有消息及其消息单元
        sql_messages = """
            SELECT 
                m.message_id,
                m.message_index,
                m.message_role as role,
                u.unit_index,
                u.unit_type as type,
                u.unit_content as content
            FROM agent_engine.conversation_message_t m
            LEFT JOIN agent_engine.conversation_message_unit_t u 
                ON m.message_id = u.message_id
            WHERE m.conversation_id = %s 
                AND m.delete_flag = 'N'
                AND (u.delete_flag = 'N' OR u.delete_flag IS NULL)
            ORDER BY m.message_index, u.unit_index
        """
        
        cursor.execute(sql_messages, (conversation_id,))
        message_records = cursor.fetchall()
        
        # 组织消息数据
        messages = []
        current_message = None
        
        for record in message_records:
            if not current_message or current_message['role'] != record['role']:
                if current_message:
                    messages.append(current_message)
                current_message = {
                    'role': record['role'],
                    'message': []
                }
            
            if record['type'] and record['content']:  # 确保消息单元存在
                current_message['message'].append({
                    'type': record['type'],
                    'content': record['content']
                })
        
        if current_message:  # 添加最后一条消息
            messages.append(current_message)
        
        # 构建最终结果
        result = {
            'conversation_id': str(conversation['conversation_id']),  # 转换为字符串
            'create_time': int(conversation['create_time']),
            'message': messages
        }
        
        return result
    except Exception as e:
        raise e
    finally:
        db_client.close_connection(conn) 