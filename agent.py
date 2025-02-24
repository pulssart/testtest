import os
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, WorkerType, cli, multimodal

load_dotenv()

PORT = int(os.getenv('PORT', '8080'))

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LIVEKIT_URL = os.getenv('LIVEKIT_URL')
LIVEKIT_API_KEY = os.getenv('LIVEKIT_API_KEY')
LIVEKIT_API_SECRET = os.getenv('LIVEKIT_API_SECRET')

if not OPENAI_API_KEY:
    raise ValueError('OPENAI_API_KEY must be set')

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
os.environ['LIVEKIT_URL'] = LIVEKIT_URL
os.environ['LIVEKIT_API_KEY'] = LIVEKIT_API_KEY
os.environ['LIVEKIT_API_SECRET'] = LIVEKIT_API_SECRET

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    agent = multimodal.MultimodalAgent(
        model=agents.RealtimeModel(
            instructions='Test',
            voice='alloy',
            temperature=0.8,
            max_response_output_tokens='inf',
            modalities=['text', 'audio'],
            turn_detection=agents.ServerVadOptions(
                threshold=0.5,
                silence_duration_ms=200,
                prefix_padding_ms=300,
            )
        )
    )
    agent.start(ctx.room)

if __name__ == '__main__':
    cli.run_app(WorkerOptions(
        entrypoint_fnc=entrypoint,
        worker_type=WorkerType.ROOM,
        port=PORT
    ))
