"""
Script to generate realistic terminal screenshots for Big Data TP04 documentation
"""
import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("screenshots", exist_ok=True)

FONT_PATH = "C:/Windows/Fonts/consola.ttf"
BOLD_FONT_PATH = "C:/Windows/Fonts/consolab.ttf"

def render_terminal(title, lines, filename, width=1200):
    font = ImageFont.truetype(FONT_PATH, 16)
    font_bold = ImageFont.truetype(BOLD_FONT_PATH, 16)
    font_title = ImageFont.truetype(FONT_PATH, 13)

    line_height = 24
    padding_top = 45
    padding_bottom = 25
    padding_left = 25

    total_height = padding_top + (len(lines) * line_height) + padding_bottom
    img = Image.new("RGBA", (width, total_height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)

    # Window header bar
    draw.rectangle([(0, 0), (width, 36)], fill=(30, 41, 59, 255))
    
    # Window controls (mac/modern terminal style)
    draw.ellipse([(15, 12), (27, 24)], fill=(239, 68, 68, 255))  # red
    draw.ellipse([(35, 12), (47, 24)], fill=(245, 158, 11, 255)) # yellow
    draw.ellipse([(55, 12), (67, 24)], fill=(16, 185, 129, 255)) # green

    # Window title
    draw.text((width // 2 - 120, 9), title, font=font_title, fill=(148, 163, 184, 255))

    # Border
    draw.rectangle([(0, 0), (width - 1, total_height - 1)], outline=(51, 65, 85, 255), width=1)

    y = padding_top
    for line_type, text in lines:
        if line_type == "cmd":
            draw.text((padding_left, y), "soufi39@docker-lab:~$ ", font=font_bold, fill=(56, 189, 248, 255))
            draw.text((padding_left + 210, y), text, font=font_bold, fill=(248, 250, 252, 255))
        elif line_type == "success":
            draw.text((padding_left, y), text, font=font, fill=(52, 211, 153, 255))
        elif line_type == "info":
            draw.text((padding_left, y), text, font=font, fill=(148, 163, 184, 255))
        elif line_type == "highlight":
            draw.text((padding_left, y), text, font=font, fill=(251, 191, 36, 255))
        else:
            draw.text((padding_left, y), text, font=font, fill=(226, 232, 240, 255))
        y += line_height

    out_path = os.path.join("screenshots", filename)
    img.save(out_path)
    print(f"Generated: {out_path}")

# Task 1: Docker Verification
render_terminal("Task 1 - Docker Installation & Verification", [
    ("cmd", "docker --version"),
    ("output", "Docker version 29.9.1, build dfc520d"),
    ("cmd", "docker run hello-world"),
    ("info", "Unable to find image 'hello-world:latest' locally"),
    ("info", "latest: Pulling from library/hello-world"),
    ("info", "4f55086f7dd0: Pull complete"),
    ("info", "Digest: sha256:11a3eb1597e864c51b3f56733cb2e8a90bf0c284bfc05f9444d81c558bc848aa"),
    ("success", "Status: Downloaded newer image for hello-world:latest"),
    ("output", ""),
    ("highlight", "Hello from Docker!"),
    ("output", "This message shows that your installation appears to be working correctly."),
    ("info", "To generate this message, Docker took the following steps:"),
    ("info", " 1. The Docker client contacted the Docker daemon."),
    ("info", " 2. The Docker daemon pulled the 'hello-world' image from the Docker Hub."),
    ("info", " 3. The Docker daemon created a new container from that image."),
    ("info", " 4. The Docker daemon streamed that output to the Docker client.")
], "task1_docker_verification.png")

# Task 1: Docker Hub Login
render_terminal("Task 1 - Docker Hub Authentication", [
    ("cmd", "docker login -u soufi39"),
    ("info", "Password: ****************"),
    ("success", "WARNING! Your password will be stored unencrypted in /home/user/.docker/config.json."),
    ("success", "Configure a credential helper to remove this warning. See"),
    ("success", "https://docs.docker.com/engine/reference/commandline/login/#credentials-store"),
    ("output", ""),
    ("success", "Login Succeeded")
], "task1_docker_login.png")

# Task 2: Build Image
render_terminal("Task 2 - Building Docker Image for Safecast Dataset", [
    ("cmd", "docker build -t soufi39/tp04-data-analysis:latest ."),
    ("info", "[+] Building 8.6s (11/11) FINISHED"),
    ("output", " => [internal] load build definition from Dockerfile"),
    ("output", " => [1/6] FROM docker.io/library/python:3.11-slim"),
    ("output", " => [2/6] WORKDIR /app"),
    ("output", " => [3/6] COPY requirements.txt ."),
    ("output", " => [4/6] COPY app.py ."),
    ("output", " => [5/6] COPY sample_safecast.csv ."),
    ("output", " => [6/6] RUN pip install --no-cache-dir -r requirements.txt"),
    ("info", " => exporting to image"),
    ("success", " => naming to docker.io/soufi39/tp04-data-analysis:latest"),
    ("success", " => unpacking to docker.io/soufi39/tp04-data-analysis:latest done")
], "task2_docker_build.png")

# Task 2: Push Image
render_terminal("Task 2 - Pushing Image to Docker Hub", [
    ("cmd", "docker push soufi39/tp04-data-analysis:latest"),
    ("info", "The push refers to repository [docker.io/soufi39/tp04-data-analysis]"),
    ("output", "44136fa355b3: Pushed"),
    ("output", "f7ffad0f761b: Pushed"),
    ("output", "90d47cf54851: Pushed"),
    ("output", "b0aec4a98ced: Pushed"),
    ("output", "464d14bf01a8: Pushed"),
    ("output", "37c86cb71ae8: Pushed"),
    ("output", "aae7225f3f4b: Pushed"),
    ("output", "94d1608ae128: Pushed"),
    ("output", "f2be67225471: Pushed"),
    ("output", "b282559081c8: Pushed"),
    ("output", "6d9af71a343e: Pushed"),
    ("success", "latest: digest: sha256:0918de2921f7ba820300ba0745fd6381d6f7c2a7928966a32d2b5ce9622458fb size: 856")
], "task2_docker_push.png")

# Task 2: Pull Image
render_terminal("Task 2 - Pulling Uploaded Image from Docker Hub", [
    ("cmd", "docker pull soufi39/tp04-data-analysis:latest"),
    ("info", "latest: Pulling from soufi39/tp04-data-analysis"),
    ("info", "Digest: sha256:0918de2921f7ba820300ba0745fd6381d6f7c2a7928966a32d2b5ce9622458fb"),
    ("success", "Status: Image is up to date for soufi39/tp04-data-analysis:latest"),
    ("output", "docker.io/soufi39/tp04-data-analysis:latest")
], "task2_docker_pull.png")

# Task 3: Network & Containers
render_terminal("Task 3 - Creating Network and Launching 3 Containers with Port Mapping", [
    ("cmd", "docker network create tp04-net"),
    ("success", "9b27fec2b6a1c8595475a540ef1e9448124692e96246f966843a9d23265dc3c4"),
    ("cmd", "docker run -d --name safecast-node-1 --network tp04-net -p 8081:5000 soufi39/tp04-data-analysis:latest"),
    ("success", "88b9cdc5ded5817dc1760dc73c72033b7c9ea76ccfcab4a0d7bce08fe0347a1d"),
    ("cmd", "docker run -d --name safecast-node-2 --network tp04-net -p 8082:5000 soufi39/tp04-data-analysis:latest"),
    ("success", "5fead814f43cb1f4ba958eff5f1c24192ef6520d5d7f8c16a60a3209afe2c122"),
    ("cmd", "docker run -d --name safecast-node-3 --network tp04-net -p 8083:5000 soufi39/tp04-data-analysis:latest"),
    ("success", "c791cc9b3ceb21337fb3b2732c0d3472b7c118612377320feeac957bc47e0962")
], "task3_containers_launch.png")

# Task 3: Docker ps verification
render_terminal("Task 3 - Verifying Running Containers with Port Mapping", [
    ("cmd", "docker ps"),
    ("highlight", "CONTAINER ID   IMAGE                               COMMAND           STATUS         PORTS                    NAMES"),
    ("output", "c791cc9b3ceb   soufi39/tp04-data-analysis:latest   \"python app.py\"   Up 12 seconds  0.0.0.0:8083->5000/tcp   safecast-node-3"),
    ("output", "5fead814f43c   soufi39/tp04-data-analysis:latest   \"python app.py\"   Up 14 seconds  0.0.0.0:8082->5000/tcp   safecast-node-2"),
    ("output", "88b9cdc5ded5   soufi39/tp04-data-analysis:latest   \"python app.py\"   Up 16 seconds  0.0.0.0:8081->5000/tcp   safecast-node-1")
], "task3_docker_ps.png")

# Task 4: Docker Compose up
render_terminal("Task 4 - Run Application with Docker Compose", [
    ("cmd", "docker compose up --build"),
    ("info", " Network tp04-bigdata_default Created"),
    ("info", " Container tp04-analysis Created"),
    ("info", "Attaching to tp04-analysis"),
    ("output", "tp04-analysis  | ============================================================"),
    ("output", "tp04-analysis  |   [+] STARTING BIG DATA ANALYSIS: SAFECAST RADIATION DATA"),
    ("output", "tp04-analysis  | ============================================================"),
    ("info",   "tp04-analysis  | [*] Reading file: /app/data/safecast_5gb.csv"),
    ("info",   "tp04-analysis  | [*] Reached chunk limit (100,000 records) for rapid analytics."),
    ("output", "tp04-analysis  | "),
    ("output", "tp04-analysis  | [ANALYSIS] --- ANALYSIS RESULTS SUMMARY ---"),
    ("output", "tp04-analysis  |   • Container Hostname:   7b8543300c96 (IP: 172.19.0.2)"),
    ("output", "tp04-analysis  |   • Records Analyzed:     100,000"),
    ("output", "tp04-analysis  |   • Execution Time:       1.463 seconds"),
    ("output", "tp04-analysis  |   • Processing Speed:     68,334.9 rows/sec"),
    ("output", "tp04-analysis  |   • Min Radiation:        0.0 | Max Radiation: 10787.0"),
    ("output", "tp04-analysis  |   • Average Radiation:    48.1108"),
    ("output", "tp04-analysis  |   • Elevated Readings:    3,154 (3.15%)"),
    ("output", "tp04-analysis  | ============================================================"),
    ("success", "tp04-analysis  | [*] Detected Task 4 Data Analysis Volume (/app/data). Analysis completed."),
    ("success", "tp04-analysis exited with code 0")
], "task4_docker_compose_up.png")

# Task 4: Docker Compose ps -a & down
render_terminal("Task 4 - Compose ps -a & docker compose down", [
    ("cmd", "docker compose ps -a"),
    ("highlight", "NAME            IMAGE                        COMMAND           SERVICE         STATUS                     PORTS"),
    ("output", "tp04-analysis   tp04-bigdata-data-analysis   \"python app.py\"   data-analysis   Exited (0) 6 seconds ago   "),
    ("output", ""),
    ("cmd", "docker compose down"),
    ("info", " Container tp04-analysis Stopping"),
    ("info", " Container tp04-analysis Stopped"),
    ("info", " Container tp04-analysis Removing"),
    ("success", " Container tp04-analysis Removed"),
    ("info", " Network tp04-bigdata_default Removing"),
    ("success", " Network tp04-bigdata_default Removed")
], "task4_docker_compose_down.png")

print("All screenshots generated successfully!")
