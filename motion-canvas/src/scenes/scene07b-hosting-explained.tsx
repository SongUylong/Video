import {
  makeScene2D,
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
  easeInCubic,
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

  const titleOpacity = createSignal(0);
  const title = createRef<Txt>();
  const subtitle = createRef<Txt>();

  // Service cards
  const vpsNode = createRef<Node>();
  const vercelNode = createRef<Node>();
  const netlifyNode = createRef<Node>();
  const herokuNode = createRef<Node>();

  const vpsOpacity = createSignal(1); // Start visible for transition
  const vercelOpacity = createSignal(1); // Start visible
  const netlifyOpacity = createSignal(1); // Start visible
  const herokuOpacity = createSignal(1); // Start visible

  // Box dimensions - start small like previous scene
  const vpsWidth = createSignal(200);
  const vpsHeight = createSignal(140);
  const paasWidth = createSignal(200);
  const paasHeight = createSignal(140);

  // Feature lists
  const vpsFeatures = createRef<Node>();
  const paasFeatures = createRef<Node>();
  const vpsFeatureOpacity = createSignal(0);
  const paasFeatureOpacity = createSignal(0);

  // Comparison
  const comparisonNode = createRef<Node>();
  const comparisonOpacity = createSignal(0);

  // PaaS title
  const paasTitleOpacity = createSignal(0);

  view.add(
    <>
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
        text={"HOSTING SERVICES"}
        fontSize={80}
        fontWeight={800}
        fill={WHITE}
        y={-800}
        opacity={() => titleOpacity()}
        shadowColor={CYAN}
        shadowBlur={25}
      />

      {/* Subtitle */}
      <Txt
        ref={subtitle}
        text={"Understanding Your Options"}
        fontSize={38}
        fontWeight={500}
        fill={"#88aaff"}
        y={-720}
        opacity={() => titleOpacity()}
      />

      {/* VPS Section */}
      <Node ref={vpsNode} x={-350} y={780}>
        <Rect
          width={() => vpsWidth()}
          height={() => vpsHeight()}
          fill={"#0d1a2a"}
          stroke={GREEN}
          lineWidth={5}
          radius={20}
          shadowColor={GREEN}
          shadowBlur={20}
          opacity={() => vpsOpacity()}
        />
        <Img
          src={"/asset/cloud-server.png"}
          width={60}
          height={60}
          y={-25}
          opacity={() => vpsOpacity()}
        />
        <Txt
          text={"VPS"}
          fontSize={28}
          fontWeight={800}
          fill={GREEN}
          y={40}
          opacity={() => vpsOpacity()}
        />
        
        {/* VPS Features */}
        <Node ref={vpsFeatures} x={50} opacity={() => vpsFeatureOpacity()}>
          <Txt
            text={"• Full server control"}
            fontSize={30}
            fontWeight={600}
            fill={WHITE}
            x={0}
            y={-60}
            textAlign={"left"}
          />
          <Txt
            text={"• Manual configuration"}
            fontSize={30}
            fontWeight={600}
            fill={WHITE}
            x={0}
            y={-10}
            textAlign={"left"}
          />
          <Txt
            text={"• More technical"}
            fontSize={30}
            fontWeight={600}
            fill={WHITE}
            x={0}
            y={40}
            textAlign={"left"}
          />
        </Node>
      </Node>

      {/* PaaS Services Container */}
      <Txt
        text={"PLATFORM AS A SERVICE (PaaS)"}
        fontSize={45}
        fontWeight={700}
        fill={CYAN}
        y={-80}
        opacity={() => paasTitleOpacity()}
        shadowColor={CYAN}
        shadowBlur={15}
      />

      {/* Vercel */}
      <Node ref={vercelNode} x={-90} y={780}>
        <Rect
          width={() => paasWidth()}
          height={() => paasHeight()}
          fill={"#1a1a2e"}
          stroke={WHITE}
          lineWidth={4}
          radius={18}
          shadowColor={WHITE}
          shadowBlur={15}
          opacity={() => vercelOpacity()}
        />
        <Img
          src={"/asset/vercel-icon.svg"}
          width={60}
          height={60}
          y={-25}
          opacity={() => vercelOpacity()}
        />
        <Txt
          text={"Vercel"}
          fontSize={28}
          fontWeight={700}
          fill={WHITE}
          y={40}
          opacity={() => vercelOpacity()}
        />
        <Txt
          text={"Next.js\nOptimized"}
          fontSize={24}
          fontWeight={500}
          fill={"#88aaff"}
          y={85}
          opacity={0}
        />
      </Node>

      {/* Netlify */}
      <Node ref={netlifyNode} x={110} y={780}>
        <Rect
          width={() => paasWidth()}
          height={() => paasHeight()}
          fill={"#1a1a2e"}
          stroke={CYAN}
          lineWidth={4}
          radius={18}
          shadowColor={CYAN}
          shadowBlur={15}
          opacity={() => netlifyOpacity()}
        />
        <Img
          src={"/asset/netlify.png"}
          width={60}
          height={60}
          y={-25}
          opacity={() => netlifyOpacity()}
        />
        <Txt
          text={"Netlify"}
          fontSize={28}
          fontWeight={700}
          fill={CYAN}
          y={40}
          opacity={() => netlifyOpacity()}
        />
        <Txt
          text={"JAMstack\nSpecialist"}
          fontSize={24}
          fontWeight={500}
          fill={"#88aaff"}
          y={85}
          opacity={0}
        />
      </Node>

      {/* Heroku */}
      <Node ref={herokuNode} x={310} y={780}>
        <Rect
          width={() => paasWidth()}
          height={() => paasHeight()}
          fill={"#1a1a2e"}
          stroke={PURPLE}
          lineWidth={4}
          radius={18}
          shadowColor={PURPLE}
          shadowBlur={15}
          opacity={() => herokuOpacity()}
        />
        <Img
          src={"/asset/heroku.png"}
          width={60}
          height={60}
          y={-25}
          opacity={() => herokuOpacity()}
        />
        <Txt
          text={"Heroku"}
          fontSize={28}
          fontWeight={700}
          fill={PURPLE}
          y={40}
          opacity={() => herokuOpacity()}
        />
        <Txt
          text={"Full-Stack\nApps"}
          fontSize={24}
          fontWeight={500}
          fill={"#88aaff"}
          y={85}
          opacity={0}
        />
      </Node>

      {/* PaaS Features */}
      <Node ref={paasFeatures} y={450} opacity={() => paasFeatureOpacity()}>
        <Rect
          width={900}
          height={200}
          fill={"#0d1a2a"}
          stroke={CYAN}
          lineWidth={4}
          radius={18}
          shadowColor={CYAN}
          shadowBlur={15}
        />
        <Txt
          text={"PaaS Benefits:"}
          fontSize={38}
          fontWeight={700}
          fill={CYAN}
          y={-60}
        />
        <Txt
          text={"✓ Easy deployment   ✓ Auto-scaling   ✓ Built-in CI/CD"}
          fontSize={28}
          fontWeight={600}
          fill={WHITE}
          y={10}
        />
        <Txt
          text={"✓ Less maintenance   ✓ Focus on code"}
          fontSize={28}
          fontWeight={600}
          fill={WHITE}
          y={55}
        />
      </Node>

      {/* Comparison */}
      <Node ref={comparisonNode} y={700} opacity={() => comparisonOpacity()}>
        <Txt
          text={"Choose based on your needs:"}
          fontSize={32}
          fontWeight={600}
          fill={"#88aaff"}
          y={0}
        />
        <Txt
          text={"VPS = Control & Flexibility"}
          fontSize={28}
          fontWeight={600}
          fill={GREEN}
          y={50}
        />
        <Txt
          text={"PaaS = Speed & Simplicity"}
          fontSize={28}
          fontWeight={600}
          fill={CYAN}
          y={100}
        />
      </Node>
    </>
  );

  // ===== ANIMATION =====

  // Boxes are already visible from previous scene transition
  // Wait a moment for scene to settle
  yield* waitFor(0.3);

  // Title fades in
  yield* titleOpacity(1, 0.6);
  yield* waitFor(0.3);

  // Morph VPS box - expand and move to final position
  yield* all(
    vpsNode().position.y(-450, 0.8, easeInOutCubic),
    vpsNode().position.x(0, 0.8, easeInOutCubic),
    vpsWidth(900, 0.8, easeInOutCubic),
    vpsHeight(280, 0.8, easeInOutCubic)
  );

  yield* waitFor(0.3);

  // VPS features appear
  yield* vpsFeatureOpacity(1, 0.5, easeOutCubic);
  yield* waitFor(0.8);

  // Show PaaS title
  yield* paasTitleOpacity(1, 0.5, easeOutCubic);
  yield* waitFor(0.3);

  // Morph PaaS boxes - expand and move to final positions
  yield* all(
    // Vercel
    vercelNode().position.x(-300, 0.8, easeInOutCubic),
    vercelNode().position.y(120, 0.8, easeInOutCubic),
    // Netlify
    netlifyNode().position.x(0, 0.8, easeInOutCubic),
    netlifyNode().position.y(120, 0.8, easeInOutCubic),
    // Heroku
    herokuNode().position.x(300, 0.8, easeInOutCubic),
    herokuNode().position.y(120, 0.8, easeInOutCubic),
    // Expand all PaaS boxes
    paasWidth(280, 0.8, easeInOutCubic),
    paasHeight(260, 0.8, easeInOutCubic)
  );

  yield* waitFor(0.5);

  // Highlight each PaaS service
  yield* vercelNode().position.y(100, 0.2);
  yield* vercelNode().position.y(120, 0.2);
  yield* waitFor(0.3);

  yield* netlifyNode().position.y(100, 0.2);
  yield* netlifyNode().position.y(120, 0.2);
  yield* waitFor(0.3);

  yield* herokuNode().position.y(100, 0.2);
  yield* herokuNode().position.y(120, 0.2);
  yield* waitFor(0.5);

  // PaaS features appear
  yield* paasFeatureOpacity(1, 0.5, easeOutCubic);
  yield* waitFor(1.0);

  // Comparison appears
  yield* comparisonOpacity(1, 0.5, easeOutCubic);
  yield* waitFor(2.0);

  // Exit
  yield* all(
    titleOpacity(0, 0.5),
    paasTitleOpacity(0, 0.5),
    vpsOpacity(0, 0.5),
    vpsFeatureOpacity(0, 0.5),
    vercelOpacity(0, 0.5),
    netlifyOpacity(0, 0.5),
    herokuOpacity(0, 0.5),
    paasFeatureOpacity(0, 0.5),
    comparisonOpacity(0, 0.5)
  );
});
