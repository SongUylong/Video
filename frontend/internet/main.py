from manim import *
import os

# === CONFIGURATION (9:16 Vertical, 1080x1920, 60fps) ===
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60

# === COLOR PALETTE ===
NETWORK_BLUE = "#0ea5e9"
SUCCESS_GREEN = "#22c55e"
ALERT_RED = "#ef4444"
DNS_PURPLE = "#a855f7"
HTTP_ORANGE = "#f97316"
HTTPS_GREEN = "#10b981"
PACKET_YELLOW = "#fbbf24"
ROUTER_CYAN = "#06b6d4"
HOST_DARK = "#1e293b"
FUTURE_PINK = "#ec4899"

# === SOUND PATHS ===
SFX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../soundeffect/")
S_BLINK = f"{SFX}blink/blink1.mp3"
S_BUILD = f"{SFX}building/building1.mp3"
S_CLICK = f"{SFX}click/click1.mp3"
S_POP1 = f"{SFX}pop/pop1.mp3"
S_POP2 = f"{SFX}pop/pop2.mp3"
S_SWOOSH1 = f"{SFX}swoosh/swoosh1.mp3"
S_SWOOSH2 = f"{SFX}swoosh/swoosh2.mp3"
S_SWOOSH3 = f"{SFX}swoosh/swoosh3.mp3"
S_SWOOSH4 = f"{SFX}swoosh/swoosh4.mp3"
S_TYPE = f"{SFX}typing/typing1.mp3"
S_WOW = f"{SFX}wow/wow.mp3"


class InternetExplained(Scene):
    """
    PRODUCTION CUT - 120 SECONDS EXACT
    ===================================
    
    TIMELINE (with proper pacing):
    0-15s    Scene 1: HOOK (globe, network flash, title)
    15-35s   Scene 2: NETWORK OF NETWORKS (houses, connections)
    35-55s   Scene 3: PACKETS & ROUTERS (data split, routing)
    55-75s   Scene 4: IP & DNS (address lookup)
    75-95s   Scene 5: HTTP/HTTPS (request/response, encryption)
    95-110s  Scene 6: TCP/IP + SSL (protocol stack)
    110-120s Scene 7: FINALE (globe expansion, end)
    """
    
    def construct(self):
        # === SOUND HELPER ===
        def sfx(path, gain=-10):
            if os.path.exists(path):
                self.add_sound(path, gain=gain)
        
        # === BACKGROUND (persistent) ===
        bg = Rectangle(
            width=config.frame_width, height=config.frame_height,
            fill_color=["#0a0a1a", "#0f172a"], fill_opacity=1, stroke_width=0
        ).set_z_index(-100)
        self.add(bg)
        
        grid = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-10, 10, 1],
            background_line_style={"stroke_color": NETWORK_BLUE, "stroke_width": 0.3, "stroke_opacity": 0.15}
        ).set_z_index(-99)
        self.add(grid)

        # ╔══════════════════════════════════════════════════════════════╗
        # ║ SCENE 1: HOOK (0-15 seconds)                                 ║
        # ║ Globe with orbiting nodes → pulse → title                    ║
        # ╚══════════════════════════════════════════════════════════════╝
        
        # Globe SVG-style construction
        globe_outer = Circle(radius=2, color=NETWORK_BLUE, stroke_width=4, fill_opacity=0.1)
        globe_lat1 = Ellipse(width=4, height=1, color=NETWORK_BLUE, stroke_width=2).shift(UP*0.6)
        globe_lat2 = Ellipse(width=4, height=1, color=NETWORK_BLUE, stroke_width=2).shift(DOWN*0.6)
        globe_long = Ellipse(width=2, height=4, color=NETWORK_BLUE, stroke_width=2)
        globe = VGroup(globe_outer, globe_lat1, globe_lat2, globe_long).move_to(ORIGIN)
        
        # Orbiting nodes
        orbit_nodes = VGroup()
        for i in range(6):
            angle = i * TAU / 6
            node = Dot(radius=0.15, color=SUCCESS_GREEN).move_to(2.5 * np.array([np.cos(angle), np.sin(angle), 0]))
            orbit_nodes.add(node)
        
        # 0-3s: Globe draws in slowly
        sfx(S_BUILD, -8)
        self.play(Create(globe_outer), run_time=2)
        self.play(Create(globe_long), Create(globe_lat1), Create(globe_lat2), run_time=2)
        
        # 3-4.5s: Nodes appear one by one
        sfx(S_POP1, -8)
        self.play(LaggedStart(*[GrowFromCenter(n) for n in orbit_nodes], lag_ratio=0.15), run_time=1.5)
        
        # 4.5-7.5s: Orbit rotation (slow, dramatic)
        sfx(S_SWOOSH1, -10)
        self.play(Rotate(orbit_nodes, angle=PI/2, about_point=ORIGIN), run_time=3)
        
        # 6.5-7.5s: Pulse effect
        sfx(S_BLINK, -8)
        self.play(
            globe.animate.scale(1.15),
            orbit_nodes.animate.scale(1.3).set_color(PACKET_YELLOW),
            run_time=0.5
        )
        self.play(
            globe.animate.scale(1/1.15),
            orbit_nodes.animate.scale(1/1.3).set_color(SUCCESS_GREEN),
            run_time=0.5
        )
        
        # 7.5-8.5s: Connection lines
        conn_lines = VGroup()
        for i in range(6):
            line = Line(ORIGIN, orbit_nodes[i].get_center(), stroke_color=NETWORK_BLUE, stroke_width=2, stroke_opacity=0.6)
            conn_lines.add(line)
        
        sfx(S_CLICK, -10)
        self.play(LaggedStart(*[Create(l) for l in conn_lines], lag_ratio=0.1), run_time=1)
        
        # 8.5-10s: Title appears
        title = Text("THE INTERNET", font_size=52, weight=BOLD, color=WHITE)
        title.move_to(DOWN*5)
        
        sfx(S_POP2, -6)
        self.play(FadeIn(title, shift=UP*0.5, scale=0.8), run_time=1.5)
        
        # 10-12s: Float animation
        self.play(
            VGroup(globe, orbit_nodes, conn_lines).animate.shift(UP*0.2),
            run_time=1, rate_func=there_and_back
        )
        self.wait(1)
        
        # 12-15s: Contract to corner
        sfx(S_SWOOSH2, -10)
        mini_globe = VGroup(globe, orbit_nodes, conn_lines)
        self.play(
            mini_globe.animate.scale(0.12).move_to(UP*6.8 + RIGHT*3.5),
            FadeOut(title, shift=DOWN*0.5),
            run_time=1.5
        )
        self.wait(1.5)
        # TOTAL SCENE 1: ~18s

        # ╔══════════════════════════════════════════════════════════════╗
        # ║ SCENE 2: NETWORK OF NETWORKS (15-35 seconds)                 ║
        # ║ Device → Local Network → Multiple Networks → Internet        ║
        # ╚══════════════════════════════════════════════════════════════╝
        
        # Device icons
        def make_device(icon_text, size=0.4):
            box = RoundedRectangle(width=size, height=size*1.3, corner_radius=0.05, color=WHITE, fill_opacity=0.9, stroke_width=1)
            icon = Text(icon_text, font_size=int(size*40))
            icon.move_to(box.get_center())
            return VGroup(box, icon)
        
        # Network 1: Your home
        home1_bg = RoundedRectangle(width=3, height=2.8, corner_radius=0.2, color=NETWORK_BLUE, fill_opacity=0.15, stroke_width=2)
        home1_label = Text("Your Home", font_size=16, color=NETWORK_BLUE)
        home1_label.move_to(home1_bg.get_top() + DOWN*0.3)
        home1_devices = VGroup(
            make_device("💻"),
            make_device("📱"),
            make_device("🖥️")
        ).arrange(RIGHT, buff=0.3)
        home1_devices.move_to(home1_bg.get_center())
        home1_router = Circle(radius=0.25, color=ROUTER_CYAN, fill_opacity=0.8, stroke_width=2)
        home1_router.move_to(home1_bg.get_center() + DOWN*0.9)
        home1_router_icon = Text("R", font_size=14, color=WHITE, weight=BOLD).move_to(home1_router.get_center())
        
        network1 = VGroup(home1_bg, home1_label, home1_devices, home1_router, home1_router_icon)
        network1.move_to(LEFT*2.5 + UP*4.5)
        
        # Network 2: Friend
        home2_bg = RoundedRectangle(width=2.8, height=2.3, corner_radius=0.2, color=SUCCESS_GREEN, fill_opacity=0.15, stroke_width=2)
        home2_label = Text("Friend", font_size=16, color=SUCCESS_GREEN)
        home2_label.move_to(home2_bg.get_top() + DOWN*0.3)
        home2_devices = VGroup(
            make_device("💻", 0.35),
            make_device("📱", 0.35)
        ).arrange(RIGHT, buff=0.4)
        home2_devices.move_to(home2_bg.get_center())
        home2_router = Circle(radius=0.2, color=ROUTER_CYAN, fill_opacity=0.8, stroke_width=2)
        home2_router.move_to(home2_bg.get_center() + DOWN*0.7)
        
        network2 = VGroup(home2_bg, home2_label, home2_devices, home2_router)
        network2.move_to(RIGHT*2.5 + UP*4.5)
        
        # Network 3: Office
        office_bg = RoundedRectangle(width=4, height=2.5, corner_radius=0.2, color=HTTP_ORANGE, fill_opacity=0.15, stroke_width=2)
        office_label = Text("Office", font_size=16, color=HTTP_ORANGE)
        office_label.move_to(office_bg.get_top() + DOWN*0.3)
        office_devices = VGroup(*[make_device("🖥️", 0.3) for i in range(4)])
        office_devices.arrange(RIGHT, buff=0.25)
        office_devices.move_to(office_bg.get_center())
        office_router = Circle(radius=0.25, color=ROUTER_CYAN, fill_opacity=0.8, stroke_width=2)
        office_router.move_to(office_bg.get_center() + DOWN*0.8)
        
        network3 = VGroup(office_bg, office_label, office_devices, office_router)
        network3.move_to(DOWN*1.5)
        
        # 15-18s: Network 1 builds
        sfx(S_BUILD, -10)
        self.play(DrawBorderThenFill(home1_bg), FadeIn(home1_label), run_time=1)
        sfx(S_POP1, -12)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in home1_devices], lag_ratio=0.2), run_time=1.5)
        sfx(S_CLICK, -10)
        self.play(GrowFromCenter(VGroup(home1_router, home1_router_icon)), run_time=0.8)
        
        # Internal connections
        home1_conns = VGroup(*[Line(d.get_bottom(), home1_router.get_top(), stroke_color=WHITE, stroke_width=1, stroke_opacity=0.5) for d in home1_devices])
        self.play(LaggedStart(*[Create(c) for c in home1_conns], lag_ratio=0.2), run_time=0.8)
        network1.add(home1_conns)
        
        self.wait(0.5)
        
        # 20-23s: Network 2
        sfx(S_BUILD, -10)
        self.play(DrawBorderThenFill(home2_bg), FadeIn(home2_label), run_time=1)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in home2_devices], lag_ratio=0.2), GrowFromCenter(home2_router), run_time=1.5)
        
        # 23-26s: Network 3
        sfx(S_BUILD, -10)
        self.play(DrawBorderThenFill(office_bg), FadeIn(office_label), run_time=1)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in office_devices], lag_ratio=0.1), GrowFromCenter(office_router), run_time=1.5)
        
        self.wait(0.5)
        
        # 26-28s: Connect networks
        backbone1 = Line(home1_router.get_center(), office_router.get_center(), stroke_color=ROUTER_CYAN, stroke_width=3)
        backbone2 = Line(home2_router.get_center(), office_router.get_center(), stroke_color=ROUTER_CYAN, stroke_width=3)
        
        sfx(S_SWOOSH3, -8)
        self.play(Create(backbone1), Create(backbone2), run_time=1.5)
        
        # 28-30s: Label
        internet_label = Text("NETWORK OF NETWORKS", font_size=28, weight=BOLD, color=SUCCESS_GREEN)
        internet_label.move_to(DOWN*4.5)
        
        outer_box = RoundedRectangle(width=8, height=10, corner_radius=0.4, color=NETWORK_BLUE, stroke_width=3, fill_opacity=0.05)
        outer_box.move_to(UP*1)
        
        sfx(S_BUILD, -8)
        self.play(Create(outer_box), run_time=1.5)
        
        sfx(S_POP2, -6)
        self.play(FadeIn(internet_label, shift=UP*0.3), run_time=1)
        
        # 31-33s: Pulse all networks
        sfx(S_BLINK, -10)
        self.play(
            home1_bg.animate.set_stroke(color=SUCCESS_GREEN, width=4),
            home2_bg.animate.set_stroke(color=SUCCESS_GREEN, width=4),
            office_bg.animate.set_stroke(color=SUCCESS_GREEN, width=4),
            run_time=0.5
        )
        self.play(
            home1_bg.animate.set_stroke(color=NETWORK_BLUE, width=2),
            home2_bg.animate.set_stroke(color=SUCCESS_GREEN, width=2),
            office_bg.animate.set_stroke(color=HTTP_ORANGE, width=2),
            run_time=0.5
        )
        
        self.wait(2.5)
        
        # 35-37s: Transition
        sfx(S_SWOOSH1, -10)
        self.play(
            FadeOut(VGroup(network1, network2, network3, backbone1, backbone2, outer_box, internet_label)),
            run_time=1.5
        )
        # TOTAL SCENE 2: ~20s (cumulative: 35s)

        # ╔══════════════════════════════════════════════════════════════╗
        # ║ SCENE 3: PACKETS & ROUTERS (35-55 seconds)                   ║
        # ║ Data → Split into packets → Route through mesh              ║
        # ╚══════════════════════════════════════════════════════════════╝
        
        # Source
        source = VGroup(
            RoundedRectangle(width=1.8, height=2.2, corner_radius=0.15, color=NETWORK_BLUE, fill_opacity=0.9, stroke_width=2),
            Text("📤", font_size=50)
        )
        source[1].move_to(source[0].get_center())
        source.move_to(LEFT*3 + UP*5)
        
        # Destination
        dest = VGroup(
            RoundedRectangle(width=1.8, height=2.2, corner_radius=0.15, color=SUCCESS_GREEN, fill_opacity=0.9, stroke_width=2),
            Text("📥", font_size=50)
        )
        dest[1].move_to(dest[0].get_center())
        dest.move_to(RIGHT*3 + DOWN*5)
        
        # 35-37s: Source and dest appear
        sfx(S_POP1, -10)
        self.play(GrowFromCenter(source), GrowFromCenter(dest), run_time=1.5)
        
        # 37-40s: Router mesh
        router_positions = [
            LEFT*1 + UP*2.5,
            RIGHT*1.5 + UP*1,
            LEFT*2 + DOWN*0.5,
            ORIGIN + DOWN*2,
            RIGHT*2 + DOWN*3
        ]
        
        routers = VGroup()
        for pos in router_positions:
            r = VGroup(
                Circle(radius=0.4, color=ROUTER_CYAN, fill_opacity=0.85, stroke_width=2),
                Text("R", font_size=20, color=WHITE, weight=BOLD)
            )
            r[1].move_to(r[0].get_center())
            r.move_to(pos)
            routers.add(r)
        
        sfx(S_BUILD, -10)
        self.play(LaggedStart(*[GrowFromCenter(r) for r in routers], lag_ratio=0.2), run_time=2)
        
        # 40-41s: Mesh connections
        mesh_pairs = [(0,1), (0,2), (1,3), (2,3), (3,4), (1,4)]
        mesh_lines = VGroup()
        for i, j in mesh_pairs:
            line = Line(routers[i].get_center(), routers[j].get_center(), stroke_color=ROUTER_CYAN, stroke_width=2, stroke_opacity=0.4)
            mesh_lines.add(line)
        
        sfx(S_CLICK, -12)
        self.play(LaggedStart(*[Create(l) for l in mesh_lines], lag_ratio=0.1), run_time=1.5)
        
        # 41-43s: Data block splits into packets
        data_block = RoundedRectangle(width=1.5, height=0.8, corner_radius=0.1, color=PACKET_YELLOW, fill_opacity=0.9, stroke_width=2)
        data_block.move_to(source.get_center())
        
        sfx(S_POP2, -10)
        self.play(FadeIn(data_block, scale=0.5), run_time=1)
        
        # Split into 4 packets
        packets = VGroup()
        packet_colors = [PACKET_YELLOW, HTTP_ORANGE, SUCCESS_GREEN, DNS_PURPLE]
        for i in range(4):
            p = RoundedRectangle(width=0.4, height=0.3, corner_radius=0.05, color=packet_colors[i], fill_opacity=0.9, stroke_width=1)
            p.move_to(data_block.get_center())
            packets.add(p)
        
        sfx(S_CLICK, -8)
        self.play(
            FadeOut(data_block),
            packets[0].animate.shift(UP*0.3 + LEFT*0.3),
            packets[1].animate.shift(UP*0.3 + RIGHT*0.3),
            packets[2].animate.shift(DOWN*0.3 + LEFT*0.3),
            packets[3].animate.shift(DOWN*0.3 + RIGHT*0.3),
            run_time=1
        )
        
        # 44-45s: Packets label
        pkt_label = Text("PACKETS", font_size=24, color=PACKET_YELLOW, weight=BOLD)
        pkt_label.next_to(source, DOWN, buff=0.5)
        sfx(S_TYPE, -12)
        self.play(FadeIn(pkt_label), run_time=0.8)
        
        self.wait(0.5)
        
        # 45-51s: Animate packets through different paths (slower, more visible)
        paths = [
            [source.get_center(), routers[0].get_center(), routers[1].get_center(), routers[4].get_center(), dest.get_center()],
            [source.get_center(), routers[0].get_center(), routers[2].get_center(), routers[3].get_center(), dest.get_center()],
            [source.get_center(), routers[0].get_center(), routers[1].get_center(), routers[3].get_center(), dest.get_center()],
            [source.get_center(), routers[0].get_center(), routers[2].get_center(), routers[3].get_center(), routers[4].get_center(), dest.get_center()],
        ]
        
        for idx, (pkt, path) in enumerate(zip(packets, paths)):
            if idx == 0:
                sfx(S_SWOOSH4, -10)
            
            for i in range(len(path) - 1):
                self.play(pkt.animate.move_to(path[i+1]), run_time=0.4)
                # Flash router on pass
                if i > 0 and i < len(path) - 1:
                    router_idx = min(idx, len(routers)-1)
                    self.play(routers[router_idx][0].animate.set_color(SUCCESS_GREEN), run_time=0.1)
                    self.play(routers[router_idx][0].animate.set_color(ROUTER_CYAN), run_time=0.1)
        
        # 51-53s: Packets reassemble
        sfx(S_BUILD, -8)
        self.play(
            packets[0].animate.move_to(dest.get_center() + UP*0.2 + LEFT*0.2),
            packets[1].animate.move_to(dest.get_center() + UP*0.2 + RIGHT*0.2),
            packets[2].animate.move_to(dest.get_center() + DOWN*0.2 + LEFT*0.2),
            packets[3].animate.move_to(dest.get_center() + DOWN*0.2 + RIGHT*0.2),
            run_time=1
        )
        
        # Merge back
        merged = RoundedRectangle(width=1, height=0.6, corner_radius=0.08, color=SUCCESS_GREEN, fill_opacity=0.9, stroke_width=2)
        merged.move_to(dest.get_center())
        
        sfx(S_POP1, -6)
        self.play(FadeOut(packets), FadeIn(merged, scale=1.2), run_time=0.8)
        
        # 53-54s: Success
        check = Text("✓", font_size=40, color=SUCCESS_GREEN, weight=BOLD).next_to(dest, UP, buff=0.3)
        sfx(S_CLICK, -8)
        self.play(FadeIn(check, scale=0.5), run_time=0.5)
        
        self.wait(1)
        
        # 54-55s: Transition
        sfx(S_SWOOSH2, -10)
        self.play(
            FadeOut(VGroup(source, dest, routers, mesh_lines, pkt_label, merged, check)),
            run_time=1.5
        )
        # TOTAL SCENE 3: ~20s (cumulative: 55s)

        # ╔══════════════════════════════════════════════════════════════╗
        # ║ SCENE 4: IP & DNS (55-75 seconds)                            ║
        # ║ IP Address → Domain Name → DNS Lookup                        ║
        # ╚══════════════════════════════════════════════════════════════╝
        
        # 55-58s: IP Address
        ip_box = RoundedRectangle(width=4.5, height=1.3, corner_radius=0.2, color=NETWORK_BLUE, fill_opacity=0.2, stroke_width=3)
        ip_box.move_to(UP*4.5)
        ip_label = Text("IP ADDRESS", font_size=18, color=NETWORK_BLUE, weight=BOLD).next_to(ip_box, UP, buff=0.15)
        ip_value = Text("172.217.14.206", font_size=32, font="monospace", color=WHITE).move_to(ip_box)
        
        sfx(S_BUILD, -10)
        self.play(Create(ip_box), FadeIn(ip_label), run_time=1)
        sfx(S_TYPE, -10)
        self.play(Write(ip_value), run_time=1.5)
        
        # Confused emoji
        confused = Text("🤔", font_size=50).next_to(ip_box, RIGHT, buff=0.5)
        sfx(S_POP1, -12)
        self.play(FadeIn(confused, scale=0.5), run_time=0.8)
        
        self.wait(1)
        
        # 60-63s: Domain name
        domain_box = RoundedRectangle(width=4, height=1.3, corner_radius=0.2, color=HTTP_ORANGE, fill_opacity=0.2, stroke_width=3)
        domain_box.move_to(UP*1.5)
        domain_label = Text("DOMAIN NAME", font_size=18, color=HTTP_ORANGE, weight=BOLD).next_to(domain_box, UP, buff=0.15)
        domain_value = Text("google.com", font_size=36, color=WHITE).move_to(domain_box)
        
        sfx(S_BUILD, -10)
        self.play(Create(domain_box), FadeIn(domain_label), run_time=1)
        sfx(S_TYPE, -10)
        self.play(Write(domain_value), run_time=1)
        
        # Happy face
        happy = Text("😊", font_size=50).next_to(domain_box, RIGHT, buff=0.5)
        sfx(S_POP2, -10)
        self.play(FadeOut(confused), FadeIn(happy, scale=0.5), run_time=0.8)
        
        self.wait(1)
        
        # 65-68s: DNS Server
        dns_box = RoundedRectangle(width=5, height=2, corner_radius=0.3, color=DNS_PURPLE, fill_opacity=0.85, stroke_width=3)
        dns_box.move_to(DOWN*2)
        dns_icon = Text("📖", font_size=45).move_to(dns_box.get_center() + UP*0.3)
        dns_text = Text("DNS", font_size=28, color=WHITE, weight=BOLD).move_to(dns_box.get_center() + DOWN*0.4)
        
        sfx(S_BUILD, -8)
        self.play(DrawBorderThenFill(dns_box), FadeIn(dns_icon), FadeIn(dns_text), run_time=1.5)
        
        # 68-70s: Query arrow
        query_arrow = Arrow(domain_box.get_bottom(), dns_box.get_top(), buff=0.15, color=DNS_PURPLE, stroke_width=4)
        query_label = Text("lookup", font_size=14, color=DNS_PURPLE).next_to(query_arrow, LEFT, buff=0.1)
        
        sfx(S_CLICK, -10)
        self.play(GrowArrow(query_arrow), FadeIn(query_label), run_time=1)
        
        # DNS processing
        sfx(S_BLINK, -10)
        self.play(dns_box.animate.set_stroke(color=SUCCESS_GREEN, width=5), run_time=0.3)
        self.play(dns_box.animate.set_stroke(color=DNS_PURPLE, width=3), run_time=0.3)
        
        # 70-72s: Response
        response_arrow = Arrow(dns_box.get_top() + RIGHT*1, ip_box.get_bottom() + RIGHT*1, buff=0.15, color=SUCCESS_GREEN, stroke_width=4)
        
        sfx(S_CLICK, -8)
        self.play(GrowArrow(response_arrow), run_time=1)
        
        # Highlight IP
        sfx(S_POP1, -6)
        self.play(
            ip_box.animate.set_stroke(color=SUCCESS_GREEN, width=4),
            ip_value.animate.set_color(SUCCESS_GREEN),
            run_time=0.8
        )
        
        # 72-74s: Result
        result = Text("✓ RESOLVED", font_size=24, color=SUCCESS_GREEN, weight=BOLD).move_to(DOWN*5)
        sfx(S_POP2, -8)
        self.play(FadeIn(result, shift=UP*0.3), run_time=0.8)
        
        self.wait(2.5)
        
        # 76-78s: Transition
        sfx(S_SWOOSH3, -10)
        self.play(
            FadeOut(VGroup(ip_box, ip_label, ip_value, domain_box, domain_label, domain_value, 
                          dns_box, dns_icon, dns_text, query_arrow, query_label, response_arrow, happy, result)),
            run_time=1.5
        )
        # TOTAL SCENE 4: ~20s (cumulative: 75s)

        # ╔══════════════════════════════════════════════════════════════╗
        # ║ SCENE 5: HTTP/HTTPS (75-100 seconds) - CLEAN LAYOUT          ║
        # ╚══════════════════════════════════════════════════════════════╝
        
        # Title first
        http_title = Text("HTTP", font_size=40, color=HTTP_ORANGE, weight=BOLD).move_to(UP*6)
        sfx(S_TYPE, -10)
        self.play(Write(http_title), run_time=0.8)
        
        # Browser (left side, upper)
        browser_box = RoundedRectangle(width=2.8, height=2, corner_radius=0.2, color=WHITE, fill_opacity=0.9, stroke_width=2)
        browser_icon = Text("🌐", font_size=35).move_to(browser_box.get_center())
        browser_label = Text("CLIENT", font_size=12, color=WHITE, weight=BOLD).next_to(browser_box, DOWN, buff=0.1)
        browser = VGroup(browser_box, browser_icon, browser_label)
        browser.move_to(LEFT*2.8 + UP*3)
        
        # Server (right side, upper)
        server_box = RoundedRectangle(width=2.8, height=2, corner_radius=0.2, color=NETWORK_BLUE, fill_opacity=0.9, stroke_width=2)
        server_icon = Text("🖥️", font_size=35).move_to(server_box.get_center())
        server_label = Text("SERVER", font_size=12, color=WHITE, weight=BOLD).next_to(server_box, DOWN, buff=0.1)
        server = VGroup(server_box, server_icon, server_label)
        server.move_to(RIGHT*2.8 + UP*3)
        
        sfx(S_BUILD, -10)
        self.play(GrowFromCenter(browser), GrowFromCenter(server), run_time=1)
        
        self.wait(0.3)
        
        # REQUEST arrow with label
        req_arrow = Arrow(browser_box.get_right(), server_box.get_left(), buff=0.2, color=HTTP_ORANGE, stroke_width=5)
        req_box = RoundedRectangle(width=2, height=0.8, corner_radius=0.1, color=HTTP_ORANGE, fill_opacity=0.85)
        req_box.next_to(req_arrow, UP, buff=0.15)
        req_text = Text("GET /", font_size=14, font="monospace", color=WHITE).move_to(req_box.get_center())
        request = VGroup(req_arrow, req_box, req_text)
        
        sfx(S_SWOOSH4, -10)
        self.play(GrowArrow(req_arrow), FadeIn(req_box), FadeIn(req_text), run_time=1)
        
        self.wait(0.3)
        
        # RESPONSE arrow with label
        res_arrow = Arrow(server_box.get_left() + DOWN*0.4, browser_box.get_right() + DOWN*0.4, buff=0.2, color=SUCCESS_GREEN, stroke_width=5)
        res_box = RoundedRectangle(width=2, height=0.8, corner_radius=0.1, color=SUCCESS_GREEN, fill_opacity=0.85)
        res_box.next_to(res_arrow, DOWN, buff=0.15)
        res_text = Text("200 OK", font_size=14, font="monospace", color=WHITE).move_to(res_box.get_center())
        response = VGroup(res_arrow, res_box, res_text)
        
        sfx(S_SWOOSH3, -10)
        self.play(GrowArrow(res_arrow), FadeIn(res_box), FadeIn(res_text), run_time=1)
        
        self.wait(0.5)
        
        # Fade out HTTP elements
        sfx(S_SWOOSH1, -10)
        self.play(FadeOut(VGroup(http_title, browser, server, request, response)), run_time=0.8)
        
        # === HTTPS SECTION ===
        https_title = Text("HTTPS", font_size=40, color=HTTPS_GREEN, weight=BOLD).move_to(UP*6)
        https_sub = Text("Secure Connection", font_size=16, color=WHITE).next_to(https_title, DOWN, buff=0.1)
        
        sfx(S_BUILD, -8)
        self.play(Write(https_title), FadeIn(https_sub), run_time=0.8)
        
        # Client (left) - positioned higher
        hs_client = VGroup(
            RoundedRectangle(width=2, height=1.5, corner_radius=0.15, color=NETWORK_BLUE, fill_opacity=0.85),
            Text("🌐", font_size=30)
        )
        hs_client[1].move_to(hs_client[0].get_center())
        hs_client.move_to(LEFT*3 + UP*3.5)
        
        # Server (right) - same height as client
        hs_server = VGroup(
            RoundedRectangle(width=2, height=1.5, corner_radius=0.15, color=SUCCESS_GREEN, fill_opacity=0.85),
            Text("🖥️", font_size=30)
        )
        hs_server[1].move_to(hs_server[0].get_center())
        hs_server.move_to(RIGHT*3 + UP*3.5)
        
        sfx(S_POP1, -10)
        self.play(FadeIn(hs_client), FadeIn(hs_server), run_time=0.6)
        
        # Connection arrow with lock - BETWEEN client and server
        conn_arrow = Arrow(hs_client.get_right(), hs_server.get_left(), buff=0.2, color=HTTPS_GREEN, stroke_width=4)
        lock_icon = Text("🔒", font_size=35).move_to(conn_arrow.get_center() + UP*0.4)
        
        sfx(S_BUILD, -10)
        self.play(GrowArrow(conn_arrow), run_time=0.6)
        sfx(S_POP2, -8)
        self.play(FadeIn(lock_icon, scale=0.5), run_time=0.5)
        
        # Encrypted packet animation
        for _ in range(2):
            pkt = RoundedRectangle(width=0.5, height=0.35, corner_radius=0.06, color=PACKET_YELLOW, fill_opacity=0.9)
            pkt.move_to(hs_client.get_right() + RIGHT*0.3)
            self.add(pkt)
            self.play(pkt.animate.move_to(hs_server.get_left() + LEFT*0.3), run_time=0.4)
            self.play(FadeOut(pkt), run_time=0.15)
        
        # Security benefits (lower section - well separated)
        benefits_title = Text("SECURITY", font_size=20, color=HTTPS_GREEN, weight=BOLD).move_to(UP*0.5)
        
        benefit1 = VGroup(Text("✓", font_size=20, color=SUCCESS_GREEN), Text("Encrypted", font_size=14, color=WHITE)).arrange(RIGHT, buff=0.15)
        benefit2 = VGroup(Text("✓", font_size=20, color=SUCCESS_GREEN), Text("Verified", font_size=14, color=WHITE)).arrange(RIGHT, buff=0.15)
        benefit3 = VGroup(Text("✓", font_size=20, color=SUCCESS_GREEN), Text("Integrity", font_size=14, color=WHITE)).arrange(RIGHT, buff=0.15)
        benefits = VGroup(benefit1, benefit2, benefit3).arrange(RIGHT, buff=0.8)
        benefits.move_to(DOWN*0.5)
        
        sfx(S_POP1, -10)
        self.play(FadeIn(benefits_title), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(b, shift=UP*0.2) for b in benefits], lag_ratio=0.15), run_time=0.8)
        
        self.wait(0.5)
        
        # Fade out upper HTTPS elements, keep bottom for SSL/TLS demo
        sfx(S_SWOOSH1, -10)
        self.play(FadeOut(VGroup(hs_client, hs_server, conn_arrow, lock_icon)), run_time=0.6)
        
        # === SSL/TLS ENCRYPTION DEMO ===
        ssl_sub = Text("SSL/TLS Encryption", font_size=18, color=HTTPS_GREEN).move_to(UP*3)
        sfx(S_BUILD, -10)
        self.play(FadeIn(ssl_sub), run_time=0.4)
        
        # Encryption flow: Plaintext → Lock → Ciphertext (positioned below SSL subtitle)
        plain = VGroup(
            RoundedRectangle(width=1.8, height=1, corner_radius=0.1, color=ALERT_RED, fill_opacity=0.3),
            Text("Hello!", font_size=14, color=WHITE)
        )
        plain[1].move_to(plain[0].get_center())
        plain.move_to(LEFT*2.5 + UP*1.5)
        
        lock_enc = VGroup(
            RoundedRectangle(width=1.5, height=1.2, corner_radius=0.12, color=HTTPS_GREEN, fill_opacity=0.85),
            Text("🔐", font_size=35)
        )
        lock_enc[1].move_to(lock_enc[0].get_center())
        lock_enc.move_to(ORIGIN + UP*1.5)
        
        cipher = VGroup(
            RoundedRectangle(width=1.8, height=1, corner_radius=0.1, color=SUCCESS_GREEN, fill_opacity=0.3),
            Text("x7#k!", font_size=14, font="monospace", color=SUCCESS_GREEN)
        )
        cipher[1].move_to(cipher[0].get_center())
        cipher.move_to(RIGHT*2.5 + UP*1.5)
        
        sfx(S_POP1, -10)
        self.play(FadeIn(plain), run_time=0.4)
        
        enc_arr1 = Arrow(plain.get_right(), lock_enc.get_left(), buff=0.1, color=WHITE, stroke_width=2)
        sfx(S_SWOOSH4, -12)
        self.play(GrowArrow(enc_arr1), FadeIn(lock_enc), run_time=0.4)
        
        enc_arr2 = Arrow(lock_enc.get_right(), cipher.get_left(), buff=0.1, color=WHITE, stroke_width=2)
        sfx(S_SWOOSH3, -12)
        self.play(GrowArrow(enc_arr2), FadeIn(cipher), run_time=0.4)
        
        self.wait(0.8)
        
        # Transition out entire HTTPS scene
        sfx(S_SWOOSH2, -10)
        self.play(
            FadeOut(VGroup(https_title, https_sub, benefits_title, benefits, ssl_sub, plain, lock_enc, cipher, enc_arr1, enc_arr2)),
            run_time=1
        )
        # ╔══════════════════════════════════════════════════════════════╗
        # ║ SCENE 6: TCP/IP + SSL/TLS - CLEAN LAYOUT                     ║
        # ╚══════════════════════════════════════════════════════════════╝
        
        # Title
        tcp_title = Text("TCP/IP", font_size=40, color=WHITE, weight=BOLD).move_to(UP*6)
        sfx(S_TYPE, -10)
        self.play(Write(tcp_title), run_time=0.8)
        
        # Create 4 layers - smaller boxes
        layer_data = [
            ("APPLICATION", HTTP_ORANGE, "HTTP, DNS"),
            ("TRANSPORT", SUCCESS_GREEN, "TCP, UDP"),
            ("INTERNET", NETWORK_BLUE, "IP"),
            ("NETWORK", ROUTER_CYAN, "Ethernet"),
        ]
        
        layers = VGroup()
        for name, color, proto in layer_data:
            layer_box = RoundedRectangle(width=5.5, height=1, corner_radius=0.12, color=color, fill_opacity=0.85, stroke_width=2)
            layer_name = Text(name, font_size=14, color=WHITE, weight=BOLD).move_to(layer_box.get_center() + LEFT*1)
            layer_proto = Text(proto, font_size=11, font="monospace", color=WHITE).move_to(layer_box.get_center() + RIGHT*1.5)
            layer = VGroup(layer_box, layer_name, layer_proto)
            layers.add(layer)
        
        layers.arrange(DOWN, buff=0.1)
        layers.move_to(UP*3)
        
        # Build stack from bottom
        sfx(S_BUILD, -8)
        for layer in reversed(list(layers)):
            self.play(GrowFromEdge(layer, DOWN), run_time=0.5)
        
        self.wait(0.5)
        
        # 3-WAY HANDSHAKE (compact, below stack)
        hs_title = Text("3-WAY HANDSHAKE", font_size=18, color=SUCCESS_GREEN, weight=BOLD).move_to(DOWN*0.8)
        sfx(S_POP2, -10)
        self.play(FadeIn(hs_title), run_time=0.4)
        
        # Client and Server circles
        client = VGroup(
            Circle(radius=0.4, color=NETWORK_BLUE, fill_opacity=0.85),
            Text("C", font_size=16, color=WHITE, weight=BOLD)
        )
        client[1].move_to(client[0].get_center())
        client.move_to(LEFT*2.5 + DOWN*2.5)
        
        server = VGroup(
            Circle(radius=0.4, color=SUCCESS_GREEN, fill_opacity=0.85),
            Text("S", font_size=16, color=WHITE, weight=BOLD)
        )
        server[1].move_to(server[0].get_center())
        server.move_to(RIGHT*2.5 + DOWN*2.5)
        
        sfx(S_POP1, -10)
        self.play(FadeIn(client), FadeIn(server), run_time=0.5)
        
        # Arrows in sequence
        syn = Arrow(client.get_right(), server.get_left(), buff=0.15, color=PACKET_YELLOW, stroke_width=3)
        syn_lbl = Text("SYN", font_size=12, color=PACKET_YELLOW).next_to(syn, UP, buff=0.05)
        sfx(S_SWOOSH4, -12)
        self.play(GrowArrow(syn), FadeIn(syn_lbl), run_time=0.4)
        
        synack = Arrow(server.get_left() + DOWN*0.2, client.get_right() + DOWN*0.2, buff=0.15, color=HTTP_ORANGE, stroke_width=3)
        synack_lbl = Text("SYN-ACK", font_size=12, color=HTTP_ORANGE).next_to(synack, DOWN, buff=0.05)
        sfx(S_SWOOSH3, -12)
        self.play(GrowArrow(synack), FadeIn(synack_lbl), run_time=0.4)
        
        ack_arrow = Arrow(client.get_right() + DOWN*0.4, server.get_left() + DOWN*0.4, buff=0.15, color=SUCCESS_GREEN, stroke_width=3)
        ack_lbl = Text("ACK", font_size=12, color=SUCCESS_GREEN).next_to(ack_arrow, DOWN, buff=0.05)
        sfx(S_SWOOSH4, -12)
        self.play(GrowArrow(ack_arrow), FadeIn(ack_lbl), run_time=0.4)
        
        # Connected
        check = Text("✓", font_size=28, color=SUCCESS_GREEN, weight=BOLD).move_to(DOWN*4.5)
        sfx(S_POP2, -8)
        self.play(FadeIn(check, scale=0.5), run_time=0.3)
        
        self.wait(0.5)
        
        # Transition
        sfx(S_SWOOSH2, -10)
        self.play(FadeOut(VGroup(tcp_title, layers, hs_title, client, server, syn, syn_lbl, synack, synack_lbl, ack_arrow, ack_lbl, check)), run_time=0.8)
        # TOTAL SCENE 6: ~15s

        # ╔══════════════════════════════════════════════════════════════╗
        # ║ SCENE 7: OUTRO - Logo Animation                              ║
        # ╚══════════════════════════════════════════════════════════════╝
        
        # Load potato logo
        try:
            logo = SVGMobject("../../docker/asset/potato.svg")
            logo.set_height(6)
        except:
            # Fallback if SVG fails
            logo = VGroup(
                Circle(radius=2, color=HTTP_ORANGE, fill_opacity=0.9),
                Text("🥔", font_size=80)
            )
            logo[1].move_to(logo[0].get_center())
        
        logo.move_to(ORIGIN + DOWN*8)  # Start below screen
        
        # Bring logo up with bounce
        sfx(S_SWOOSH1, -6)
        self.play(
            logo.animate.move_to(ORIGIN),
            run_time=1.5,
            rate_func=smooth
        )
        
        # Scale pulse effect
        sfx(S_POP1, -8)
        self.play(logo.animate.scale(1.15), run_time=0.3)
        self.play(logo.animate.scale(1/1.15), run_time=0.3)
        
        # Gentle shake animation
        sfx(S_BLINK, -6)
        original_pos = logo.get_center()
        for _ in range(3):
            self.play(
                logo.animate.shift(LEFT*0.1),
                run_time=0.08,
                rate_func=there_and_back
            )
            self.play(
                logo.animate.shift(RIGHT*0.1),
                run_time=0.08,
                rate_func=there_and_back
            )
        
        logo.move_to(original_pos)
        
        # Final glow and hold
        sfx(S_WOW, -4)
        self.play(
            logo.animate.scale(1.3),
            run_time=1.5,
            rate_func=smooth
        )
        
        self.wait(1.5)
        
        # Fade out
        self.play(
            FadeOut(logo),
            run_time=1
        )
        
        self.wait(0.5)
        # TOTAL SCENE 7: ~10s

