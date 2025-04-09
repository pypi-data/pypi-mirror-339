"""FFmpeg utilities for video and audio processing."""

import logging
from pathlib import Path
from typing import Union, Tuple, Optional
import subprocess
from ..styling.style import FontManager
import platform
import shutil

logger = logging.getLogger(__name__)

def extract_audio(video_path: Union[str, Path], output_path: Union[str, Path]) -> None:
    """Extract audio from video file.
    
    Args:
        video_path: Input video file path
        output_path: Output audio file path
    
    Raises:
        subprocess.CalledProcessError: If FFmpeg command fails
    """
    try:
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vn',  # No video
            '-acodec', 'aac',
            '-b:a', '192k',
            '-y',  # Overwrite output file
            str(output_path)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info("Audio extracted successfully")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg audio extraction failed: {e.stderr}")
        raise

def combine_video_subtitles(
    video_path: Union[str, Path],
    subtitle_path: Union[str, Path],
    output_path: Union[str, Path],
    cuda: Optional[bool] = False
) -> None:
    """Combine video with ASS subtitles.
    
    Args:
        video_path: Input videeo file path
        subtitle_path: ASS subtitle file path
        output_path: Output video file path
    
    Raises:
        subprocess.CalledProcessError: If FFmpeg command fails
    """
    try:
        font_manager = FontManager()
        print(f"Font directory: {font_manager.font_dir}")
        print(f"Available fonts: {font_manager.list_fonts()}")
        print(f"KOMIKAX_ font path: {font_manager.get_font_path('KOMIKAX_')}")

        fonts_dir_path = str(font_manager.font_dir.resolve())  # Get absolute path
        escaped_fonts_dir = str(fonts_dir_path).replace('\\', '/').replace(':', '\\:')
        ensure_font_available(fonts_dir_path)

        if cuda:
            cmd = [
                "ffmpeg",
                "-hwaccel", "cuda",
                "-hwaccel_output_format", "cuda",
                "-i", str(video_path),
                "-vf", f"hwdownload,format=nv12,ass={subtitle_path}:fontsdir={escaped_fonts_dir}",
                "-c:v", "h264_nvenc",
                "-preset", "medium",
                "-g", "60",
                "-keyint_min", "60",
                "-c:a", "copy",
                "-y",
                "-loglevel", "error",  # Only show errors
                output_path
            ]
        else:
            cmd = [
                "ffmpeg",
                "-i", str(video_path),
                "-vf", f"ass={subtitle_path}:fontsdir={escaped_fonts_dir}",
                "-c:a", "copy",  # Copy audio stream
                "-preset", "medium",  # Encoding preset
                "-movflags", "+faststart",  # Enable fast start for web playback
                "-y",  # Overwrite output file
                "-loglevel", "error",  # Only show errors
                str(output_path)
            ]
        
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info("Subtitles combined with video successfully")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg subtitle combination failed: {e.stderr}")
        raise

def get_video_duration(video_path: Union[str, Path]) -> float:
    """Get video duration in seconds.
    
    Args:
        video_path: Input video file path
        
    Returns:
        Duration in seconds
        
    Raises:
        subprocess.CalledProcessError: If FFmpeg command fails
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(video_path)
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        duration = float(result.stdout.strip())
        return duration
        
    except subprocess.CalledProcessError as e:
        logger.error(f"FFprobe duration check failed: {e.stderr}")
        raise

def get_video_dimensions(video_path: Union[str, Path]) -> Tuple[int, int]:
    """Get video width and height.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Tuple of (width, height)
        
    Raises:
        subprocess.CalledProcessError: If FFmpeg command fails
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=s=x:p=0',
            str(video_path)
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        width, height = map(int, result.stdout.strip().split('x'))
        return width, height
        
    except subprocess.CalledProcessError as e:
        logger.error(f"FFprobe dimension check failed: {e.stderr}")
        raise

def ensure_font_available(font_path):
    """Ensure a font is available to the system by temporarily installing it if needed."""
    system = platform.system()
    font_path = Path(font_path)
    
    if system == "Darwin":  # macOS
        # Copy to user fonts directory
        user_font_dir = Path.home() / "Library" / "Fonts"
        user_font_dir.mkdir(exist_ok=True, parents=True)
        
        # Create a temporary copy if it doesn't exist
        temp_font_path = user_font_dir / font_path.name
        if not temp_font_path.exists():
            shutil.copy2(font_path, temp_font_path)
            return temp_font_path
    
    return font_path