import re

def convert_timestamp_to_seconds(timestamp):
    parts = timestamp.split(':')
    length = len(parts)
    if length == 3:
        #if we have 3 parts, that means that our timestamp is in the format of hours:minutes:seconds
        hh, mm, ss_ms = float(parts[0]), float(parts[1]), parts[2]
    elif length == 2:
        hh = 0.0
        mm, ss_ms = float(parts[0]), parts[1]
        #if we have 2 parts, that means that our timestamp is in the format of minutes:seconds
    else:
        hh = mm = 0.0
        ss_ms = parts[0]
        #if we have 1 part, that means that our timestamp is in the format of seconds only
    ss, ms = map(float, ss_ms.split('.'))
    return hh * 3600 + mm * 60 + ss + ms / 1000

def split_chapters_from_vtt(chapters, vtt_content):
    output_list = []
    for chapter in chapters:

        output = ""

        webvtt_line, *rest_of_content = vtt_content.split("\n")
        adjusted_vtt = "\n".join(rest_of_content)

        start_seconds = chapter['start'] / 1000
        end_seconds = chapter['end'] / 1000

        for block in adjusted_vtt.split("\n\n"):
            timecode, *lines = block.split("\n")

            if " --> " not in timecode:
                continue  # skip this block

            start_time, end_time = timecode.split(" --> ")

            if len(start_time) > 0 and len(end_time) > 0:
                start = convert_timestamp_to_seconds(start_time)
                end = convert_timestamp_to_seconds(end_time)

                if start <= end_seconds and end >= start_seconds:
                    output += f"{timecode}\n"
                    for line in lines:
                        output += f"{line}\n"

        output_list.append(output)
    return output_list

def vtt_chapters_to_text(chapters):
    new_chapters = []
    for chapter in chapters:
        lines = chapter.split('\n')
        timestamp_pattern = r'((\d{1,2}:)?\d{2}:)?\d{2}\.\d{3} --> ((\d{1,2}:)?\d{2}:)?\d{2}\.\d{3}'
        filtered_lines = [line for line in lines if not re.match(timestamp_pattern, line)]
        plain_text = ' '.join(filtered_lines)
        new_chapters.append(plain_text)
    return new_chapters


def text_from_chapters(chapters, vtt):
    vtt_chapters = split_chapters_from_vtt(chapters, vtt)
    return vtt_chapters_to_text(vtt_chapters)
