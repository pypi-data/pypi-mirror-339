"""
MiniMax MCP Server

⚠️ IMPORTANT: This server provides access to Minimax API endpoints which may incur costs.
Each tool that makes an API call is marked with a cost warning. Please follow these guidelines:

1. Only use tools when explicitly requested by the user
2. For tools that generate audio, consider the length of the text as it affects costs
3. Some operations like voice cloning or text-to-voice may have higher costs

Tools without cost warnings in their description are free to use as they only read existing data.
"""

import os
import requests
import json
import time
from datetime import datetime
from io import BytesIO
from typing import Literal
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from minimax_mcp.utils import (
    throw_error,
    make_output_path,
    make_output_file,
    handle_input_file,
    play
)

load_dotenv()
api_key = os.getenv("MINIMAX_API_KEY")
base_path = os.getenv("MINIMAX_MCP_BASE_PATH") or os.path.expanduser("~/Desktop")
api_host = os.getenv("MINIMAX_API_HOST")
DEFAULT_VOICE_ID = "female-shaonv"

if not api_key:
    raise ValueError("MINIMAX_API_KEY environment variable is required")


mcp = FastMCP("Minimax")


@mcp.tool(
    description="""Convert text to speech with a given voice and save the output audio file to a given directory.
    Directory is optional, if not provided, the output file will be saved to $HOME/Desktop.
    Only one of voice_id or voice_name can be provided. If none are provided, the default voice will be used.

    ⚠️ COST WARNING: This tool makes an API call to Minimax which may incur costs. Only use when explicitly requested by the user.

     Args:
        text (str): The text to convert to speech.
        voice_id (str, optional): The id of the voice to use.
        model (string, optional): The model to use.
        speed (float, optional): Speed of the generated audio. Controls the speed of the generated speech. Values range from 0.5 to 2.0, with 1.0 being the default speed. 
        vol (float, optional): Volume of the generated audio. Controls the volume of the generated speech. Values range from 0 to 10, with 1 being the default volume.
        pitch (int, optional): Pitch of the generated audio. Controls the speed of the generated speech. Values range from -12 to 12, with 0 being the default speed.
        emotion (str, optional): Emotion of the generated audio. Controls the emotion of the generated speech. Values range ["happy", "sad", "angry", "fearful", "disgusted", "surprised", "neutral"], with "happy" being the default emotion.

    Returns:
        Text content with the path to the output file and name of the voice used.
    """
)
def text_to_speech(
    text: str,
    output_directory: str | None = None,
    voice_id: str = DEFAULT_VOICE_ID,
    model: str = "speech-02-hd",
    speed: float = 1.0,
    vol: float = 1.0,
    pitch: int = 0,
    emotion: str = "happy",
):

    if text == "":
        throw_error("Text is required.")
    format = "wav"
    output_path = make_output_path(output_directory, base_path)
    output_file_name = make_output_file("tts", text, output_path, format)

    url = f"{api_host}/v1/t2a_v2"

    payload = {
        "model": model,
        "text": text,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
            "emotion": emotion
        },
        "audio_setting": {
            "sample_rate": 8000,
            "bitrate": 128000,
            "format": format,
            "channel": 1
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        throw_error(f"Failed to convert text to speech: {response.text}")

    if response.json().get("base_resp",{}).get("status_code") != 0:
        throw_error(f"Failed to convert text to speech: {response.json().get('base_resp',{}).get('status_msg')}")

    response_data = response.json().get('data', {}).get('audio', '')
    if response_data == '':
        throw_error(f"Failed to get audio data from response, traceID:{response.headers.get('Trace-Id')}")

    # 将hex音频数据转换为字节流 (hex->bytes)
    audio_bytes = bytes.fromhex(response_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path / output_file_name, "wb") as f:
        f.write(audio_bytes)

    return TextContent(
        type="text",
        text=f"Success. File saved as: {output_path / output_file_name}. Voice used: {voice_id}",
    )

@mcp.tool(
    description="""List all voices available.

    ⚠️ COST WARNING: This tool makes an API call to Minimax which may incur costs. Only use when explicitly requested by the user.

     Args:
        voice_type (str, optional): The type of voices to list. Values range ["all", "system", "voice_cloning"], with "all" being the default.
    Returns:
        Text content with the list of voices.
    """
)
def list_voices(
    voice_type: str = "all"
):
    url = f'{api_host}/v1/get_voice'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'voice_type': voice_type
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        throw_error(f"Failed to list voices: {response.text}")
    if response.json().get("base_resp",{}).get("status_code") != 0:
        throw_error(f"Failed to list voices: {response.json().get('base_resp',{}).get('status_msg')} {response.headers.get('Trace-Id')}")

    system_voices = response.json().get('system_voice', [])
    voice_cloning_voices = response.json().get('voice_cloning_voice', [])
    voices = system_voices + voice_cloning_voices
    voice_list = []
    for voice in voices:
        voice_list.append(f"Name: {voice.get('voice_name')}, ID: {voice.get('voice_id')}")

    return TextContent(
        type="text",
        text=f"Success. Voices: {voice_list}"
    )

@mcp.tool(
    description="""Clone a voice using provided audio files.

    ⚠️ COST WARNING: This tool makes an API call to Minimax which may incur costs. Only use when explicitly requested by the user.

     Args:
        voice_id (str): The id of the voice to use.
        file (str): The path to the audio file to clone.
    Returns:
        Text content with the voice id of the cloned voice.
    """
)
def voice_clone(
    voice_id: str, file: str) -> TextContent:
    # step1: upload file
    url = f'{api_host}/v1/files/upload'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'purpose': 'voice_clone'
    }
    files = {
        'file': open(file, 'rb')
    }
    response = requests.post(url, headers=headers, data=data, files=files)
    if response.status_code != 200:
        throw_error(f"Failed to upload file: {response.text}")
    file_id = response.json().get("file",{}).get("file_id",0)
    if file_id == 0:
        throw_error(f"Failed to upload file: {response.text}")

    # step2: clone voice
    url = f'{api_host}/v1/voice_clone'
    payload = {
        "file_id": file_id,
        "voice_id": voice_id,
    }
    headers = {
        'Authorization': f'Bearer {api_key}',
        'content-type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        throw_error(f"Failed to clone voice: {response.text}")
    if response.json().get("base_resp",{}).get("status_code") != 0:
        throw_error(f"Failed to clone voice: {response.json().get('base_resp',{}).get('status_msg')}")
    
    return TextContent(
        type="text",
        text=f"""Voice cloned successfully: Voice ID: {voice_id}""",
    )

@mcp.tool(description="Play an audio file. Supports WAV and MP3 formats. Not supports video.")
def play_audio(input_file_path: str) -> TextContent:
    file_path = handle_input_file(input_file_path)
    play(open(file_path, "rb").read())
    return TextContent(type="text", text=f"Successfully played audio file: {file_path}")


@mcp.tool(
    description="""Generate a video from a prompt.

    ⚠️ COST WARNING: This tool makes an API call to Minimax which may incur costs. Only use when explicitly requested by the user.

     Args:
        model (str, optional): The model to use. Values range ["T2V-01", "I2V-01"], with "T2V-01" being the default.
        prompt (str): The prompt to generate the video from.
        output_directory (str, optional): The directory to save the video to.
        first_frame_image (str, optional): The path to the first frame image to use for the video.
    Returns:
        Text content with the path to the output video file.
    """
)
def generate_video(
    model: str = "T2V-01",
    prompt: str = "",
    output_directory: str | None = None,
    first_frame_image: str | None = None,
):
    
    url = f'{api_host}/v1/video_generation'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    payload = json.dumps({
    "model": model, 
    "prompt": prompt,
    })

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        throw_error(f"Failed to generate video: {response.text} {response.headers.get('Trace-Id')}")
    if response.json().get("base_resp",{}).get("status_code") != 0:
        throw_error(f"Failed to generate video: {response.json().get('base_resp',{}).get('status_msg')} {response.headers.get('Trace-Id')}")
    
    task_id = response.json().get("task_id")
    if task_id == "":
        throw_error(f"Failed to generate video: {response.text} {response.headers.get('Trace-Id')}")

    file_id = ""
    # wait for 5 minutes
    for _ in range(30):
        file_id, status = query_video_generation(task_id)
        if status == "Fail":
            throw_error(f"Failed to generate video: task_id {task_id}")
        elif status == "Success":
            break
        time.sleep(10)

    if file_id == "":
        throw_error(f"Failed to generate video: task_id {task_id}")

    
    output_path = make_output_path(output_directory, base_path)
    output_file_name = make_output_file("video", task_id, output_path, "mp4")

    fetch_video_result(file_id, output_file_name)

    return TextContent(
        type="text",
        text=f"Success. Video saved as: {output_file_name}"
    )


def query_video_generation(task_id: str):
    url = f'{api_host}/v1/query/video_generation?task_id={task_id}'
    headers = {
      'Authorization': f'Bearer {api_key}'
    }
    response = requests.request("GET", url, headers=headers)
    status = response.json()['status']
    if status == 'Success':
        return response.json().get('file_id',''), status
    return "", status

def fetch_video_result(file_id: str, output_file_name: str | None = None):
    url = f'{api_host}/v1/files/retrieve?file_id={file_id}'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        throw_error(f"Failed to fetch video result: {response.text}")

    download_url = response.json()['file']['download_url']
    with open(output_file_name, 'wb') as f:
        f.write(requests.get(download_url).content)


def main():
    print("Starting MCP server")
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
