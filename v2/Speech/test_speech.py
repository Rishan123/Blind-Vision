import subprocess

def espeak(text: str, pitch: int=50) -> int:
    """ Use espeak to convert text to speech. """
    return subprocess.run(['espeak', f'-p {pitch}', text]).returncode

espeak("hello")