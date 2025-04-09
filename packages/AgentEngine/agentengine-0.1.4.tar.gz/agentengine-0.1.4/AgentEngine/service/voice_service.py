import argparse
import logging
from pathlib import Path
from typing import Optional, Union
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from AgentEngine.core.models.stt_model import STTModel, STTConfig
from AgentEngine.core.models.tts_model import TTSModel, TTSConfig

class VoiceService:
    """Unified voice service that hosts both STT and TTS on a single FastAPI application"""
    
    def __init__(self, 
                 stt_config: Optional[STTConfig] = None, 
                 tts_config: Optional[TTSConfig] = None,
                 env_file: Optional[Union[str, Path]] = None,
                 enable_cors: bool = True):
        """
        Initialize the voice service with STT and TTS configurations.
        
        Args:
            stt_config: STT configuration. If None, loads from environment.
            tts_config: TTS configuration. If None, loads from environment.
            env_file: Optional path to .env file with configuration.
            enable_cors: Whether to enable CORS middleware
        """
        # Load configurations from environment if not provided
        if env_file:
            load_dotenv(env_file)
            
        self.stt_config = stt_config or STTConfig.from_env()
        self.tts_config = tts_config or TTSConfig.from_env()
        
        # Initialize models
        self.stt_model = STTModel(self.stt_config)
        self.tts_model = TTSModel(self.tts_config)
        
        print(f"STT Config: {self.stt_config}")
        print(f"TTS Config: {self.tts_config}")
        
        # Create FastAPI application
        self.app = FastAPI(
            title="Voice Services API",
            description="Unified API for Speech-to-Text and Text-to-Speech services"
        )
        
        # Add CORS middleware if enabled
        if enable_cors:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],  # Allow all origins
                allow_credentials=True,
                allow_methods=["*"],  # Allow all methods
                allow_headers=["*"],  # Allow all headers
            )
        
        # Set up routes
        self._setup_routes()
        
    def _setup_routes(self):
        """Configure API routes for voice services"""
        
        # STT WebSocket route
        @self.app.websocket("/stt/ws")
        async def stt_websocket(websocket: WebSocket):
            """WebSocket endpoint for real-time audio streaming and STT"""
            print("STT WebSocket connection attempt...")
            await websocket.accept()
            print("STT WebSocket connection accepted")
            try:
                # Start streaming session
                await self.stt_model.start_streaming_session(websocket)
            except Exception as e:
                print(f"STT WebSocket error: {str(e)}")
                import traceback
                traceback.print_exc()
                try:
                    await websocket.send_json({"error": str(e)})
                except:
                    pass
            finally:
                print("STT WebSocket connection closed")
                
        # TTS WebSocket route
        @self.app.websocket("/tts/ws")
        async def tts_websocket(websocket: WebSocket):
            """WebSocket endpoint for streaming TTS"""
            print("TTS WebSocket connection attempt...")
            await websocket.accept()
            print("TTS WebSocket connection accepted")
            try:
                while True:
                    # Receive text from client
                    data = await websocket.receive_json()
                    text = data.get("text")
                    if not text:
                        await websocket.send_json({"error": "No text provided"})
                        continue

                    # Generate and stream audio chunks
                    try:
                        # First try to use it as a coroutine that returns an async iterator
                        speech_result = await self.tts_model.generate_speech(text, stream=True)
                        
                        # Check if it's an async iterator or a regular iterable
                        if hasattr(speech_result, '__aiter__'):
                            # It's an async iterator, use async for
                            async for chunk in speech_result:
                                await websocket.send_bytes(chunk)
                        elif hasattr(speech_result, '__iter__'):
                            # It's a regular iterator, use normal for
                            for chunk in speech_result:
                                await websocket.send_bytes(chunk)
                        else:
                            # It's a single chunk, send it directly
                            await websocket.send_bytes(speech_result)
                            
                    except TypeError as te:
                        # If speech_result is still a coroutine, try calling it directly without stream=True
                        if "async for" in str(te) and "requires an object with __aiter__" in str(te):
                            print("Falling back to non-streaming TTS")
                            speech_data = await self.tts_model.generate_speech(text, stream=False)
                            await websocket.send_bytes(speech_data)
                        else:
                            raise

                    # Send end marker after successful TTS generation
                    await websocket.send_json({"status": "completed"})

            except Exception as e:
                print(f"TTS WebSocket error: {str(e)}")
                import traceback
                traceback.print_exc()
                try:
                    await websocket.send_json({"error": str(e)})
                except:
                    pass
            finally:
                print("TTS WebSocket connection closed")
    
    async def check_connectivity(self, model_type: str) -> bool:
        """
        检查语音服务（STT和TTS）的连接状态

        Args:
            model_type: 要检查的模型类型，可选值为'stt', 'tts'
        
        Returns:
            bool: 所有服务连接正常返回True，任一服务连接失败返回False
        """
        try:
            stt_connected = False
            tts_connected = False

            if model_type == 'stt':
                stt_connected = await self.stt_model.check_connectivity()
                if not stt_connected:
                    logging.error("语音识别(STT)服务连接失败")
            
            if model_type == 'tts':
                tts_connected = await self.tts_model.check_connectivity()
                if not tts_connected:
                    logging.error("语音合成(TTS)服务连接失败")
            
            # 根据model_type返回相应的连接状态
            if model_type == 'stt':
                return stt_connected
            elif model_type == 'tts':
                return tts_connected
            else:
                logging.error(f"未知的模型类型: {model_type}")
                return False

        except Exception as e:
            logging.error(f"语音服务连接测试发生异常: {str(e)}")
            return False


def create_voice_app(
    stt_config: Optional[STTConfig] = None,
    tts_config: Optional[TTSConfig] = None,
    env_file: Optional[Union[str, Path]] = None,
    enable_cors: bool = True
) -> FastAPI:
    """
    Create a FastAPI application with unified voice services.
    
    Args:
        stt_config: Optional STT configuration
        tts_config: Optional TTS configuration
        env_file: Optional path to .env file
        enable_cors: Whether to enable CORS middleware
        
    Returns:
        FastAPI: The configured FastAPI application
    """
    service = VoiceService(stt_config, tts_config, env_file, enable_cors)
    return service.app


if __name__ == "__main__":
    import uvicorn
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run unified voice services (STT and TTS)')
    parser.add_argument('--env', type=str, help='Path to .env file with configuration')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind server to')
    parser.add_argument('--port', type=int, default=8004, help='Port to bind server to')
    parser.add_argument('--no-cors', action='store_true', help='Disable CORS middleware')
    args = parser.parse_args()
    
    # Print startup information
    print(f"Starting unified voice service (STT & TTS)")
    print(f"Host: {args.host}, Port: {args.port}")
    print(f"CORS middleware: {'disabled' if args.no_cors else 'enabled'}")
    if args.env:
        print(f"Using environment file: {args.env}")
    
    # Create and run the FastAPI app
    app = create_voice_app(
        env_file=args.env,
        enable_cors=not args.no_cors
    )
    
    # Run the server
    uvicorn.run(app, host=args.host, port=args.port) 