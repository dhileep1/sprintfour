import argparse
import os
import shutil
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

# Import modules
import config
from script_gen import generate_script
from audio_gen import generate_audio_sync
from image_gen import generate_image
from video_renderer import check_ffmpeg, get_audio_duration, render_final_video
from subtitle_gen import generate_subtitles

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Audio-First YouTube Shorts Generator")
    parser.add_argument("--idea", required=True, help="Original idea for the video")
    parser.add_argument("--tone", default="Energetic", help="Tone of the narration")
    parser.add_argument("--style", default="Digital Art", help="Visual style for images")
    parser.add_argument("--duration", type=int, default=30, help="Target duration in seconds")
    
    args = parser.parse_args()
    
    # 0. Check Environment
    if not check_ffmpeg():
        console.print("[bold red]Error:[/] FFmpeg not found. Please ensure it is installed.")
        return

    output_dir = "output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    console.print(Panel(f"[bold green]Generating Short:[/] {args.idea}\n[bold blue]Duration:[/] {args.duration}s", title="YouTube Shorts Generator"))

    # 1. Generate Script
    with console.status("[bold blue]Generating Optimized Script...[/]"):
        try:
            script_data = generate_script(args.idea, args.tone, args.style, args.duration)
        except Exception as e:
            console.print(f"[bold red]Script Gen Error:[/] {e}")
            return
            
    meta = script_data.get("meta", {})
    full_narration = meta.get("full_narration", "")
    scenes = script_data.get("scenes", [])
    
    console.print(f"[green]Title:[/] {meta.get('title')}")

    # 2. Generate Master Audio
    master_audio_path = os.path.join(output_dir, "master_audio.mp3")
    with console.status("[bold yellow]Generating Master Voiceover...[/]"):
        try:
             generate_audio_sync(full_narration, master_audio_path)
             master_duration = get_audio_duration(master_audio_path)
             console.print(f"[yellow]Master Audio Duration:[/] {master_duration:.2f}s")
        except Exception as e:
             console.print(f"[bold red]Audio Error:[/] {e}")
             return

    # 3. Calculate Timings
    # Weight = number of words in segment_text
    weights = [len(s.get("segment_text", "").split()) for s in scenes]
    total_weight = sum(weights)
    if total_weight == 0: total_weight = 1 # Avoid div by zero
    
    scene_durations = [(w / total_weight) * master_duration for w in weights]
    
    # 4. Generate Subtitles
    srt_path = os.path.join(output_dir, "subtitles.srt")
    with console.status("[bold cyan]Transcribing for subtitles...[/]"):
        if not generate_subtitles(master_audio_path, srt_path):
            srt_path = None

    # 5. Generate Images
    image_paths = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        img_task = progress.add_task("[green]Generating Scene Images...", total=len(scenes))
        
        for idx, scene in enumerate(scenes):
            scene_id = idx + 1
            img_path = os.path.join(output_dir, f"image_{scene_id}.jpg")
            prompt = scene.get("visual_prompt", "")
            
            progress.update(img_task, description=f"Image {scene_id}/{len(scenes)}")
            if generate_image(prompt, img_path):
                image_paths.append(img_path)
            else:
                image_paths.append(img_path)
            
            progress.advance(img_task)

    # 6. Render Final Video
    final_output = "final_short.mp4"
    bgm_mood = meta.get("bgm_mood", "").lower()
    bgm_path = os.path.join("Audio", f"{bgm_mood}.mp3")
    
    if not os.path.exists(bgm_path):
        console.print(f"[yellow]Warning:[/] BGM mood '{bgm_mood}' not found in Audio folder. Proceeding without BGM.")
        bgm_path = None
    else:
        console.print(f"[blue]BGM Mood:[/] {bgm_mood}")

    with console.status("[bold purple]Stitching video with dynamic timing, BGM & Subtitles...[/]"):
        if render_final_video(image_paths, master_audio_path, final_output, scene_durations, bgm_path=bgm_path, srt_path=srt_path):
            console.print(Panel(f"[bold green]SUCCESS![/] Video saved to [bold]{final_output}[/]", border_style="green"))
        else:
            console.print("[bold red]Failed to stitch master video.[/]")

if __name__ == "__main__":
    main()
