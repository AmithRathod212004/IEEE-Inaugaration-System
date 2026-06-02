import cv2
import numpy as np

# Video parameters
VIDEO_PATH = 'inauguration_video.mp4'
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
FPS = 30
VIDEO_DURATION = 8

def get_text_size(text, font, font_scale, thickness):
    """Get text size for centering"""
    return cv2.getTextSize(text, font, font_scale, thickness)[0]

def put_text_centered(frame, text, y_pos, font, font_scale, color, thickness):
    """Put text centered horizontally with bounds checking"""
    text_size = get_text_size(text, font, font_scale, thickness)
    x_pos = (VIDEO_WIDTH - text_size[0]) // 2
    
    # Ensure text doesn't go beyond screen boundaries
    x_pos = max(10, min(x_pos, VIDEO_WIDTH - text_size[0] - 10))
    y_pos = max(30, min(y_pos, VIDEO_HEIGHT - 20))
    
    cv2.putText(frame, text, (x_pos, y_pos), font, font_scale, color, thickness)

def create_inauguration_video(output_path):
    """Create an inauguration video for IEEE Women's Society"""
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, FPS, (VIDEO_WIDTH, VIDEO_HEIGHT))
    
    total_frames = VIDEO_DURATION * FPS
    
    print(f"Creating inauguration video: {output_path}")
    print(f"Total frames: {total_frames}")
    
    for frame_num in range(total_frames):
        # Create frame
        frame = np.zeros((VIDEO_HEIGHT, VIDEO_WIDTH, 3), dtype=np.uint8)
        
        # Background gradient effect
        for y in range(VIDEO_HEIGHT):
            color_value = int((y / VIDEO_HEIGHT) * 255)
            frame[y, :] = [50, 50 + color_value // 2, 100 + color_value // 3]
        
        # Progress through different scenes
        scene_progress = frame_num / total_frames
        
        if scene_progress < 0.3:  # Scene 1: Title with animation
            alpha = min(scene_progress / 0.15, 1.0)  # Fade in over first 0.15 of scene
            scale = 0.8 + 0.2 * alpha  # Grow from 0.8 to 1.0
            
            overlay = frame.copy()
            
            # Main title with scaling animation (reduced from 2.5 to 1.8)
            font_scale_title = max(1.2, min(1.8 * scale, 1.8))
            put_text_centered(overlay, "IEEE WOMEN'S SOCIETY", 
                            int(VIDEO_HEIGHT // 2 - 80), 
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale_title, (0, 255, 255), 2)
            
            # Subtitle with slight delay and separate animation
            alpha_subtitle = max(min((scene_progress - 0.05) / 0.15, 1.0), 0)
            if alpha_subtitle > 0:
                overlay2 = overlay.copy()
                put_text_centered(overlay2, "Inauguration Ceremony", 
                                int(VIDEO_HEIGHT // 2 + 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 0), 2)
                overlay = cv2.addWeighted(overlay, 1 - alpha_subtitle, overlay2, alpha_subtitle, 0)
            
            frame = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)
            
        elif scene_progress < 0.6:  # Scene 2: Taglines with bounce animation
            local_progress = (scene_progress - 0.3) / 0.3
            bounce = 0.2 * np.sin(local_progress * np.pi * 2)  # Bouncing effect
            
            # Line 1 - Empowering Women
            alpha1 = min(local_progress / 0.2, 1.0)
            if alpha1 > 0:
                overlay1 = frame.copy()
                put_text_centered(overlay1, "Empowering Women in Technology", 
                                int(VIDEO_HEIGHT // 2 - 100 + bounce * 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (100, 255, 200), 2)
                frame = cv2.addWeighted(frame, 1 - alpha1, overlay1, alpha1, 0)
            
            # Line 2 - Vision Impact Innovation
            alpha2 = max(min((local_progress - 0.15) / 0.2, 1.0), 0)
            if alpha2 > 0:
                overlay2 = frame.copy()
                put_text_centered(overlay2, "Vision. Impact. Innovation.", 
                                int(VIDEO_HEIGHT // 2 + 80 - bounce * 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 200, 100), 2)
                frame = cv2.addWeighted(frame, 1 - alpha2, overlay2, alpha2, 0)
            
        else:  # Scene 3: Closing with pulse animation
            local_progress = (scene_progress - 0.6) / 0.4
            
            # Fade in at start
            fade_in_alpha = min(local_progress / 0.2, 1.0)
            # Pulse effect - grows and shrinks
            pulse = 1.0 + 0.15 * np.sin(local_progress * np.pi * 3)
            
            overlay = frame.copy()
            font_scale_welcome = max(2.0, min(2.5 * pulse, 2.5))
            put_text_centered(overlay, "Welcome!", 
                            int(VIDEO_HEIGHT // 2 + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale_welcome, (0, 255, 100), 3)
            frame = cv2.addWeighted(frame, 1 - fade_in_alpha, overlay, fade_in_alpha, 0)
        
        out.write(frame)
        
        if (frame_num + 1) % 30 == 0:
            print(f"  Progress: {frame_num + 1}/{total_frames} frames")
    
    out.release()
    print(f"✓ Inauguration video created: {output_path}")

if __name__ == "__main__":
    create_inauguration_video(VIDEO_PATH)

