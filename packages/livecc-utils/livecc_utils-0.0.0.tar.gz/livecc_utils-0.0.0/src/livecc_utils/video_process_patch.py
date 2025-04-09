# NOTE: Some parts were borrowed from qwen2_vl_utils. We modified them for better use in LiveCC.
# Feel free to contact joyachen@u.nus.edu for any problems. Thank you!

import os, torch, functools
import numpy as np
import decord # NOTE: import decord should be after torch, otherwise seg fault
from transformers import Qwen2VLForConditionalGeneration, logging
from torchvision import transforms

os.environ['FORCE_QWENVL_VIDEO_READER'] = 'decord+'
os.environ['VIDEO_MAX_PIXELS'] = str(int(os.environ.get('VIDEO_MAX_PIXELS', 24576 * 28 * 28))) # increase this for streaming. 24576 * 28 * 28 = 19267584
import qwen_vl_utils.vision_process
qwen_vl_utils.vision_process.VIDEO_MIN_PIXELS = int(os.environ.get('VIDEO_MIN_PIXELS', 100 * 28 * 28)) # follow qwen2vl paper
qwen_vl_utils.vision_process.FPS_MAX_FRAMES = int(os.environ.get('FPS_MAX_FRAMES', 480)) # decrease this for efficiency 
from qwen_vl_utils.vision_process import (
    FORCE_QWENVL_VIDEO_READER, VIDEO_TOTAL_PIXELS, FPS_MAX_FRAMES, VIDEO_MIN_PIXELS, VIDEO_MAX_PIXELS, FRAME_FACTOR, IMAGE_FACTOR, FPS,
    process_vision_info, smart_nframes, smart_resize
)

logger = logging.get_logger(__name__)

logger.warning(f'{__name__}: {FORCE_QWENVL_VIDEO_READER=}, {FPS_MAX_FRAMES=}, {VIDEO_MIN_PIXELS=}, {VIDEO_TOTAL_PIXELS=}')

def _read_video_decord_plus(ele: dict, strict_fps: bool = False, drop_last: bool = True, return_pts: bool = False):
    """read video using decord.VideoReader. can handle more cases compared to _read_video_decord.

    Args:
        ele (dict): a dict contains the configuration of video.
        support keys:
            - video: the path of video. support "file://", "http://", "https://" and local path.
            - video_start: the start time of video.
            - video_end: the end time of video.
    Returns:
        torch.Tensor: the video tensor with shape (T, C, H, W).
        sample_fps
        clip_pts if return_pts=True
    """
    video_path = ele["video"]
    vr = decord.VideoReader(video_path, num_threads=2)
    video_start = ele.get('video_start', None)
    video_end = ele.get('video_end', None)
    video_fps = vr.get_avg_fps()
    clip_idxs, clip_pts = None, None
    if video_start is not None or video_end is not None:
        vr.get_frame_timestamp(0)
        video_pts = vr._frame_pts[:,1]
        video_start = video_pts[0] if not video_start else video_start
        video_end = video_pts[-1] if not video_end else video_end
        clip_idxs = ((video_start <= video_pts) & (video_pts <= video_end)).nonzero()[0]
        clip_pts = video_pts[clip_idxs]
        total_frames = len(clip_idxs)
    else:
        total_frames = len(vr)
    if not strict_fps:
        nframes = smart_nframes(ele, total_frames=total_frames, video_fps=video_fps)
        nframes_idxs = np.linspace(0, total_frames - 1, nframes).round().astype(int)
        clip_idxs = nframes_idxs if clip_idxs is None else clip_idxs[nframes_idxs]
    else:
        if clip_pts is None: # no video_start/video_end
            vr.get_frame_timestamp(0)
            clip_pts = vr._frame_pts[:,1]
            clip_idxs = np.arange(len(clip_pts))
        expected_timestamps = np.arange(clip_pts[0], clip_pts[-1] + 1e-6, 1 / FPS)
        if len(expected_timestamps) > FPS_MAX_FRAMES:
            if drop_last:
                expected_timestamps = expected_timestamps[:FPS_MAX_FRAMES]
            else:
                expected_timestamps = expected_timestamps[np.linspace(0, len(expected_timestamps) - 1, FPS_MAX_FRAMES).round().astype(int)]
        expected_idxs_for_clip_pts = (expected_timestamps[:, None] <= clip_pts).argmax(axis=1)
        clip_pts, clip_idxs = clip_pts[expected_idxs_for_clip_pts].tolist(), clip_idxs[expected_idxs_for_clip_pts].tolist()
        while len(clip_idxs) % FRAME_FACTOR != 0:
            clip_idxs.append(clip_idxs[-1])
            clip_pts.append(clip_pts[-1])
    clip = torch.from_numpy(vr.get_batch(clip_idxs).asnumpy()).permute(0, 3, 1, 2)  # Convert to TCHW format
    sample_fps = len(clip_idxs) / max(total_frames, 1e-6) * video_fps
    if return_pts:
        return clip, sample_fps, clip_pts
    return clip, sample_fps

from qwen_vl_utils.vision_process import VIDEO_READER_BACKENDS
_video_reader_backend = VIDEO_READER_BACKENDS['decord+'] = _read_video_decord_plus

def _spatial_resize_video(video: torch.Tensor, nframes: int = None):
    if not nframes:
        nframes, _, height, width = video.shape
    else:
        height, width = video.shape[2:]
    max_pixels = max(min(VIDEO_MAX_PIXELS, VIDEO_TOTAL_PIXELS / nframes * FRAME_FACTOR), int(VIDEO_MIN_PIXELS * 1.05))
    resized_height, resized_width = smart_resize(
        height,
        width,
        factor=IMAGE_FACTOR,
        min_pixels=VIDEO_MIN_PIXELS,
        max_pixels=max_pixels,
    )
    video = transforms.functional.resize(
        video,
        [resized_height, resized_width],
        interpolation=transforms.InterpolationMode.BICUBIC,
        antialias=True,
    ).float() # need float?
    return video

def get_smart_resized_video_reader(video_path: str, max_pixels: int = None):
    video_reader = decord.VideoReader(video_path)
    nframes = min(len(video_reader), FPS_MAX_FRAMES)
    height, width, _ = video_reader.next().shape

    if max_pixels is None:
        max_pixels = max(min(VIDEO_MAX_PIXELS, VIDEO_TOTAL_PIXELS / nframes * FRAME_FACTOR), int(VIDEO_MIN_PIXELS * 1.05))
    resized_height, resized_width = smart_resize(
        height,
        width,
        factor=IMAGE_FACTOR,
        min_pixels=VIDEO_MIN_PIXELS,
        max_pixels=max_pixels,
    )
    video_reader = decord.VideoReader(video_path, num_threads=2)
    return video_reader, resized_height, resized_width

def get_smart_resized_clip(
    video_reader: decord.VideoReader, 
    resized_height: int,
    resized_width: int,
    timestamps: torch.Tensor, 
    video_pts: np.ndarray, 
    video_pts_index_from: int = 0, 
):
    while len(timestamps) % FRAME_FACTOR != 0:
        timestamps = torch.cat([timestamps, timestamps[-1:] + 1 / FPS])
    clip_idxs = []
    for timestamp in timestamps:
        while video_pts_index_from < len(video_pts) and video_pts[video_pts_index_from] < timestamp:
            video_pts_index_from += 1
        if video_pts_index_from >= len(video_pts):
            break
        clip_idxs.append(video_pts_index_from)
    while len(clip_idxs) % FRAME_FACTOR != 0:
        clip_idxs = clip_idxs[:-1]
        timestamps = timestamps[:-1]
    clip = torch.from_numpy(video_reader.get_batch(clip_idxs).asnumpy()).permute(0, 3, 1 ,2)
    clip = transforms.functional.resize(
        clip,
        [resized_height, resized_width],
        interpolation=transforms.InterpolationMode.BICUBIC,
        antialias=True,
    )
    return clip, timestamps, clip_idxs

def video_qa(model, processor, video_path: str, query: str, answer_prefix: str = '', video_start: float = None, video_end: float = None, max_new_tokens: int = 128, strict_fps: bool = False, strict_abcd: bool = False):
    if strict_fps:
        video_inputs, _ = _video_reader_backend({'video': video_path, 'video_start': video_start, 'video_end': video_end}, strict_fps=True, drop_last=False)
        video_inputs = _spatial_resize_video(video_inputs)
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "video", "video": video_inputs},
                    {"type": "text", "text": query},
                ],
            }
        ]
        image_inputs = None
    else:
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "video", "video": video_path, "video_start": video_start, "video_end": video_end},
                    {"type": "text", "text": query},
                ],
            }
        ]
        image_inputs, video_inputs = process_vision_info(conversation)
    text = processor.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True) + answer_prefix
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")
    if not strict_abcd:
        generated_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)
        output_text = processor.decode(generated_ids[0, inputs.input_ids.size(1):], clean_up_tokenization_spaces=False)
    else:
        ABCD_ids = torch.tensor([362, 425, 356, 422], device='cuda', dtype=torch.long)
        outputs = model.generate(**inputs, do_sample=False, max_new_tokens=1, return_dict_in_generate=True, output_scores=True)
        output_text = ['A', 'B', 'C', 'D'][outputs.scores[0][0, ABCD_ids].argmax()]
    return output_text

def video_cc(model, processor, video_path: str, query: str, video_start: float = None, video_end: float = None, max_new_tokens: int = 16):
    video, _ = _video_reader_backend({'video': video_path, 'video_start': video_start, 'video_end': video_end}, strict_fps=True, drop_last=False)
    video = _spatial_resize_video(video, nframes=min(max(video.shape[0], 120), FPS_MAX_FRAMES))

    system_prompt_offset, past_key_values, generated = None, None, ''
    frames_list = [video[:6]] + list(video[6:].split(2))

    for i, frames in enumerate(frames_list):
        start_timestamp, end_timestamp = (0, 3) if i == 0 else (i + 2, i + 3)
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": f'Time={start_timestamp:.1f}-{end_timestamp:.1f}s'},
                {"type": "video", "video": frames},
            ]
        }
        if i == 0:
            message['content'].append({"type": "text", "text": query})
        texts = processor.apply_chat_template([message], tokenize=False, add_generation_prompt=True, return_tensors='pt')
        if system_prompt_offset is None:
            system_prompt_offset = texts.index('<|im_start|>user')
        if i > 0:
            texts = '<|im_end|>\n' + texts[system_prompt_offset:]
        inputs = processor(
            text=texts,
            images=None,
            videos=[frames],
            return_tensors="pt",
            return_attention_mask=False
        )
        inputs.to('cuda')
        if i > 0:
            inputs['input_ids'] = torch.cat([generated_ids[:, :-1], inputs.input_ids], dim=1)
        outputs = model.generate(**inputs, do_sample=False, past_key_values=past_key_values, max_new_tokens=max_new_tokens, return_dict_in_generate=True)
        past_key_values = outputs.past_key_values
        generated_ids = outputs.sequences
        this_generated = processor.decode(generated_ids[0, inputs.input_ids.size(1):], skip_special_tokens = True).replace(' ...', '').strip()
        if this_generated:
            generated += ' ' + this_generated
    return generated.strip()

if __name__ == '__main__':
    from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
    # model = Qwen2VLForConditionalGeneration.from_pretrained("Qwen/Qwen2-VL-7B-Instruct", torch_dtype="auto", attn_implementation='flash_attention_2')
    # model.to('cuda')
    processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
    # print(video_qa(
    #     model=model,
    #     processor=processor,
    #     video_path='demo/assets/5nj1KMq3nKw.mp4',
    #     # video_start=0, # optional
    #     # video_end=10, # optional
    #     query='Question: Which country has appeared in this video?\nA. UK\nB. Singapore\nC. USA\nD. Japan\nPlease select the correct answer.',
    #     answer_prefix = 'Answer:',
    #     max_new_tokens=32,
    #     strict_fps=True,
    #     strict_abcd=True,
    # )) # B

    model = Qwen2VLForConditionalGeneration.from_pretrained("checkpoint-15740", torch_dtype="auto", attn_implementation='flash_attention_2')
    model.to('cuda')
    from utils.livecc_utils import _video_reader_backend, prepare_inputs_for_generation
    model.prepare_inputs_for_generation = functools.partial(prepare_inputs_for_generation, model)
    title = "Singapore vs China | FIFA World Cup 2026™ Qualifiers"
    print(video_cc(
        model=model,
        processor=processor,
        video_path='demo/assets/5nj1KMq3nKw.mp4',
        video_start=42, # optional
        video_end=120, # optional  
        query=f'Provide real-time commentary for the video titled "{title}".',
        do_sample=False,
    ))