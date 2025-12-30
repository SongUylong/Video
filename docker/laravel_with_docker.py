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
            docker_logo.animate.scale(0.3).to_edge(UP, buff=0.3),
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
        
        backend_dev = create_dev("Laravel API", LARAVEL_RED, "Laravel.png", UP*0.5, asset_scale=0.3)
        frontend_dev = create_dev("Nuxt.js", VUE_GREEN, "nuxt.png", UP*0.5 + LEFT*2.5, asset_scale=0.35)
        mobile_dev = create_dev("Flutter", FLUTTER_BLUE, "flutter.png", UP*0.5 + RIGHT*2.5, asset_scale=0.35)
        
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
            backend_dev.animate.scale(0.9).move_to(UP*2),
            FadeOut(frontend_dev),
            FadeOut(mobile_dev)
        )
        
        setup_text = Text("Laravel API Setup", font_size=36, color=SUCCESS_GREEN, weight=BOLD)
        setup_text.move_to(UP*4.5)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(setup_text))
        
        # Show Laravel with PHP and MySQL (working - green border)
        working_box = RoundedRectangle(
            width=6,
            height=3,
            color=SUCCESS_GREEN,
            fill_opacity=0.15,
            stroke_width=5
        ).move_to(UP*0.5)
        
        # Laravel + PHP + MySQL logos
        laravel_logo = load_asset("Laravel.png", scale=0.6)
        php_logo = load_asset("php.png", scale=0.5)
        mysql_logo = load_asset("mysql.png", scale=0.5)
        
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
        
        # Show XAMPP for setup (can be wrong version)
        xampp_logo = load_asset("xamp.png", scale=0.7)
        if xampp_logo:
            xampp_logo.move_to(DOWN*3)
            xampp_label = Text("XAMPP Setup", font_size=20, color=WARN_COLOR)
            xampp_label.next_to(xampp_logo, DOWN, buff=0.2)
            
            add_sound_safe(SOUND_CLICK, gain=-10)
            self.play(
                SpinInFromNothing(xampp_logo),
                FadeIn(xampp_label)
            )
            
            # Show "maybe wrong version" warning
            version_warn = Text("(version conflicts?)", font_size=16, color=WARN_COLOR, slant=ITALIC)
            version_warn.next_to(xampp_label, DOWN, buff=0.1)
            self.play(FadeIn(version_warn), run_time=0.5)
        
        self.wait(1)
        
        # Transition: send to Nuxt and Flutter
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        
        # Bring back frontend and mobile
        frontend_dev_return = create_dev("Nuxt.js", VUE_GREEN, "nuxt.png", LEFT*2.5 + DOWN*2, asset_scale=0.35)
        mobile_dev_return = create_dev("Flutter", FLUTTER_BLUE, "flutter.png", RIGHT*2.5 + DOWN*2, asset_scale=0.35)
        
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
        
        self.wait(1.5)
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        self.play(*[FadeOut(m) for m in self.mobjects if m != docker_logo and m != background and m != grid])
        
        # ==========================
        # SCENE 4: Dockerfile Explanation (28-50s)
        # Using actual production Dockerfile
        # ==========================
        
        dockerfile_title = Text("Dockerfile Setup", font_size=38, color=WARN_COLOR, weight=BOLD)
        dockerfile_title.to_edge(UP, buff=2)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(dockerfile_title))
        
        # Dockerfile box (larger for real content)
        dockerfile_box = RoundedRectangle(
            corner_radius=0.2,
            width=7.5,
            height=11,
            color=WHITE,
            fill_opacity=0.95,
            stroke_width=3
        ).move_to(DOWN*0.3)
        
        dockerfile_header = Text("Dockerfile", font_size=24, color=BLACK, weight=BOLD)
        dockerfile_header.move_to(dockerfile_box.get_top() + DOWN*0.5)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(
            DrawBorderThenFill(dockerfile_box),
            Write(dockerfile_header)
        )
        
        # Real Dockerfile sections with explanations
        sections_data = [
            # (code, icon, explanation, icon_scale, is_header, wait_time)
            ("Base Image", None, None, None, True, 0),
            ("FROM php:8.2-fpm", "php.png", "Official PHP 8.2 FPM image", 0.5, False, 3),
            
            ("", None, None, None, False, 0),  # Spacer
            ("Install Dependencies", None, None, None, True, 0),
            ("RUN apt-get update", None, "Update package lists", None, False, 2),
            ("RUN apt-get install -y git curl...", None, "Install system packages", None, False, 2),
            
            ("", None, None, None, False, 0),  # Spacer
            ("PHP Extensions", None, None, None, True, 0),
            ("RUN docker-php-ext-install", None, "pdo_mysql, mbstring, gd", None, False, 2.5),
            
            ("", None, None, None, False, 0),  # Spacer
            ("Composer", None, None, None, True, 0),
            ("COPY --from=composer:latest", None, "Get Composer binary", None, False, 2.5),
            
            ("", None, None, None, False, 0),  # Spacer
            ("MySQL Connection", None, None, None, True, 0),
            ("ENV DB_HOST=db", "mysql.png", "Connect to MySQL container", 0.45, False, 3),
            ("ENV DB_DATABASE=laravel", None, "Database: laravel", None, False, 2.5),
            
            ("", None, None, None, False, 0),  # Spacer
            ("WORKDIR /var/www", None, "Set working directory", None, False, 2),
            ("USER laravel", None, "Run as laravel user", None, False, 2),
        ]
        
        y_position = dockerfile_box.get_top() + DOWN*1.2
        
        for code_line, icon_asset, explanation, icon_scale, is_header, wait_time in sections_data:
            if code_line == "":  # Spacer
                y_position += DOWN*0.3
                continue
            
            if is_header:
                # Section header
                header = Text(code_line, font_size=18, font="Monospace", color=DOCKER_BLUE, weight=BOLD)
                header.move_to(y_position)
                
                add_sound_safe(SOUND_WRITE, gain=-12)
                self.play(Write(header), run_time=0.6)
                y_position += DOWN*0.65
                continue
            
            # Code line (centered)
            code = Text(code_line, font_size=14, font="Monospace", color=BLACK, weight=BOLD)
            code.move_to(y_position)
            
            add_sound_safe(SOUND_WRITE, gain=-14)
            self.play(Write(code), run_time=0.8)
            
            # Icon if available
            if icon_asset:
                icon = load_asset(icon_asset, scale=icon_scale)
                if icon:
                    icon.next_to(code, RIGHT, buff=0.3)
                    add_sound_safe(SOUND_CLICK, gain=-16)
                    self.play(FadeIn(icon, scale=0.5), run_time=0.4)
            
            # Explanation text (centered below)
            if explanation:
                explain = Text(explanation, font_size=12, color="#555555", slant=ITALIC)
                explain.move_to(y_position + DOWN*0.35)
                
                self.play(FadeIn(explain), run_time=0.4)
            
            y_position += DOWN*0.85
            
            # Variable wait time per line
            if wait_time > 0:
                self.wait(wait_time)
        
        self.wait(0.5)
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        self.play(*[FadeOut(m) for m in self.mobjects if m != docker_logo and m != background and m != grid])
        
        # ==========================
        # SCENE 5: docker-compose Explanation & Setup (50-75s)
        # First explain, then show actual docker-compose.yml
        # ==========================
        
        # Part 1: What is docker-compose? (5s)
        compose_intro_title = Text("What is docker-compose?", font_size=36, color=DOCKER_BLUE, weight=BOLD)
        compose_intro_title.to_edge(UP, buff=2)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(compose_intro_title))
        
        explanation_points = VGroup(
            Text("• Defines multi-container apps", font_size=20, color=WHITE),
            Text("• Connects services together", font_size=20, color=SUCCESS_GREEN),
            Text("• One command to start all", font_size=20, color=WARN_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        explanation_points.move_to(ORIGIN)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        for point in explanation_points:
            self.play(FadeIn(point, shift=UP*0.1), run_time=0.5)
        
        self.wait(2)
        
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(FadeOut(compose_intro_title), FadeOut(explanation_points))
        
        # Part 2: Show actual docker-compose.yml
        compose_title = Text("docker-compose.yml", font_size=36, color=SUCCESS_GREEN, weight=BOLD)
        compose_title.to_edge(UP, buff=1.5)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(compose_title))
        
        # Service 1: Laravel App
        service1_label = Text("Service 1: Laravel App", font_size=26, color=LARAVEL_RED, weight=BOLD)
        service1_label.move_to(UP*5.5)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(service1_label, shift=DOWN*0.2))
        
        service1_box = RoundedRectangle(
            width=6.5,
            height=4,
            color=LARAVEL_RED,
            fill_opacity=0.9,
            stroke_width=3
        ).move_to(UP*2.5)
        
        service1_code = VGroup(
            Text("app:", font_size=16, color=WHITE, weight=BOLD),
            Text("  build: .", font_size=14, color=WHITE),
            Text("  image: laravel-app", font_size=14, color=WHITE),
            Text("  ports: \"8000:8000\"", font_size=14, color=WARN_COLOR),
            Text("  environment:", font_size=14, color=WHITE),
            Text("    DB_HOST: db", font_size=13, color=VUE_GREEN),
            Text("    DB_DATABASE: laravel", font_size=13, color=VUE_GREEN),
            Text("  command: php artisan serve", font_size=14, color=FLUTTER_BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        service1_code.move_to(service1_box.get_center())
        
        laravel_icon = load_asset("Laravel.png", scale=0.35)
        if laravel_icon:
            laravel_icon.move_to(service1_box.get_left() + RIGHT*0.5 + UP*1.5)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(service1_box))
        
        if laravel_icon:
            self.play(FadeIn(laravel_icon, scale=0.5))
        
        for line in service1_code:
            self.play(Write(line), run_time=0.35)
        
        check1 = Text("✓", font_size=28, color=SUCCESS_GREEN, weight=BOLD)
        check1.next_to(service1_box, RIGHT, buff=0.2)
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(FadeIn(check1, scale=1.3), run_time=0.3)
        
        self.wait(1.5)
        
        # Service 2: MySQL Database
        add_sound_safe(SOUND_TRANSITION, gain=-14)
        self.play(
            *[FadeOut(m) for m in [service1_label, service1_box, service1_code] + ([laravel_icon, check1] if laravel_icon else [check1])]
        )
        
        service2_label = Text("Service 2: MySQL Database", font_size=26, color="#00758f", weight=BOLD)
        service2_label.move_to(UP*5.5)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(service2_label, shift=DOWN*0.2))
        
        service2_box = RoundedRectangle(
            width=6.5,
            height=4.5,
            color="#00758f",
            fill_opacity=0.9,
            stroke_width=3
        ).move_to(UP*2)
        
        service2_code = VGroup(
            Text("db:", font_size=16, color=WHITE, weight=BOLD),
            Text("  image: mysql:8.0", font_size=14, color=WHITE),
            Text("  environment:", font_size=14, color=WHITE),
            Text("    MYSQL_DATABASE: laravel", font_size=13, color=WARN_COLOR),
            Text("    MYSQL_USER: laravel", font_size=13, color=WARN_COLOR),
            Text("    MYSQL_PASSWORD: secret", font_size=13, color=WARN_COLOR),
            Text("  ports: \"33061:3306\"", font_size=14, color=SUCCESS_GREEN),
            Text("  volumes: dbdata:/var/lib/mysql", font_size=13, color=FLUTTER_BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        service2_code.move_to(service2_box.get_center())
        
        mysql_icon = load_asset("mysql.png", scale=0.35)
        if mysql_icon:
            mysql_icon.move_to(service2_box.get_left() + RIGHT*0.5 + UP*1.8)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(service2_box))
        
        if mysql_icon:
            self.play(FadeIn(mysql_icon, scale=0.5))
        
        for line in service2_code:
            self.play(Write(line), run_time=0.32)
        
        check2 = Text("✓", font_size=28, color=SUCCESS_GREEN, weight=BOLD)
        check2.next_to(service2_box, RIGHT, buff=0.2)
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(FadeIn(check2, scale=1.3), run_time=0.3)
        
        self.wait(1.5)
        
        # Both services connected
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(
            *[FadeOut(m) for m in [service2_label, service2_box, service2_code] + ([mysql_icon, check2] if mysql_icon else [check2])]
        )
        
        # Show docker-compose up command
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
        
        # Services starting
        starting_text = Text("Starting services...", font_size=24, color=WARN_COLOR)
        starting_text.move_to(UP*1)
        self.play(FadeIn(starting_text))
        
        self.wait(0.5)
        
        # Show both running
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
        self.play(*[FadeOut(m) for m in [compose_title, terminal_box, command_text, starting_text, running_services, ready_text]])
        
        # ==========================
        # SCENE 6: Running from Web Access (75-95s)
        # ==========================
        
        web_title = Text("Setup & Web Access", font_size=36, color=VUE_GREEN, weight=BOLD)
        web_title.to_edge(UP, buff=1.5)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(web_title))
        
        # Show actual setup commands
        setup_label = Text("How to Run", font_size=24, color=WARN_COLOR, weight=BOLD)
        setup_label.move_to(UP*5.5)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(setup_label))
        
        # Terminal with real commands
        terminal = RoundedRectangle(
            width=7.5,
            height=5,
            color="#1e1e1e",
            fill_opacity=0.95,
            stroke_width=2,
            stroke_color="#00ff00"
        ).move_to(UP*2.5)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(terminal))
        
        commands = VGroup(
            Text("# 1. Start containers", font_size=14, font="Monospace", color="#888888", slant=ITALIC),
            Text("$ docker-compose up -d --build", font_size=15, font="Monospace", color=SUCCESS_GREEN, weight=BOLD),
            Text("", font_size=10),
            Text("# 2. Install dependencies", font_size=14, font="Monospace", color="#888888", slant=ITALIC),
            Text("$ docker-compose exec app composer install", font_size=14, font="Monospace", color=FLUTTER_BLUE, weight=BOLD),
            Text("", font_size=10),
            Text("# 3. Run migrations", font_size=14, font="Monospace", color="#888888", slant=ITALIC),
            Text("$ docker-compose exec app php artisan migrate", font_size=14, font="Monospace", color=LARAVEL_RED, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        commands.scale(0.85)
        commands.move_to(terminal.get_center() + UP*0.2)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        for cmd in commands:
            if cmd.text:  # Skip empty lines
                self.play(Write(cmd), run_time=0.5)
            else:
                self.wait(0.1)
        
        self.wait(1.5)
        
        # Show running status
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(FadeOut(setup_label), FadeOut(terminal), FadeOut(commands))
        
        # Nuxt access
        nuxt_access = Text("Accessing from Nuxt.js", font_size=22, color=VUE_GREEN, weight=BOLD)
        nuxt_access.move_to(UP*5)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(Write(nuxt_access))
        
        # Compact browser
        browser = RoundedRectangle(width=6, height=3.5, color=WHITE, fill_opacity=0.95, stroke_width=3)
        browser.move_to(UP*1.5)
        
        url_bar = RoundedRectangle(width=5.5, height=0.5, color="#e0e0e0", fill_opacity=1)
        url_bar.move_to(browser.get_top() + DOWN*0.5)
        
        url_text = Text("localhost:8000", font_size=16, font="Monospace", color=BLACK)
        url_text.move_to(url_bar)
        
        laravel_logo = load_asset("Laravel.png", scale=0.45)
        nuxt_logo = load_asset("nuxt.png", scale=0.4)
        
        logos_group = Group()
        if laravel_logo:
            logos_group.add(laravel_logo)
        if nuxt_logo:
            if laravel_logo:
                nuxt_logo.next_to(laravel_logo, RIGHT, buff=0.4)
            logos_group.add(nuxt_logo)
        
        if len(logos_group) > 0:
            logos_group.move_to(browser.get_center() + DOWN*0.2)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(
            DrawBorderThenFill(browser),
            FadeIn(url_bar),
            Write(url_text)
        )
        
        if len(logos_group) > 0:
            add_sound_safe(SOUND_CLICK, gain=-8)
            for logo in logos_group:
                self.play(FadeIn(logo, scale=0.8), run_time=0.4)
        
        success_web = Text("✓ Running!", font_size=24, color=SUCCESS_GREEN, weight=BOLD)
        success_web.move_to(DOWN*1.5)
        
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(FadeIn(success_web, shift=UP*0.2))
        
        self.wait(1.5)
        
        # ==========================
        # SCENE 7: Running from Mobile Access (95-110s)  
        # ==========================
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        self.play(*[FadeOut(m) for m in self.mobjects if m != docker_logo and m != background and m != grid])
        
        mobile_title = Text("Flutter API Access", font_size=36, color=FLUTTER_BLUE, weight=BOLD)
        mobile_title.to_edge(UP, buff=1.5)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(mobile_title))
        
        # Mobile device with Flutter logo
        mobile_device = load_asset("mobile.svg", scale=1.3)
        flutter_logo = load_asset("flutter.png", scale=0.4)
        
        if mobile_device is None:
            mobile_device = RoundedRectangle(width=2, height=3.8, color=WHITE, fill_opacity=0.3, stroke_width=3)
        
        mobile_group = Group()
        if mobile_device:
            mobile_device.move_to(LEFT*2.8 + UP*2.5)
            mobile_group.add(mobile_device)
        if flutter_logo:
            flutter_logo.move_to(LEFT*2.8 + UP*5.5)
            mobile_group.add(flutter_logo)
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(mobile_group, scale=0.8))
        
        # API request
        api_label = Text("API Request", font_size=18, color=WARN_COLOR, weight=BOLD, slant=ITALIC)
        api_label.move_to(UP*5 + RIGHT*1.8)
        
        api_request = Text("GET /api/users", font_size=15, font="Monospace", color=WARN_COLOR, weight=BOLD)
        api_request.move_to(UP*4.2 + RIGHT*1.8)
        
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(api_label))
        self.play(Write(api_request), run_time=0.6)
        
        # Arrow to backend
        arrow_to_backend = Arrow(
            api_request.get_right(),
            api_request.get_right() + RIGHT*1.2,
            color=FLUTTER_BLUE,
            stroke_width=3
        )
        
        add_sound_safe(SOUND_CLICK, gain=-12)
        self.play(GrowArrow(arrow_to_backend), run_time=0.4)
        
        # Backend processing (compact)
        backend_flow = VGroup(
            Text("Laravel", font_size=15, color=LARAVEL_RED, weight=BOLD),
            Text("→", font_size=14, color=WHITE),
            Text("MySQL", font_size=15, color="#00758f", weight=BOLD)
        ).arrange(RIGHT, buff=0.2)
        backend_flow.move_to(UP*2.8 + RIGHT*1.8)
        
        add_sound_safe(SOUND_BUILD, gain=-10)
        for item in backend_flow:
            self.play(FadeIn(item, shift=DOWN*0.1), run_time=0.25)
        
        # SQL query
        sql_query = Text("SELECT * FROM users", font_size=13, font="Monospace", color="#00758f")
        sql_query.move_to(UP*1.8 + RIGHT*1.8)
        
        add_sound_safe(SOUND_WRITE, gain=-12)
        self.play(Write(sql_query), run_time=0.5)
        
        # JSON response
        json_box = RoundedRectangle(
            width=3.5,
            height=1.2,
            color=SUCCESS_GREEN,
            fill_opacity=0.2,
            stroke_width=2
        ).move_to(UP*0.5 + RIGHT*1.8)
        
        json_response = VGroup(
            Text('{ "users": [', font_size=12, font="Monospace", color=SUCCESS_GREEN),
            Text('  {id: 1, name: "John"},', font_size=11, font="Monospace", color=WHITE),
            Text('  {id: 2, name: "Jane"}', font_size=11, font="Monospace", color=WHITE),
            Text(']}', font_size=12, font="Monospace", color=SUCCESS_GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        json_response.move_to(json_box.get_center())
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(DrawBorderThenFill(json_box))
        for line in json_response:
            self.play(Write(line), run_time=0.3)
        
        # Arrow back to mobile
        arrow_response = Arrow(
            json_box.get_left(),
            mobile_device.get_right() if mobile_device else LEFT*2 + UP*2.5,
            color=SUCCESS_GREEN,
            stroke_width=3
        )
        
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(GrowArrow(arrow_response), run_time=0.5)
        
        # Data rendered on mobile (very compact)
        mobile_list = VGroup(
            Text("John", font_size=12, color=WHITE),
            Text("Jane", font_size=12, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        mobile_list.move_to((mobile_device.get_center() if mobile_device else LEFT*2.8 + UP*2.5) + DOWN*0.5)
        
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(FadeIn(mobile_list, shift=UP*0.15), run_time=0.5)
        
        success_mobile = Text("✓ API Connected!", font_size=24, color=SUCCESS_GREEN, weight=BOLD)
        success_mobile.move_to(DOWN*2.2)
        
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(FadeIn(success_mobile, shift=UP*0.2))
        
        self.wait(1.5)
        
        # ==========================
        # SCENE 9: Team Success (110-115s)
        # ==========================
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        self.play(*[FadeOut(m) for m in self.mobjects if m != docker_logo and m != background and m != grid])
        
        success_title = Text("Same Environment for Everyone!", font_size=34, color=SUCCESS_GREEN, weight=BOLD)
        success_title.to_edge(UP, buff=2)
        
        self.play(Write(success_title))
        
        # All platforms running
        all_devs = load_asset("workingcodehumen.png", scale=0.5)
        if all_devs:
            all_devs.move_to(UP*1.5)
            self.play(FadeIn(all_devs, scale=0.8))
        
        platforms = Group(
            Group(
                load_asset("laptop.svg", scale=0.6) or Text("💻", font_size=30),
                Text("✓ Web", font_size=18, color=VUE_GREEN, weight=BOLD)
            ).arrange(DOWN, buff=0.2),
            Group(
                load_asset("Laravel.png", scale=0.6) or Text("🚀", font_size=30),
                Text("✓ API", font_size=18, color=LARAVEL_RED, weight=BOLD)
            ).arrange(DOWN, buff=0.2),
            Group(
                load_asset("mobile.svg", scale=0.6) or Text("📱", font_size=30),
                Text("✓ Mobile", font_size=18, color=FLUTTER_BLUE, weight=BOLD)
            ).arrange(DOWN, buff=0.2)
        ).arrange(RIGHT, buff=1.5)
        platforms.move_to(DOWN*1.5)
        
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(*[FadeIn(p, scale=0.5) for p in platforms], lag_ratio=0.2)
        
        # Celebration particles
        celebration = VGroup()
        for i in range(20):
            particle = Star(n=5, outer_radius=0.1, color=random_bright_color()).set_opacity(0.8)
            particle.move_to(
                np.array([
                    np.random.uniform(-3, 3),
                    np.random.uniform(-2, 2),
                    0
                ])
            )
            celebration.add(particle)
        
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(
            *[FadeIn(p, scale=0.3) for p in celebration],
            lag_ratio=0.05,
            run_time=1
        )
        
        self.wait(1)
        
        # ==========================
        # SCENE 10: Ending (115-120s)
        # ==========================
        
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        self.play(*[FadeOut(m) for m in self.mobjects if m != background and m != grid])
        
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
