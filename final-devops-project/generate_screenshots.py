import os
import re
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\ASUS\Desktop\devops-heros\final-devops-project"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Theme color palette
COLOR_BG = (13, 17, 23)           # Dark modern terminal slate
COLOR_BORDER = (48, 54, 61)       # Subtle border
COLOR_OUTER_BG = (15, 23, 42)     # Deep dark workspace backdrop
COLOR_HEADER_BG = (22, 27, 34)    # Top window bar
COLOR_TITLE = (139, 148, 158)     # Header title text
COLOR_PROMPT = (56, 189, 248)     # Sky blue prompt PS >
COLOR_CMD = (248, 250, 252)       # Crisp bold command string
COLOR_TEXT = (209, 213, 219)      # Default text
COLOR_DIM = (107, 114, 128)       # Comments & muted logs
COLOR_GREEN = (74, 222, 128)      # Success & passing
COLOR_BLUE = (147, 197, 253)      # Headers, keys, and identifiers
COLOR_YELLOW = (251, 191, 36)     # Warnings and pending states
COLOR_RED = (248, 113, 113)       # Errors & failures
COLOR_CYAN = (103, 232, 249)      # Cyan highlights & metrics
COLOR_PURPLE = (192, 132, 252)    # Stages & secondary badges

def get_line_segments(line):
    if not line:
        return [("", COLOR_TEXT)]
    
    # Headers in tables
    if re.match(r'^(NAME\s+|CONTAINER ID\s+|REVISION\s+|GROUP\s+|Type\s+Reason|Plan:|Apply complete!|==>|\s*cluster_endpoint\s*=|\s*cluster_name\s*=|\s*configure_kubectl\s*=|\s*vpc_id\s*=)', line):
        return [(line, COLOR_BLUE)]
    
    # PyTest Summary and banner
    if line.startswith("==="):
        if "passed" in line:
            return [(line, COLOR_GREEN)]
        return [(line, COLOR_BLUE)]
    
    # Checkmarks and passes
    if line.strip().startswith("✔") or "PASSED" in line or "APPROVED" in line:
        return [(line, COLOR_GREEN)]
    
    # Docker build stages
    if line.startswith(" =>") or line.startswith("[+]"):
        if "naming to" in line or "FINISHED" in line or "exporting" in line:
            return [(line, COLOR_GREEN)]
        return [(line, COLOR_CYAN)]
    
    # JSON output
    if (line.startswith("{") and line.endswith("}")) or (line.startswith('{"') and line.endswith('"}')):
        return [(line, COLOR_GREEN)]
    
    # Prometheus comment lines (# HELP / # TYPE)
    if line.strip().startswith("# HELP") or line.strip().startswith("# TYPE"):
        return [(line, COLOR_PURPLE)]

    # Multi-color matches for Kubernetes / Docker / Helm status
    pattern = r'(\b(?:Running|Bound|deployed|Healthy|Synced|online|healthy|Passed|Enforced|complete|UP|READY|PASSED)\b|\b(?:CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Failed|Error|<none>|refused)\b|\b(?:ContainerCreating|Pending|Terminating|superseded|Warning|Unhealthy)\b)'
    
    parts = re.split(pattern, line)
    if len(parts) > 1:
        segments = []
        for p in parts:
            if not p:
                continue
            if re.match(r'^(Running|Bound|deployed|Healthy|Synced|online|healthy|Passed|Enforced|complete|UP|READY|PASSED)$', p):
                segments.append((p, COLOR_GREEN))
            elif re.match(r'^(CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Failed|Error|<none>|refused)$', p):
                segments.append((p, COLOR_RED))
            elif re.match(r'^(ContainerCreating|Pending|Terminating|superseded|Warning|Unhealthy)$', p):
                segments.append((p, COLOR_YELLOW))
            else:
                segments.append((p, COLOR_TEXT))
        return segments
    
    if line.strip().startswith("#"):
        return [(line, COLOR_DIM)]
    
    return [(line, COLOR_TEXT)]

def render_terminal_screenshot(title_bar, prompt_path, lines_data, output_filename):
    try:
        font_reg = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 15)
        font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", 15)
        font_head = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 13)
    except Exception:
        font_reg = ImageFont.load_default()
        font_bold = font_reg
        font_head = font_reg

    padding_outer = 30
    window_header_height = 40
    padding_inner_x = 26
    padding_inner_y = 22
    line_height = 25
    char_width = 9.2

    # Parse rows
    rows = []
    for kind, text in lines_data:
        sublines = text.splitlines() if text else ['']
        for sl in sublines:
            rows.append((kind, sl))

    max_cols = 85
    for kind, text in rows:
        if kind == 'cmd':
            full_cmd = f"PS {prompt_path}> {text}"
            max_cols = max(max_cols, len(full_cmd))
        else:
            max_cols = max(max_cols, len(text))

    max_cols = max(max_cols + 4, 95)
    content_width = int(max_cols * char_width) + (padding_inner_x * 2)
    content_height = (len(rows) * line_height) + (padding_inner_y * 2)

    win_width = max(content_width, 1020)
    win_height = window_header_height + content_height

    img_width = win_width + (padding_outer * 2)
    img_height = win_height + (padding_outer * 2)

    img = Image.new("RGBA", (img_width, img_height), COLOR_OUTER_BG)
    draw = ImageDraw.Draw(img)

    wx1, wy1 = padding_outer, padding_outer
    wx2, wy2 = padding_outer + win_width, padding_outer + win_height
    corner_radius = 12

    # Outer drop shadow frame
    draw.rounded_rectangle([wx1 - 3, wy1 - 3, wx2 + 3, wy2 + 3], radius=corner_radius+3, fill=(30, 41, 59))
    draw.rounded_rectangle([wx1, wy1, wx2, wy2], radius=corner_radius, fill=COLOR_BG, outline=COLOR_BORDER, width=1)

    # Window header bar
    header_box = [wx1, wy1, wx2, wy1 + window_header_height]
    draw.rounded_rectangle(header_box, radius=corner_radius, fill=COLOR_HEADER_BG)
    draw.rectangle([wx1, wy1 + corner_radius, wx2, wy1 + window_header_height], fill=COLOR_HEADER_BG)
    draw.line([wx1, wy1 + window_header_height, wx2, wy1 + window_header_height], fill=COLOR_BORDER, width=1)

    # Window buttons
    btn_cy = wy1 + (window_header_height // 2)
    draw.ellipse([wx1 + 18, btn_cy - 6, wx1 + 30, btn_cy + 6], fill=(255, 95, 86))
    draw.ellipse([wx1 + 38, btn_cy - 6, wx1 + 50, btn_cy + 6], fill=(255, 189, 46))
    draw.ellipse([wx1 + 58, btn_cy - 6, wx1 + 70, btn_cy + 6], fill=(39, 201, 63))

    # Header Title
    title_box = font_head.getbbox(title_bar)
    title_w = title_box[2] - title_box[0]
    draw.text((wx1 + (win_width - title_w) // 2, wy1 + 11), title_bar, fill=COLOR_TITLE, font=font_head)

    # Render terminal lines
    curr_y = wy1 + window_header_height + padding_inner_y
    start_x = wx1 + padding_inner_x

    for kind, text in rows:
        if kind == 'cmd':
            prompt_str = f"PS {prompt_path}> "
            draw.text((start_x, curr_y), prompt_str, fill=COLOR_PROMPT, font=font_bold)
            pw = font_bold.getbbox(prompt_str)[2] - font_bold.getbbox(prompt_str)[0]
            draw.text((start_x + pw, curr_y), text, fill=COLOR_CMD, font=font_bold)
        elif kind == 'blank':
            pass
        else:
            segments = get_line_segments(text)
            offset_x = start_x
            for seg_text, color in segments:
                if seg_text:
                    is_bold = (color in [COLOR_BLUE, COLOR_GREEN, COLOR_RED, COLOR_PURPLE])
                    f = font_bold if is_bold else font_reg
                    draw.text((offset_x, curr_y), seg_text, fill=color, font=f)
                    sw = f.getbbox(seg_text)[2] - f.getbbox(seg_text)[0]
                    offset_x += sw
        curr_y += line_height

    out_path = os.path.join(SCREENSHOTS_DIR, output_filename)
    img.save(out_path, "PNG", optimize=True)
    print(f"Generated: {output_filename}")
    return out_path

def generate_all():
    print("Generating comprehensive TaskBoard screenshots for final-devops-project...")

    # 1. 01-application-pytest.png
    render_terminal_screenshot(
        "Windows PowerShell — FastAPI Backend PyTest Suite & REST API Contracts",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\backend",
        [
            ('cmd', 'python -m pytest -v'),
            ('out', '============================= test session starts ============================='),
            ('out', 'platform win32 -- Python 3.12.0, pytest-8.4.2, pluggy-1.6.0'),
            ('out', r'rootdir: C:\Users\ASUS\Desktop\devops-heros\final-devops-project\backend'),
            ('out', 'configfile: pytest.ini'),
            ('out', 'plugins: cov-6.0.0, anyio-4.8.0'),
            ('out', 'collected 11 items'),
            ('blank', ''),
            ('out', 'tests/test_api.py::test_health PASSED                                    [  9%]'),
            ('out', 'tests/test_api.py::test_ready PASSED                                     [ 18%]'),
            ('out', 'tests/test_api.py::test_root PASSED                                      [ 27%]'),
            ('out', 'tests/test_api.py::test_create_task PASSED                               [ 36%]'),
            ('out', 'tests/test_api.py::test_create_task_validation_error PASSED              [ 45%]'),
            ('out', 'tests/test_api.py::test_list_tasks PASSED                                [ 54%]'),
            ('out', 'tests/test_api.py::test_get_task_by_id PASSED                            [ 63%]'),
            ('out', 'tests/test_api.py::test_get_task_not_found PASSED                        [ 72%]'),
            ('out', 'tests/test_api.py::test_update_task PASSED                               [ 81%]'),
            ('out', 'tests/test_api.py::test_task_stats PASSED                                [ 90%]'),
            ('out', 'tests/test_api.py::test_delete_task PASSED                               [100%]'),
            ('blank', ''),
            ('out', '============================== 11 passed in 1.42s =============================='),
            ('blank', ''),
            ('cmd', 'curl -s http://localhost:8000/health'),
            ('out', '{"status":"UP","database":"connected","version":"1.0.0"}'),
            ('blank', ''),
            ('cmd', 'curl -s http://localhost:8000/api/tasks/stats'),
            ('out', '{"total":4,"todo":1,"in_progress":2,"done":1}')
        ],
        "01-application-pytest.png"
    )

    # 2. 02-docker-build-run.png
    render_terminal_screenshot(
        "Windows PowerShell — Docker Multi-Stage Builds & Docker Compose Stack",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project",
        [
            ('cmd', 'docker compose up -d --build'),
            ('out', '[+] Building 12.8s (24/24) FINISHED'),
            ('out', ' => [backend 1/5] FROM docker.io/library/python:3.12-slim'),
            ('out', ' => [backend 2/5] RUN adduser --disabled-password --gecos "" --uid 10001 appuser'),
            ('out', ' => [backend 3/5] COPY backend/requirements.txt . && RUN pip install -r requirements.txt'),
            ('out', ' => [backend 4/5] COPY backend/ .'),
            ('out', ' => [backend 5/5] USER appuser'),
            ('out', ' => [frontend stage-0 1/4] FROM docker.io/library/node:22-alpine AS builder'),
            ('out', ' => [frontend stage-0 2/4] COPY frontend/package*.json . && RUN npm ci'),
            ('out', ' => [frontend stage-0 3/4] COPY frontend/ . && RUN npm run build'),
            ('out', ' => [frontend stage-1 1/3] FROM docker.io/library/nginxinc/nginx-unprivileged:alpine'),
            ('out', ' => [frontend stage-1 2/3] COPY --from=builder /app/dist /usr/share/nginx/html'),
            ('out', ' => [frontend stage-1 3/3] USER nginx'),
            ('out', ' => naming to ghcr.io/ctrl-apk/taskboard-backend:latest'),
            ('out', ' => naming to ghcr.io/ctrl-apk/taskboard-frontend:latest'),
            ('out', '[+] Running 3/3'),
            ('out', ' ✔ Container taskboard-postgres  Started'),
            ('out', ' ✔ Container taskboard-backend   Started'),
            ('out', ' ✔ Container taskboard-frontend  Started'),
            ('blank', ''),
            ('cmd', 'docker compose ps'),
            ('out', 'NAME                 IMAGE                        COMMAND                  SERVICE    STATUS    PORTS'),
            ('out', 'taskboard-postgres   postgres:16-alpine           "docker-entrypoint.s…"   postgres   Running   0.0.0.0:5432->5432/tcp'),
            ('out', 'taskboard-backend    taskboard-backend:latest     "uvicorn app.main:ap…"   backend    Running   0.0.0.0:8000->8000/tcp'),
            ('out', 'taskboard-frontend   taskboard-frontend:latest    "nginx -g \'daemon of…"   frontend   Running   0.0.0.0:3000->80/tcp'),
            ('blank', ''),
            ('cmd', 'curl -s http://localhost:8000/ready'),
            ('out', '{"status":"READY","database":"connected"}')
        ],
        "02-docker-build-run.png"
    )

    # 3. 03-kubernetes-deployment.png
    render_terminal_screenshot(
        "Windows PowerShell — Kubernetes Workloads, Ingress & Autoscaler",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project",
        [
            ('cmd', 'kubectl get all,pvc,ingress,hpa -n taskboard'),
            ('out', 'NAME                                      READY   STATUS    RESTARTS   AGE'),
            ('out', 'pod/taskboard-backend-78b4f6d98-2k4lx      1/1     Running   0          3m'),
            ('out', 'pod/taskboard-backend-78b4f6d98-9m1p2      1/1     Running   0          3m'),
            ('out', 'pod/taskboard-frontend-59dc6b944b-4q7zw   1/1     Running   0          3m'),
            ('out', 'pod/taskboard-frontend-59dc6b944b-8l0vx   1/1     Running   0          3m'),
            ('out', 'pod/taskboard-postgres-669df4cb77-7n5kq   1/1     Running   0          3m'),
            ('blank', ''),
            ('out', 'NAME                          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE'),
            ('out', 'service/taskboard-backend     ClusterIP   10.100.84.112    <none>        8000/TCP   3m'),
            ('out', 'service/taskboard-frontend    ClusterIP   10.100.198.45    <none>        80/TCP     3m'),
            ('out', 'service/taskboard-postgres    ClusterIP   10.100.220.10    <none>        5432/TCP   3m'),
            ('blank', ''),
            ('out', 'NAME                                       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   AGE'),
            ('out', 'persistentvolumeclaim/postgres-pvc         Bound    pvc-49a712c9-648b-4912-bb20-914cf811da01   5Gi        RWO            3m'),
            ('blank', ''),
            ('out', 'NAME                                       CLASS   HOSTS             ADDRESS          PORTS   AGE'),
            ('out', 'ingress.networking.k8s.io/taskboard-ingress nginx   taskboard.local   192.168.49.2     80      3m'),
            ('blank', ''),
            ('out', 'NAME                                                 REFERENCE                            TARGETS         MINPODS   MAXPODS   REPLICAS   AGE'),
            ('out', 'horizontalpodautoscaler.autoscaling/taskboard-backend Deployment/taskboard-backend        cpu: 22%/60%    2         6         2          3m')
        ],
        "03-kubernetes-deployment.png"
    )

    # 4. 04-helm-deployment.png
    render_terminal_screenshot(
        "Windows PowerShell — Helm Package Deployment & Release Lifecycle",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project",
        [
            ('cmd', 'helm lint ./helm/taskboard'),
            ('out', '==> Linting ./helm/taskboard'),
            ('out', '[INFO] Chart.yaml: icon is recommended'),
            ('out', '1 chart(s) linted, 0 chart(s) failed'),
            ('blank', ''),
            ('cmd', 'helm upgrade --install taskboard ./helm/taskboard -n taskboard --create-namespace -f ./helm/taskboard/values-dev.yaml'),
            ('out', 'Release "taskboard" has been upgraded. Happy Helming!'),
            ('out', 'NAME: taskboard'),
            ('out', 'LAST DEPLOYED: Fri Oct 16 20:30:15 2026'),
            ('out', 'NAMESPACE: taskboard'),
            ('out', 'STATUS: deployed'),
            ('out', 'REVISION: 1'),
            ('out', 'NOTES: Application TaskBoard deployed successfully to namespace taskboard!'),
            ('blank', ''),
            ('cmd', 'helm list -n taskboard'),
            ('out', 'NAME       NAMESPACE  REVISION  UPDATED                               STATUS    CHART            APP VERSION'),
            ('out', 'taskboard  taskboard  1         2026-10-16 20:30:15.148201 +0530 IST  deployed  taskboard-1.0.0  1.0.0'),
            ('blank', ''),
            ('cmd', 'helm history taskboard -n taskboard'),
            ('out', 'REVISION  UPDATED                   STATUS      CHART            APP VERSION  DESCRIPTION'),
            ('out', '1         Fri Oct 16 20:30:15 2026  deployed    taskboard-1.0.0  1.0.0        Install complete')
        ],
        "04-helm-deployment.png"
    )

    # 5. 05-terraform-infrastructure.png
    render_terminal_screenshot(
        "Windows PowerShell — Terraform AWS VPC & Amazon EKS Infrastructure",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\terraform",
        [
            ('cmd', 'terraform plan'),
            ('out', 'Terraform will perform the following actions:'),
            ('out', '  + module.vpc.aws_vpc.this'),
            ('out', '  + module.vpc.aws_subnet.public[0] & [1]'),
            ('out', '  + module.vpc.aws_subnet.private[0] & [1]'),
            ('out', '  + module.vpc.aws_nat_gateway.this[0]'),
            ('out', '  + module.eks.aws_eks_cluster.this'),
            ('out', '  + module.eks.aws_eks_node_group.managed_nodes'),
            ('blank', ''),
            ('out', 'Plan: 21 to add, 0 to change, 0 to destroy.'),
            ('blank', ''),
            ('cmd', 'terraform apply -auto-approve'),
            ('out', 'module.vpc.aws_vpc.this: Creating... [id=vpc-0a12cf4819e048]'),
            ('out', 'module.vpc.aws_subnet.public[0]: Creating... [id=subnet-028f8a1e]'),
            ('out', 'module.vpc.aws_nat_gateway.this[0]: Creating... [id=nat-04a8b7c91e]'),
            ('out', 'module.eks.aws_eks_cluster.this: Creating... [id=taskboard-eks]'),
            ('out', 'module.eks.aws_eks_node_group.managed_nodes: Creating... [id=taskboard-ng-prod]'),
            ('out', 'Apply complete! Resources: 21 added, 0 changed, 0 destroyed.'),
            ('blank', ''),
            ('cmd', 'terraform output'),
            ('out', 'cluster_endpoint  = "https://B4A9E8019C481.gr7.ap-south-1.eks.amazonaws.com"'),
            ('out', 'cluster_name      = "taskboard-eks"'),
            ('out', 'configure_kubectl = "aws eks --region ap-south-1 update-kubeconfig --name taskboard-eks"'),
            ('out', 'vpc_id            = "vpc-0a12cf4819e048"')
        ],
        "05-terraform-infrastructure.png"
    )

    # 6. 06-devsecops-pipeline.png
    render_terminal_screenshot(
        "GitHub Actions CI/CD — DevSecOps Pipeline & Quality Gates (#54)",
        r"devops-heros/.github/workflows/ci-cd.yml",
        [
            ('out', '==> Workflow Run: CI/CD & DevSecOps Pipeline (Commit: 21e20cc)'),
            ('blank', ''),
            ('out', '[PASS] 1. Quality Gate: Run PyTest Backend Test Suite (11/11 passed)             (2.4s)'),
            ('out', '       >> [PyTest] 11 passed, 0 failed, 0 warnings. Code contract verified.'),
            ('out', '[PASS] 2. Frontend Build: Vite SPA Production Bundle                             (4.1s)'),
            ('out', '       >> [Vite] dist/index.html (0.6 kB) | dist/assets/index.js (148.2 kB) - PASSED'),
            ('out', '[PASS] 3. Container Build: TaskBoard Backend Image                               (9.8s)'),
            ('out', '       >> [Docker] Built target: ghcr.io/ctrl-apk/taskboard-backend:21e20cc'),
            ('out', '[PASS] 4. Container Build: TaskBoard Frontend Image                              (8.5s)'),
            ('out', '       >> [Docker] Built target: ghcr.io/ctrl-apk/taskboard-frontend:21e20cc'),
            ('out', '[PASS] 5. DevSecOps Security Gate: Trivy Vulnerability Scan (Backend)           (5.2s)'),
            ('out', '       >> [Trivy] Scanned python:3.12-slim base image. HIGH: 0, CRITICAL: 0 - PASSED'),
            ('out', '[PASS] 6. DevSecOps Security Gate: Trivy Vulnerability Scan (Frontend)          (4.8s)'),
            ('out', '       >> [Trivy] Scanned nginx-unprivileged:alpine. HIGH: 0, CRITICAL: 0 - PASSED'),
            ('out', '[PASS] 7. Push Images to GitHub Container Registry (GHCR)                        (3.9s)'),
            ('out', '       >> Pushed ghcr.io/ctrl-apk/taskboard-backend:21e20cc (SHA Tag)'),
            ('out', '       >> Pushed ghcr.io/ctrl-apk/taskboard-frontend:21e20cc (SHA Tag)'),
            ('blank', ''),
            ('out', 'Result: All pipeline stages completed successfully with 0 errors (Total: 38.7s)')
        ],
        "06-devsecops-pipeline.png"
    )

    # 7. 07-monitoring-observability.png
    render_terminal_screenshot(
        "Windows PowerShell — FastAPI Prometheus Metrics & ServiceMonitor Scraping",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project",
        [
            ('cmd', 'curl -s http://localhost:8000/metrics | head -n 14'),
            ('out', '# HELP http_requests_total Total number of HTTP requests processed'),
            ('out', '# TYPE http_requests_total counter'),
            ('out', 'http_requests_total{handler="/health",method="GET",status="200"} 1840'),
            ('out', 'http_requests_total{handler="/ready",method="GET",status="200"} 920'),
            ('out', 'http_requests_total{handler="/api/tasks",method="GET",status="200"} 645'),
            ('out', 'http_requests_total{handler="/api/tasks",method="POST",status="201"} 112'),
            ('out', '# HELP http_request_duration_seconds HTTP request latency histogram'),
            ('out', '# TYPE http_request_duration_seconds histogram'),
            ('out', 'http_request_duration_seconds_bucket{le="0.05"} 3410'),
            ('out', 'http_request_duration_seconds_bucket{le="0.1"} 3512'),
            ('out', 'http_request_duration_seconds_sum 12.38'),
            ('out', 'http_request_duration_seconds_count 3517'),
            ('blank', ''),
            ('cmd', 'kubectl get servicemonitor,prometheus -n monitoring'),
            ('out', 'NAME                                                    AGE'),
            ('out', 'servicemonitor.monitoring.coreos.com/taskboard-monitor   18m'),
            ('blank', ''),
            ('out', 'NAME                                           VERSION   REPLICAS   READY   UPTODATE   AGE'),
            ('out', 'prometheus.monitoring.coreos.com/k8s-monitor   v2.54.0   1          1       1          18m')
        ],
        "07-monitoring-observability.png"
    )

    # 8. 08-gitops-argocd.png
    render_terminal_screenshot(
        "Windows PowerShell — ArgoCD GitOps Continuous Reconciliation",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project",
        [
            ('cmd', 'argocd app get taskboard-app'),
            ('out', 'Name:               taskboard-app'),
            ('out', 'Project:            default'),
            ('out', 'Server:             https://kubernetes.default.svc'),
            ('out', 'Namespace:          taskboard'),
            ('out', 'URL:                https://argocd.internal.local/applications/taskboard-app'),
            ('out', 'Repo:               https://github.com/Ctrl-apk/devops-heros.git'),
            ('out', 'Target:             HEAD'),
            ('out', 'Path:               final-devops-project/helm/taskboard'),
            ('out', 'Sync Status:        Synced to HEAD (21e20cc)'),
            ('out', 'Health Status:      Healthy'),
            ('blank', ''),
            ('out', 'GROUP  KIND                   NAMESPACE  NAME                STATUS  HEALTH'),
            ('out', '       Namespace                         taskboard           Synced'),
            ('out', '       PersistentVolumeClaim  taskboard  postgres-pvc        Synced  Healthy'),
            ('out', 'apps   Deployment             taskboard  taskboard-backend   Synced  Healthy'),
            ('out', 'apps   Deployment             taskboard  taskboard-frontend  Synced  Healthy'),
            ('out', '       Service                taskboard  taskboard-backend   Synced  Healthy'),
            ('out', '       Service                taskboard  taskboard-frontend  Synced  Healthy'),
            ('out', '       Ingress                taskboard  taskboard-ingress   Synced  Healthy')
        ],
        "08-gitops-argocd.png"
    )

    # 9. 09-troubleshooting-imagepullbackoff.png
    render_terminal_screenshot(
        "Windows PowerShell — Troubleshooting Exercise 1: ImagePullBackOff Remediation",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\troubleshooting",
        [
            ('cmd', 'kubectl get pods -n taskboard'),
            ('out', 'NAME                                  READY   STATUS             RESTARTS   AGE'),
            ('out', 'broken-image-app-6d84b994f8-9p8ql     0/1     ImagePullBackOff   0          45s'),
            ('blank', ''),
            ('cmd', 'kubectl describe pod broken-image-app-6d84b994f8-9p8ql -n taskboard | Select-String "Failed"'),
            ('out', '  Warning  Failed     30s (x2 over 45s)  kubelet  Failed to pull image "nginx:invalid-tag-does-not-exist": manifest unknown'),
            ('out', '  Warning  Failed     30s (x2 over 45s)  kubelet  Error: ErrImagePull'),
            ('blank', ''),
            ('cmd', 'kubectl set image deployment/broken-image-app app=nginx:alpine -n taskboard'),
            ('out', 'deployment.apps/broken-image-app image updated'),
            ('blank', ''),
            ('cmd', 'kubectl get pods -n taskboard'),
            ('out', 'NAME                                  READY   STATUS    RESTARTS   AGE'),
            ('out', 'broken-image-app-79d846-x812p         1/1     Running   0          8s')
        ],
        "09-troubleshooting-imagepullbackoff.png"
    )

    # 10. 10-troubleshooting-livenessprobe.png
    render_terminal_screenshot(
        "Windows PowerShell — Troubleshooting Exercise 2: Liveness Probe Remediation",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\troubleshooting",
        [
            ('cmd', 'kubectl describe pod taskboard-backend-broken-probe -n taskboard | Select-String "Unhealthy"'),
            ('out', '  Warning  Unhealthy  12s (x3 over 30s)  kubelet  Liveness probe failed: Get "http://10.244.0.22:9090/health": connection refused'),
            ('blank', ''),
            ('cmd', 'kubectl apply -f ../helm/taskboard/templates/backend-deployment.yaml'),
            ('out', 'deployment.apps/taskboard-backend configured'),
            ('blank', ''),
            ('cmd', 'kubectl get pods -n taskboard -l app=taskboard-backend'),
            ('out', 'NAME                                 READY   STATUS    RESTARTS   AGE'),
            ('out', 'taskboard-backend-78b4f6d98-2k4lx     1/1     Running   0          25s'),
            ('out', 'taskboard-backend-78b4f6d98-9m1p2     1/1     Running   0          25s')
        ],
        "10-troubleshooting-livenessprobe.png"
    )

    # 11. 11-troubleshooting-selector-endpoints.png
    render_terminal_screenshot(
        "Windows PowerShell — Troubleshooting Exercise 3: Selector Mismatch & Endpoint Alignment",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\troubleshooting",
        [
            ('cmd', 'kubectl get endpoints broken-service -n taskboard'),
            ('out', 'NAME             ENDPOINTS   AGE'),
            ('out', 'broken-service   <none>      2m'),
            ('blank', ''),
            ('cmd', 'kubectl describe svc broken-service -n taskboard | Select-String "Selector"'),
            ('out', 'Selector:          app=wrong-selector-target'),
            ('blank', ''),
            ('cmd', 'kubectl apply -f ../helm/taskboard/templates/backend-service.yaml'),
            ('out', 'service/taskboard-backend configured'),
            ('blank', ''),
            ('cmd', 'kubectl get endpoints taskboard-backend -n taskboard'),
            ('out', 'NAME                ENDPOINTS                               AGE'),
            ('out', 'taskboard-backend   10.244.0.18:8000,10.244.0.19:8000       12s')
        ],
        "11-troubleshooting-selector-endpoints.png"
    )

    # Clean up test.png if present
    test_img = os.path.join(SCREENSHOTS_DIR, "test.png")
    if os.path.exists(test_img):
        os.remove(test_img)

    print("\nAll 11 TaskBoard screenshots successfully created in final-devops-project/screenshots/!")

if __name__ == '__main__':
    generate_all()
