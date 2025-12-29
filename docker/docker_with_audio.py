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
HOST_COLOR = "#555555"
LIB_COLOR_A = "#FF5733" # Orange
LIB_COLOR_B = "#33FF57" # Green
APP_COLOR = "#FFC300"   # Yellow
SUCCESS_GREEN = "#28a745"
FAIL_RED = "#dc3545"
WARN_COLOR = "#ffc107"

# --- Sound Effect Paths (Using only available sounds from docker/sounds) ---
SOUND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds/")

# Available sounds mapped to animation events:
SOUND_CLICK = f"{SOUND_DIR}click.mp3"  # Small UI interactions, clicks
SOUND_ERROR = f"{SOUND_DIR}Error_04_Universfield.mp3"              # X marks, failures
SOUND_TRANSITION = f"{SOUND_DIR}transition.mp3"              # Scene transitions (Trimmed to 2s)
SOUND_WRITE = f"{SOUND_DIR}typing_short.mp3"                       # Text writing (Trimmed to 1.5s)
SOUND_BUILD = f"{SOUND_DIR}build.mp3"                              # Building/creating
# Note: Some sound files appear corrupted (very small file size), using available ones strategically

class DockerTikTokWithAudio(Scene):
    def construct(self):
        # Helper to safely add sounds (won't crash if file doesn't exist)
        def add_sound_safe(sound_path, gain=-10):
            # Verify file exists first
            if not os.path.exists(sound_path):
                print(f"Warning: Sound file not found: {sound_path}")
                return
            self.add_sound(sound_path, gain=gain)
        
        # --- Helpers ---
        def get_std_box(color=DOCKER_BLUE, text_str="", width=1.5, height=1.5):
            box = RoundedRectangle(corner_radius=0.2, width=width, height=height, color=color, fill_opacity=0.5)
            if text_str:
                txt = Text(text_str, font_size=20).move_to(box.get_center())
                return VGroup(box, txt)
            return box

        # --- No Background Music (using only available sound effects) ---
        
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
        # SCENE 1: Fancy Intro
        # ==========================
        
        # Create glowing particles
        particles = VGroup()
        for i in range(12):
            angle = i * (TAU / 12)
            particle = Dot(color=DOCKER_BLUE, radius=0.08).set_opacity(0.7)
            particle.move_to(2.5 * np.array([np.cos(angle), np.sin(angle), 0]))
            particles.add(particle)
        particles.move_to(ORIGIN)
        
        # Docker logo (loading from SVG file)
        try:
            docker_logo = SVGMobject("docker.svg").scale(0.1).set_z_index(10)
        except:
            # Fallback to emoji if SVG loading fails
            docker_logo = Text("🐳", font_size=80).set_z_index(10)
        docker_logo.move_to(ORIGIN)
        
        # 🔊 SOUND: Transition for intro
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(
            *[FadeIn(p, scale=0.3) for p in particles],
            lag_ratio=0.05,
            run_time=0.8
        )
        
        # 🔊 SOUND: Build as particles rotate and logo appears
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(
            Rotate(particles, angle=PI, about_point=ORIGIN),
            particles.animate.scale(0.3).set_opacity(0),
            docker_logo.animate.scale(20),
            run_time=1.5,
            rate_func=smooth
        )
        self.remove(particles)
        
        # 🔊 SOUND: Click for pulse
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(
            docker_logo.animate.scale(1.15),
            run_time=0.3,
            rate_func=there_and_back
        )
        
        # Glow ring
        glow_ring = Circle(radius=1.5, color=DOCKER_BLUE, stroke_width=4, fill_opacity=0)
        glow_ring.move_to(docker_logo.get_center())
        
        # 🔊 SOUND: Click for glow ring
        add_sound_safe(SOUND_CLICK, gain=-12)
        self.play(Create(glow_ring), run_time=0.5)
        self.play(
            glow_ring.animate.scale(2).set_opacity(0),
            run_time=0.8,
            rate_func=smooth
        )
        self.remove(glow_ring)
        
        # Title appears
        title_text = Text("Docker", font_size=60, weight=BOLD, color=WHITE)
        title_text.next_to(docker_logo, DOWN, buff=0.6)
        
        # 🔊 SOUND: Write sound for title
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(
            FadeIn(title_text, shift=UP*0.3, scale=0.9),
            run_time=0.6
        )
        
        # 🔊 SOUND: Click for floating animation
        add_sound_safe(SOUND_CLICK, gain=-14)
        self.play(
            docker_logo.animate.shift(UP * 0.15),
            title_text.animate.shift(UP * 0.15),
            run_time=1.0,
            rate_func=there_and_back
        )
        
        self.wait(0.5)
        
        # 🔊 SOUND: Transition for scene change
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(
            FadeOut(title_text, shift=DOWN*0.5),
            docker_logo.animate.scale(0.4).to_edge(UP, buff=0.3).shift(RIGHT*0.2),
            run_time=0.8
        )

        # =========================================
        # SCENE 2: Docker Containers
        # =========================================
        

        
        container_title = Text("Docker Containers", font_size=36, weight=BOLD).to_edge(UP, buff=2.5)
        # 🔊 SOUND: Write for title
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(container_title))

        def make_layer(width, height, color, label_text, **kwargs):
            rect = RoundedRectangle(corner_radius=0.1, width=width, height=height, color=color, fill_opacity=0.6, **kwargs)
            lbl = Text(label_text, font_size=18, color=WHITE).move_to(rect.get_center())
            return VGroup(rect, lbl)

        # Docker Stack
        dk_infra = make_layer(4.5, 0.8, HOST_COLOR, "Infrastructure")
        dk_host_os = make_layer(4.5, 0.8, HOST_COLOR, "Host OS")
        docker_engine = make_layer(4.5, 1.0, DOCKER_BLUE, "Docker Engine")
        
        container_box1 = RoundedRectangle(corner_radius=0.1, width=1.8, height=1.2, color=DOCKER_BLUE, fill_opacity=0.8, stroke_color=WHITE, stroke_width=3)
        container_lbl1 = Text("App 1\n+Libs", font_size=14, color=WHITE).move_to(container_box1.get_center())
        container_grp1 = VGroup(container_box1, container_lbl1)
        
        container_box2 = RoundedRectangle(corner_radius=0.1, width=1.8, height=1.2, color=SUCCESS_GREEN, fill_opacity=0.8, stroke_color=WHITE, stroke_width=3)
        container_lbl2 = Text("App 2\n+Libs", font_size=14, color=WHITE).move_to(container_box2.get_center())
        container_grp2 = VGroup(container_box2, container_lbl2)
        
        dk_host_os.next_to(dk_infra, UP, buff=0.1)
        docker_engine.next_to(dk_host_os, UP, buff=0.1)
        container_grp1.next_to(docker_engine, UP, buff=0.3).shift(LEFT * 1.2)
        container_grp2.next_to(docker_engine, UP, buff=0.3).shift(RIGHT * 1.2)
        
        dk_stack_full = VGroup(dk_infra, dk_host_os, docker_engine, container_grp1, container_grp2)
        dk_stack_full.move_to(DOWN * 0.5)

        # 🔊 SOUND: Build sounds for infrastructure
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(GrowFromCenter(dk_infra), run_time=0.5)
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(GrowFromEdge(dk_host_os, DOWN), run_time=0.5)
        
        # 🔊 SOUND: Build for Docker Engine
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(GrowFromEdge(docker_engine, DOWN), run_time=0.6, rate_func=smooth)
        self.wait(0.3)
        
        # 🔊 SOUND: Click for each container
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(GrowFromCenter(container_grp1), run_time=0.5)
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(GrowFromCenter(container_grp2), run_time=0.5)
        
        # 🔊 SOUND: Click for pulse
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(
            container_grp1.animate.scale(1.1),
            container_grp2.animate.scale(1.1),
            run_time=0.3, rate_func=there_and_back,
        )

        lightweight_text = Text("Lightweight & Isolated!", color=SUCCESS_GREEN, font_size=28, weight=BOLD)
        lightweight_text.next_to(dk_stack_full, DOWN, buff=0.8)
        
        # 🔊 SOUND: Click for success text
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(
            FadeIn(lightweight_text, shift=UP*0.2),
            run_time=0.8
        )
        self.wait(2)

        # 🔊 SOUND: Transition for scene change
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(
            *[FadeOut(mob) for mob in [dk_stack_full, container_title, lightweight_text]],
             docker_logo.animate.set_opacity(0.3) 
        )

        # ==============================================
        # SCENE 3: Solving "Works on My Machine"
        # ==============================================
        


        problem_text = Text('Problem: "Works on my machine!"', font_size=32, color=FAIL_RED).to_edge(UP, buff=2.5)
        # 🔊 SOUND: Write for problem text
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(problem_text))

        # Assets
        laptop_screen = RoundedRectangle(corner_radius=0.1, width=3, height=2, color=GRAY_C, fill_opacity=1)
        laptop_base = RoundedRectangle(corner_radius=0.05, width=3.5, height=0.3, color=GRAY_D, fill_opacity=1).next_to(laptop_screen, DOWN, buff=0)
        laptop = VGroup(laptop_screen, laptop_base).shift(LEFT*2.2 + UP*0.5)
        laptop_label = Text("Dev Laptop", font_size=20).next_to(laptop, DOWN)

        server_box = RoundedRectangle(corner_radius=0.1, width=2, height=3, color=GRAY_E, fill_opacity=1)
        led1 = Dot(color=GREEN).shift(UP*1 + RIGHT*0.6)
        led2 = Dot(color=GREEN).shift(UP*0.7 + RIGHT*0.6)
        server = VGroup(server_box, led1, led2).shift(RIGHT*2.2 + UP*0.5)
        server_label = Text("Production Server", font_size=20).next_to(server, DOWN)

        app_code_box = RoundedRectangle(corner_radius=0.1, width=0.8, height=0.8, color=APP_COLOR, fill_opacity=1)
        app_code_txt = Text("Code", font_size=16).move_to(app_code_box)
        app_group = VGroup(app_code_box, app_code_txt).move_to(laptop_screen.get_center())

        # 🔊 SOUND: Click for devices appearing
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(
            FadeIn(laptop, shift=LEFT), FadeIn(laptop_label),
            FadeIn(server, shift=RIGHT), FadeIn(server_label)
        )
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(GrowFromCenter(app_group))
        
        # 🔊 SOUND: Click for checkmark
        check_mark = Text("✔", color=SUCCESS_GREEN, font_size=40).next_to(laptop, UP)
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(check_mark, shift=UP*0.2))
        self.wait(0.5)
        self.play(FadeOut(check_mark))

        # 🔊 SOUND: Build for code movement
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(
            app_group.animate.move_to(server_box.get_center()), 
            path_arc=-1, run_time=1.2
        )

        # 🔊 SOUND: Error buzz for failure
        fail_x = Text("✘", color=FAIL_RED, font_size=60).move_to(server_box.get_center())
        add_sound_safe(SOUND_ERROR, gain=-8)
        self.play(
            Transform(app_group, fail_x),
            Flash(server_box.get_center(), color=FAIL_RED, line_length=0.5),
            run_time=0.4
        )
        self.play(FadeOut(app_group))

        # Solution with Docker
        docker_fix_text = Text("Solution: Dockerize It!", font_size=32, color=DOCKER_BLUE).move_to(problem_text)
        # 🔊 SOUND: Transition for solution
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(Transform(problem_text, docker_fix_text))

        app_group_2 = VGroup(
            RoundedRectangle(corner_radius=0.1, width=0.8, height=0.8, color=APP_COLOR, fill_opacity=1), 
            Text("Code", font_size=16)
        ).move_to(laptop_screen.get_center())
        
        container_wrap = RoundedRectangle(corner_radius=0.2, width=1.4, height=1.4, color=DOCKER_BLUE, fill_opacity=0.4, stroke_width=4).move_to(app_group_2)
        deps_txt = Text("+ Deps & Config", font_size=14, color=WARN_COLOR).next_to(container_wrap, DOWN, buff=0.1)
        container_full = VGroup(container_wrap, app_group_2, deps_txt)

        # 🔊 SOUND: Click for code
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(app_group_2))
        
        # 🔊 SOUND: Build for containerization
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(
            DrawBorderThenFill(container_wrap), 
            Write(deps_txt),
            run_time=1
        )
        
        # 🔊 SOUND: Build for movement
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(
            container_full.animate.move_to(server_box.get_center()), 
            path_arc=-1,
            run_time=1.2
        )

        # 🔊 SOUND: Click for success!
        success_check = Text("✔ Works!", color=SUCCESS_GREEN, font_size=36, weight=BOLD).next_to(server, UP)
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(
            FadeIn(success_check, shift=UP*0.3), 
            container_wrap.animate.set_color(SUCCESS_GREEN).set_fill(opacity=0.6)
        )
        self.wait(1.5)

        # 🔊 SOUND: Transition for scene change
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(
             *[FadeOut(mob) for mob in self.mobjects if mob != docker_logo and mob != background and mob != grid]
        )
        docker_logo.set_opacity(1)

        # ==============================================
        # SCENE 4: Key Concepts Explained
        # ==============================================
        

        
        concepts_title = Text("Key Concepts", font_size=40, color=DOCKER_BLUE, weight=BOLD).to_edge(UP, buff=2.5)
        # 🔊 SOUND: Write title
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(concepts_title))
        self.wait(0.3)
        
        # --- Concept 1: Dockerfile ---
        concept1_label = Text("Dockerfile", font_size=32, color=WARN_COLOR, weight=BOLD).to_edge(UP, buff=3.5)
        
        doc_box = RoundedRectangle(corner_radius=0.2, width=4, height=3, color=WHITE, fill_opacity=0.95, stroke_width=4)
        doc_icon = Text("📄", font_size=50).move_to(doc_box.get_top() + DOWN*0.6)
        doc_desc = Text("Recipe for your app", font_size=18, color=BLACK).move_to(doc_box.get_center())
        
        code_snippet = VGroup(
            Text("FROM ubuntu", font_size=14, color=DOCKER_BLUE),
            Text("COPY app /app", font_size=14, color=SUCCESS_GREEN),
            Text("RUN install deps", font_size=14, color=WARN_COLOR)
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(doc_box.get_center() + DOWN*0.6)
        
        dockerfile_visual = VGroup(doc_box, doc_icon, doc_desc, code_snippet)
        dockerfile_visual.move_to(ORIGIN)
        
        # 🔊 SOUND: Click for label
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeOut(concepts_title), FadeIn(concept1_label, shift=DOWN*0.3))
        
        # 🔊 SOUND: Build for document
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(doc_box), FadeIn(doc_icon))
        self.play(Write(doc_desc))
        
        # 🔊 SOUND: Write for code lines
        add_sound_safe(SOUND_WRITE, gain=-12)
        for line in code_snippet:
            self.play(FadeIn(line, shift=UP*0.2), run_time=0.3)
        self.wait(1.2)
        
        # 🔊 SOUND: Transition
        add_sound_safe(SOUND_TRANSITION, gain=-14)
        self.play(FadeOut(concept1_label), FadeOut(dockerfile_visual))
        
        # --- Concept 2: Image ---
        concept2_label = Text("Docker Image", font_size=32, color=WARN_COLOR, weight=BOLD).to_edge(UP, buff=3.5)
        
        image_outer = RoundedRectangle(corner_radius=0.2, width=4, height=3, color=DOCKER_BLUE, fill_opacity=0.9, stroke_width=4)
        blueprint_icon = Text("📦", font_size=50).move_to(image_outer.get_top() + DOWN*0.6)
        image_desc = Text("Ready-to-run package", font_size=18, color=WHITE).move_to(image_outer.get_center() + UP*0.2)
        
        layer_group = VGroup(
            Rectangle(width=3, height=0.2, color=WHITE, fill_opacity=0.7, stroke_width=0),
            Rectangle(width=3, height=0.2, color=WHITE, fill_opacity=0.7, stroke_width=0),
            Rectangle(width=3, height=0.2, color=WHITE, fill_opacity=0.7, stroke_width=0),
        ).arrange(DOWN, buff=0.1).move_to(image_outer.get_center() + DOWN*0.6)
        
        image_visual = VGroup(image_outer, blueprint_icon, image_desc, layer_group)
        image_visual.move_to(ORIGIN)
        
        # 🔊 SOUND: Click for label
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(concept2_label, shift=DOWN*0.3))
        
        # 🔊 SOUND: Build for image
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(DrawBorderThenFill(image_outer), FadeIn(blueprint_icon))
        self.play(Write(image_desc))
        
        # 🔊 SOUND: Build sound for layers
        add_sound_safe(SOUND_BUILD, gain=-10)
        for layer in layer_group:
            self.play(GrowFromEdge(layer, UP), run_time=0.4)
        self.wait(1.2)
        
        # 🔊 SOUND: Transition
        add_sound_safe(SOUND_TRANSITION, gain=-14)
        self.play(FadeOut(concept2_label), FadeOut(image_visual))
        
        # --- Concept 3: Registry / Docker Hub ---
        concept3_label = Text("Docker Hub", font_size=32, color=WARN_COLOR, weight=BOLD).to_edge(UP, buff=3.5)
        
        registry_box = RoundedRectangle(corner_radius=0.3, width=4.5, height=3, color=GRAY_B, fill_opacity=0.95, stroke_width=4)
        cloud_big = Text("☁", font_size=70, color=DOCKER_BLUE).move_to(registry_box.get_center() + UP*0.3)
        registry_desc = Text("Image library", font_size=18, color=BLACK).move_to(registry_box.get_center() + DOWN*0.5)
        
        mini_image1 = Text("📦", font_size=20).move_to(registry_box.get_center() + LEFT*1 + DOWN*0.8)
        mini_image2 = Text("📦", font_size=20).move_to(registry_box.get_center() + DOWN*0.8)
        mini_image3 = Text("📦", font_size=20).move_to(registry_box.get_center() + RIGHT*1 + DOWN*0.8)
        
        registry_visual = VGroup(registry_box, cloud_big, registry_desc, mini_image1, mini_image2, mini_image3)
        registry_visual.move_to(ORIGIN)
        
        # 🔊 SOUND: Click for label
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(concept3_label, shift=DOWN*0.3))
        
        # 🔊 SOUND: Build for cloud
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(registry_box))
        self.play(FadeIn(cloud_big, scale=0.5), cloud_big.animate.scale(1.2), run_time=0.6)
        self.play(cloud_big.animate.scale(1/1.2), run_time=0.2)
        self.play(Write(registry_desc))
        
        # 🔊 SOUND: Click for mini images
        add_sound_safe(SOUND_CLICK, gain=-12)
        self.play(FadeIn(mini_image1), FadeIn(mini_image2), FadeIn(mini_image3), lag_ratio=0.2)
        self.wait(1.2)
        
        # 🔊 SOUND: Transition
        add_sound_safe(SOUND_TRANSITION, gain=-14)
        self.play(FadeOut(concept3_label), FadeOut(registry_visual))

        # ==============================================
        # SCENE 5: Complete Docker Flow
        # ==============================================
        

        
        # Hide the Docker logo from this point onward
        self.play(FadeOut(docker_logo), run_time=0.5)
        
        flow_title = Text("How Docker Works", font_size=38, color=DOCKER_BLUE, weight=BOLD)
        flow_title.move_to(UP*6.5)
        # 🔊 SOUND: Write title
        add_sound_safe(SOUND_WRITE, gain=-10)
        self.play(Write(flow_title))
        self.wait(0.3)
        
        # ===== PART 1: Build Phase =====
        
        # Step 1: Write Dockerfile
        step1_label = Text("1. Write", font_size=18, color=WARN_COLOR, weight=BOLD)
        step1_label.move_to(UP*5.5)
        
        dockerfile_box = RoundedRectangle(
            corner_radius=0.15, width=3.2, height=1.8, 
            color=WHITE, fill_opacity=0.95, stroke_width=3
        )
        dockerfile_box.move_to(UP*4.0)
        
        dockerfile_header = Text("Dockerfile", font_size=14, color=BLACK, weight=BOLD)
        dockerfile_header.move_to(dockerfile_box.get_top() + DOWN*0.2)
        
        code_lines = VGroup(
            Text("FROM node:18", font_size=11, color=DOCKER_BLUE),
            Text("COPY . /app", font_size=11, color=SUCCESS_GREEN),
            Text("RUN npm install", font_size=11, color=WARN_COLOR),
            Text('CMD ["npm","start"]', font_size=11, color=RED),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        code_lines.move_to(dockerfile_box.get_center() + DOWN*0.15)
        
        dockerfile_group = VGroup(dockerfile_box, dockerfile_header, code_lines)
        
        # 🔊 SOUND: Click for step
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(step1_label, shift=DOWN*0.2))
        
        # 🔊 SOUND: Build for document
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(dockerfile_box), Write(dockerfile_header))
        
        # 🔊 SOUND: Write for code lines
        add_sound_safe(SOUND_WRITE, gain=-10)
        for line in code_lines:
            self.play(FadeIn(line, shift=RIGHT*0.1), run_time=0.2)
        self.wait(0.3)
        
        # Step 2: Build
        image_box = RoundedRectangle(
            corner_radius=0.15, width=3.0, height=1.2,
            color=DOCKER_BLUE, fill_opacity=0.9, stroke_width=3
        )
        image_box.move_to(UP*1.6)

        build_arrow = Arrow(
            start=dockerfile_box.get_bottom() + DOWN*0.1,
            end=image_box.get_top() + UP*0.1,
            buff=0, color=DOCKER_BLUE, stroke_width=4
        )
        
        step2_label = Text("2. Build", font_size=18, color=WARN_COLOR, weight=BOLD)
        step2_label.next_to(build_arrow, LEFT, buff=0.3)
        
        image_icon = Text("📦", font_size=26).move_to(image_box.get_left() + RIGHT*0.5)
        image_name = Text("myapp:v1", font_size=13, color=WHITE, weight=BOLD)
        image_name.move_to(image_box.get_center() + RIGHT*0.25)
        
        image_group = VGroup(image_box, image_icon, image_name)
        
        # 🔊 SOUND: Click for step
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(step2_label, shift=DOWN*0.2))
        
        # 🔊 SOUND: Click for arrow
        add_sound_safe(SOUND_CLICK, gain=-12)
        self.play(GrowArrow(build_arrow), run_time=0.4)
        
        # 🔊 SOUND: Build sound
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(DrawBorderThenFill(image_box), FadeIn(image_icon))
        self.play(Write(image_name))
        
        # 🔊 SOUND: Click for build complete
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(
            image_box.animate.set_stroke(color=SUCCESS_GREEN, width=5),
            run_time=0.25, rate_func=there_and_back
        )
        self.wait(0.3)
        
        # Step 3: Push
        registry_box = RoundedRectangle(
            corner_radius=0.2, width=3.0, height=1.4,
            color=GRAY_B, fill_opacity=0.95, stroke_width=3
        )
        registry_box.move_to(DOWN*0.7)

        push_arrow = Arrow(
            start=image_box.get_bottom() + DOWN*0.1,
            end=registry_box.get_top() + UP*0.1,
            buff=0, color=SUCCESS_GREEN, stroke_width=4
        )
        
        step3_label = Text("3. Push", font_size=18, color=WARN_COLOR, weight=BOLD)
        step3_label.next_to(push_arrow, LEFT, buff=0.3)
        
        cloud_icon = Text("☁️", font_size=35).move_to(registry_box.get_center() + UP*0.1)
        hub_label = Text("Docker Hub", font_size=12, color=BLACK, weight=BOLD)
        hub_label.move_to(registry_box.get_center() + DOWN*0.4)
        
        registry_group = VGroup(registry_box, cloud_icon, hub_label)
        
        # 🔊 SOUND: Click for step
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(step3_label, shift=DOWN*0.2))
        
        # 🔊 SOUND: Click for arrow
        add_sound_safe(SOUND_CLICK, gain=-12)
        self.play(GrowArrow(push_arrow), run_time=0.4)
        
        # 🔊 SOUND: Build for upload
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(registry_box), FadeIn(cloud_icon), Write(hub_label))
        
        # Data flow particles with click sounds
        flow_line = Line(image_box.get_bottom(), registry_box.get_top())
        for i in range(3):
            dot = Dot(color=SUCCESS_GREEN, radius=0.1).move_to(flow_line.get_start())
            if i == 0:
                add_sound_safe(SOUND_CLICK, gain=-14)
            self.play(MoveAlongPath(dot, flow_line, run_time=0.4), FadeOut(dot, run_time=0.1))
        
        # 🔊 SOUND: Click for checkmark
        check = Text("✓", font_size=22, color=SUCCESS_GREEN, weight=BOLD)
        check.move_to(registry_box.get_corner(UR) + LEFT*0.3 + DOWN*0.25)
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(check, scale=0.5), run_time=0.3)
        
        self.wait(0.5)
        
        # ===== TRANSITION =====
        build_phase = VGroup(
            step1_label, dockerfile_group, step2_label, build_arrow, 
            image_group, step3_label, push_arrow
        )
        
        # 🔊 SOUND: Transition for phase change
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        self.play(
            FadeOut(build_phase, shift=LEFT*3),
            registry_group.animate.move_to(UP*5.0).scale(0.85),
            check.animate.move_to(UP*5.0 + RIGHT*1.2 + DOWN*0.15).scale(0.85),
            run_time=0.7
        )
        
        # ===== PART 2: Deploy Phase =====
        
        # 🔊 SOUND: Transition for deploy phase
        add_sound_safe(SOUND_TRANSITION, gain=-15)
        
        # Step 4: Pull
        server_box = RoundedRectangle(
            corner_radius=0.12, width=3.0, height=1.2,
            color=GRAY_D, fill_opacity=0.9, stroke_width=3
        )
        server_box.move_to(UP*2.8)

        pull_arrow = Arrow(
            start=registry_group.get_bottom() + DOWN*0.1,
            end=server_box.get_top() + UP*0.1,
            buff=0, color=DOCKER_BLUE, stroke_width=4
        )
        
        step4_label = Text("4. Pull", font_size=18, color=WARN_COLOR, weight=BOLD)
        step4_label.next_to(pull_arrow, RIGHT, buff=0.3)
        
        server_icon = Text("🖥️", font_size=26).move_to(server_box.get_left() + RIGHT*0.5)
        server_label = Text("Server", font_size=12, color=WHITE)
        server_label.move_to(server_box.get_center() + RIGHT*0.25)
        
        server_group = VGroup(server_box, server_icon, server_label)
        
        # 🔊 SOUND: Click for step
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(step4_label, shift=DOWN*0.2))
        
        # 🔊 SOUND: Click for arrow
        add_sound_safe(SOUND_CLICK, gain=-12)
        self.play(GrowArrow(pull_arrow), run_time=0.4)
        
        # 🔊 SOUND: Build for download
        add_sound_safe(SOUND_BUILD, gain=-10)
        self.play(DrawBorderThenFill(server_box), FadeIn(server_icon), Write(server_label))
        
        # Download particles
        download_line = Line(registry_group.get_bottom(), server_box.get_top())
        for i in range(3):
            dot = Dot(color=DOCKER_BLUE, radius=0.1).move_to(download_line.get_start())
            if i == 0:
                add_sound_safe(SOUND_CLICK, gain=-14)
            self.play(MoveAlongPath(dot, download_line, run_time=0.4), FadeOut(dot, run_time=0.1))
        
        self.wait(0.3)
        
        # Step 5: Run
        container_box = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=2.0,
            color=SUCCESS_GREEN, fill_opacity=0.9, stroke_width=4
        )
        container_box.move_to(DOWN*0.2)

        run_arrow = Arrow(
            start=server_box.get_bottom() + DOWN*0.1,
            end=container_box.get_top() + UP*0.1,
            buff=0, color=SUCCESS_GREEN, stroke_width=4
        )
        
        step5_label = Text("5. Run", font_size=18, color=WARN_COLOR, weight=BOLD)
        step5_label.next_to(run_arrow, RIGHT, buff=0.3)
        
        whale = Text("🐳", font_size=45).move_to(container_box.get_center() + UP*0.1)
        running_text = Text("Running", font_size=16, color=WHITE, weight=BOLD)
        running_text.move_to(container_box.get_center() + DOWN*0.6)
        
        container_group = VGroup(container_box, whale, running_text)
        
        # 🔊 SOUND: Click for step
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(step5_label, shift=DOWN*0.2))
        
        # 🔊 SOUND: Click for arrow
        add_sound_safe(SOUND_CLICK, gain=-12)
        self.play(GrowArrow(run_arrow), run_time=0.4)
        
        # 🔊 SOUND: Build/Run sound
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(DrawBorderThenFill(container_box))
        
        # 🔊 SOUND: Transition for container start
        add_sound_safe(SOUND_TRANSITION, gain=-12)
        self.play(FadeIn(whale, scale=0.5), whale.animate.scale(1.1), run_time=0.5)
        self.play(whale.animate.scale(1/1.1), run_time=0.2)
        self.play(Write(running_text))
        
        # Pulse rings with click sounds
        for i in range(2):
            pulse = Circle(radius=0.5, color=WHITE, stroke_width=3, fill_opacity=0)
            pulse.move_to(whale.get_center())
            self.add(pulse)
            if i == 0:
                add_sound_safe(SOUND_CLICK, gain=-14)
            self.play(pulse.animate.scale(2).set_opacity(0), run_time=0.6)
            self.remove(pulse)
        
        # 🔊 SOUND: Click for success!
        success = Text("✓ Live!", font_size=26, color=SUCCESS_GREEN, weight=BOLD)
        success.move_to(DOWN*2.5)
        add_sound_safe(SOUND_CLICK, gain=-8)
        self.play(FadeIn(success, scale=0.5), success.animate.scale(1.1), run_time=0.4)
        self.play(success.animate.scale(1/1.1), run_time=0.15)
        
        # Final container glow with click
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(
            container_box.animate.set_stroke(color=WHITE, width=6),
            run_time=0.25, rate_func=there_and_back
        )
        
        self.wait(2)

        # 🔊 SOUND: Transition for scene change
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob != background and mob != grid])
        
        # ==============================================
        # ENDING: Animated Logo
        # ==============================================
        

        
        # Load the ending logo
        try:
            ending_logo = SVGMobject("potato.svg").scale(1.5)
        except:
            # Fallback to text if SVG doesn't load
            ending_logo = Text("Thanks for Watching!", font_size=60, color=DOCKER_BLUE, weight=BOLD)
        
        ending_logo.move_to(ORIGIN)
        
        # Fade in the logo
        add_sound_safe(SOUND_CLICK, gain=-10)
        self.play(FadeIn(ending_logo, scale=0.8), run_time=0.8)
        self.wait(0.3)
        
        # Shake animation - wiggle left and right
        # 🔊 SOUND: Click for shake
        add_sound_safe(SOUND_CLICK, gain=-8)
        for _ in range(3):
            self.play(
                ending_logo.animate.shift(LEFT*0.1).rotate(angle=-0.05),
                run_time=0.08,
                rate_func=linear
            )
            self.play(
                ending_logo.animate.shift(RIGHT*0.2).rotate(angle=0.1),
                run_time=0.08,
                rate_func=linear
            )
            self.play(
                ending_logo.animate.shift(LEFT*0.1).rotate(angle=-0.05),
                run_time=0.08,
                rate_func=linear
            )
        
        self.wait(0.3)
        
        # Scale up to full screen
        # 🔊 SOUND: Build for scale up
        add_sound_safe(SOUND_BUILD, gain=-8)
        self.play(
            ending_logo.animate.scale(8).set_opacity(0.9),
            run_time=2.0,
            rate_func=rush_into
        )
        
        # Hold for a moment
        self.wait(0.5)
        
        # Final fadeout
        # 🔊 SOUND: Transition for final fadeout
        add_sound_safe(SOUND_TRANSITION, gain=-10)
        self.play(FadeOut(ending_logo), FadeOut(background), FadeOut(grid), run_time=1.0)
