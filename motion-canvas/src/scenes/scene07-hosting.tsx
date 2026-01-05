import {
  makeScene2D,
  Grid,
  Line,
  Node,
  Rect,
  Txt,
  Img,
  Circle,
  Code,
  CODE,
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
const YELLOW = "#ffd93d";
const PURPLE = "#a29bfe";
const WHITE = "#ffffff";
const DARK = "#0a0a1a";

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const title = createRef<Txt>();
  const titleOpacity = createSignal(0);
  const subtitle = createRef<Txt>();

  // Main box that morphs
  const mainBox = createRef<Node>();
  const mainBoxOpacity = createSignal(0);
  const mainBoxWidth = createSignal(500);
  const mainBoxHeight = createSignal(300);
  const mainBoxY = createSignal(0);
  const mainBoxStroke = createSignal(YELLOW);

  // Code content
  const codeContent = createRef<Node>();
  const codeContentOpacity = createSignal(1);
  const htmlIconOpacity = createSignal(0);
  const cssIconOpacity = createSignal(0);
  const jsIconOpacity = createSignal(0);

  // VPS content
  const vpsContent = createRef<Node>();
  const vpsContentOpacity = createSignal(0);

  // Terminal code
  const terminalCode = createRef<Code>();

  // PaaS content
  const paasContent = createRef<Node>();
  const paasContentOpacity = createSignal(0);

  // Deploy button
  const deployBtnOpacity = createSignal(0);
  const deployBtnScale = createSignal(1);
  const liveOpacity = createSignal(0);
  const livePulse = createSignal(1);
  
  // Features text
  const featuresText = createRef<Txt>();

  // Platform logos
  const logosNode = createRef<Node>();
  const logosOpacity = createSignal(0);

  // Summary content
  const summaryContent = createRef<Node>();
  const summaryContentOpacity = createSignal(0);

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
        text={"WHERE TO HOST?"}
        fontSize={80}
        fontWeight={800}
        fill={WHITE}
        y={-750}
        opacity={() => titleOpacity()}
        shadowColor={CYAN}
        shadowBlur={25}
      />

      {/* Subtitle */}
      <Txt
        ref={subtitle}
        text={"Your website needs a home"}
        fontSize={36}
        fontWeight={500}
        fill={"#88aaff"}
        y={-670}
        opacity={() => titleOpacity()}
      />

      {/* Main Morphing Box */}
      <Node ref={mainBox} y={() => mainBoxY()} opacity={() => mainBoxOpacity()}>
        <Rect
          width={() => mainBoxWidth()}
          height={() => mainBoxHeight()}
          fill={"#0d1a2a"}
          stroke={() => mainBoxStroke()}
          lineWidth={6}
          radius={30}
          shadowColor={() => mainBoxStroke()}
          shadowBlur={30}
        />

        {/* Code Content (initial state) */}
        <Node ref={codeContent} opacity={() => codeContentOpacity()}>
          <Txt
            text={"Your Code"}
            fontSize={48}
            fontWeight={700}
            fill={YELLOW}
            y={-80}
          />
          
          {/* Code Icons Row */}
          <Node y={20}>
            {/* HTML Icon */}
            <Img
              src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg"}
              width={70}
              height={70}
              x={-100}
              opacity={() => htmlIconOpacity()}
            />
            <Txt
              text={"HTML"}
              fontSize={24}
              fontWeight={700}
              fill={"#e44d26"}
              x={-100}
              y={55}
              opacity={() => htmlIconOpacity()}
            />
            
            {/* CSS Icon */}
            <Img
              src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg"}
              width={70}
              height={70}
              x={0}
              opacity={() => cssIconOpacity()}
            />
            <Txt
              text={"CSS"}
              fontSize={24}
              fontWeight={700}
              fill={"#264de4"}
              x={0}
              y={55}
              opacity={() => cssIconOpacity()}
            />
            
            {/* JavaScript Icon */}
            <Img
              src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg"}
              width={70}
              height={70}
              x={100}
              opacity={() => jsIconOpacity()}
            />
            <Txt
              text={"JS"}
              fontSize={24}
              fontWeight={700}
              fill={"#f7df1e"}
              x={100}
              y={55}
              opacity={() => jsIconOpacity()}
            />
          </Node>
        </Node>

        {/* VPS Content */}
        <Node ref={vpsContent} opacity={() => vpsContentOpacity()}>
          <Img
            src={"/asset/cloud-server.png"}
            width={120}
            height={120}
            y={-220}
          />
          <Txt
            text={"VPS"}
            fontSize={60}
            fontWeight={800}
            fill={GREEN}
            y={-110}
          />
          <Txt
            text={"Virtual Private Server"}
            fontSize={28}
            fontWeight={500}
            fill={WHITE}
            y={-65}
          />
          
          {/* Terminal */}
          <Node y={80}>
            <Rect
              width={700}
              height={240}
              fill={"#0a0a0a"}
              stroke={"#333"}
              lineWidth={4}
              radius={15}
            />
            <Code
              ref={terminalCode}
              fontSize={24}
              fontFamily={"monospace"}
              fontWeight={600}
              offsetX={-1}
              x={-330}
              y={-40}
              code={''}
            />
          </Node>
        </Node>

        {/* PaaS Content */}
        <Node ref={paasContent} opacity={() => paasContentOpacity()}>
          <Txt
            text={"PaaS"}
            fontSize={70}
            fontWeight={800}
            fill={CYAN}
            y={-200}
          />
          <Txt
            text={"Platform as a Service"}
            fontSize={32}
            fontWeight={500}
            fill={WHITE}
            y={-140}
          />

          {/* Deploy Button */}
          <Node y={-30} scale={() => deployBtnScale()} opacity={() => deployBtnOpacity()}>
            <Rect
              width={350}
              height={100}
              fill={CYAN}
              radius={50}
              shadowColor={CYAN}
              shadowBlur={40}
            />
            <Txt
              text={"🚀 DEPLOY"}
              fontSize={44}
              fontWeight={900}
              fill={DARK}
            />
          </Node>

          {/* Live indicator */}
          <Node y={100} opacity={() => liveOpacity()} scale={() => livePulse()}>
            <Rect
              width={250}
              height={80}
              fill={GREEN}
              radius={40}
              shadowColor={GREEN}
              shadowBlur={30}
            />
            <Circle
              width={20}
              height={20}
              fill={WHITE}
              x={-80}
            />
            <Txt
              text={"LIVE"}
              fontSize={40}
              fontWeight={900}
              fill={DARK}
              x={15}
            />
          </Node>

          {/* Features */}
          <Txt
            ref={featuresText}
            text={""}
            fontSize={28}
            fontWeight={600}
            fill={WHITE}
            y={220}
          />
        </Node>

        {/* Summary Content */}
        <Node ref={summaryContent} opacity={() => summaryContentOpacity()}>
          {/* VPS Side */}
          <Node x={-220}>
            <Img
              src={"/asset/cloud-server.png"}
              width={100}
              height={100}
              y={-120}
            />
            <Txt
              text={"VPS"}
              fontSize={50}
              fontWeight={800}
              fill={GREEN}
              y={-20}
            />
            <Txt
              text={"Full Control"}
              fontSize={28}
              fontWeight={600}
              fill={WHITE}
              y={30}
            />
            <Txt
              text={"More Setup"}
              fontSize={28}
              fontWeight={600}
              fill={WHITE}
              y={70}
            />
            <Txt
              text={"$5-50/mo"}
              fontSize={32}
              fontWeight={700}
              fill={YELLOW}
              y={120}
            />
          </Node>

          {/* Divider */}
          <Line
            stroke={"#444"}
            lineWidth={4}
            points={[new Vector2(0, -180), new Vector2(0, 180)]}
          />

          {/* PaaS Side */}
          <Node x={220}>
            <Node y={-120}>
              <Img src={"/asset/vercel-icon.svg"} width={50} height={50} x={-60} />
              <Img src={"/asset/netlify.png"} width={50} height={50} x={0} />
              <Img src={"/asset/heroku.png"} width={50} height={50} x={60} />
            </Node>
            <Txt
              text={"PaaS"}
              fontSize={50}
              fontWeight={800}
              fill={CYAN}
              y={-20}
            />
            <Txt
              text={"1-Click Deploy"}
              fontSize={28}
              fontWeight={600}
              fill={WHITE}
              y={30}
            />
            <Txt
              text={"Less Control"}
              fontSize={28}
              fontWeight={600}
              fill={WHITE}
              y={70}
            />
            <Txt
              text={"Free - $$$"}
              fontSize={32}
              fontWeight={700}
              fill={YELLOW}
              y={120}
            />
          </Node>
        </Node>
      </Node>

      {/* Platform Logos (separate for animation) */}
      <Node ref={logosNode} y={550} opacity={() => logosOpacity()}>
        <Node x={-200}>
          <Rect
            width={160}
            height={130}
            fill={"#1a1a2e"}
            stroke={WHITE}
            lineWidth={4}
            radius={20}
            shadowColor={WHITE}
            shadowBlur={15}
          />
          <Img src={"/asset/vercel-icon.svg"} width={60} height={60} y={-15} />
          <Txt text={"Vercel"} fontSize={24} fontWeight={700} fill={WHITE} y={45} />
        </Node>

        <Node x={0}>
          <Rect
            width={160}
            height={130}
            fill={"#1a1a2e"}
            stroke={CYAN}
            lineWidth={4}
            radius={20}
            shadowColor={CYAN}
            shadowBlur={15}
          />
          <Img src={"/asset/netlify.png"} width={60} height={60} y={-15} />
          <Txt text={"Netlify"} fontSize={24} fontWeight={700} fill={CYAN} y={45} />
        </Node>

        <Node x={200}>
          <Rect
            width={160}
            height={130}
            fill={"#1a1a2e"}
            stroke={PURPLE}
            lineWidth={4}
            radius={20}
            shadowColor={PURPLE}
            shadowBlur={15}
          />
          <Img src={"/asset/heroku.png"} width={60} height={60} y={-15} />
          <Txt text={"Heroku"} fontSize={24} fontWeight={700} fill={PURPLE} y={45} />
        </Node>
      </Node>
    </>
  );

  // ===== ANIMATION =====

  // 1. Title and Code box appear
  yield* titleOpacity(1, 0.5);
  yield* waitFor(0.3);
  yield* mainBoxOpacity(1, 0.6, easeOutCubic);
  yield* waitFor(0.5);
  
  // Show code icons in sequence
  yield* htmlIconOpacity(1, 0.4, easeOutCubic);
  yield* waitFor(0.3);
  
  yield* cssIconOpacity(1, 0.4, easeOutCubic);
  yield* waitFor(0.3);
  
  yield* jsIconOpacity(1, 0.4, easeOutCubic);
  yield* waitFor(1.0);

  // 2. Morph to VPS
  yield* all(
    title().text("OPTION 1: VPS", 0.5),
    subtitle().text("Virtual Private Server", 0.5),
    codeContentOpacity(0, 0.4),
    mainBoxWidth(800, 0.8, easeInOutCubic),
    mainBoxHeight(550, 0.8, easeInOutCubic),
    mainBoxY(100, 0.8, easeInOutCubic),
    mainBoxStroke(GREEN, 0.5)
  );

  yield* vpsContentOpacity(1, 0.5, easeOutCubic);
  yield* waitFor(0.3);

  // Type terminal commands
  yield* terminalCode().code(`$ ssh root@server`, 0.6);
  yield* waitFor(0.2);
  yield* terminalCode().code(`$ ssh root@server
$ apt install nginx nodejs`, 0.6);
  yield* waitFor(0.2);
  yield* terminalCode().code(`$ ssh root@server
$ apt install nginx nodejs
$ npm run build && pm2 start`, 0.6);
  yield* waitFor(1.2);

  // 3. Morph to PaaS
  yield* all(
    title().text("OPTION 2: PaaS", 0.5),
    subtitle().text("Platform as a Service", 0.5),
    vpsContentOpacity(0, 0.4),
    mainBoxHeight(500, 0.8, easeInOutCubic),
    mainBoxY(50, 0.8, easeInOutCubic),
    mainBoxStroke(CYAN, 0.5)
  );

  yield* paasContentOpacity(1, 0.5, easeOutCubic);
  yield* waitFor(0.3);

  // Show deploy button first
  yield* deployBtnOpacity(1, 0.4, easeOutCubic);
  yield* waitFor(0.3);

  // Click deploy button
  yield* deployBtnScale(0.9, 0.1);
  yield* deployBtnScale(1.15, 0.2, easeOutBounce);
  yield* deployBtnScale(1, 0.15);

  yield* waitFor(0.3);

  // Show LIVE
  yield* liveOpacity(1, 0.4, easeOutCubic);
  
  // Pulse live indicator
  yield* livePulse(1.2, 0.25);
  yield* livePulse(1, 0.25);
  yield* livePulse(1.2, 0.25);
  yield* livePulse(1, 0.25);

  yield* waitFor(0.3);

  // Show features with typing effect
  yield* featuresText().text("✓ Auto-scaling  ✓ CI/CD  ✓ Free tier", 1.2);
  yield* waitFor(0.5);

  // Show platform logos
  yield* logosOpacity(1, 0.5, easeOutCubic);
  yield* waitFor(1.5);

  // 4. Morph to Summary
  yield* all(
    title().text("WHICH TO CHOOSE?", 0.5),
    subtitle().text("Compare your options", 0.5),
    paasContentOpacity(0, 0.4),
    logosOpacity(0, 0.4),
    mainBoxWidth(900, 0.8, easeInOutCubic),
    mainBoxHeight(450, 0.8, easeInOutCubic),
    mainBoxY(100, 0.8, easeInOutCubic),
    mainBoxStroke(WHITE, 0.5)
  );

  yield* summaryContentOpacity(1, 0.5, easeOutCubic);
  yield* waitFor(3.0);

  // Exit
  yield* all(
    titleOpacity(0, 0.5),
    mainBoxOpacity(0, 0.5)
  );
});
