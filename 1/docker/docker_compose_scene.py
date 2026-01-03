from manim import *
import os

# --- Configuration ---
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60

# --- Palette ---
DOCKER_BLUE = "#2496ED"
LARAVEL_RED = "#FF2D20"
VUE_GREEN = "#42b883"
FLUTTER_BLUE = "#02569B"
SUCCESS_GREEN = "#28a745"
FAIL_RED = "#dc3545"
WARN_COLOR = "#ffc107"
HOST_COLOR = "#555555"

# --- VSCode Colors ---
VSCODE_BG = "#1e1e1e"
VSCODE_SIDEBAR = "#252526"
VSCODE_TITLEBAR = "#323233"
VSCODE_BLUE = "#569cd6"
VSCODE_GREEN = "#6a9955"
VSCODE_ORANGE = "#ce9178"
VSCODE_YELLOW = "#dcdcaa"
VSCODE_WHITE = "#d4d4d4"
VSCODE_GRAY = "#6a6a6a"
VSCODE_CYAN = "#4ec9b0"
VSCODE_PURPLE = "#c586c0"

# --- Paths ---
# Use absolute paths to prevent "File Not Found" errors
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(SCRIPT_DIR, "sounds/")
ASSET_DIR = os.path.join(SCRIPT_DIR, "asset/")

class TikTokScene(Scene):
    def setup(self):
        # Universal Background
        self.bg = Rectangle(width=10, height=17, fill_color="#111111", fill_opacity=1, stroke_width=0).set_z_index(-10)
        self.grid = NumberPlane(x_range=[-10, 10], y_range=[-20, 20], background_line_style={"stroke_opacity": 0.1}).set_z_index(-9)
        self.add(self.bg, self.grid)

    def add_sound_safe(self, filename, gain=-10):
        path = os.path.join(SOUND_DIR, filename)
        if os.path.exists(path): self.add_sound(path, gain=gain)

    def load_asset(self, filename, scale=1.0):
        path = os.path.join(ASSET_DIR, filename)
        if os.path.exists(path):
            if filename.endswith('.svg'): return SVGMobject(path).scale(scale)
            return ImageMobject(path).scale(scale)
        return Text(filename, font_size=24, color=RED).scale(scale)

    def create_vscode_window(self, code_lines, title="script.php", height=6.0, width=7.5):
        # 1. Container Structure
        box = RoundedRectangle(corner_radius=0.15, width=width, height=height,
                               color=VSCODE_SIDEBAR, fill_color=VSCODE_BG, fill_opacity=1, stroke_width=2)
        title_bar = Rectangle(width=width, height=0.5, color=VSCODE_TITLEBAR, fill_opacity=1, stroke_width=0).move_to(box.get_top() + DOWN*0.25)
        buttons = VGroup(*[Circle(0.08, c, fill_opacity=1, stroke_width=0) for c in ["#ff5f56", "#ffbd2e", "#27ca40"]]).arrange(RIGHT, buff=0.12).move_to(title_bar.get_left() + RIGHT*0.5)
        tab_name = Text(title, font_size=12, color=VSCODE_WHITE).move_to(title_bar.get_center())
        gutter = Rectangle(width=0.6, height=height-0.5, color=VSCODE_BG, fill_opacity=1, stroke_width=0).move_to(box.get_left() + RIGHT*0.35 + DOWN*0.25)

        window_group = VGroup(box, title_bar, buttons, tab_name, gutter)

        # 2. Code Content Generation (With Auto-Scaling)
        text_group_list = []
        start_y = title_bar.get_bottom()[1] - 0.5
        start_x = gutter.get_right()[0] + 0.2
        max_code_width = width - 1.2 # Strict margin to prevent overflow

        for i, (line_num, parts) in enumerate(code_lines):
            y_pos = start_y - (i * 0.5)
            if y_pos < box.get_bottom()[1] + 0.2: break

            ln = Text(str(line_num), font_size=10, color=VSCODE_GRAY).move_to([gutter.get_center()[0], y_pos, 0])
            line_content = VGroup(ln)

            # Build the code line
            current_x = start_x
            code_line_group = VGroup()
            for text_str, color in parts:
                t = Text(text_str, font_size=12, font="Monospace", color=color)
                t.move_to([current_x + t.width/2, y_pos, 0])
                code_line_group.add(t)
                current_x += t.width + 0.08

            # --- CRITICAL FIX: Scale down line if it's too wide ---
            if code_line_group.width > max_code_width:
                code_line_group.scale(max_code_width / code_line_group.width)
                # Re-align left after scaling
                code_line_group.move_to([start_x + code_line_group.width/2, y_pos, 0])

            line_content.add(code_line_group)
            text_group_list.append(line_content)

        return window_group, text_group_list

    def play_outro(self):
        self.add_sound_safe("transition.mp3")
        self.play(*[FadeOut(m) for m in self.mobjects if m != self.bg and m != self.grid])

        potato = self.load_asset("potato.svg", scale=1.5)
        if isinstance(potato, Text): potato = Text("Thanks!", color=DOCKER_BLUE, font_size=60) # Fallback

        potato.move_to(ORIGIN)
        self.add_sound_safe("click.mp3")
        self.play(FadeIn(potato, scale=0.5))

        # Shake
        self.add_sound_safe("click.mp3")
        for _ in range(3):
            self.play(potato.animate.shift(LEFT*0.1).rotate(-0.05), run_time=0.08, rate_func=linear)
            self.play(potato.animate.shift(RIGHT*0.2).rotate(0.1), run_time=0.08, rate_func=linear)
            self.play(potato.animate.shift(LEFT*0.1).rotate(-0.05), run_time=0.08, rate_func=linear)

        self.add_sound_safe("build.mp3")
        self.play(potato.animate.scale(8).set_opacity(0), run_time=1.5)
        self.wait(0.5)


# ============================================
# DOCKER COMPOSE SCENE - MEANINGFUL & ANIMATED
# ============================================

class DockerComposeScene(TikTokScene):
    def construct(self):
        # ==========================================
        # ACT 1: THE PROBLEM - Manual Container Hell (0s - 50s)
        # ==========================================
        
        # Dramatic opening with Docker logo
        docker_logo = self.load_asset("docker.svg", scale=1.0)
        docker_logo.move_to(ORIGIN)
        
        self.add_sound_safe("build.mp3")
        self.play(FadeIn(docker_logo, scale=0.3), run_time=1.0)
        
        # Pulse effect
        for _ in range(2):
            self.play(docker_logo.animate.scale(1.15), rate_func=there_and_back, run_time=0.4)
        
        self.wait(0.5)
        
        # Move logo up and add title
        self.play(docker_logo.animate.move_to(UP * 5).scale(0.7), run_time=0.8)
        
        self.add_sound_safe("click.mp3")
        title = Text("DOCKER COMPOSE", font_size=52, color=DOCKER_BLUE, weight=BOLD)
        title.move_to(UP * 2.5)
        
        subtitle = Text("Multi-Container Made Simple", font_size=26, color=VSCODE_WHITE)
        subtitle.next_to(title, DOWN, buff=0.4)
        
        self.play(Write(title, run_time=1.0))
        self.play(FadeIn(subtitle, shift=UP*0.2))
        self.wait(1.5)
        
        # Transition to problem
        self.add_sound_safe("transition.mp3")
        self.play(FadeOut(docker_logo), FadeOut(title), FadeOut(subtitle))
        self.wait(0.3)
        
        # Show the problem scenario
        problem_title = Text("WITHOUT COMPOSE:", font_size=38, color=FAIL_RED, weight=BOLD)
        problem_title.move_to(UP * 6.5)
        self.add_sound_safe("click.mp3")
        self.play(Write(problem_title, run_time=0.8))
        
        # Show a frustrated developer
        dev_sad = self.load_asset("developer.svg", scale=0.5)
        dev_sad.move_to(UP * 4.5)
        self.play(FadeIn(dev_sad, scale=0.8))
        
        # Show the pain: Multiple terminal commands
        pain_label = Text("Managing 10+ commands manually", font_size=20, color=WARN_COLOR)
        pain_label.move_to(UP * 3)
        self.play(FadeIn(pain_label))
        self.wait(0.5)
        
        # Animated terminal commands appearing chaotically
        cmd_group = VGroup()
        commands_text = [
            "docker run mysql -e PASS=...",
            "docker run redis -p 6379",
            "docker run nginx -v ...",
            "docker network create app",
            "docker volume create data",
            "docker network connect...",
        ]
        
        for i, cmd_text in enumerate(commands_text):
            cmd = Text(f"$ {cmd_text}", font_size=16, font="Monospace", color=VSCODE_GRAY)
            cmd.move_to(UP * (1 - i * 0.6))
            cmd_group.add(cmd)
            
            self.add_sound_safe("typing_short.mp3")
            self.play(FadeIn(cmd, shift=RIGHT * 0.3), run_time=0.3)
            
            # Add error indicator
            if i % 2 == 0:
                error = Text("!", font_size=24, color=FAIL_RED, weight=BOLD)
                error.next_to(cmd, LEFT, buff=0.2)
                self.play(FadeIn(error, scale=0.5), run_time=0.2)
                cmd_group.add(error)
            
            self.wait(0.15)
        
        self.wait(0.5)
        
        # Add problem labels with icons
        problems = VGroup(
            Text("❌ Easy to forget steps", font_size=18, color=FAIL_RED),
            Text("❌ Hard to reproduce", font_size=18, color=FAIL_RED),
            Text("❌ Team onboarding nightmare", font_size=18, color=FAIL_RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 4.5)
        
        for problem in problems:
            self.add_sound_safe("click.mp3")
            self.play(FadeIn(problem, shift=RIGHT * 0.3), run_time=0.4)
            self.wait(0.3)
        
        self.add_sound_safe("Error_04_Universfield.mp3")
        
        # Shake everything
        chaos = VGroup(problem_title, dev_sad, pain_label, cmd_group, problems)
        for _ in range(3):
            self.play(chaos.animate.shift(LEFT*0.15), run_time=0.04)
            self.play(chaos.animate.shift(RIGHT*0.3), run_time=0.04)
            self.play(chaos.animate.shift(LEFT*0.15), run_time=0.04)
        
        self.wait(1.0)
        
        # Clear
        self.add_sound_safe("transition.mp3")
        self.play(FadeOut(chaos))
        self.wait(0.5)
        
        # ==========================================
        # ACT 2: THE SOLUTION - Docker Compose (50s - 110s)
        # ==========================================
        
        solution_title = Text("WITH COMPOSE:", font_size=38, color=SUCCESS_GREEN, weight=BOLD)
        solution_title.move_to(UP * 7.2)
        self.add_sound_safe("build.mp3")
        self.play(Write(solution_title, run_time=0.8))
        
        # Happy developer
        dev_happy = self.load_asset("developer.svg", scale=0.45)
        dev_happy.move_to(UP * 6)
        self.play(FadeIn(dev_happy, scale=0.8))
        self.wait(0.3)
        
        # Show docker-compose.yml with meaningful content
        compose_code = [
            (1, [("version:", VSCODE_PURPLE), (" '3.8'", VSCODE_ORANGE)]),
            (2, [("services:", VSCODE_BLUE)]),
            (3, []),
            (4, [("  ", VSCODE_WHITE), ("# Database", VSCODE_GREEN)]),
            (5, [("  ", VSCODE_WHITE), ("mysql:", VSCODE_CYAN)]),
            (6, [("    ", VSCODE_WHITE), ("image:", VSCODE_PURPLE), (" mysql:8", VSCODE_ORANGE)]),
            (7, [("    ", VSCODE_WHITE), ("environment:", VSCODE_PURPLE)]),
            (8, [("      ", VSCODE_WHITE), ("MYSQL_ROOT_PASSWORD:", VSCODE_CYAN), (" secret", VSCODE_ORANGE)]),
            (9, [("    ", VSCODE_WHITE), ("volumes:", VSCODE_PURPLE)]),
            (10, [("      - ", VSCODE_WHITE), ("db_data:/var/lib/mysql", VSCODE_ORANGE)]),
            (11, []),
            (12, [("  ", VSCODE_WHITE), ("# Cache", VSCODE_GREEN)]),
            (13, [("  ", VSCODE_WHITE), ("redis:", VSCODE_CYAN)]),
            (14, [("    ", VSCODE_WHITE), ("image:", VSCODE_PURPLE), (" redis:alpine", VSCODE_ORANGE)]),
            (15, []),
            (16, [("  ", VSCODE_WHITE), ("# Web Server", VSCODE_GREEN)]),
            (17, [("  ", VSCODE_WHITE), ("nginx:", VSCODE_CYAN)]),
            (18, [("    ", VSCODE_WHITE), ("image:", VSCODE_PURPLE), (" nginx:latest", VSCODE_ORANGE)]),
            (19, [("    ", VSCODE_WHITE), ("ports:", VSCODE_PURPLE)]),
            (20, [("      - ", VSCODE_WHITE), ('"80:80"', VSCODE_ORANGE)]),
        ]
        
        window, code_lines = self.create_vscode_window(
            compose_code,
            title="docker-compose.yml",
            height=10.5,
            width=7.6
        )
        window.move_to(DOWN * 0.5)
        
        # Animate window
        self.add_sound_safe("build.mp3")
        self.play(FadeIn(window, scale=0.9), run_time=0.7)
        self.wait(0.4)
        
        # Type code line by line
        for i, line in enumerate(code_lines):
            self.add_sound_safe("typing_short.mp3")
            self.play(FadeIn(line, shift=DOWN*0.08), run_time=0.3)
            self.wait(0.2)
        
        self.wait(1.0)
        
        # Highlight services with labels
        if len(code_lines) > 5:
            mysql_highlight = SurroundingRectangle(
                VGroup(code_lines[4], code_lines[5], code_lines[6]), 
                color="#FF6B6B", buff=0.08, corner_radius=0.05
            )
            mysql_label = Text("Database", font_size=13, color="#FF6B6B", weight=BOLD)
            mysql_label.next_to(mysql_highlight, LEFT, buff=0.15)
            
            self.add_sound_safe("click.mp3")
            self.play(Create(mysql_highlight), FadeIn(mysql_label))
            self.wait(0.6)
            
            if len(code_lines) > 13:
                redis_highlight = SurroundingRectangle(
                    VGroup(code_lines[12], code_lines[13]), 
                    color="#4ECDC4", buff=0.08, corner_radius=0.05
                )
                redis_label = Text("Cache", font_size=13, color="#4ECDC4", weight=BOLD)
                redis_label.next_to(redis_highlight, LEFT, buff=0.15)
                
                self.add_sound_safe("click.mp3")
                self.play(Create(redis_highlight), FadeIn(redis_label))
                self.wait(0.6)
                
                if len(code_lines) > 17:
                    nginx_highlight = SurroundingRectangle(
                        VGroup(code_lines[16], code_lines[17], code_lines[18]), 
                        color="#95E1D3", buff=0.08, corner_radius=0.05
                    )
                    nginx_label = Text("Web", font_size=13, color="#95E1D3", weight=BOLD)
                    nginx_label.next_to(nginx_highlight, LEFT, buff=0.15)
                    
                    self.add_sound_safe("click.mp3")
                    self.play(Create(nginx_highlight), FadeIn(nginx_label))
                    self.wait(1.0)
                    
                    self.play(
                        FadeOut(mysql_highlight), FadeOut(mysql_label),
                        FadeOut(redis_highlight), FadeOut(redis_label),
                        FadeOut(nginx_highlight), FadeOut(nginx_label)
                    )
        
        # Show the magic command
        self.add_sound_safe("build.mp3")
        magic_cmd = Text("docker-compose up", font_size=38, font="Monospace", color=SUCCESS_GREEN, weight=BOLD)
        magic_cmd.move_to(UP * 6.5)
        
        magic_box = RoundedRectangle(
            width=magic_cmd.width + 0.8,
            height=magic_cmd.height + 0.5,
            color=SUCCESS_GREEN,
            fill_opacity=0.15,
            stroke_width=4,
            corner_radius=0.15
        ).move_to(magic_cmd.get_center())
        
        self.play(Create(magic_box))
        self.add_sound_safe("typing_short.mp3")
        self.play(Write(magic_cmd), run_time=1.0)
        
        # Add "ONE COMMAND!" label
        one_cmd_label = Text("ONE COMMAND!", font_size=24, color=SUCCESS_GREEN, weight=BOLD)
        one_cmd_label.next_to(magic_box, DOWN, buff=0.25)
        self.add_sound_safe("click.mp3")
        self.play(FadeIn(one_cmd_label, shift=UP*0.2))
        
        # Pulse effect
        self.play(
            magic_box.animate.scale(1.08),
            magic_cmd.animate.scale(1.08),
            rate_func=there_and_back,
            run_time=0.6
        )
        
        self.wait(2.0)
        
        # Clear
        self.add_sound_safe("transition.mp3")
        self.play(
            FadeOut(solution_title),
            FadeOut(dev_happy),
            FadeOut(window),
            FadeOut(VGroup(*code_lines)),
            FadeOut(magic_cmd),
            FadeOut(magic_box),
            FadeOut(one_cmd_label)
        )
        self.wait(0.5)
        
        # ==========================================
        # ACT 3: HOW IT WORKS - Architecture (110s - 160s)
        # ==========================================
        
        arch_title = Text("HOW IT WORKS", font_size=44, color=DOCKER_BLUE, weight=BOLD)
        arch_title.move_to(UP * 7.2)
        self.add_sound_safe("click.mp3")
        self.play(Write(arch_title, run_time=0.8))
        self.wait(0.4)
        
        # Create detailed containers
        mysql_box = RoundedRectangle(width=2.6, height=1.8, corner_radius=0.15, 
                                      color="#FF6B6B", fill_opacity=0.2, stroke_width=3)
        mysql_img = self.load_asset("mysql.png", scale=0.4)
        mysql_text = Text("MySQL", font_size=15, color=VSCODE_WHITE, weight=BOLD)
        mysql_port = Text(":3306", font_size=11, color=VSCODE_GRAY)
        mysql_container = Group(mysql_box, mysql_img, mysql_text, mysql_port).arrange(DOWN, buff=0.12)
        mysql_container.move_to(LEFT * 2.5 + UP * 3)
        
        redis_box = RoundedRectangle(width=2.6, height=1.8, corner_radius=0.15,
                                      color="#4ECDC4", fill_opacity=0.2, stroke_width=3)
        redis_circle = Circle(radius=0.28, color=FAIL_RED, fill_opacity=0.85, stroke_width=2, stroke_color=WHITE)
        redis_text = Text("Redis", font_size=15, color=VSCODE_WHITE, weight=BOLD)
        redis_port = Text(":6379", font_size=11, color=VSCODE_GRAY)
        redis_container = Group(redis_box, redis_circle, redis_text, redis_port).arrange(DOWN, buff=0.12)
        redis_container.move_to(RIGHT * 2.5 + UP * 3)
        
        nginx_box = RoundedRectangle(width=2.6, height=1.8, corner_radius=0.15,
                                      color="#95E1D3", fill_opacity=0.2, stroke_width=3)
        nginx_img = self.load_asset("php.png", scale=0.5)
        nginx_text = Text("Nginx", font_size=15, color=VSCODE_WHITE, weight=BOLD)
        nginx_port = Text(":80", font_size=11, color=VSCODE_GRAY)
        nginx_container = Group(nginx_box, nginx_img, nginx_text, nginx_port).arrange(DOWN, buff=0.12)
        nginx_container.move_to(DOWN * 0.5)
        
        # Network
        network_box = RoundedRectangle(
            width=8,
            height=6,
            corner_radius=0.3,
            color=VUE_GREEN,
            fill_opacity=0.05,
            stroke_width=3,
            stroke_opacity=0.6
        ).move_to(UP * 1.2)
        
        network_label = Text("Docker Network", font_size=17, color=VUE_GREEN, weight=BOLD)
        network_label.next_to(network_box, UP, buff=0.2)
        
        # Animate network
        self.add_sound_safe("build.mp3")
        self.play(Create(network_box), Write(network_label), run_time=0.9)
        self.wait(0.3)
        
        # Containers start up
        containers = [mysql_container, redis_container, nginx_container]
        names = ["MySQL", "Redis", "Nginx"]
        
        for container, name in zip(containers, names):
            self.add_sound_safe("click.mp3")
            self.play(FadeIn(container, scale=0.7), run_time=0.5)
            
            # Starting animation
            starting = Text("Starting...", font_size=11, color=WARN_COLOR)
            starting.next_to(container, DOWN, buff=0.15)
            self.play(FadeIn(starting))
            self.wait(0.3)
            
            # Running
            running = Text("✓ Running", font_size=11, color=SUCCESS_GREEN, weight=BOLD)
            running.move_to(starting.get_center())
            self.play(Transform(starting, running))
            self.wait(0.2)
            self.play(FadeOut(starting))
        
        self.wait(0.5)
        
        # Show connections
        arrow1 = Arrow(nginx_container.get_top(), mysql_container.get_bottom(), 
                      color=WARN_COLOR, buff=0.15, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        arrow2 = Arrow(nginx_container.get_top(), redis_container.get_bottom(), 
                      color=WARN_COLOR, buff=0.15, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        
        self.add_sound_safe("click.mp3")
        self.play(Create(arrow1), Create(arrow2), run_time=0.7)
        self.wait(0.5)
        
        # Animated data flow (4 iterations with variety)
        for iteration in range(4):
            # Request
            request = Circle(radius=0.16, color=DOCKER_BLUE, fill_opacity=1, stroke_width=2, stroke_color=WHITE)
            request.move_to(nginx_container.get_center())
            
            # Query to MySQL
            query = Circle(radius=0.16, color="#FF6B6B", fill_opacity=1, stroke_width=2, stroke_color=WHITE)
            query.move_to(nginx_container.get_center())
            
            # Cache check
            cache = Circle(radius=0.16, color="#4ECDC4", fill_opacity=1, stroke_width=2, stroke_color=WHITE)
            cache.move_to(nginx_container.get_center())
            
            self.add_sound_safe("click.mp3")
            
            # Send to both
            self.play(
                query.animate.move_to(mysql_container.get_center()),
                cache.animate.move_to(redis_container.get_center()),
                run_time=0.7,
                rate_func=smooth
            )
            
            # Pulse on arrival
            self.play(
                query.animate.scale(1.3),
                cache.animate.scale(1.3),
                run_time=0.15,
                rate_func=there_and_back
            )
            
            # Response back
            response = Circle(radius=0.16, color=SUCCESS_GREEN, fill_opacity=1, stroke_width=2, stroke_color=WHITE)
            response.move_to(mysql_container.get_center())
            
            self.play(
                response.animate.move_to(nginx_container.get_center()),
                run_time=0.7,
                rate_func=smooth
            )
            
            self.play(FadeOut(query), FadeOut(cache), FadeOut(response), run_time=0.25)
            self.wait(0.2)
        
        # Success indicators
        self.add_sound_safe("build.mp3")
        check1 = Text("✓", font_size=42, color=SUCCESS_GREEN, weight=BOLD).next_to(mysql_container, RIGHT, buff=0.25)
        check2 = Text("✓", font_size=42, color=SUCCESS_GREEN, weight=BOLD).next_to(redis_container, LEFT, buff=0.25)
        check3 = Text("✓", font_size=42, color=SUCCESS_GREEN, weight=BOLD).next_to(nginx_container, DOWN, buff=0.25)
        
        for check in [check1, check2, check3]:
            self.play(GrowFromCenter(check), run_time=0.25)
            self.play(check.animate.scale(1.15), rate_func=there_and_back, run_time=0.25)
        
        self.wait(0.5)
        
        # Add status label
        status = Text("ALL SERVICES CONNECTED!", font_size=28, color=SUCCESS_GREEN, weight=BOLD)
        status.move_to(DOWN * 4)
        status_box = RoundedRectangle(
            width=status.width + 0.6,
            height=status.height + 0.4,
            color=SUCCESS_GREEN,
            fill_opacity=0.15,
            stroke_width=3
        ).move_to(status.get_center())
        
        self.add_sound_safe("build.mp3")
        self.play(Create(status_box), Write(status))
        self.wait(1.5)
        
        # Clear
        self.add_sound_safe("transition.mp3")
        self.play(
            *[FadeOut(m) for m in [
                arch_title, network_box, network_label,
                mysql_container, redis_container, nginx_container,
                arrow1, arrow2, check1, check2, check3,
                status, status_box
            ]]
        )
        self.wait(0.5)
        
        # ==========================================
        # ACT 4: KEY BENEFITS (160s - 200s)
        # ==========================================
        
        benefits_title = Text("KEY BENEFITS", font_size=46, color=DOCKER_BLUE, weight=BOLD)
        benefits_title.move_to(UP * 6.5)
        self.add_sound_safe("build.mp3")
        self.play(Write(benefits_title, run_time=0.9))
        self.wait(0.5)
        
        # Benefit items with icons
        benefit_list = [
            ("🎯", "Declarative configuration", UP * 4),
            ("♻️", "Reproducible environments", UP * 2),
            ("⚡", "Quick team onboarding", ORIGIN),
            ("🔧", "Easy to scale services", DOWN * 2),
            ("📦", "Version control ready", DOWN * 4),
        ]
        
        all_benefits = []
        for emoji, text, pos in benefit_list:
            icon = Text(emoji, font_size=36)
            desc = Text(text, font_size=24, color=VSCODE_WHITE)
            benefit = VGroup(icon, desc).arrange(RIGHT, buff=0.4).move_to(pos)
            
            self.add_sound_safe("click.mp3")
            self.play(FadeIn(benefit, shift=RIGHT*0.4), run_time=0.5)
            
            # Check mark
            check = Text("✓", font_size=26, color=SUCCESS_GREEN, weight=BOLD)
            check.next_to(benefit, RIGHT, buff=0.3)
            self.play(GrowFromCenter(check), run_time=0.2)
            
            all_benefits.extend([benefit, check])
            self.wait(0.6)
        
        self.wait(2.0)
        
        # Clear benefits
        self.add_sound_safe("transition.mp3")
        self.play(FadeOut(benefits_title), *[FadeOut(b) for b in all_benefits])
        self.wait(0.5)
        
        # ==========================================
        # ACT 5: FINAL RECAP (200s - 220s)
        # ==========================================
        
        recap_title = Text("REMEMBER", font_size=50, color=DOCKER_BLUE, weight=BOLD)
        recap_title.move_to(UP * 6)
        self.add_sound_safe("build.mp3")
        self.play(Write(recap_title, run_time=0.8))
        self.wait(0.5)
        
        # Three key steps
        step1 = VGroup(
            Text("1", font_size=44, color=WARN_COLOR, weight=BOLD),
            Text("Create docker-compose.yml", font_size=26, color=VSCODE_WHITE, weight=BOLD)
        ).arrange(RIGHT, buff=0.5).move_to(UP * 3.5)
        
        step2 = VGroup(
            Text("2", font_size=44, color=WARN_COLOR, weight=BOLD),
            Text("Run: docker-compose up", font_size=26, color=SUCCESS_GREEN, weight=BOLD)
        ).arrange(RIGHT, buff=0.5).move_to(UP * 1)
        
        step3 = VGroup(
            Text("3", font_size=44, color=WARN_COLOR, weight=BOLD),
            Text("Your stack is live!", font_size=26, color=DOCKER_BLUE, weight=BOLD)
        ).arrange(RIGHT, buff=0.5).move_to(DOWN * 1.5)
        
        final_msg = Text("Simple. Powerful. Essential.", font_size=30, color=SUCCESS_GREEN, weight=BOLD)
        final_msg.move_to(DOWN * 4.5)
        
        steps = [step1, step2, step3]
        for step in steps:
            self.add_sound_safe("click.mp3")
            self.play(FadeIn(step, scale=0.85), run_time=0.6)
            self.play(step.animate.scale(1.08), rate_func=there_and_back, run_time=0.4)
            self.wait(0.8)
        
        self.add_sound_safe("build.mp3")
        self.play(Write(final_msg, run_time=1.0))
        self.wait(2.5)
        
        # Outro
        self.play_outro()
