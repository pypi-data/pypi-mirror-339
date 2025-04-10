"""
MiniMax MCP Server

⚠️ IMPORTANT: This server connects to Minimax API endpoints which may involve costs.
Any tool that makes an API call is clearly marked with a cost warning. Please follow these guidelines:

1. Only use these tools when users specifically ask for them
2. For audio generation tools, be mindful that text length affects the cost
3. Voice cloning features are charged upon first use after cloning

Note: Tools without cost warnings are free to use as they only read existing data.
"""

import os
import requests
import json
import time
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from minimax_mcp.utils import (
    throw_error,
    build_output_path,
    build_output_file,
    process_input_file,
    play
)
from minimax_mcp.const import *

load_dotenv()
api_key = os.getenv(ENV_MINIMAX_API_KEY)
base_path = os.getenv(ENV_MINIMAX_MCP_BASE_PATH)
api_host = os.getenv(ENV_MINIMAX_API_HOST)


if not api_key:
    raise ValueError("MINIMAX_API_KEY environment variable is required")
if not api_host:
    raise ValueError("MINIMAX_API_HOST environment variable is required")

mcp = FastMCP("Minimax")


@mcp.tool(
    description="""Convert text to audio with a given voice and save the output audio file to a given directory.
    Directory is optional, if not provided, the output file will be saved to $HOME/Desktop.
    Voice id is optional, if not provided, the default voice will be used.

    COST WARNING: This tool makes an API call to Minimax which may incur costs. Only use when explicitly requested by the user.

     Args:
        text (str): The text to convert to speech.
        voice_id (str, optional): The id of the voice to use.
        model (string, optional): The model to use.
        speed (float, optional): Speed of the generated audio. Controls the speed of the generated speech. Values range from 0.5 to 2.0, with 1.0 being the default speed. 
        vol (float, optional): Volume of the generated audio. Controls the volume of the generated speech. Values range from 0 to 10, with 1 being the default volume.
        pitch (int, optional): Pitch of the generated audio. Controls the speed of the generated speech. Values range from -12 to 12, with 0 being the default speed.
        emotion (str, optional): Emotion of the generated audio. Controls the emotion of the generated speech. Values range ["happy", "sad", "angry", "fearful", "disgusted", "surprised", "neutral"], with "happy" being the default emotion.
        sample_rate (int, optional): Sample rate of the generated audio. Controls the sample rate of the generated speech. Values range [8000,16000,22050,24000,32000,44100] with 32000 being the default sample rate.
        bitrate (int, optional): Bitrate of the generated audio. Controls the bitrate of the generated speech. Values range [32000,64000,128000,256000] with 128000 being the default bitrate.
        channel (int, optional): Channel of the generated audio. Controls the channel of the generated speech. Values range [1, 2] with 1 being the default channel.
        format (str, optional): Format of the generated audio. Controls the format of the generated speech. Values range ["pcm", "mp3","flac"] with "mp3" being the default format.
        language_boost (str, optional): Language boost of the generated audio. Controls the language boost of the generated speech. Values range ['Chinese', 'Chinese,Yue', 'English', 'Arabic', 'Russian', 'Spanish', 'French', 'Portuguese', 'German', 'Turkish', 'Dutch', 'Ukrainian', 'Vietnamese', 'Indonesian', 'Japanese', 'Italian', 'Korean', 'Thai', 'Polish', 'Romanian', 'Greek', 'Czech', 'Finnish', 'Hindi', 'auto'] with "auto" being the default language boost.
    Returns:
        Text content with the path to the output file and name of the voice used.
    """
)
def text_to_audio(
    text: str,
    output_directory: str | None = None,
    voice_id: str = DEFAULT_VOICE_ID,
    model: str = DEFAULT_MODEL,
    speed: float = DEFAULT_SPEED,
    vol: float = DEFAULT_VOLUME,
    pitch: int = DEFAULT_PITCH,
    emotion: str = DEFAULT_EMOTION,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    bitrate: int = DEFAULT_BITRATE,
    channel: int = DEFAULT_CHANNEL,
    format: str = DEFAULT_FORMAT,
    language_boost: str = DEFAULT_LANGUAGE_BOOST,
):

    if text == "":
        throw_error("Text is required.")

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
            "sample_rate": sample_rate,
            "bitrate": bitrate,
            "format": format,
            "channel": channel
        },
        "language_boost": language_boost

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

    # hex->bytes
    audio_bytes = bytes.fromhex(response_data)

    # save audio to file
    output_path = build_output_path(output_directory, base_path)
    output_file_name = build_output_file("t2a", text, output_path, format)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path / output_file_name, "wb") as f:
        f.write(audio_bytes)

    return TextContent(
        type="text",
        text=f"Success. File saved as: {output_path / output_file_name}. Voice used: {voice_id}",
    )

@mcp.tool(
    description="""List all voices available.

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

    COST WARNING: This tool makes an API call to Minimax which may incur costs. Only use when explicitly requested by the user.

     Args:
        voice_id (str): The id of the voice to use.
        file (str): The path to the audio file to clone.
        text (str, optional): The text to use for the demo audio.
    Returns:
        Text content with the voice id of the cloned voice.
    """
)
def voice_clone(
    voice_id: str, 
    file: str,
    text: str,
    output_directory: str | None = None
) -> TextContent:
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
    if text != "":
        payload["text"] = text
        payload["model"] = DEFAULT_MODEL

    headers = {
        'Authorization': f'Bearer {api_key}',
        'content-type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        throw_error(f"Failed to clone voice: {response.text}")
    if response.json().get("base_resp",{}).get("status_code") != 0:
        throw_error(f"Failed to clone voice: {response.json().get('base_resp',{}).get('status_msg')}")
    
    if response.json().get("demo_audio") == "":
        return TextContent(
            type="text",
            text=f"""Voice cloned successfully: Voice ID: {voice_id}""",
        )
    
    # step3: download demo audio
    output_path = build_output_path(output_directory, base_path)
    output_file_name = build_output_file("voice_clone", text, output_path, "wav")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path / output_file_name, "wb") as f:
        f.write(requests.get(response.json().get("demo_audio")).content)

    return TextContent(
        type="text",
        text=f"""Voice cloned successfully: Voice ID: {voice_id}, demo audio saved as: {output_path / output_file_name}""",
    )

@mcp.tool(description="Play an audio file. Supports WAV and MP3 formats. Not supports video.")
def play_audio(input_file_path: str) -> TextContent:
    file_path = process_input_file(input_file_path)
    play(open(file_path, "rb").read())
    return TextContent(type="text", text=f"Successfully played audio file: {file_path}")


@mcp.tool(
    description="""Generate a video from a prompt.

    COST WARNING: This tool makes an API call to Minimax which may incur costs. Only use when explicitly requested by the user.

     Args:
        model (str, optional): The model to use. Values range ["T2V-01", "T2V-01-Director"], with "T2V-01" being the default. "Director" supports inserting instructions for camera movement control.
        prompt (str): The prompt to generate the video from. When use Director model, the promptSupported 15 Camera Movement Instructions (Enumerated Values)
            -Truck: [Truck left], [Truck right]
            -Pan: [Pan left], [Pan right]
            -Push: [Push in], [Pull out]
            -Pedestal: [Pedestal up], [Pedestal down]
            -Tilt: [Tilt up], [Tilt down]
            -Zoom: [Zoom in], [Zoom out]
            -Shake: [Shake]
            -Follow: [Tracking shot]
            -Static: [Static shot]
        output_directory (str, optional): The directory to save the video to.
    Returns:
        Text content with the path to the output video file.
    """
)
def text_to_video(
    model: str = "T2V-01",
    prompt: str = "",
    output_directory: str | None = None,
):
    
    # step1: submit video generation task
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

    # step2: wait for video generation task to complete
    file_id = ""
    # wait for 10 minutes
    for _ in range(60):
        file_id, status = query_video_generation(task_id)
        if status == "Fail":
            throw_error(f"Failed to generate video: task_id {task_id}")
        elif status == "Success":
            break
        time.sleep(10)

    if file_id == "":
        throw_error(f"Failed to generate video: task_id {task_id}")

    # step3: fetch video result
    output_path = build_output_path(output_directory, base_path)
    output_file_name = build_output_file("video", task_id, output_path, "mp4")

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
    response = requests.get(url, headers=headers)
    status = response.json().get('status')
    if status == 'Success':
        return response.json().get('file_id',''), status
    return "", status

def fetch_video_result(file_id: str, output_file_name: str | None = None):
    url = f'{api_host}/v1/files/retrieve?file_id={file_id}'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        throw_error(f"Failed to fetch video result: {response.text}")

    download_url = response.json().get('file',{}).get('download_url')
    if download_url == "":
        throw_error(f"Failed to fetch video result: {response.text}")

    with open(output_file_name, 'wb') as f:
        f.write(requests.get(download_url).content)


def main():
    print("Starting Minimax MCP server")
    """Run the Minimax MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
