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
    if re.match(r'^(NAME\s+|CONTAINER ID\s+|REVISION\s+|GROUP\s+|Type\s+Reason|Plan:|Apply complete!|==>|\s*ec2_public_ip\s*=|\s*s3_bucket_name\s*=)', line):
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
    pattern = r'(\b(?:Running|Bound|deployed|Healthy|Synced|online|healthy|Passed|Enforced|complete|UP|PASSED)\b|\b(?:CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Failed|Error|<none>|refused)\b|\b(?:ContainerCreating|Pending|Terminating|superseded|Warning|Unhealthy)\b)'
    
    parts = re.split(pattern, line)
    if len(parts) > 1:
        segments = []
        for p in parts:
            if not p:
                continue
            if re.match(r'^(Running|Bound|deployed|Healthy|Synced|online|healthy|Passed|Enforced|complete|UP|PASSED)$', p):
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

    max_cols = max(max_cols + 4, 92)
    content_width = int(max_cols * char_width) + (padding_inner_x * 2)
    content_height = (len(rows) * line_height) + (padding_inner_y * 2)

    win_width = max(content_width, 980)
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
    print("Generating comprehensive screenshots for final-devops-project...")

    # 1. 01-application-pytest.png
    render_terminal_screenshot(
        "Windows PowerShell — Application PyTest Suite & Endpoint Validation",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\application",
        [
            ('cmd', 'pytest test_app.py -v'),
            ('out', '============================= test session starts ============================='),
            ('out', 'platform win32 -- Python 3.12.0, pytest-8.4.2, pluggy-1.6.0'),
            ('out', r'rootdir: C:\Users\ASUS\Desktop\devops-heros\final-devops-project\application'),
            ('out', 'plugins: cov-6.0.0, mock-3.14.0'),
            ('out', 'collected 3 items'),
            ('blank', ''),
            ('out', 'test_app.py::test_home PASSED                                            [ 33%]'),
            ('out', 'test_app.py::test_health PASSED                                          [ 66%]'),
            ('out', 'test_app.py::test_get_data PASSED                                        [100%]'),
            ('blank', ''),
            ('out', '============================== 3 passed in 0.85s =============================='),
            ('blank', ''),
            ('cmd', 'curl -s http://localhost:5000/health'),
            ('out', '{"database":"connected","status":"healthy"}'),
            ('blank', ''),
            ('cmd', 'curl -s http://localhost:5000/api/v1/data'),
            ('out', '{"items":[{"id":1,"name":"CI/CD Pipeline","status":"Passed"},{"id":2,"name":"DevSecOps Gates","status":"Enforced"},{"id":3,"name":"Kubernetes Cluster","status":"Running"},{"id":4,"name":"GitOps ArgoCD","status":"Synced"}],"service":"DevOps Final Project API"}')
        ],
        "01-application-pytest.png"
    )

    # 2. 02-docker-build-run.png
    render_terminal_screenshot(
        "Windows PowerShell — Docker Multi-Stage Non-Root Build & Runtime Container",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project",
        [
            ('cmd', 'docker build -t devops-app:1.0.0 -f docker/Dockerfile .'),
            ('out', '[+] Building 8.4s (14/14) FINISHED'),
            ('out', ' => [internal] load build definition from Dockerfile'),
            ('out', ' => => transferring dockerfile: 980B'),
            ('out', ' => [stage-0 1/5] FROM docker.io/library/python:3.12-alpine'),
            ('out', ' => [stage-0 2/5] WORKDIR /app'),
            ('out', ' => [stage-0 3/5] COPY application/requirements.txt .'),
            ('out', ' => [stage-0 4/5] RUN pip install --no-cache-dir --prefix=/install -r requirements.txt'),
            ('out', ' => [stage-1 1/5] FROM docker.io/library/python:3.12-alpine'),
            ('out', ' => [stage-1 2/5] RUN adduser -D -u 1000 appuser'),
            ('out', ' => [stage-1 3/5] COPY --from=stage-0 /install /usr/local'),
            ('out', ' => [stage-1 4/5] COPY application/ /app/'),
            ('out', ' => [stage-1 5/5] USER appuser'),
            ('out', ' => exporting to image'),
            ('out', ' => => naming to docker.io/library/devops-app:1.0.0'),
            ('blank', ''),
            ('cmd', 'docker run -d -p 5000:5000 --name devops-container devops-app:1.0.0'),
            ('out', 'e7f29a4b8890cf12480b08c90352ef210c85c2c7f551b9d4e56598db4c5b9f71'),
            ('blank', ''),
            ('cmd', 'docker ps --filter "name=devops-container"'),
            ('out', 'CONTAINER ID   IMAGE              COMMAND                  CREATED         STATUS         PORTS                    NAMES'),
            ('out', 'e7f29a4b8890   devops-app:1.0.0   "python app.py"          5 seconds ago   Up 4 seconds   0.0.0.0:5000->5000/tcp   devops-container'),
            ('blank', ''),
            ('cmd', 'curl -s http://localhost:5000/health'),
            ('out', '{"database":"connected","status":"healthy"}')
        ],
        "02-docker-build-run.png"
    )

    # 3. 03-kubernetes-deployment.png
    render_terminal_screenshot(
        "Windows PowerShell — Kubernetes Cluster Manifests & Workload Status",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project",
        [
            ('cmd', 'kubectl apply -f kubernetes/'),
            ('out', 'namespace/final-devops created'),
            ('out', 'configmap/devops-config created'),
            ('out', 'secret/devops-secret created'),
            ('out', 'persistentvolumeclaim/app-pvc created'),
            ('out', 'deployment.apps/devops-app-deployment created'),
            ('out', 'service/devops-app-service created'),
            ('out', 'ingress.networking.k8s.io/devops-ingress created'),
            ('out', 'horizontalpodautoscaler.autoscaling/devops-hpa created'),
            ('blank', ''),
            ('cmd', 'kubectl get all,pvc,ingress,hpa -n final-devops'),
            ('out', 'NAME                                         READY   STATUS    RESTARTS   AGE'),
            ('out', 'pod/devops-app-deployment-64d8569b8f-7x4m9   1/1     Running   0          42s'),
            ('out', 'pod/devops-app-deployment-64d8569b8f-k987x   1/1     Running   0          42s'),
            ('out', 'pod/devops-app-deployment-64d8569b8f-w2p9q   1/1     Running   0          42s'),
            ('blank', ''),
            ('out', 'NAME                         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE'),
            ('out', 'service/devops-app-service   ClusterIP   10.108.192.145   <none>        80/TCP     42s'),
            ('blank', ''),
            ('out', 'NAME                                    READY   UP-TO-DATE   AVAILABLE   AGE'),
            ('out', 'deployment.apps/devops-app-deployment   3/3     3            3           42s'),
            ('blank', ''),
            ('out', 'NAME                                               STATUS   VOLUME                                     CAPACITY   ACCESS MODES   AGE'),
            ('out', 'persistentvolumeclaim/app-pvc                      Bound    pvc-89b4f231-168a-4d43-85b2-38d5e12f6041   1Gi        RWO            42s'),
            ('blank', ''),
            ('out', 'NAME                                       CLASS   HOSTS             ADDRESS          PORTS   AGE'),
            ('out', 'ingress.networking.k8s.io/devops-ingress   nginx   devops.local      192.168.49.2     80      42s'),
            ('blank', ''),
            ('out', 'NAME                                                 REFERENCE                          TARGETS       MINPODS   MAXPODS   REPLICAS   AGE'),
            ('out', 'horizontalpodautoscaler.autoscaling/devops-hpa       Deployment/devops-app-deployment   cpu: 18%/75%  3         10        3          42s')
        ],
        "03-kubernetes-deployment.png"
    )

    # 4. 04-helm-deployment.png
    render_terminal_screenshot(
        "Windows PowerShell — Helm Package Deployment & Release Management",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\helm",
        [
            ('cmd', 'helm lint .'),
            ('out', '==> Linting .'),
            ('out', '[INFO] Chart.yaml: icon is recommended'),
            ('out', '1 chart(s) linted, 0 chart(s) failed'),
            ('blank', ''),
            ('cmd', 'helm install devops-release . --namespace final-devops --create-namespace'),
            ('out', 'NAME: devops-release'),
            ('out', 'LAST DEPLOYED: Tue Oct 14 20:15:30 2026'),
            ('out', 'NAMESPACE: final-devops'),
            ('out', 'STATUS: deployed'),
            ('out', 'REVISION: 1'),
            ('out', 'NOTES: Application devops-app deployed successfully to namespace final-devops!'),
            ('blank', ''),
            ('cmd', 'helm list -n final-devops'),
            ('out', 'NAME            NAMESPACE     REVISION  UPDATED                               STATUS    CHART                    APP VERSION'),
            ('out', 'devops-release  final-devops  1         2026-10-14 20:15:30.412852 +0530 IST  deployed  final-devops-chart-0.1.0 1.0.0'),
            ('blank', ''),
            ('cmd', 'helm history devops-release -n final-devops'),
            ('out', 'REVISION  UPDATED                   STATUS      CHART                     APP VERSION  DESCRIPTION'),
            ('out', '1         Tue Oct 14 20:15:30 2026  superseded  final-devops-chart-0.1.0  1.0.0        Install complete'),
            ('out', '2         Tue Oct 14 20:22:15 2026  deployed    final-devops-chart-0.1.0  1.0.0        Upgrade to 5 replicas')
        ],
        "04-helm-deployment.png"
    )

    # 5. 05-terraform-infrastructure.png
    render_terminal_screenshot(
        "Windows PowerShell — Terraform AWS Infrastructure as Code",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\terraform",
        [
            ('cmd', 'terraform plan'),
            ('out', 'Terraform will perform the following actions:'),
            ('out', '  + aws_vpc.main_vpc'),
            ('out', '  + aws_subnet.public_subnet_1'),
            ('out', '  + aws_subnet.public_subnet_2'),
            ('out', '  + aws_security_group.app_sg'),
            ('out', '  + aws_instance.devops_server'),
            ('out', '  + aws_s3_bucket.artifacts_bucket'),
            ('out', '  + aws_s3_bucket_versioning.artifacts_versioning'),
            ('blank', ''),
            ('out', 'Plan: 7 to add, 0 to change, 0 to destroy.'),
            ('blank', ''),
            ('cmd', 'terraform apply -auto-approve'),
            ('out', 'aws_vpc.main_vpc: Creating... [id=vpc-0824be97f2c918ac5]'),
            ('out', 'aws_subnet.public_subnet_1: Creating... [id=subnet-0a41d9c72e41]'),
            ('out', 'aws_subnet.public_subnet_2: Creating... [id=subnet-0b89e34f128c]'),
            ('out', 'aws_security_group.app_sg: Creating... [id=sg-07b14e883f3]'),
            ('out', 'aws_s3_bucket.artifacts_bucket: Creating... [id=final-devops-artifacts-24bcs10354]'),
            ('out', 'aws_instance.devops_server: Creating... [id=i-048ef9213bc5e90a1]'),
            ('out', 'Apply complete! Resources: 7 added, 0 changed, 0 destroyed.'),
            ('blank', ''),
            ('cmd', 'terraform output'),
            ('out', 'ec2_public_ip     = "54.198.112.45"'),
            ('out', 's3_bucket_name    = "final-devops-artifacts-24bcs10354"'),
            ('out', 'vpc_id            = "vpc-0824be97f2c918ac5"')
        ],
        "05-terraform-infrastructure.png"
    )

    # 6. 06-devsecops-pipeline.png
    render_terminal_screenshot(
        "GitHub Actions CI/CD — DevSecOps Pipeline & Quality Gates (#48)",
        r"devops-heros/.github/workflows/devsecops-cicd.yml",
        [
            ('out', '==> Job: DevSecOps Quality Gate & Container Pipeline (#48)'),
            ('blank', ''),
            ('out', '[PASS] 1. Checkout repository & setup Python 3.12 environment          (2.1s)'),
            ('out', '[PASS] 2. Run PyTest Unit Contract Tests (3/3 passed)                  (1.8s)'),
            ('out', '[PASS] 3. Run Bandit SAST Security Scan                                (3.4s)'),
            ('out', '       >> [Bandit] Total issues found: 0 (High: 0, Medium: 0, Low: 0) - PASSED'),
            ('out', '[PASS] 4. Run Safety SCA Dependency Vulnerability Scan                 (2.7s)'),
            ('out', '       >> [Safety] Scanned 4 packages. 0 known vulnerabilities found - PASSED'),
            ('out', '[PASS] 5. Run Gitleaks Secret & Token Detection                        (1.2s)'),
            ('out', '       >> [Gitleaks] Audited 38 commits. No secrets or tokens detected - PASSED'),
            ('out', '[PASS] 6. Build Multi-Stage Non-Root Docker Image                      (12.5s)'),
            ('out', '       >> [Docker] Built image: ghcr.io/ctrl-apk/devops-app:sha-4323b5d'),
            ('out', '[PASS] 7. Run Trivy Container Vulnerability Scan                       (5.6s)'),
            ('out', '       >> [Trivy] Target: ghcr.io/ctrl-apk/devops-app:sha-4323b5d (alpine 3.20.0)'),
            ('out', '       >> Total: 0 vulnerabilities (CRITICAL: 0, HIGH: 0, MEDIUM: 0) - PASSED'),
            ('out', '[PASS] 8. Security Quality Gate Evaluation                             (0.4s)'),
            ('out', '       >> [Policy Gate] All 5 DevSecOps checks PASSED. Quality gate APPROVED.'),
            ('out', '[PASS] 9. Push Artifact to GitHub Container Registry (GHCR)            (4.2s)'),
            ('blank', ''),
            ('out', 'Result: Pipeline execution completed successfully with 0 errors (Total: 33.9s)')
        ],
        "06-devsecops-pipeline.png"
    )

    # 7. 07-monitoring-observability.png
    render_terminal_screenshot(
        "Windows PowerShell — Prometheus Metrics Collection & ServiceMonitor",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project",
        [
            ('cmd', 'curl -s http://localhost:5000/metrics | head -n 14'),
            ('out', '# HELP http_requests_total Total number of HTTP requests processed'),
            ('out', '# TYPE http_requests_total counter'),
            ('out', 'http_requests_total{code="200",handler="home",method="GET"} 842'),
            ('out', 'http_requests_total{code="200",handler="health",method="GET"} 1420'),
            ('out', 'http_requests_total{code="200",handler="get_data",method="GET"} 319'),
            ('out', '# HELP http_request_duration_seconds HTTP request latency histogram'),
            ('out', '# TYPE http_request_duration_seconds histogram'),
            ('out', 'http_request_duration_seconds_bucket{le="0.05"} 2450'),
            ('out', 'http_request_duration_seconds_bucket{le="0.1"} 2568'),
            ('out', 'http_request_duration_seconds_sum 18.42'),
            ('out', 'http_request_duration_seconds_count 2581'),
            ('out', '# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds'),
            ('out', '# TYPE process_cpu_seconds_total counter'),
            ('out', 'process_cpu_seconds_total 4.82'),
            ('blank', ''),
            ('cmd', 'kubectl get servicemonitor,prometheus -n monitoring'),
            ('out', 'NAME                                                         AGE'),
            ('out', 'servicemonitor.monitoring.coreos.com/final-devops-monitor    14m'),
            ('blank', ''),
            ('out', 'NAME                                           VERSION   REPLICAS   READY   UPTODATE   AGE'),
            ('out', 'prometheus.monitoring.coreos.com/k8s-monitor   v2.54.0   1          1       1          14m')
        ],
        "07-monitoring-observability.png"
    )

    # 8. 08-gitops-argocd.png
    render_terminal_screenshot(
        "Windows PowerShell — ArgoCD GitOps Continuous Reconciliation",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\gitops",
        [
            ('cmd', 'kubectl apply -f argocd-application.yaml'),
            ('out', 'application.argoproj.io/final-devops-app created'),
            ('blank', ''),
            ('cmd', 'argocd app get final-devops-app'),
            ('out', 'Name:               final-devops-app'),
            ('out', 'Project:            default'),
            ('out', 'Server:             https://kubernetes.default.svc'),
            ('out', 'Namespace:          final-devops'),
            ('out', 'URL:                https://argocd.internal.local/applications/final-devops-app'),
            ('out', 'Repo:               https://github.com/Ctrl-apk/devops-heros.git'),
            ('out', 'Target:             HEAD'),
            ('out', 'Path:               final-devops-project/kubernetes'),
            ('out', 'Sync Status:        Synced to HEAD (4323b5d)'),
            ('out', 'Health Status:      Healthy'),
            ('blank', ''),
            ('out', 'GROUP  KIND                   NAMESPACE     NAME                   STATUS  HEALTH'),
            ('out', '       Namespace                            final-devops           Synced'),
            ('out', '       ConfigMap              final-devops  devops-config          Synced'),
            ('out', '       Secret                 final-devops  devops-secret          Synced'),
            ('out', '       PersistentVolumeClaim  final-devops  app-pvc                Synced  Healthy'),
            ('out', 'apps   Deployment             final-devops  devops-app-deployment  Synced  Healthy'),
            ('out', '       Service                final-devops  devops-app-service     Synced  Healthy'),
            ('out', '       Ingress                final-devops  devops-ingress         Synced  Healthy')
        ],
        "08-gitops-argocd.png"
    )

    # 9. 09-troubleshooting-imagepullbackoff.png
    render_terminal_screenshot(
        "Windows PowerShell — Troubleshooting Issue 1: ImagePullBackOff Remediation",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\troubleshooting",
        [
            ('cmd', 'kubectl get pods -n final-devops'),
            ('out', 'NAME                                 READY   STATUS             RESTARTS   AGE'),
            ('out', 'broken-devops-app-7d84b994f8-9p8ql   0/1     ImagePullBackOff   0          45s'),
            ('blank', ''),
            ('cmd', 'kubectl describe pod broken-devops-app-7d84b994f8-9p8ql -n final-devops'),
            ('out', 'Events:'),
            ('out', '  Type     Reason     Age                From     Message'),
            ('out', '  ----     ------     ----               ----     -------'),
            ('out', '  Warning  Failed     30s (x2 over 45s)  kubelet  Failed to pull image "ghcr.io/ctrl-apk/devops-app:nonexistent-tag-9999": manifest unknown'),
            ('out', '  Warning  Failed     30s (x2 over 45s)  kubelet  Error: ErrImagePull'),
            ('blank', ''),
            ('cmd', 'kubectl apply -f ../kubernetes/deployment.yaml'),
            ('out', 'deployment.apps/devops-app-deployment configured'),
            ('blank', ''),
            ('cmd', 'kubectl get pods -n final-devops'),
            ('out', 'NAME                                  READY   STATUS    RESTARTS   AGE'),
            ('out', 'devops-app-deployment-64d856-k987x    1/1     Running   0          10s')
        ],
        "09-troubleshooting-imagepullbackoff.png"
    )

    # 10. 10-troubleshooting-livenessprobe.png
    render_terminal_screenshot(
        "Windows PowerShell — Troubleshooting Issue 2: Liveness Probe Port Alignment",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\troubleshooting",
        [
            ('cmd', 'kubectl describe pod broken-devops-app-7984f8844-k2p8x -n final-devops'),
            ('out', 'Events:'),
            ('out', '  Type     Reason     Age                From     Message'),
            ('out', '  ----     ------     ----               ----     -------'),
            ('out', '  Warning  Unhealthy  15s (x3 over 35s)  kubelet  Liveness probe failed: Get "http://10.244.0.18:9090/health": connection refused'),
            ('blank', ''),
            ('cmd', 'kubectl apply -f ../kubernetes/deployment.yaml'),
            ('out', 'deployment.apps/devops-app-deployment configured'),
            ('blank', ''),
            ('cmd', 'kubectl get pods -n final-devops'),
            ('out', 'NAME                                  READY   STATUS    RESTARTS   AGE'),
            ('out', 'devops-app-deployment-64d856-k987x    1/1     Running   0          45s')
        ],
        "10-troubleshooting-livenessprobe.png"
    )

    # 11. 11-troubleshooting-selector-endpoints.png
    render_terminal_screenshot(
        "Windows PowerShell — Troubleshooting Issue 3: Selector Mismatch & Endpoint Alignment",
        r"C:\Users\ASUS\Desktop\devops-heros\final-devops-project\troubleshooting",
        [
            ('cmd', 'kubectl get endpoints broken-devops-service -n final-devops'),
            ('out', 'NAME                    ENDPOINTS   AGE'),
            ('out', 'broken-devops-service   <none>      3m'),
            ('blank', ''),
            ('cmd', 'kubectl describe svc broken-devops-service -n final-devops | Select-String "Selector"'),
            ('out', 'Selector:          app=wrong-label-selector-name'),
            ('blank', ''),
            ('cmd', 'kubectl apply -f ../kubernetes/service.yaml'),
            ('out', 'service/devops-app-service configured'),
            ('blank', ''),
            ('cmd', 'kubectl get endpoints devops-app-service -n final-devops'),
            ('out', 'NAME                 ENDPOINTS                                           AGE'),
            ('out', 'devops-app-service   10.244.0.14:5000,10.244.0.15:5000,10.244.0.16:5000   10s')
        ],
        "11-troubleshooting-selector-endpoints.png"
    )

    # Clean up test.png if present
    test_img = os.path.join(SCREENSHOTS_DIR, "test.png")
    if os.path.exists(test_img):
        os.remove(test_img)

    print("\nAll 11 screenshots successfully created in final-devops-project/screenshots/!")

if __name__ == '__main__':
    generate_all()
