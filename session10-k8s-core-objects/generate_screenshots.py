import os
import subprocess
import time
import shutil
from PIL import Image, ImageDraw, ImageFont

CWD = r"c:\Users\ASUS\Desktop\devops-heros\session10-k8s-core-objects"
PROMPT_PATH = r"C:\Users\ASUS\Desktop\devops-heros\session10-k8s-core-objects"
SCREENSHOTS_DIR = os.path.join(CWD, "screenshots")

def get_line_segments(line):
    if not line:
        return [("", (209, 213, 219))]
    if subprocess.re.match(r'^(NAME\s+READY|NAME\s+TYPE|NAME\s+ENDPOINTS|NAME\s+DESIRED)', line):
        return [(line, (147, 197, 253))]
    if subprocess.re.search(r'\b(created|configured|deleted|unchanged)\b', line, subprocess.re.IGNORECASE):
        return [(line, (74, 222, 128))]
    if subprocess.re.search(r'\bRunning\b', line):
        parts = line.split('Running')
        return [(parts[0], (229, 231, 235)), ('Running', (74, 222, 128)), (parts[1], (229, 231, 235))]
    if subprocess.re.search(r'\bCompleted\b', line):
        parts = line.split('Completed')
        return [(parts[0], (229, 231, 235)), ('Completed', (74, 222, 128)), (parts[1], (229, 231, 235))]
    if subprocess.re.search(r'\bContainerCreating\b', line):
        parts = line.split('ContainerCreating')
        return [(parts[0], (229, 231, 235)), ('ContainerCreating', (251, 191, 36)), (parts[1], (229, 231, 235))]
    if subprocess.re.search(r'\bPending\b', line):
        parts = line.split('Pending')
        return [(parts[0], (229, 231, 235)), ('Pending', (251, 191, 36)), (parts[1], (229, 231, 235))]
    if subprocess.re.search(r'\bTerminating\b', line):
        parts = line.split('Terminating')
        return [(parts[0], (229, 231, 235)), ('Terminating', (251, 146, 60)), (parts[1], (229, 231, 235))]
    if subprocess.re.search(r'\b(CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Error|Failed)\b', line):
        m = subprocess.re.search(r'\b(CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Error|Failed)\b', line)
        matched_str = m.group(1)
        parts = line.split(matched_str, 1)
        return [(parts[0], (229, 231, 235)), (matched_str, (248, 113, 113)), (parts[1], (229, 231, 235))]
    if line.strip().startswith('Selector:'):
        return [("Selector:", (147, 197, 253)), (line.split('Selector:', 1)[1], (253, 224, 71))]
    return [(line, (209, 213, 219))]

def render_terminal_image(title_bar_text, prompt_path, lines_data, output_filepath):
    try:
        font_regular = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 15)
        font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", 15)
        font_header = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 13)
    except Exception:
        font_regular = ImageFont.load_default()
        font_bold = font_regular
        font_header = font_regular

    padding_outer = 35
    window_header_height = 38
    padding_inner_x = 24
    padding_inner_y = 20
    line_height = 24
    char_width = 9.0

    all_render_rows = []
    for type_, text in lines_data:
        sublines = text.splitlines()
        if not sublines and text == '':
            sublines = ['']
        for subline in sublines:
            all_render_rows.append((type_, subline))

    max_cols = max(len(line) for _, line in all_render_rows) if all_render_rows else 60
    for type_, line in all_render_rows:
        if type_ == 'cmd':
            max_cols = max(max_cols, len(f"PS {prompt_path}> " + line))

    max_cols = max(max_cols + 4, 85)
    
    content_width = int(max_cols * char_width) + (padding_inner_x * 2)
    content_height = (len(all_render_rows) * line_height) + (padding_inner_y * 2)

    win_width = max(content_width, 920)
    win_height = window_header_height + content_height

    img_width = win_width + (padding_outer * 2)
    img_height = win_height + (padding_outer * 2)

    bg_color = (15, 23, 42)
    img = Image.new("RGBA", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    win_x1, win_y1 = padding_outer, padding_outer
    win_x2, win_y2 = padding_outer + win_width, padding_outer + win_height
    corner_radius = 12

    draw.rounded_rectangle([win_x1 - 2, win_y1 - 2, win_x2 + 2, win_y2 + 2], radius=corner_radius+2, fill=(30, 41, 59))
    draw.rounded_rectangle([win_x1, win_y1, win_x2, win_y2], radius=corner_radius, fill=(13, 17, 23), outline=(48, 54, 61), width=1)

    header_box = [win_x1, win_y1, win_x2, win_y1 + window_header_height]
    draw.rounded_rectangle(header_box, radius=corner_radius, fill=(22, 27, 34))
    draw.rectangle([win_x1, win_y1 + corner_radius, win_x2, win_y1 + window_header_height], fill=(22, 27, 34))

    btn_y = win_y1 + 19
    draw.ellipse([win_x1 + 16, btn_y - 6, win_x1 + 28, btn_y + 6], fill=(255, 95, 86))
    draw.ellipse([win_x1 + 34, btn_y - 6, win_x1 + 46, btn_y + 6], fill=(255, 189, 46))
    draw.ellipse([win_x1 + 52, btn_y - 6, win_x1 + 64, btn_y + 6], fill=(39, 201, 63))

    title_bbox = font_header.getbbox(title_bar_text)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text((win_x1 + (win_width - title_w) // 2, win_y1 + 10), title_bar_text, fill=(139, 148, 158), font=font_header)

    curr_y = win_y1 + window_header_height + padding_inner_y
    start_x = win_x1 + padding_inner_x

    for type_, line in all_render_rows:
        if type_ == 'cmd':
            prompt_str = f"PS {prompt_path}> "
            draw.text((start_x, curr_y), prompt_str, fill=(56, 189, 248), font=font_bold)
            prompt_w = font_bold.getbbox(prompt_str)[2] - font_bold.getbbox(prompt_str)[0]
            draw.text((start_x + prompt_w, curr_y), line, fill=(243, 244, 246), font=font_bold)
        elif type_ == 'blank':
            pass
        else:
            segments = get_line_segments(line)
            x_offset = start_x
            for seg_text, color in segments:
                if seg_text:
                    is_bold = (color == (147, 197, 253))
                    f = font_bold if is_bold else font_regular
                    draw.text((x_offset, curr_y), seg_text, fill=color, font=f)
                    seg_w = f.getbbox(seg_text)[2] - f.getbbox(seg_text)[0]
                    x_offset += seg_w
        
        curr_y += line_height

    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    img.save(output_filepath, "PNG")
    print(f"Generated screenshot: {output_filepath}")

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=CWD)
    out = res.stdout.strip()
    err = res.stderr.strip()
    full = out
    if err:
        full = (out + "\n" + err).strip()
    return full

def clean_k8s():
    subprocess.run("kubectl delete pods,rs,deployment,daemonset,svc --all --grace-period=0 --force", shell=True, capture_output=True, cwd=CWD)
    time.sleep(3)

def save_screenshot(lines, filename):
    out_file = os.path.join(SCREENSHOTS_DIR, filename)
    root_file = os.path.join(CWD, filename)
    render_terminal_image("Windows PowerShell", PROMPT_PATH, lines, out_file)
    shutil.copy(out_file, root_file)
    print(f"Successfully generated: {filename}")

def main():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    # 1. core-objects.png
    clean_k8s()
    lines1 = []
    for c in ["kubectl apply -f pod/nginx-pod.yaml", "kubectl apply -f replicaset/backend-rs.yaml", "kubectl apply -f deployment/deployment-v1.yaml", "kubectl apply -f daemonset/node-agent-ds.yaml"]:
        lines1.append(('cmd', c))
        lines1.append(('out', run_cmd(c)))
    time.sleep(8)
    c_get1 = "kubectl get pods,rs,deployment,daemonset"
    lines1.append(('cmd', c_get1))
    lines1.append(('out', run_cmd(c_get1)))
    save_screenshot(lines1, "core-objects.png")

    # 2. pod-lifecycle.png
    clean_k8s()
    lines2 = []
    c_apply2 = "kubectl apply -f pod-lifecycle/01-running.yaml -f pod-lifecycle/02-pending.yaml -f pod-lifecycle/04-failed.yaml -f pod-lifecycle/05-crashloopbackoff.yaml -f pod-lifecycle/06-imagepullbackoff.yaml"
    lines2.append(('cmd', c_apply2))
    lines2.append(('out', run_cmd(c_apply2)))
    time.sleep(8)
    c_get2 = "kubectl get pods"
    lines2.append(('cmd', c_get2))
    lines2.append(('out', run_cmd(c_get2)))
    save_screenshot(lines2, "pod-lifecycle.png")

    # 3. rolling-update.png
    clean_k8s()
    lines3 = []
    for c in ["kubectl apply -f 01-rolling-update/deployment-v1.yaml", "kubectl apply -f 01-rolling-update/service.yaml", "kubectl apply -f 01-rolling-update/deployment-v2.yaml"]:
        lines3.append(('cmd', c))
        lines3.append(('out', run_cmd(c)))
    time.sleep(5)
    c_get3 = "kubectl get pods -l app=app-rolling --show-labels"
    lines3.append(('cmd', c_get3))
    lines3.append(('out', run_cmd(c_get3)))
    save_screenshot(lines3, "rolling-update.png")

    # 4. blue-green.png
    clean_k8s()
    lines4 = []
    for c in ["kubectl apply -f 02-blue-green/deployment-blue.yaml", "kubectl apply -f 02-blue-green/deployment-green.yaml", "kubectl apply -f 02-blue-green/service-blue.yaml", "kubectl apply -f 02-blue-green/service-green.yaml"]:
        lines4.append(('cmd', c))
        lines4.append(('out', run_cmd(c)))
    time.sleep(4)
    c_get4 = "kubectl describe svc myapp-service"
    lines4.append(('cmd', c_get4))
    lines4.append(('out', run_cmd(c_get4)))
    save_screenshot(lines4, "blue-green.png")

    # 5. canary.png
    clean_k8s()
    lines5 = []
    for c in ["kubectl apply -f 03-canary/deployment-stable.yaml", "kubectl apply -f 03-canary/deployment-canary.yaml", "kubectl apply -f 03-canary/service.yaml"]:
        lines5.append(('cmd', c))
        lines5.append(('out', run_cmd(c)))
    time.sleep(4)
    c_get5 = "kubectl get pods --show-labels"
    lines5.append(('cmd', c_get5))
    lines5.append(('out', run_cmd(c_get5)))
    save_screenshot(lines5, "canary.png")

    # 6. recreate.png
    clean_k8s()
    lines6 = []
    for c in ["kubectl apply -f 04-recreate/deployment-v1.yaml", "kubectl apply -f 04-recreate/service.yaml", "kubectl apply -f 04-recreate/deployment-v2.yaml"]:
        lines6.append(('cmd', c))
        lines6.append(('out', run_cmd(c)))
    time.sleep(4)
    c_get6 = "kubectl get pods -l app=app-recreate"
    lines6.append(('cmd', c_get6))
    lines6.append(('out', run_cmd(c_get6)))
    save_screenshot(lines6, "recreate.png")

    # 7. troubleshooting.png
    clean_k8s()
    lines7 = []
    for c in ["kubectl apply -f troubleshooting/broken-image.yaml", "kubectl apply -f troubleshooting/selector-mismatch.yaml"]:
        lines7.append(('cmd', c))
        lines7.append(('out', run_cmd(c)))
    time.sleep(5)
    c_get7a = "kubectl get pods"
    lines7.append(('cmd', c_get7a))
    lines7.append(('out', run_cmd(c_get7a)))
    c_get7b = "kubectl get endpoints selector-error-demo"
    lines7.append(('cmd', c_get7b))
    lines7.append(('out', run_cmd(c_get7b)))
    save_screenshot(lines7, "troubleshooting.png")

    print("\nDONE_ALL_SCREENSHOTS")

if __name__ == '__main__':
    main()
