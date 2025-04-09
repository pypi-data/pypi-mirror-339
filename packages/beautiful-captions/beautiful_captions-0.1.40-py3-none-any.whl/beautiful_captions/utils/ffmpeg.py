"""FFmpeg utilities for video and audio processing."""

import logging
from pathlib import Path
from typing import Union, Tuple, Optional
import subprocess
import importlib.resources
import tempfile 
import os      


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

def _get_bundled_fonts_dir() -> Optional[Path]:
    """
    Finds the path to the bundled 'fonts' directory within the package.
    Returns: Path object to the fonts directory, or None if not found.
    """
    try:
        fonts_dir_resource = importlib.resources.files('beautiful_captions').joinpath('fonts')
        with importlib.resources.as_file(fonts_dir_resource) as fonts_dir_path:
            if fonts_dir_path.is_dir():
                 logger.info(f"Successfully found fonts directory via importlib.resources: {fonts_dir_path}")
                 return fonts_dir_path
            else:
                logger.warning(f"Found resource '{fonts_dir_resource}' but it's not a directory.")
                return None
    except Exception as e:
        logger.error(f"Could not locate the bundled fonts directory using importlib.resources: {e}")
        try:
            fallback_path = Path(__file__).parent.parent / "fonts"
            if fallback_path.is_dir():
                logger.warning(f"Using fallback method (__file__) to find fonts directory: {fallback_path}")
                return fallback_path
        except Exception:
             pass
        return None

def combine_video_subtitles(
    video_path: Union[str, Path],
    subtitle_path: Union[str, Path],
    output_path: Union[str, Path],
    cuda: Optional[bool] = False
) -> None:
    """Combine video with ASS subtitles, forcing use of bundled fonts via Fontconfig."""

    fonts_dir_path = _get_bundled_fonts_dir()

    if not fonts_dir_path:
        raise FileNotFoundError("Could not locate the bundled fonts directory for beautiful_captions.")

    abs_fonts_dir = str(fonts_dir_path.resolve()).replace('\\', '/')
    abs_subtitle_path = str(Path(subtitle_path).resolve()).replace('\\', '/')

    str_video_path = str(video_path)
    str_output_path = str(output_path)

    fonts_conf_content = f"""<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>{abs_fonts_dir}</dir>
  <cachedir>/dev/null</cachedir> <!-- Attempt to disable system cache, might be ignored -->
  <config>
    <!-- Reject system font directories - Adjust paths if needed for broader Linux/macOS coverage -->
    <rejectfont><glob>/System/Library/Fonts/*</glob></rejectfont>
    <rejectfont><glob>/Library/Fonts/*</glob></rejectfont>
    <rejectfont><glob>/usr/share/fonts/*</glob></rejectfont>
    <rejectfont><glob>~/.fonts/*</glob></rejectfont>
    <rejectfont><glob>~/.local/share/fonts/*</glob></rejectfont>
  </config>
</fontconfig>
"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.conf', delete=True) as temp_conf_file:
        temp_conf_file.write(fonts_conf_content)
        temp_conf_file.flush() 
        conf_file_path = temp_conf_file.name
        logger.info(f"Using temporary Fontconfig file: {conf_file_path}")

        env = os.environ.copy()
        env['FONTCONFIG_FILE'] = conf_file_path

        try:
            filter_complex = f"ass='{abs_subtitle_path}':fontsdir='{abs_fonts_dir}'"
            if cuda:
                 filter_complex = f"hwdownload,format=nv12,{filter_complex}" 

            cmd = [
                "ffmpeg",
            ]
            if cuda:
                cmd.extend(["-hwaccel", "cuda", "-hwaccel_output_format", "cuda"])
            cmd.extend([
                "-i", str_video_path,
                "-vf", filter_complex,
            ])
            if cuda:
                cmd.extend([
                    "-c:v", "h264_nvenc", "-preset", "medium", "-g", "60", "-keyint_min", "60"
                ])
            else:
                 cmd.extend(["-c:v", "libx264", "-preset", "medium", "-crf", "23"])

            cmd.extend([
                "-c:a", "copy",
                "-movflags", "+faststart", 
                "-y",
                "-loglevel", "error", 
                str_output_path
            ])

            logger.debug(f"Running FFmpeg command with custom fontconfig: {' '.join(cmd)}")

            process = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', env=env)
            logger.info("Subtitles combined with video successfully using custom fontconfig.")
            if process.stdout: logger.debug(f"FFmpeg stdout: {process.stdout}")
            if process.stderr: logger.debug(f"FFmpeg stderr: {process.stderr}")

        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg subtitle combination failed with custom fontconfig. Return code: {e.returncode}")
            logger.error(f"Command: {' '.join(e.cmd)}")
            logger.error(f"Using Fontconfig file: {conf_file_path}")
            try:
                with open(conf_file_path, 'r') as f_read:
                    logger.error(f"Fontconfig file contents:\n{f_read.read()}")
            except Exception:
                 logger.error("Could not read back temporary fontconfig file content.")
            logger.error(f"Stderr: {e.stderr}")
            raise
        except FileNotFoundError as e:
            if "ffmpeg" in str(e):
                 logger.error("FFmpeg command not found. Please ensure FFmpeg is installed and in your system's PATH.")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred during subtitle combination: {e}")
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