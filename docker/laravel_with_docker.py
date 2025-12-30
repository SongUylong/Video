from manim import *
import os

# --- Configuration for TikTok Format (9:16 aspect ratio, 1080x1920) ---
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60

# --- Color Palette ---
DOCKER_BLUE = "#2496ED"
LARAVEL_RED = "#FF2D20"
VUE_GREEN = "#42b883"
FLUTTER_BLUE = "#02569B"
SUCCESS_GREEN = "#28a745"
FAIL_RED = "#dc3545"
WARN_COLOR = "#ffc107"
HOST_COLOR = "#555555"

# --- Sound Effect Paths ---
SOUND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds/")
ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "asset/")

SOUND_CLICK = f"{SOUND_DIR}click.mp3"
SOUND_ERROR = f"{SOUND_DIR}Error_04_Universfield.mp3"
SOUND_TRANSITION = f"{SOUND_DIR}transition.mp3"
SOUND_WRITE = f"{SOUND_DIR}typing_short.mp3"
SOUND_BUILD = f"{SOUND_DIR}build.mp3"


class LaravelDockerStory(Scene):
    """
    A comprehensive 2-minute Laravel Docker animation with detailed 
    Dockerfile line-by-line and docker-compose service-by-service explanations.
    """
    
    def construct(self):
        # Helper to safely add sounds
        def add_sound_safe(sound_path, gain=-10):
            if not os.path.exists(sound_path):
                print(f"Warning: Sound file not found: {sound_path}")
                return
            self.add_sound(sound_path, gain=gain)
        
        # Helper to load images/SVGs safely
        def load_asset(filename, scale=1.0):
            path = f"{ASSET_DIR}{filename}"
            if os.path.exists(path):
                if filename.lower().endswith('.svg'):
                    return SVGMobject(path).scale(scale)
                else:
                    return ImageMobject(path).scale(scale)
            return None
        
        # --- Background ---
        background = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=[BLACK, "#111111", "#1a1a2e"],
            fill_opacity=1,
            stroke_width=0
        ).set_z_index(-10)
        self.add(background)
        
        grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-20, 20, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.1
            }
        ).set_z_index(-9)
        self.add(grid)
        
        # ==========================
        # SCENE 1: Fancy Intro (0-10s)
        # ==========================
        
        # Particle spiral
        particles = VGroup()
        for i in range(12):
            angle = i * (TAU / 12)
            particle = Dot(color=DOCKER_BLUE, radius=0.08).set_opacity(0.7)
            particle.move_to(2.5 * np.array([np.cos(angle), np.sin(angle), 0]))
            particles.add(particle)
        particles.move_to(ORIGIN)
        
        # Docker logo
        docker_logo = load_asset("docker.svg", scale=0.1)
        if docker_logo is None:
            docker_logo = Text("🐳", font_size=80)
        docker_logo.move_to(ORIGIN).set_z_index(10)
        
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(
            *[FadeIn(p, scale=0.3) for p in particles],
            lag_ratio=0.05,
            run_time=0.8
        )
        
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(
            Rotate(particles, angle=PI, about_point=ORIGIN),
            particles.animate.scale(0.3).set_opacity(0),
            docker_logo.animate.scale(20),
            run_time=1.5,
            rate_func=smooth
        )
        self.remove(particles)
        
        # Logo pulse
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(
            docker_logo.animate.scale(1.15),
            run_time=0.3,
            rate_func=there_and_back
        )
        
        # Glow ring
        glow_ring = Circle(radius=1.5, color=DOCKER_BLUE, stroke_width=4, fill_opacity=0)
        glow_ring.move_to(docker_logo.get_center())
        
        add_sound_safe(SOUND_CLICK, gain=-12)
        self.play(Create(glow_ring), run_time=0.5)
        self.play(
            glow_ring.animate.scale(2).set_opacity(0),
            run_time=0.8,
            rate_func=smooth
        )
        self.remove(glow_ring)
        
        # Title
        title_text = Text("Part 2", font_size=70, weight=BOLD, color=DOCKER_BLUE)
        title_text.next_to(docker_logo, DOWN, buff=0.6)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(
            FadeIn(title_text, shift=UP*0.3, scale=0.9),
            run_time=0.8
        )
        
        self.wait(0.5)
        
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(
            FadeOut(title_text, shift=DOWN*0.5),
            FadeOut(docker_logo),
            run_time=0.8
        )
        
        # ==========================
        # SCENE 2: Meet the Team (10-18s)
        # ==========================
        
        team_title = Text("The Development Team", font_size=36, weight=BOLD).to_edge(UP, buff=2.5)
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(team_title))
        
        # Developer avatars
        def create_dev(name, color, asset_name, position, asset_scale=0.4):
            circle = Circle(radius=0.7, color=color, fill_opacity=0.3, stroke_width=4)
            asset = load_asset(asset_name, scale=asset_scale)
            if asset:
                asset.move_to(circle.get_center())
            else:
                asset = Text("👨‍💻", font_size=35).move_to(circle.get_center())
            label = Text(name, font_size=20, color=color, weight=BOLD).next_to(circle, DOWN, buff=0.2)
            group = Group(circle, asset, label)  # Use Group instead of VGroup for ImageMobject
            group.move_to(position)
            return group
        
        backend_dev = create_dev("Laravel API", LARAVEL_RED, "Laravel.png", UP*0.5, asset_scale=0.032)
        frontend_dev = create_dev("Nuxt.js", VUE_GREEN, "nuxt.png", UP*0.5 + LEFT*2.5, asset_scale=0.032)
        mobile_dev = create_dev("Flutter", FLUTTER_BLUE, "flutter.png", UP*0.5 + RIGHT*2.5, asset_scale=0.12)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(backend_dev, scale=0.5))
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(
            FadeIn(frontend_dev, shift=RIGHT*0.3),
            FadeIn(mobile_dev, shift=LEFT*0.3)
        )
        
        self.wait(1)
        
        # ==========================
        # SCENE 3: Laravel API Working Setup (18-28s)
        # ==========================
        
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(
            FadeOut(team_title),
            backend_dev.animate.scale(0.7).move_to(UP*6),
            FadeOut(frontend_dev),
            FadeOut(mobile_dev)
        )
        
        setup_text = Text("Laravel API Setup", font_size=36, color=SUCCESS_GREEN, weight=BOLD)
        setup_text.move_to(UP*4.5)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(setup_text))
        
        # Show Laravel with PHP and MySQL (working - green border)
        working_box = RoundedRectangle(
            width=7,
            height=3.5,
            color=SUCCESS_GREEN,
            fill_opacity=0.15,
            stroke_width=5
        ).move_to(UP*2)
        
        # Laravel + PHP + MySQL logos (bigger for better visibility)
        laravel_logo = load_asset("Laravel.png", scale=0.05)
        php_logo = load_asset("php.png", scale=0.35)
        mysql_logo = load_asset("mysql.png", scale=0.35)
        
        tech_stack = Group()
        if laravel_logo:
            tech_stack.add(laravel_logo)
        if php_logo:
            tech_stack.add(php_logo)
        if mysql_logo:
            tech_stack.add(mysql_logo)
        
        tech_stack.arrange(RIGHT, buff=0.5).move_to(working_box.get_center())
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(working_box))
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        for logo in tech_stack:
            self.play(FadeIn(logo, scale=0.8), run_time=0.4)
        
        checkmark = Text("✓ Working!", font_size=28, color=SUCCESS_GREEN, weight=BOLD)
        checkmark.next_to(working_box, DOWN, buff=0.3)
        
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(FadeIn(checkmark, shift=UP*0.2))
        
        self.wait(1)
        
        # Transition: send to Nuxt and Flutter
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        
        # Bring back frontend and mobile
        frontend_dev_return = create_dev("Nuxt.js", VUE_GREEN, "nuxt.png", LEFT*2.5 + DOWN*2, asset_scale=0.032)
        mobile_dev_return = create_dev("Flutter", FLUTTER_BLUE, "flutter.png", RIGHT*2.5 + DOWN*2, asset_scale=0.12)
        
        self.play(
            FadeIn(frontend_dev_return, shift=UP*0.3),
            FadeIn(mobile_dev_return, shift=UP*0.3)
        )
        
        # Arrows from Laravel to apps
        arrow_to_nuxt = Arrow(working_box.get_bottom() + LEFT*1, frontend_dev_return.get_top(), color=SUCCESS_GREEN, stroke_width=4)
        arrow_to_flutter = Arrow(working_box.get_bottom() + RIGHT*1, mobile_dev_return.get_top(), color=SUCCESS_GREEN, stroke_width=4)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(
            GrowArrow(arrow_to_nuxt),
            GrowArrow(arrow_to_flutter)
        )
        
        # Add "need a lot of setup" warning
        setup_warning = Text("Need a lot of setup!", font_size=24, color=WARN_COLOR, weight=BOLD)
        setup_warning.move_to(DOWN*4.5)
        
        add_sound_safe(SOUND_ERROR, gain=-10)
        self.play(FadeIn(setup_warning, scale=1.2))
        
        self.wait(1.5)
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        self.play(
            FadeOut(backend_dev),
            FadeOut(setup_text),
            FadeOut(working_box),
            FadeOut(tech_stack),
            FadeOut(checkmark),
            FadeOut(frontend_dev_return),
            FadeOut(mobile_dev_return),
            FadeOut(arrow_to_nuxt),
            FadeOut(arrow_to_flutter),
            FadeOut(setup_warning)
        )
        
        # ==========================
        # SCENE 4: Dockerfile Explanation Part 1 (28-40s)
        # Base Image and Dependencies - VSCode Style
        # ==========================
        
        dockerfile_title = Text("Dockerfile Setup", font_size=38, color=WARN_COLOR, weight=BOLD)
        dockerfile_title.to_edge(UP, buff=2)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(dockerfile_title))
        
        # VSCode-style editor - dark background
        VSCODE_BG = "#1e1e1e"
        VSCODE_SIDEBAR = "#252526"
        VSCODE_TITLEBAR = "#323233"
        VSCODE_BLUE = "#569cd6"
        VSCODE_GREEN = "#6a9955"
        VSCODE_ORANGE = "#ce9178"
        VSCODE_YELLOW = "#dcdcaa"
        VSCODE_PURPLE = "#c586c0"
        VSCODE_WHITE = "#d4d4d4"
        VSCODE_GRAY = "#6a6a6a"
        
        # Main editor container
        editor_box = RoundedRectangle(
            corner_radius=0.15,
            width=7.5,
            height=8,
            color=VSCODE_SIDEBAR,
            fill_color=VSCODE_BG,
            fill_opacity=1,
            stroke_width=2
        ).move_to(DOWN*0.3)
        
        # Title bar
        title_bar = Rectangle(
            width=7.5,
            height=0.5,
            color=VSCODE_TITLEBAR,
            fill_color=VSCODE_TITLEBAR,
            fill_opacity=1,
            stroke_width=0
        )
        title_bar.move_to(editor_box.get_top() + DOWN*0.25)
        
        # Window buttons (macOS style)
        btn_close = Circle(radius=0.08, color="#ff5f56", fill_opacity=1, stroke_width=0)
        btn_minimize = Circle(radius=0.08, color="#ffbd2e", fill_opacity=1, stroke_width=0)
        btn_maximize = Circle(radius=0.08, color="#27ca40", fill_opacity=1, stroke_width=0)
        window_btns = VGroup(btn_close, btn_minimize, btn_maximize).arrange(RIGHT, buff=0.12)
        window_btns.move_to(title_bar.get_left() + RIGHT*0.5)
        
        # File name in title bar
        file_tab = Text("Dockerfile", font_size=12, color=VSCODE_WHITE)
        file_tab.move_to(title_bar.get_center())
        
        # Line numbers background
        line_num_bg = Rectangle(
            width=0.6,
            height=7.3,
            color="#1e1e1e",
            fill_color="#1e1e1e",
            fill_opacity=1,
            stroke_width=0
        )
        line_num_bg.move_to(editor_box.get_left() + RIGHT*0.35 + DOWN*0.15)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(
            FadeIn(editor_box),
            FadeIn(title_bar),
            FadeIn(window_btns),
            FadeIn(file_tab),
            FadeIn(line_num_bg)
        )
        
        # Code content with syntax highlighting - LEFT ALIGNED
        code_start_x = editor_box.get_left()[0] + 1.0
        code_lines = []
        
        # Part 1: Base Image and Dependencies with syntax highlighting
        dockerfile_content = [
            # (line_num, keyword, value, comment, icon_asset, icon_scale, wait_time)
            (1, "# Base Image", None, None, None, None, 0.5),
            (2, "FROM", "php:8.2-fpm", None, "php.png", 0.15, 1.5),
            (3, "", None, None, None, None, 0),
            (4, "# Install Dependencies", None, None, None, None, 0.5),
            (5, "RUN", "apt-get update && \\", None, None, None, 1),
            (6, "    ", "apt-get install -y \\", None, None, None, 0.5),
            (7, "    ", "git curl zip unzip", None, None, None, 1),
            (8, "", None, None, None, None, 0),
            (9, "# PHP Extensions", None, None, None, None, 0.5),
            (10, "RUN", "docker-php-ext-install \\", None, None, None, 0.8),
            (11, "    ", "pdo_mysql mbstring gd", None, None, None, 1.5),
        ]
        
        y_position = editor_box.get_top()[1] - 1.2
        
        # VSCode-like cursor
        cursor = Rectangle(width=0.06, height=0.28, color=WHITE, fill_opacity=1, stroke_width=0)
        
        for line_num, keyword, value, comment, icon_asset, icon_scale, wait_time in dockerfile_content:
            # Skip empty lines
            if keyword == "" and value is None:
                y_position -= 0.45
                continue
            
            # Line number
            line_num_text = Text(str(line_num), font_size=10, color=VSCODE_GRAY)
            line_num_text.move_to([editor_box.get_left()[0] + 0.35, y_position, 0])
            
            line_group = VGroup(line_num_text)
            
            # Code content - LEFT ALIGNED
            x_pos = code_start_x
            
            if keyword.startswith("#"):
                # Comment line - green
                code_text = Text(keyword, font_size=12, font="Monospace", color=VSCODE_GREEN)
                code_text.move_to([x_pos + code_text.width/2, y_position, 0])
                line_group.add(code_text)
            elif keyword in ["FROM", "RUN", "COPY", "WORKDIR", "ENV", "USER", "CMD"]:
                # Dockerfile keyword - blue
                keyword_text = Text(keyword, font_size=12, font="Monospace", color=VSCODE_BLUE, weight=BOLD)
                keyword_text.move_to([x_pos + keyword_text.width/2, y_position, 0])
                line_group.add(keyword_text)
                x_pos += keyword_text.width + 0.15
                
                if value:
                    # Value - orange for strings, white otherwise
                    value_text = Text(value, font_size=12, font="Monospace", color=VSCODE_ORANGE)
                    value_text.move_to([x_pos + value_text.width/2, y_position, 0])
                    line_group.add(value_text)
            elif keyword.startswith("    "):
                # Indented continuation - white
                code_text = Text(keyword + (value if value else ""), font_size=12, font="Monospace", color=VSCODE_WHITE)
                code_text.move_to([x_pos + code_text.width/2, y_position, 0])
                line_group.add(code_text)
            
            # Animate with cursor
            cursor.move_to([code_start_x - 0.1, y_position, 0])
            add_sound_safe(SOUND_WRITE, gain=-14)
            self.play(
                FadeIn(cursor),
                FadeIn(line_group),
                run_time=0.35
            )
            self.play(FadeOut(cursor), run_time=0.08)
            
            # Show icon if specified
            if icon_asset:
                icon = load_asset(icon_asset, scale=icon_scale)
                if icon:
                    icon.move_to([editor_box.get_right()[0] - 0.6, y_position, 0])
                    add_sound_safe(SOUND_CLICK, gain=-16)
                    self.play(FadeIn(icon, scale=0.5), run_time=0.3)
            
            y_position -= 0.5
            
            if wait_time > 0:
                self.wait(wait_time)
        
        self.wait(0.5)
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        # Safely fade out all objects except background and grid
        to_remove = [m for m in self.mobjects if m != background and m != grid]
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove])
        
        # ==========================
        # SCENE 4B: Dockerfile Explanation Part 2 (40-50s)
        # Composer, Environment, Workdir - VSCode Style
        # ==========================
        
        dockerfile_title2 = Text("Dockerfile Setup", font_size=38, color=WARN_COLOR, weight=BOLD)
        dockerfile_title2.to_edge(UP, buff=2)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(dockerfile_title2))
        
        # VSCode-style editor - dark background (reusing color constants from Part 1)
        VSCODE_BG = "#1e1e1e"
        VSCODE_SIDEBAR = "#252526"
        VSCODE_TITLEBAR = "#323233"
        VSCODE_BLUE = "#569cd6"
        VSCODE_GREEN = "#6a9955"
        VSCODE_ORANGE = "#ce9178"
        VSCODE_YELLOW = "#dcdcaa"
        VSCODE_PURPLE = "#c586c0"
        VSCODE_WHITE = "#d4d4d4"
        VSCODE_GRAY = "#6a6a6a"
        
        # Main editor container
        editor_box2 = RoundedRectangle(
            corner_radius=0.15,
            width=7.5,
            height=8.5,
            color=VSCODE_SIDEBAR,
            fill_color=VSCODE_BG,
            fill_opacity=1,
            stroke_width=2
        ).move_to(DOWN*0.1)
        
        # Title bar
        title_bar2 = Rectangle(
            width=7.5,
            height=0.5,
            color=VSCODE_TITLEBAR,
            fill_color=VSCODE_TITLEBAR,
            fill_opacity=1,
            stroke_width=0
        )
        title_bar2.move_to(editor_box2.get_top() + DOWN*0.25)
        
        # Window buttons (macOS style)
        btn_close2 = Circle(radius=0.08, color="#ff5f56", fill_opacity=1, stroke_width=0)
        btn_minimize2 = Circle(radius=0.08, color="#ffbd2e", fill_opacity=1, stroke_width=0)
        btn_maximize2 = Circle(radius=0.08, color="#27ca40", fill_opacity=1, stroke_width=0)
        window_btns2 = VGroup(btn_close2, btn_minimize2, btn_maximize2).arrange(RIGHT, buff=0.12)
        window_btns2.move_to(title_bar2.get_left() + RIGHT*0.5)
        
        # File name in title bar
        file_tab2 = Text("Dockerfile (continued)", font_size=12, color=VSCODE_WHITE)
        file_tab2.move_to(title_bar2.get_center())
        
        # Line numbers background
        line_num_bg2 = Rectangle(
            width=0.6,
            height=7.8,
            color="#1e1e1e",
            fill_color="#1e1e1e",
            fill_opacity=1,
            stroke_width=0
        )
        line_num_bg2.move_to(editor_box2.get_left() + RIGHT*0.35 + DOWN*0.1)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(
            FadeIn(editor_box2),
            FadeIn(title_bar2),
            FadeIn(window_btns2),
            FadeIn(file_tab2),
            FadeIn(line_num_bg2)
        )
        
        # Code content with syntax highlighting - LEFT ALIGNED
        code_start_x2 = editor_box2.get_left()[0] + 1.0
        
        # Part 2: Composer, Environment, Workdir
        dockerfile_content2 = [
            # (line_num, keyword, value, comment, icon_asset, icon_scale, wait_time)
            (12, "# Composer", None, None, None, None, 0.5),
            (13, "COPY", "--from=composer:latest \\", None, None, None, 0.8),
            (14, "    ", "/usr/bin/composer /usr/bin/composer", None, None, None, 1.2),
            (15, "", None, None, None, None, 0),
            (16, "# MySQL Connection", None, None, None, None, 0.5),
            (17, "ENV", "DB_HOST=db", None, "mysql.png", 0.15, 1.2),
            (18, "ENV", "DB_DATABASE=laravel", None, None, None, 0.8),
            (19, "ENV", "DB_USERNAME=laravel", None, None, None, 0.8),
            (20, "", None, None, None, None, 0),
            (21, "# Working Directory", None, None, None, None, 0.5),
            (22, "WORKDIR", "/var/www", None, None, None, 1),
            (23, "USER", "laravel", None, None, None, 1),
        ]
        
        y_position2 = editor_box2.get_top()[1] - 1.0
        
        # VSCode-like cursor
        cursor2 = Rectangle(width=0.06, height=0.28, color=WHITE, fill_opacity=1, stroke_width=0)
        
        for line_num, keyword, value, comment, icon_asset, icon_scale, wait_time in dockerfile_content2:
            # Skip empty lines
            if keyword == "" and value is None:
                y_position2 -= 0.45
                continue
            
            # Line number
            line_num_text = Text(str(line_num), font_size=10, color=VSCODE_GRAY)
            line_num_text.move_to([editor_box2.get_left()[0] + 0.35, y_position2, 0])
            
            line_group = VGroup(line_num_text)
            
            # Code content - LEFT ALIGNED
            x_pos = code_start_x2
            
            if keyword.startswith("#"):
                # Comment line - green
                code_text = Text(keyword, font_size=12, font="Monospace", color=VSCODE_GREEN)
                code_text.move_to([x_pos + code_text.width/2, y_position2, 0])
                line_group.add(code_text)
            elif keyword in ["FROM", "RUN", "COPY", "WORKDIR", "ENV", "USER", "CMD"]:
                # Dockerfile keyword - blue
                keyword_text = Text(keyword, font_size=12, font="Monospace", color=VSCODE_BLUE, weight=BOLD)
                keyword_text.move_to([x_pos + keyword_text.width/2, y_position2, 0])
                line_group.add(keyword_text)
                x_pos += keyword_text.width + 0.15
                
                if value:
                    # Value - orange for strings, white otherwise
                    value_text = Text(value, font_size=12, font="Monospace", color=VSCODE_ORANGE)
                    value_text.move_to([x_pos + value_text.width/2, y_position2, 0])
                    line_group.add(value_text)
            elif keyword.startswith("    "):
                # Indented continuation - white
                code_text = Text(keyword + (value if value else ""), font_size=12, font="Monospace", color=VSCODE_WHITE)
                code_text.move_to([x_pos + code_text.width/2, y_position2, 0])
                line_group.add(code_text)
            
            # Animate with cursor
            cursor2.move_to([code_start_x2 - 0.1, y_position2, 0])
            add_sound_safe(SOUND_WRITE, gain=-14)
            self.play(
                FadeIn(cursor2),
                FadeIn(line_group),
                run_time=0.35
            )
            self.play(FadeOut(cursor2), run_time=0.08)
            
            # Show icon if specified
            if icon_asset:
                icon = load_asset(icon_asset, scale=icon_scale)
                if icon:
                    icon.move_to([editor_box2.get_right()[0] - 0.6, y_position2, 0])
                    add_sound_safe(SOUND_CLICK, gain=-16)
                    self.play(FadeIn(icon, scale=0.5), run_time=0.3)
            
            y_position2 -= 0.5
            
            if wait_time > 0:
                self.wait(wait_time)
        
        self.wait(0.5)
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        # Safely fade out all objects except background and grid
        to_remove = [m for m in self.mobjects if m != background and m != grid]
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove])
        
        # ==========================
        # SCENE 5: docker-compose Explanation (50-60s)
        # Visual Animation with Icons
        # ==========================
        
        compose_intro_title = Text("What is docker-compose?", font_size=36, color=DOCKER_BLUE, weight=BOLD)
        compose_intro_title.to_edge(UP, buff=2)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(compose_intro_title))
        
        # Explanation text
        explanation1 = Text("Manages multiple containers", font_size=20, color=WHITE)
        explanation1.move_to(UP*4.5)
        add_sound_safe(SOUND_CLICK, gain=-12)
        self.play(FadeIn(explanation1, shift=UP*0.2))
        
        # Container 1: Laravel App
        container1 = RoundedRectangle(width=2.5, height=2, color=LARAVEL_RED, fill_opacity=0.3, stroke_width=3)
        container1.move_to(LEFT*2.5 + UP*1.5)
        laravel_mini = load_asset("Laravel.png", scale=0.035)
        if laravel_mini:
            laravel_mini.move_to(container1.get_center())
        label1 = Text("Laravel App", font_size=14, color=LARAVEL_RED, weight=BOLD)
        label1.next_to(container1, DOWN, buff=0.15)
        
        # Container 2: MySQL
        container2 = RoundedRectangle(width=2.5, height=2, color="#00758f", fill_opacity=0.3, stroke_width=3)
        container2.move_to(RIGHT*2.5 + UP*1.5)
        mysql_mini = load_asset("mysql.png", scale=0.25)
        if mysql_mini:
            mysql_mini.move_to(container2.get_center())
        label2 = Text("MySQL DB", font_size=14, color="#00758f", weight=BOLD)
        label2.next_to(container2, DOWN, buff=0.15)
        
        # Docker compose wrapper box
        compose_wrapper = RoundedRectangle(width=7.5, height=5, color=DOCKER_BLUE, fill_opacity=0.1, stroke_width=4, stroke_color=DOCKER_BLUE)
        compose_wrapper.move_to(UP*1)
        compose_label = Text("docker-compose.yml", font_size=18, color=DOCKER_BLUE, weight=BOLD)
        compose_label.move_to(compose_wrapper.get_top() + DOWN*0.4)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(compose_wrapper), Write(compose_label))
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(DrawBorderThenFill(container1), Write(label1))
        if laravel_mini:
            add_sound_safe(SOUND_CLICK, gain=-12)
            self.play(FadeIn(laravel_mini, scale=0.5))
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(DrawBorderThenFill(container2), Write(label2))
        if mysql_mini:
            add_sound_safe(SOUND_CLICK, gain=-12)
            self.play(FadeIn(mysql_mini, scale=0.5))
        
        # Show connection arrow with animation
        connection_arrow = DoubleArrow(container1.get_right(), container2.get_left(), color=SUCCESS_GREEN, stroke_width=4)
        connection_label = Text("Network Link", font_size=14, color=SUCCESS_GREEN, weight=BOLD)
        connection_label.next_to(connection_arrow, UP, buff=0.15)
        
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(GrowArrow(connection_arrow))
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(connection_label, scale=0.8))
        
        # Benefits list
        benefits = VGroup(
            Text("✓ Single config file", font_size=16, color=SUCCESS_GREEN),
            Text("✓ Shared network", font_size=16, color=SUCCESS_GREEN),
            Text("✓ Easy scaling", font_size=16, color=SUCCESS_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        benefits.move_to(DOWN*2.5)
        
        for benefit in benefits:
            add_sound_safe(SOUND_CLICK, gain=-12)
            self.play(FadeIn(benefit, shift=RIGHT*0.2), run_time=0.4)
        
        one_command = Text("One command to start all!", font_size=24, color=WARN_COLOR, weight=BOLD)
        one_command.move_to(DOWN*4.5)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(Write(one_command))
        
        self.wait(1.5)
        
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        # Safely fade out all objects except background and grid
        to_remove = [m for m in self.mobjects if m != background and m != grid]
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove])
        
        # ==========================
        # SCENE 5B: docker-compose.yml Services (60-75s) - VSCode Style
        # ==========================
        
        compose_title = Text("docker-compose.yml", font_size=36, color=SUCCESS_GREEN, weight=BOLD)
        compose_title.to_edge(UP, buff=1.5)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(compose_title))
        
        # VSCode colors
        VSCODE_BG = "#1e1e1e"
        VSCODE_SIDEBAR = "#252526"
        VSCODE_TITLEBAR = "#323233"
        VSCODE_BLUE = "#569cd6"
        VSCODE_GREEN = "#6a9955"
        VSCODE_ORANGE = "#ce9178"
        VSCODE_YELLOW = "#dcdcaa"
        VSCODE_PURPLE = "#c586c0"
        VSCODE_WHITE = "#d4d4d4"
        VSCODE_GRAY = "#6a6a6a"
        VSCODE_CYAN = "#4ec9b0"
        
        # Service 1: Laravel App - VSCode Style
        service1_label = Text("Service 1: Laravel App", font_size=26, color=LARAVEL_RED, weight=BOLD)
        service1_label.move_to(UP*5.5)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(service1_label, shift=DOWN*0.2))
        
        # VSCode editor for Service 1
        editor1_box = RoundedRectangle(
            corner_radius=0.15,
            width=7,
            height=5,
            color=VSCODE_SIDEBAR,
            fill_color=VSCODE_BG,
            fill_opacity=1,
            stroke_width=2
        ).move_to(UP*2)
        
        title_bar1 = Rectangle(
            width=7,
            height=0.45,
            color=VSCODE_TITLEBAR,
            fill_color=VSCODE_TITLEBAR,
            fill_opacity=1,
            stroke_width=0
        )
        title_bar1.move_to(editor1_box.get_top() + DOWN*0.225)
        
        btn_c1 = Circle(radius=0.07, color="#ff5f56", fill_opacity=1, stroke_width=0)
        btn_m1 = Circle(radius=0.07, color="#ffbd2e", fill_opacity=1, stroke_width=0)
        btn_x1 = Circle(radius=0.07, color="#27ca40", fill_opacity=1, stroke_width=0)
        win_btns1 = VGroup(btn_c1, btn_m1, btn_x1).arrange(RIGHT, buff=0.1)
        win_btns1.move_to(title_bar1.get_left() + RIGHT*0.45)
        
        file_tab1 = Text("docker-compose.yml", font_size=11, color=VSCODE_WHITE)
        file_tab1.move_to(title_bar1.get_center())
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(
            FadeIn(editor1_box),
            FadeIn(title_bar1),
            FadeIn(win_btns1),
            FadeIn(file_tab1)
        )
        
        # Laravel service code with YAML syntax highlighting
        service1_yaml = [
            ("1", "app:", None, VSCODE_CYAN),
            ("2", "  build", ": .", VSCODE_BLUE),
            ("3", "  image", ": laravel-app", VSCODE_BLUE),
            ("4", "  ports", ":", VSCODE_BLUE),
            ("5", "    - ", "\"8000:8000\"", VSCODE_ORANGE),
            ("6", "  environment", ":", VSCODE_BLUE),
            ("7", "    DB_HOST", ": db", VSCODE_YELLOW),
            ("8", "    DB_DATABASE", ": laravel", VSCODE_YELLOW),
            ("9", "  command", ": php artisan serve", VSCODE_BLUE),
        ]
        
        code_start_x1 = editor1_box.get_left()[0] + 0.8
        y_pos1 = editor1_box.get_top()[1] - 0.9
        
        cursor1 = Rectangle(width=0.06, height=0.26, color=WHITE, fill_opacity=1, stroke_width=0)
        
        for line_num, key, value, key_color in service1_yaml:
            line_num_text = Text(line_num, font_size=10, color=VSCODE_GRAY)
            line_num_text.move_to([editor1_box.get_left()[0] + 0.3, y_pos1, 0])
            
            key_text = Text(key, font_size=12, font="Monospace", color=key_color)
            key_text.move_to([code_start_x1 + key_text.width/2, y_pos1, 0])
            
            line_group = VGroup(line_num_text, key_text)
            
            if value:
                value_text = Text(value, font_size=12, font="Monospace", color=VSCODE_WHITE if not value.startswith('"') else VSCODE_ORANGE)
                value_text.move_to([code_start_x1 + key_text.width + value_text.width/2, y_pos1, 0])
                line_group.add(value_text)
            
            cursor1.move_to([code_start_x1 - 0.1, y_pos1, 0])
            add_sound_safe(SOUND_WRITE, gain=-14)
            self.play(FadeIn(cursor1), FadeIn(line_group), run_time=0.3)
            self.play(FadeOut(cursor1), run_time=0.06)
            
            y_pos1 -= 0.42
        
        check1 = Text("✓", font_size=28, color=SUCCESS_GREEN, weight=BOLD)
        check1.move_to(editor1_box.get_right() + RIGHT*0.3)
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(FadeIn(check1, scale=1.3), run_time=0.3)
        
        self.wait(0.8)
        
        # Fade out Service 1
        add_sound_safe(SOUND_TRANSITION, gain=-14)
        self.play(
            FadeOut(service1_label),
            FadeOut(editor1_box),
            FadeOut(title_bar1),
            FadeOut(win_btns1),
            FadeOut(file_tab1),
            FadeOut(check1),
            *[FadeOut(m) for m in self.mobjects if m != background and m != grid and m != compose_title]
        )
        
        # Service 2: MySQL Database - VSCode Style
        service2_label = Text("Service 2: MySQL Database", font_size=26, color="#00758f", weight=BOLD)
        service2_label.move_to(UP*5.5)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(service2_label, shift=DOWN*0.2))
        
        # VSCode editor for Service 2
        editor2_box = RoundedRectangle(
            corner_radius=0.15,
            width=7,
            height=5.5,
            color=VSCODE_SIDEBAR,
            fill_color=VSCODE_BG,
            fill_opacity=1,
            stroke_width=2
        ).move_to(UP*1.8)
        
        title_bar2 = Rectangle(
            width=7,
            height=0.45,
            color=VSCODE_TITLEBAR,
            fill_color=VSCODE_TITLEBAR,
            fill_opacity=1,
            stroke_width=0
        )
        title_bar2.move_to(editor2_box.get_top() + DOWN*0.225)
        
        btn_c2 = Circle(radius=0.07, color="#ff5f56", fill_opacity=1, stroke_width=0)
        btn_m2 = Circle(radius=0.07, color="#ffbd2e", fill_opacity=1, stroke_width=0)
        btn_x2 = Circle(radius=0.07, color="#27ca40", fill_opacity=1, stroke_width=0)
        win_btns2 = VGroup(btn_c2, btn_m2, btn_x2).arrange(RIGHT, buff=0.1)
        win_btns2.move_to(title_bar2.get_left() + RIGHT*0.45)
        
        file_tab2 = Text("docker-compose.yml", font_size=11, color=VSCODE_WHITE)
        file_tab2.move_to(title_bar2.get_center())
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(
            FadeIn(editor2_box),
            FadeIn(title_bar2),
            FadeIn(win_btns2),
            FadeIn(file_tab2)
        )
        
        # MySQL service code with YAML syntax highlighting
        service2_yaml = [
            ("10", "db:", None, VSCODE_CYAN),
            ("11", "  image", ": mysql:8.0", VSCODE_BLUE),
            ("12", "  environment", ":", VSCODE_BLUE),
            ("13", "    MYSQL_DATABASE", ": laravel", VSCODE_YELLOW),
            ("14", "    MYSQL_USER", ": laravel", VSCODE_YELLOW),
            ("15", "    MYSQL_PASSWORD", ": secret", VSCODE_YELLOW),
            ("16", "    MYSQL_ROOT_PASSWORD", ": secret", VSCODE_YELLOW),
            ("17", "  ports", ":", VSCODE_BLUE),
            ("18", "    - ", "\"33061:3306\"", VSCODE_ORANGE),
            ("19", "  volumes", ":", VSCODE_BLUE),
            ("20", "    - ", "dbdata:/var/lib/mysql", VSCODE_WHITE),
        ]
        
        code_start_x2 = editor2_box.get_left()[0] + 0.8
        y_pos2 = editor2_box.get_top()[1] - 0.85
        
        cursor2 = Rectangle(width=0.06, height=0.26, color=WHITE, fill_opacity=1, stroke_width=0)
        
        for line_num, key, value, key_color in service2_yaml:
            line_num_text = Text(line_num, font_size=10, color=VSCODE_GRAY)
            line_num_text.move_to([editor2_box.get_left()[0] + 0.3, y_pos2, 0])
            
            key_text = Text(key, font_size=12, font="Monospace", color=key_color)
            key_text.move_to([code_start_x2 + key_text.width/2, y_pos2, 0])
            
            line_group = VGroup(line_num_text, key_text)
            
            if value:
                value_text = Text(value, font_size=12, font="Monospace", color=VSCODE_WHITE if not value.startswith('"') else VSCODE_ORANGE)
                value_text.move_to([code_start_x2 + key_text.width + value_text.width/2, y_pos2, 0])
                line_group.add(value_text)
            
            cursor2.move_to([code_start_x2 - 0.1, y_pos2, 0])
            add_sound_safe(SOUND_WRITE, gain=-14)
            self.play(FadeIn(cursor2), FadeIn(line_group), run_time=0.3)
            self.play(FadeOut(cursor2), run_time=0.06)
            
            y_pos2 -= 0.4
        
        check2 = Text("✓", font_size=28, color=SUCCESS_GREEN, weight=BOLD)
        check2.move_to(editor2_box.get_right() + RIGHT*0.3)
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(FadeIn(check2, scale=1.3), run_time=0.3)
        
        self.wait(0.8)
        
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        # Safely fade out all objects except background and grid
        to_remove = [m for m in self.mobjects if m != background and m != grid]
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove])
        
        # ==========================
        # SCENE 6: docker-compose up command (75-85s)
        # ==========================
        
        terminal_box = RoundedRectangle(
            width=7,
            height=1.5,
            color="#333333",
            fill_opacity=0.95,
            stroke_width=2
        ).move_to(UP*3)
        
        command_text = Text("$ docker-compose up -d", font_size=22, font="Monospace", color=SUCCESS_GREEN, weight=BOLD)
        command_text.move_to(terminal_box.get_center())
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(terminal_box))
        add_sound_safe(SOUND_WRITE, gain=-8)
        self.play(Write(command_text), run_time=1)
        
        starting_text = Text("Starting services...", font_size=24, color=WARN_COLOR)
        starting_text.move_to(UP*1)
        self.play(FadeIn(starting_text))
        
        self.wait(0.5)
        
        running_services = Group(
            Group(
                RoundedRectangle(width=2.5, height=0.8, color=LARAVEL_RED, fill_opacity=0.8),
                Text("App ✓", font_size=16, color=WHITE, weight=BOLD)
            ),
            Group(
                RoundedRectangle(width=2.5, height=0.8, color="#00758f", fill_opacity=0.8),
                Text("MySQL ✓", font_size=16, color=WHITE, weight=BOLD)
            )
        ).arrange(RIGHT, buff=1)
        
        for service in running_services:
            service[1].move_to(service[0].get_center())
        
        running_services.move_to(DOWN*0.5)
        
        add_sound_safe(SOUND_BUILD, gain=-8)
        for service in running_services:
            self.play(FadeIn(service, scale=0.6), run_time=0.4)
            add_sound_safe(SOUND_CLICK, gain=-14)
        
        ready_text = Text("✓ All Services Ready!", font_size=32, color=SUCCESS_GREEN, weight=BOLD)
        ready_text.move_to(DOWN*2.5)
        
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(Write(ready_text), Flash(ready_text, color=SUCCESS_GREEN))
        
        self.wait(2)
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        # Safely fade out all objects except background and grid
        to_remove = [m for m in self.mobjects if m != background and m != grid]
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove])
        
        # ==========================
        # SCENE 7: Running from Flutter & Nuxt.js API Access (85-100s)
        # ==========================
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        # Safely fade out all objects except background and grid
        to_remove = [m for m in self.mobjects if m != background and m != grid]
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove])
        
        api_access_title = Text("API Access", font_size=36, color=DOCKER_BLUE, weight=BOLD)
        api_access_title.to_edge(UP, buff=1.5)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(api_access_title))
        
        # --- Left Side: Flutter (White filled phone shape) ---
        flutter_section_title = Text("Flutter Mobile", font_size=22, color=FLUTTER_BLUE, weight=BOLD)
        flutter_section_title.move_to(LEFT*2.5 + UP*5)
        
        # Create a white filled phone shape
        phone_outer = RoundedRectangle(
            width=1.6, height=3.0, corner_radius=0.2,
            color=WHITE, fill_opacity=0.95, stroke_width=3, stroke_color=FLUTTER_BLUE
        )
        phone_screen = RoundedRectangle(
            width=1.3, height=2.4, corner_radius=0.1,
            color=FLUTTER_BLUE, fill_opacity=0.15, stroke_width=1, stroke_color=FLUTTER_BLUE
        )
        phone_button = Circle(radius=0.1, color=FLUTTER_BLUE, fill_opacity=0.5, stroke_width=1)
        phone_speaker = RoundedRectangle(width=0.3, height=0.05, color=FLUTTER_BLUE, fill_opacity=0.5, stroke_width=0)
        
        phone_screen.move_to(phone_outer.get_center() + UP*0.15)
        phone_button.move_to(phone_outer.get_bottom() + UP*0.2)
        phone_speaker.move_to(phone_outer.get_top() + DOWN*0.15)
        
        mobile_device = VGroup(phone_outer, phone_screen, phone_button, phone_speaker)
        mobile_device.move_to(LEFT*2.5 + UP*2.5)
        
        flutter_logo = load_asset("flutter.png", scale=0.12)
        if flutter_logo:
            flutter_logo.move_to(LEFT*2.5 + UP*4.3)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(flutter_section_title, shift=DOWN*0.2))
        add_sound_safe(SOUND_BUILD, gain=-12)
        self.play(FadeIn(mobile_device, scale=0.8))
        if flutter_logo:
            add_sound_safe(SOUND_CLICK, gain=-12)
            self.play(FadeIn(flutter_logo, scale=0.8))
        
        # --- Right Side: Nuxt.js (White filled laptop shape) ---
        nuxt_section_title = Text("Nuxt.js Web", font_size=22, color=VUE_GREEN, weight=BOLD)
        nuxt_section_title.move_to(RIGHT*2.5 + UP*5)
        
        # Create a white filled laptop shape
        laptop_screen = RoundedRectangle(
            width=2.4, height=1.6, corner_radius=0.1,
            color=WHITE, fill_opacity=0.95, stroke_width=3, stroke_color=VUE_GREEN
        )
        laptop_display = RoundedRectangle(
            width=2.1, height=1.3, corner_radius=0.05,
            color=VUE_GREEN, fill_opacity=0.15, stroke_width=1, stroke_color=VUE_GREEN
        )
        laptop_base = RoundedRectangle(
            width=2.8, height=0.15, corner_radius=0.05,
            color=WHITE, fill_opacity=0.95, stroke_width=2, stroke_color=VUE_GREEN
        )
        laptop_touchpad = RoundedRectangle(
            width=0.6, height=0.08, corner_radius=0.02,
            color=VUE_GREEN, fill_opacity=0.3, stroke_width=0
        )
        
        laptop_display.move_to(laptop_screen.get_center())
        laptop_base.move_to(laptop_screen.get_bottom() + DOWN*0.1)
        laptop_touchpad.move_to(laptop_base.get_center())
        
        laptop_device = VGroup(laptop_screen, laptop_display, laptop_base, laptop_touchpad)
        laptop_device.move_to(RIGHT*2.5 + UP*2.8)
        
        nuxt_logo = load_asset("nuxt.png", scale=0.025)
        if nuxt_logo:
            nuxt_logo.move_to(RIGHT*2.5 + UP*4.3)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(nuxt_section_title, shift=DOWN*0.2))
        add_sound_safe(SOUND_BUILD, gain=-12)
        self.play(FadeIn(laptop_device, scale=0.8))
        if nuxt_logo:
            add_sound_safe(SOUND_CLICK, gain=-12)
            self.play(FadeIn(nuxt_logo, scale=0.8))
        
        # --- Center: Laravel API Backend ---
        backend_box = RoundedRectangle(
            width=5,
            height=2,
            color=LARAVEL_RED,
            fill_opacity=0.2,
            stroke_width=3
        ).move_to(DOWN*2)
        
        laravel_api_logo = load_asset("Laravel.png", scale=0.03)
        backend_label = Text("Laravel API", font_size=20, color=LARAVEL_RED, weight=BOLD)
        backend_label.move_to(backend_box.get_top() + DOWN*0.4)
        
        if laravel_api_logo:
            laravel_api_logo.move_to(backend_box.get_center() + DOWN*0.2)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(backend_box))
        add_sound_safe(SOUND_WRITE, gain=-12)
        self.play(Write(backend_label))
        if laravel_api_logo:
            self.play(FadeIn(laravel_api_logo, scale=0.8))
        
        # --- API Request arrows ---
        flutter_request_arrow = Arrow(
            mobile_device.get_bottom() + DOWN*0.2,
            backend_box.get_left() + UP*0.3,
            color=WHITE,
            stroke_width=3
        )
        flutter_request_label = Text("GET /api/users", font_size=11, font="Monospace", color=WHITE)
        flutter_request_label.next_to(flutter_request_arrow, LEFT, buff=0.1).shift(DOWN*0.3)
        
        nuxt_request_arrow = Arrow(
            laptop_device.get_bottom() + DOWN*0.2,
            backend_box.get_right() + UP*0.3,
            color=WHITE,
            stroke_width=3
        )
        nuxt_request_label = Text("GET /api/products", font_size=11, font="Monospace", color=WHITE)
        nuxt_request_label.next_to(nuxt_request_arrow, RIGHT, buff=0.1).shift(DOWN*0.3)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(
            GrowArrow(flutter_request_arrow),
            GrowArrow(nuxt_request_arrow),
            run_time=0.6
        )
        self.play(
            Write(flutter_request_label),
            Write(nuxt_request_label),
            run_time=0.5
        )
        
        # --- JSON Response ---
        json_response_box = RoundedRectangle(
            width=4,
            height=1.5,
            color=SUCCESS_GREEN,
            fill_opacity=0.15,
            stroke_width=2
        ).move_to(DOWN*4.5)
        
        json_text = VGroup(
            Text('{ "status": "success",', font_size=11, font="Monospace", color=SUCCESS_GREEN),
            Text('  "data": [...] }', font_size=11, font="Monospace", color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        json_text.move_to(json_response_box.get_center())
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(DrawBorderThenFill(json_response_box))
        add_sound_safe(SOUND_WRITE, gain=-12)
        self.play(Write(json_text), run_time=0.6)
        
        # Response arrows back
        flutter_response_arrow = Arrow(
            backend_box.get_left() + DOWN*0.3,
            mobile_device.get_bottom() + DOWN*0.5,
            color=WHITE,
            stroke_width=2
        )
        nuxt_response_arrow = Arrow(
            backend_box.get_right() + DOWN*0.3,
            laptop_device.get_bottom() + DOWN*0.5,
            color=WHITE,
            stroke_width=2
        )
        
        add_sound_safe(SOUND_CLICK, gain=-12)
        self.play(
            GrowArrow(flutter_response_arrow),
            GrowArrow(nuxt_response_arrow),
            run_time=0.5
        )
        
        # Success indicators on devices
        flutter_check = Text("✓", font_size=20, color=SUCCESS_GREEN, weight=BOLD)
        flutter_check.move_to(mobile_device.get_center())
        
        nuxt_check = Text("✓", font_size=20, color=SUCCESS_GREEN, weight=BOLD)
        nuxt_check.move_to(laptop_device.get_center())
        
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(
            FadeIn(flutter_check, scale=1.5),
            FadeIn(nuxt_check, scale=1.5),
            run_time=0.4
        )
        
        # Final success message
        success_api = Text("✓ Both Apps Connected!", font_size=26, color=SUCCESS_GREEN, weight=BOLD)
        success_api.move_to(DOWN*6.5)
        
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(FadeIn(success_api, shift=UP*0.2))
        
        self.wait(1.5)
        
        # ==========================
        # SCENE 9: Team Success (110-115s)
        # ==========================
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        # Safely fade out all objects except background and grid
        to_remove = [m for m in self.mobjects if m != background and m != grid]
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove])
        
        success_title = Text("Same Environment for Everyone!", font_size=28, color=SUCCESS_GREEN, weight=BOLD)
        success_title.to_edge(UP, buff=1.5)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(success_title))
        
        # Docker wrapper box to show unified environment
        docker_env_box = RoundedRectangle(
            width=7.5,
            height=9,
            color=DOCKER_BLUE,
            fill_opacity=0.08,
            stroke_width=3
        ).move_to(DOWN*1)
        
        docker_env_label = Text("Docker Environment", font_size=16, color=DOCKER_BLUE, weight=BOLD)
        docker_env_label.move_to(docker_env_box.get_top() + DOWN*0.35)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(docker_env_box))
        add_sound_safe(SOUND_CLICK, gain=-12)
        self.play(Write(docker_env_label))
        
        # All platforms in a cleaner vertical layout with proper spacing
        # Web Platform
        web_box = RoundedRectangle(width=6, height=1.3, color=VUE_GREEN, fill_opacity=0.25, stroke_width=2)
        web_box.move_to(UP*2)
        nuxt_icon = load_asset("nuxt.png", scale=0.018)
        web_label = Text("Nuxt.js Web", font_size=15, color=VUE_GREEN, weight=BOLD)
        web_check = Text("✓", font_size=22, color=SUCCESS_GREEN, weight=BOLD)
        
        if nuxt_icon:
            nuxt_icon.move_to(web_box.get_left() + RIGHT*0.7)
        web_label.move_to(web_box.get_center())
        web_check.move_to(web_box.get_right() + LEFT*0.5)
        
        # API Platform
        api_box = RoundedRectangle(width=6, height=1.3, color=LARAVEL_RED, fill_opacity=0.25, stroke_width=2)
        api_box.move_to(UP*0.3)
        laravel_icon = load_asset("Laravel.png", scale=0.022)
        api_label = Text("Laravel API", font_size=15, color=LARAVEL_RED, weight=BOLD)
        api_check = Text("✓", font_size=22, color=SUCCESS_GREEN, weight=BOLD)
        
        if laravel_icon:
            laravel_icon.move_to(api_box.get_left() + RIGHT*0.7)
        api_label.move_to(api_box.get_center())
        api_check.move_to(api_box.get_right() + LEFT*0.5)
        
        # Mobile Platform
        mobile_box = RoundedRectangle(width=6, height=1.3, color=FLUTTER_BLUE, fill_opacity=0.25, stroke_width=2)
        mobile_box.move_to(DOWN*1.4)
        flutter_icon = load_asset("flutter.png", scale=0.15)
        mobile_label = Text("Flutter Mobile", font_size=15, color=FLUTTER_BLUE, weight=BOLD)
        mobile_check = Text("✓", font_size=22, color=SUCCESS_GREEN, weight=BOLD)
        
        if flutter_icon:
            flutter_icon.move_to(mobile_box.get_left() + RIGHT*0.7)
        mobile_label.move_to(mobile_box.get_center())
        mobile_check.move_to(mobile_box.get_right() + LEFT*0.5)
        
        # Database Platform
        db_box = RoundedRectangle(width=6, height=1.3, color="#00758f", fill_opacity=0.25, stroke_width=2)
        db_box.move_to(DOWN*3.1)
        mysql_icon_env = load_asset("mysql.png", scale=0.20)
        db_label = Text("MySQL Database", font_size=15, color="#00758f", weight=BOLD)
        db_check = Text("✓", font_size=22, color=SUCCESS_GREEN, weight=BOLD)
        
        if mysql_icon_env:
            mysql_icon_env.move_to(db_box.get_left() + RIGHT*0.7)
        db_label.move_to(db_box.get_center())
        db_check.move_to(db_box.get_right() + LEFT*0.5)
        
        # Animate platforms one by one
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(DrawBorderThenFill(web_box), run_time=0.4)
        if nuxt_icon:
            self.play(FadeIn(nuxt_icon, scale=0.8), run_time=0.25)
        self.play(Write(web_label), FadeIn(web_check, scale=1.2), run_time=0.3)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(DrawBorderThenFill(api_box), run_time=0.4)
        if laravel_icon:
            self.play(FadeIn(laravel_icon, scale=0.8), run_time=0.25)
        self.play(Write(api_label), FadeIn(api_check, scale=1.2), run_time=0.3)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(DrawBorderThenFill(mobile_box), run_time=0.4)
        if flutter_icon:
            self.play(FadeIn(flutter_icon, scale=0.8), run_time=0.25)
        self.play(Write(mobile_label), FadeIn(mobile_check, scale=1.2), run_time=0.3)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(DrawBorderThenFill(db_box), run_time=0.4)
        if mysql_icon_env:
            self.play(FadeIn(mysql_icon_env, scale=0.8), run_time=0.25)
        self.play(Write(db_label), FadeIn(db_check, scale=1.2), run_time=0.3)
        
        # Connection lines between layers
        line_web_api = Line(web_box.get_bottom(), api_box.get_top(), color=WHITE, stroke_width=1.5)
        line_api_mobile = Line(api_box.get_bottom(), mobile_box.get_top(), color=WHITE, stroke_width=1.5)
        line_mobile_db = Line(mobile_box.get_bottom(), db_box.get_top(), color=WHITE, stroke_width=1.5)
        
        add_sound_safe(SOUND_CLICK, gain=-14)
        self.play(
            Create(line_web_api),
            Create(line_api_mobile),
            Create(line_mobile_db),
            run_time=0.4
        )
        
        # Final success message
        final_message = Text("One Command - All Services!", font_size=20, color=WARN_COLOR, weight=BOLD)
        final_message.move_to(DOWN*5)
        
        command_reminder = Text("$ docker-compose up -d", font_size=14, font="Monospace", color=SUCCESS_GREEN)
        command_reminder.move_to(DOWN*5.8)
        
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(Write(final_message), run_time=0.5)
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(command_reminder), run_time=0.4)
        
        self.wait(1.2)
        
        # ==========================
        # SCENE 10: Ending (115-120s)
        # ==========================
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        # Safely fade out all objects except background and grid
        to_remove = [m for m in self.mobjects if m != background and m != grid]
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove])
        
        # Ending logo
        ending_logo = load_asset("potato.svg", scale=1.5)
        if ending_logo is None:
            ending_logo = Text("Thanks for Watching!", font_size=60, color=DOCKER_BLUE, weight=BOLD)
        ending_logo.move_to(ORIGIN)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(ending_logo, scale=0.8), run_time=0.8)
        self.wait(0.3)
        
        # Shake animation
        add_sound_safe(SOUND_CLICK, gain=-8)
        for _ in range(3):
            self.play(
                ending_logo.animate.shift(LEFT*0.1).rotate(angle=-0.05),
                run_time=0.08, rate_func=linear
            )
            self.play(
                ending_logo.animate.shift(RIGHT*0.2).rotate(angle=0.1),
                run_time=0.08, rate_func=linear
            )
            self.play(
                ending_logo.animate.shift(LEFT*0.1).rotate(angle=-0.05),
                run_time=0.08, rate_func=linear
            )
        
        # Scale up
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(
            ending_logo.animate.scale(8).set_opacity(0.9),
            run_time=1.5, rate_func=smooth
        )
        
        self.wait(0.5)
