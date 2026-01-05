import {
  makeScene2D,
  Camera,
  Grid,
  Line,
  Node,
  Rect,
  Txt,
  Img,
} from "@motion-canvas/2d";
import {
  Vector2,
  all,
  createRef,
  createSignal,
  waitFor,
  easeOutCubic,
  easeInOutCubic,
  easeOutBounce,
} from "@motion-canvas/core";

const CYAN = "#00d4ff";
const GREEN = "#00ff88";
const RED = "#ff6b6b";
const TEAL = "#4ecdc4";
const YELLOW = "#ffd93d";
const PINK = "#ff66aa";
const ORANGE = "#ffaa00";
const PURPLE = "#a29bfe";
const WHITE = "#ffffff";
const DARK = "#0a0a1a";

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const camera = createRef<Camera>();
  const titleOpacity = createSignal(0);
  const title = createRef<Txt>();

  // Refs for position animations
  const serverNode = createRef<Node>();
  const userNode = createRef<Node>();
  const fileNodes = [
    createRef<Node>(),
    createRef<Node>(),
    createRef<Node>(),
    createRef<Node>(),
  ];
  const hostingNodes = [
    createRef<Node>(),
    createRef<Node>(),
    createRef<Node>(),
    createRef<Node>(),
  ];

  const serverOpacity = createSignal(0);
  const userOpacity = createSignal(0);
  const fileOpacities = [
    createSignal(0),
    createSignal(0),
    createSignal(0),
    createSignal(0),
  ];
  const hostingOpacities = [
    createSignal(0),
    createSignal(0),
    createSignal(0),
    createSignal(0),
  ];
  const arrowProgress = createSignal(0);

  const files = [
    { type: "HTML", color: RED, icon: "code" },
    { type: "CSS", color: TEAL, icon: "script" },
    { type: "JS", color: YELLOW, icon: "script" },
    { type: "IMG", color: PURPLE, icon: "binary-code" },
  ];

  const hostingTypes = [
    { name: "Shared", color: CYAN },
    { name: "VPS", color: GREEN },
    { name: "Cloud", color: PINK },
    { name: "Dedicated", color: ORANGE },
  ];

  // File starting positions (inside server area - centered)
  const fileStartX = [-150, -50, 50, 150];
  const fileStartY = [200, 200, 200, 200];
  // File end positions (spread out middle - keep within screen bounds)
  const fileEndX = [-270, -90, 90, 270];
  const fileEndY = [200, 200, 200, 200];

  view.add(
    <Camera ref={camera}>
      <Grid
        width={1080}
        height={1920}
        spacing={60}
        stroke={"#1a1a2e"}
        lineWidth={1}
      />

      {/* Title */}
      <Txt
        ref={title}
        text={"WEB HOSTING"}
        fontSize={80}
        fontWeight={800}
        fill={WHITE}
        y={-800}
        opacity={() => titleOpacity()}
        shadowColor={GREEN}
        shadowBlur={25}
      />

      {/* Subtitle */}
      <Txt
        text={"Files stored on servers"}
        fontSize={38}
        fontWeight={500}
        fill={"#88aaff"}
        y={-720}
        opacity={() => titleOpacity()}
      />

      {/* SERVER BOX */}
      <Node ref={serverNode} y={-380}>
        <Rect
          width={500}
          height={420}
          fill={"#0d1a2a"}
          stroke={GREEN}
          lineWidth={6}
          radius={28}
          shadowColor={GREEN}
          shadowBlur={30}
          opacity={() => serverOpacity()}
        />
        <Img
          src={"/asset/cloud-server.png"}
          width={140}
          height={140}
          y={-100}
          opacity={() => serverOpacity()}
        />
        <Txt
          text={"SERVER"}
          fontSize={44}
          fontWeight={700}
          fill={GREEN}
          y={80}
          opacity={() => serverOpacity()}
        />
      </Node>

      {/* File boxes - each at their own starting position */}
      {files.map((file, i) => (
        <Node
          key={`file-${i}`}
          ref={fileNodes[i]}
          x={fileStartX[i]}
          y={fileStartY[i]}
        >
          <Rect
            width={150}
            height={130}
            fill={"#1a1a3a"}
            stroke={file.color}
            lineWidth={5}
            radius={18}
            shadowColor={file.color}
            shadowBlur={16}
            opacity={() => fileOpacities[i]()}
          />
          <Img
            src={`/asset/${file.icon}.png`}
            width={55}
            height={55}
            y={-18}
            opacity={() => fileOpacities[i]()}
          />
          <Txt
            text={file.type}
            fontSize={26}
            fontWeight={700}
            fill={file.color}
            y={42}
            opacity={() => fileOpacities[i]()}
          />
        </Node>
      ))}

      {/* Arrow showing data flow */}
      <Line
        stroke={GREEN}
        lineWidth={8}
        lineDash={[25, 12]}
        endArrow
        arrowSize={32}
        end={() => arrowProgress()}
        points={[new Vector2(0, -100), new Vector2(0, 380)]}
      />

      {/* USER BOX */}
      <Node ref={userNode} y={520}>
        <Rect
          width={420}
          height={220}
          fill={"#1a2a4a"}
          stroke={CYAN}
          lineWidth={6}
          radius={28}
          shadowColor={CYAN}
          shadowBlur={30}
          opacity={() => userOpacity()}
        />
        <Img
          src={"/asset/browser.png"}
          width={100}
          height={100}
          y={-30}
          opacity={() => userOpacity()}
        />
        <Txt
          text={"USER"}
          fontSize={40}
          fontWeight={700}
          fill={CYAN}
          y={70}
          opacity={() => userOpacity()}
        />
      </Node>

      {/* Hosting types - in a row at bottom */}
      {hostingTypes.map((hosting, i) => (
        <Node
          key={`hosting-${i}`}
          ref={hostingNodes[i]}
          x={-220 + i * 150}
          y={780}
        >
          <Rect
            width={175}
            height={85}
            fill={"#1a1a2e"}
            stroke={hosting.color}
            lineWidth={4}
            radius={16}
            shadowColor={hosting.color}
            shadowBlur={14}
            opacity={() => hostingOpacities[i]()}
          />
          <Txt
            text={hosting.name}
            fontSize={28}
            fontWeight={700}
            fill={hosting.color}
            opacity={() => hostingOpacities[i]()}
          />
        </Node>
      ))}
    </Camera>
  );

  // ===== ANIMATION =====

  // Title fades in
  yield* titleOpacity(1, 0.6);
  yield* waitFor(0.4);

  // Server appears
  yield* serverOpacity(1, 0.5, easeOutCubic);
  yield* waitFor(0.3);

  // Files appear inside server (they're already positioned there)
  for (let i = 0; i < files.length; i++) {
    yield* fileOpacities[i](1, 0.25, easeOutCubic);
  }

  yield* waitFor(0.5);

  // Update title
  yield* title().text("DATA TRANSFER", 0.4);

  yield* waitFor(0.3);

  // User appears
  yield* userOpacity(1, 0.5, easeOutCubic);

  yield* waitFor(0.3);

  // Arrow draws
  yield* arrowProgress(1, 0.6);

  yield* waitFor(0.4);

  // Files move from server to middle (showing transfer)
  yield* all(
    fileNodes[0]().position.x(fileEndX[0], 0.6, easeOutCubic),
    fileNodes[0]().position.y(fileEndY[0], 0.6, easeOutCubic),
    fileNodes[1]().position.x(fileEndX[1], 0.6, easeOutCubic),
    fileNodes[1]().position.y(fileEndY[1], 0.6, easeOutCubic),
    fileNodes[2]().position.x(fileEndX[2], 0.6, easeOutCubic),
    fileNodes[2]().position.y(fileEndY[2], 0.6, easeOutCubic),
    fileNodes[3]().position.x(fileEndX[3], 0.6, easeOutCubic),
    fileNodes[3]().position.y(fileEndY[3], 0.6, easeOutCubic)
  );

  yield* waitFor(0.3);

  // Files continue to user
  yield* all(
    ...fileNodes.map((n) => n().position.y(520, 0.5, easeInOutCubic)),
    ...fileOpacities.map((o) => o(0, 0.5))
  );

  // Pulse user to show received
  yield* userOpacity(1.2, 0.2);
  yield* userOpacity(1, 0.2);

  yield* waitFor(0.6);

  // Update title
  yield* title().text("HOSTING TYPES", 0.4);

  yield* waitFor(0.4);

  // Hosting types appear
  for (let i = 0; i < hostingTypes.length; i++) {
    yield* hostingOpacities[i](1, 0.3, easeOutCubic);
    yield* waitFor(0.1);
  }

  // Highlight Cloud
  yield* hostingNodes[2]().position.y(760, 0.2);
  yield* hostingNodes[2]().position.y(780, 0.2);

  yield* waitFor(1.5);

  // Exit
  yield* all(
    camera().zoom(0.7, 0.6, easeInOutCubic),
    titleOpacity(0, 0.4),
    serverOpacity(0, 0.4),
    userOpacity(0, 0.4),
    arrowProgress(0, 0.4),
    ...hostingOpacities.map((o) => o(0, 0.4))
  );
});
