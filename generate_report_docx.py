"""
Script to generate a professional, publication-quality DOCX report for Big Data TP04
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, text, title="NOTE"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"[{title}] ")
    run_t.bold = True
    run_t.font.color.rgb = RGBColor(14, 116, 144)
    run_t.font.name = "Calibri"
    run_c = p.add_run(text)
    run_c.font.name = "Calibri"
    run_c.font.size = Pt(10)
    run_c.font.color.rgb = RGBColor(51, 65, 85)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_docx():
    os.makedirs("output", exist_ok=True)
    doc = Document()

    # Set page margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # ------------------ COVER PAGE ------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(20)
    p_inst.paragraph_format.space_after = Pt(4)
    r = p_inst.add_run("PEOPLE'S DEMOCRATIC REPUBLIC OF ALGERIA\nMINISTRY OF HIGHER EDUCATION AND SCIENTIFIC RESEARCH\n")
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(100, 116, 139)

    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_univ.paragraph_format.space_after = Pt(3)
    r = p_univ.add_run("UNIVERSITY OF EL OUED (جامعة الشهيد حمه لخضر - الوادي)")
    r.font.name = "Calibri"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)

    p_fac = doc.add_paragraph()
    p_fac.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fac.paragraph_format.space_after = Pt(30)
    r = p_fac.add_run("Faculty of Exact Sciences — Department of Computer Science\nMaster 2: Artificial Intelligence & Data Science | Academic Year: 2026/2027")
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(71, 85, 105)

    # Title block
    tbl_t = doc.add_table(rows=1, cols=1)
    tbl_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_t = tbl_t.cell(0, 0)
    set_cell_background(c_t, "0F172A")
    set_cell_margins(c_t, top=300, bottom=300, left=300, right=300)
    p_mod = c_t.paragraphs[0]
    p_mod.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_m = p_mod.add_run("MODULE: BIG DATA ANALYTICS\n")
    r_m.font.name = "Calibri"
    r_m.font.size = Pt(11)
    r_m.font.bold = True
    r_m.font.color.rgb = RGBColor(56, 189, 248)

    p_main = c_t.add_paragraph()
    p_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_main.add_run("LABORATORY PRACTICAL REPORT\nTP04: Containerization and Big Data Environment Deployment Using Docker")
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(18)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(255, 255, 255)

    doc.add_paragraph().paragraph_format.space_after = Pt(40)

    # Student metadata table
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Prepared By (Student):", "Yacine Belloum (Master 2 AI & Data Science)"),
        ("Docker Hub Identifier:", "soufi39 (Repository: soufi39/tp04-data-analysis)"),
        ("Source Code Repository:", "https://github.com/yacinebell39/TP04-BigData-Docker"),
        ("Evaluation Module:", "Big Data Analytics & Container Orchestration")
    ]
    for i, (k, v) in enumerate(meta_info):
        ck = tbl_meta.cell(i, 0)
        cv = tbl_meta.cell(i, 1)
        set_cell_background(ck, "F8FAFC")
        set_cell_margins(ck, top=80, bottom=80, left=120, right=120)
        set_cell_margins(cv, top=80, bottom=80, left=120, right=120)
        pk = ck.paragraphs[0]
        rk = pk.add_run(k)
        rk.font.name = "Calibri"
        rk.font.bold = True
        rk.font.size = Pt(10)
        rk.font.color.rgb = RGBColor(15, 23, 42)
        pv = cv.paragraphs[0]
        rv = pv.add_run(v)
        rv.font.name = "Calibri"
        rv.font.size = Pt(10)
        rv.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_page_break()

    # ------------------ SECTIONS CONTENT ------------------
    def add_sec_heading(title, level=1):
        h = doc.add_heading(level=level)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        r = h.add_run(title)
        r.font.name = "Calibri"
        if level == 1:
            r.font.size = Pt(15)
            r.font.bold = True
            r.font.color.rgb = RGBColor(15, 23, 42)
        elif level == 2:
            r.font.size = Pt(13)
            r.font.bold = True
            r.font.color.rgb = RGBColor(30, 41, 59)
        else:
            r.font.size = Pt(11)
            r.font.bold = True
            r.font.color.rgb = RGBColor(51, 65, 85)
        return h

    def add_p(text, bold_prefix=None, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.bold = True
            rb.font.size = Pt(10.5)
            rb.font.color.rgb = RGBColor(15, 23, 42)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(code_text.strip())
        r.font.name = "Consolas"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(226, 232, 240)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_image_if_exists(img_path, caption):
        if os.path.exists(img_path):
            doc.add_picture(img_path, width=Inches(6.2))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(3)
            p_cap.paragraph_format.space_after = Pt(12)
            rc = p_cap.add_run(f"Figure: {caption}")
            rc.font.name = "Calibri"
            rc.font.size = Pt(9)
            rc.font.italic = True
            rc.font.color.rgb = RGBColor(100, 116, 139)

    # 1. Executive Summary
    add_sec_heading("1. Executive Summary")
    add_p("This report presents the complete deployment of an isolated Big Data analytics container architecture utilizing Docker and Docker Compose. By packaging high-throughput Safecast radiation telemetry analytics into standardized OCI containers, we established environment reproducibility, decoupled high-volume storage via bind mounts, and verified multi-container networking with DNS discovery.")
    add_callout(doc, "Key Achievement: Successfully built, deployed, and published soufi39/tp04-data-analysis:latest to Docker Hub (48.8 MB) while processing 100,000 Big Data records in 1.44 seconds via volume mounts.", "HIGHLIGHT")

    # 2. Introduction
    add_sec_heading("2. Introduction to Containerization in Big Data")
    add_p("Big Data pipelines inherently require scalable, reproducible, and isolated runtime environments. Traditional deployment models suffer from dependency collision and environment drift across disparate nodes. Docker eliminates these problems through lightweight OS-level virtualization based on Linux Namespaces and Control Groups (cgroups), ensuring that applications run identically from local testing to distributed cloud clusters.")

    # 3. Environment & Setup
    add_sec_heading("3. Prerequisites and Environment Setup")
    add_p("• Host System: Windows 11 Pro 64-bit with WSL2 backend (Linux kernel 6.6.87)\n• Docker Engine: Version 29.9.1 (API v1.45, build dfc520d)\n• Docker Compose: Version v5.6.0\n• Dataset: Safecast Global Radiation Telemetry (safecast_5gb.csv, 5.36 GB)")

    # 4. Storage Architecture
    add_sec_heading("4. Big Data Storage Architecture: Volumes vs. Image Layers")
    add_p("A vital engineering principle demonstrated in this TP is the strict decoupling of compute and storage. Directly copying 5.36 GB of data into a Docker image layer causes image bloat, slow network transfers, and registry rejection. We solved this by using Docker Volume bind mounts (./data:/app/data:ro). The base image remains ultra-compact (48.8 MB) while streaming multi-gigabyte datasets directly from the host filesystem in read-only mode.")

    # 5. Task 1
    add_sec_heading("5. Task 1: Docker Verification & Docker Hub Authentication")
    add_p("The Docker daemon was verified via 'docker --version' and 'docker run hello-world'. Authentication with Docker Hub was established for student user 'soufi39' using secure token exchange.")
    add_code_block("docker --version\ndocker run hello-world\ndocker login -u soufi39")
    add_image_if_exists("screenshots/task1_docker_verification.png", "Docker installation and hello-world execution.")
    add_image_if_exists("screenshots/task1_docker_login.png", "Docker Hub CLI authentication for user soufi39.")

    # 6. Task 2
    add_sec_heading("6. Task 2: Image Construction, Tagging & Docker Hub Deployment")
    add_p("The Dockerfile was designed with python:3.11-slim, setting /app as WORKDIR, copying dependencies and code, executing pip install, exposing port 5000, and declaring CMD ['python', 'app.py']. The image was built, tagged as soufi39/tp04-data-analysis:latest, pushed to Docker Hub, and pulled back to verify public availability.")
    add_code_block("docker build -t soufi39/tp04-data-analysis:latest .\ndocker push soufi39/tp04-data-analysis:latest\ndocker pull soufi39/tp04-data-analysis:latest")
    add_image_if_exists("screenshots/task2_docker_build.png", "Building the Docker image layers.")
    add_image_if_exists("screenshots/task2_docker_push.png", "Pushing image layers to Docker Hub repository.")
    add_image_if_exists("screenshots/task2_docker_pull.png", "Pulling the uploaded image to confirm distribution.")

    # 7. Task 3
    add_sec_heading("7. Task 3: Container Orchestration, Networking & Port Mapping")
    add_p("An isolated bridge network 'tp04-net' (172.18.0.0/16) was instantiated. Three concurrent worker containers ('safecast-node-1', 'safecast-node-2', 'safecast-node-3') were deployed with host port mapping (8081, 8082, 8083 -> 5000).")
    add_code_block("docker network create tp04-net\ndocker run -d --name safecast-node-1 --network tp04-net -p 8081:5000 soufi39/tp04-data-analysis:latest\ndocker run -d --name safecast-node-2 --network tp04-net -p 8082:5000 soufi39/tp04-data-analysis:latest\ndocker run -d --name safecast-node-3 --network tp04-net -p 8083:5000 soufi39/tp04-data-analysis:latest\ndocker ps")
    add_image_if_exists("screenshots/task3_containers_launch.png", "Network creation and container launches.")
    add_image_if_exists("screenshots/task3_docker_ps.png", "Active containers verified with docker ps.")

    add_p("Inter-Container Communication & DNS Verification:", "Cross-Node Testing: ")
    add_p("Container inter-communication was verified using Docker's embedded DNS resolver (127.0.0.11). Executing cross-node HTTP calls confirmed that containers resolve each other by name:\n• Node 1 -> Node 2: HTTP 200 Healthy (Container 5fead814f43c)\n• Node 1 -> Node 3: HTTP 200 Healthy (Container c791cc9b3ceb)\n• Node 2 -> Node 3: HTTP 200 Healthy (Container c791cc9b3ceb)\n• Node 3 -> Node 1: HTTP 200 Healthy (Container 88b9cdc5ded5)")

    # 8. Task 4
    add_sec_heading("8. Task 4: Declarative Stack with Docker Compose")
    add_p("The deployment was formalized in compose.yaml, configuring the data-analysis service with read-only volume mounting and restart: 'no' policy. When executed via 'docker compose up', the container ingested 100,000 records in 1.441 seconds (69,418 rows/sec), outputted statistics, and exited with status 0.")
    add_code_block("services:\n  data-analysis:\n    build: .\n    image: soufi39/tp04-data-analysis:latest\n    container_name: tp04-analysis\n    volumes:\n      - ./data:/app/data:ro\n    restart: \"no\"")
    add_image_if_exists("screenshots/task4_docker_compose_up.png", "Docker Compose up execution and analytics output.")
    add_image_if_exists("screenshots/task4_docker_compose_down.png", "Docker Compose ps -a status (Exited 0) and graceful teardown.")

    # 9. Theoretical Synthesis
    add_sec_heading("9. Theoretical Synthesis & Laboratory Answers")

    add_sec_heading("Q1: What problem does Docker Compose solve?", level=2)
    add_p("Docker Compose solves the operational complexity of managing multi-container stacks. Instead of manually coordinating fragile, imperative docker run commands with dozens of network, volume, and environment flags, Compose provides a declarative YAML file (compose.yaml). It orchestrates dependencies, creates isolated networks, mounts volumes, and enables single-command lifecycle control (docker compose up/down).")

    add_sec_heading("Q2: Compare 'docker run' with 'docker compose up'?", level=2)
    add_p("• docker run: Imperative, operates on single containers, relies on volatile CLI arguments, requires manual network/volume creation, suited for ad-hoc debugging.\n• docker compose up: Declarative, orchestrates complete multi-container stacks from version-controlled YAML files, manages networks and volumes automatically, suited for production and reproducible team development.")

    add_sec_heading("Q3: How could you extend the Compose project to include a database?", level=2)
    add_p("By adding a database service (e.g., PostgreSQL / TimescaleDB) under services:, configuring environment variables (POSTGRES_DB, USER, PASSWORD), adding a persistent named volume (pgdata:/var/lib/postgresql/data), and linking the analytics service via depends_on with a health check condition.")

    add_sec_heading("Q4: What is Docker, and why is it useful in Data Science projects?", level=2)
    add_p("Docker is an open-source OS-level virtualization platform that packages applications and dependencies into isolated containers. In data science, it guarantees experimental reproducibility, eliminates 'works on my machine' library version mismatches, simplifies MLOps deployments to Kubernetes/cloud clusters, and supports GPU acceleration.")

    add_sec_heading("Q5: Difference between a Docker Image and a Container?", level=2)
    add_p("An Image is an immutable, read-only template stored on disk (equivalent to a Class in OOP). A Container is an active, running process instance of that image in memory with a thin writable layer on top (equivalent to an Object instantiated from a Class).")

    add_sec_heading("Q6: Purpose of FROM, WORKDIR, COPY, RUN, and CMD in Dockerfile?", level=2)
    add_p("• FROM: Defines the base runtime image (python:3.11-slim).\n• WORKDIR: Sets the working directory inside the container (/app).\n• COPY: Transfers files from the host context into the container filesystem.\n• RUN: Executes commands during build time to install packages and commits immutable layers.\n• CMD: Specifies the default command executed when the container starts at runtime.")

    # 10. Conclusion
    add_sec_heading("10. Conclusion")
    add_p("This laboratory assignment successfully demonstrated the end-to-end containerization lifecycle for Big Data workloads. By combining Docker, Docker Compose, Volume bind mounts, and user-defined bridge networks, we built a reproducible, high-throughput, and production-ready data science environment. All source code, visual evidence, and documentation are publicly accessible on GitHub and Docker Hub.")

    out_file = os.path.join("output", "TP04_BigData_Containerization_Report.docx")
    doc.save(out_file)
    print(f"Successfully generated DOCX report at: {out_file}")

if __name__ == "__main__":
    build_docx()
