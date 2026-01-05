import {makeScene2D, Circle, Grid, Line, Node, Rect, Txt, Img} from '@motion-canvas/2d';
import {Vector2, all, createRef, createSignal, waitFor, easeOutCubic, easeInOutCubic, easeOutBounce} from '@motion-canvas/core';

const CYAN = '#00d4ff';
const GREEN = '#00ff88';
const YELLOW = '#ffd93d';
const WHITE = '#ffffff';
const DARK = '#0a0a1a';
const ORANGE = '#e44d26';
const BLUE = '#264de4';

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const title = createRef<Txt>();
  const titleOpacity = createSignal(0);
  const subtitle = createRef<Txt>();

  // Server
  const serverOpacity = createSignal(0);
  const serverY = createSignal(-400);
  const serverPulse = createSignal(1);

  // Browser
  const browserOpacity = createSignal(0);
  const browserY = createSignal(400);
  const browserScale = createSignal(1);

  // File icons traveling
  const htmlIcon = createRef<Node>();
  const htmlY = createSignal(-200);
  const htmlOpacity = createSignal(0);
  const htmlScale = createSignal(1);

  const cssIcon = createRef<Node>();
  const cssY = createSignal(-200);
  const cssOpacity = createSignal(0);
  const cssScale = createSignal(1);

  const jsIcon = createRef<Node>();
  const jsY = createSignal(-200);
  const jsOpacity = createSignal(0);
  const jsScale = createSignal(1);

  // Connection line
  const lineProgress = createSignal(0);

  // Browser content states
  const loadingOpacity = createSignal(0);
  const loadingRotation = createSignal(0);
  const receivedFilesOpacity = createSignal(0);
  const renderedSiteOpacity = createSignal(0);

  // Rendered site elements
  const headerWidth = createSignal(0);
  const contentBox1Scale = createSignal(0);
  const contentBox2Scale = createSignal(0);
  const buttonScale = createSignal(0);
  const buttonPulse = createSignal(1);

  view.add(
    <>
      <Grid
        width={1080}
        height={1920}
        spacing={60}
        stroke={'#1a1a2e'}
        lineWidth={1}
      />

      {/* Title */}
      <Txt
        ref={title}
        text={'HOW BROWSERS WORK'}
        fontSize={70}
        fontWeight={800}
        fill={WHITE}
        y={-820}
        opacity={() => titleOpacity()}
        shadowColor={CYAN}
        shadowBlur={25}
      />

      <Txt
        ref={subtitle}
        text={'From server to screen'}
        fontSize={32}
        fontWeight={500}
        fill={'#88aaff'}
        y={-750}
        opacity={() => titleOpacity()}
      />

      {/* Connection line */}
      <Line
        stroke={CYAN}
        lineWidth={4}
        lineDash={[20, 10]}
        opacity={0.5}
        points={() => [
          new Vector2(0, -250),
          new Vector2(0, -250 + lineProgress() * 500),
        ]}
      />

      {/* Server */}
      <Node y={() => serverY()} opacity={() => serverOpacity()} scale={() => serverPulse()}>
        <Rect
          width={320}
          height={200}
          fill={'#0d1a2a'}
          stroke={GREEN}
          lineWidth={5}
          radius={20}
          shadowColor={GREEN}
          shadowBlur={40}
        />
        <Img
          src={"/asset/cloud-server.png"}
          width={80}
          height={80}
          y={-10}
        />
        <Txt
          text={'SERVER'}
          fontSize={28}
          fontWeight={800}
          fill={GREEN}
          y={60}
        />

        {/* Server files indicators - actual icons */}
        <Img
          src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg"}
          width={35}
          height={35}
          x={-100}
          y={-85}
        />
        <Img
          src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg"}
          width={35}
          height={35}
          x={0}
          y={-85}
        />
        <Img
          src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg"}
          width={35}
          height={35}
          x={100}
          y={-85}
        />
      </Node>

      {/* HTML Icon traveling */}
      <Node ref={htmlIcon} y={() => htmlY()} x={-100} opacity={() => htmlOpacity()} scale={() => htmlScale()}>
        <Circle
          width={90}
          height={90}
          fill={'#0d1a2a'}
          stroke={ORANGE}
          lineWidth={4}
          shadowColor={ORANGE}
          shadowBlur={20}
        />
        <Img
          src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg"}
          width={50}
          height={50}
        />
      </Node>

      {/* CSS Icon traveling */}
      <Node ref={cssIcon} y={() => cssY()} x={0} opacity={() => cssOpacity()} scale={() => cssScale()}>
        <Circle
          width={90}
          height={90}
          fill={'#0d1a2a'}
          stroke={BLUE}
          lineWidth={4}
          shadowColor={BLUE}
          shadowBlur={20}
        />
        <Img
          src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg"}
          width={50}
          height={50}
        />
      </Node>

      {/* JS Icon traveling */}
      <Node ref={jsIcon} y={() => jsY()} x={100} opacity={() => jsOpacity()} scale={() => jsScale()}>
        <Circle
          width={90}
          height={90}
          fill={'#0d1a2a'}
          stroke={YELLOW}
          lineWidth={4}
          shadowColor={YELLOW}
          shadowBlur={20}
        />
        <Img
          src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg"}
          width={50}
          height={50}
        />
      </Node>

      {/* Browser */}
      <Node y={() => browserY()} opacity={() => browserOpacity()} scale={() => browserScale()}>
        <Rect
          width={480}
          height={650}
          fill={'#1a1a2e'}
          stroke={CYAN}
          lineWidth={5}
          radius={25}
          shadowColor={CYAN}
          shadowBlur={40}
        />

        {/* Browser top bar */}
        <Rect
          width={480}
          height={60}
          fill={'#2a2a4a'}
          radius={[25, 25, 0, 0]}
          y={-295}
        />

        {/* Browser buttons */}
        <Circle width={16} height={16} fill={'#ff5f57'} x={-200} y={-295} />
        <Circle width={16} height={16} fill={'#ffbd2e'} x={-170} y={-295} />
        <Circle width={16} height={16} fill={'#28c940'} x={-140} y={-295} />

        {/* URL bar */}
        <Rect
          width={280}
          height={32}
          fill={WHITE}
          radius={16}
          x={50}
          y={-295}
        />
        <Txt
          text={'example.com'}
          fontSize={16}
          fontWeight={600}
          fill={'#333'}
          x={50}
          y={-295}
        />

        {/* Browser label */}
        <Img
          src={"/asset/browser.png"}
          width={50}
          height={50}
          y={-220}
        />
        <Txt
          text={'BROWSER'}
          fontSize={24}
          fontWeight={800}
          fill={CYAN}
          y={-175}
        />

        {/* Content area */}
        <Rect
          width={440}
          height={380}
          fill={'#ffffff'}
          radius={15}
          y={95}
        />

        {/* Loading spinner */}
        <Node y={95} opacity={() => loadingOpacity()}>
          <Circle
            width={80}
            height={80}
            stroke={CYAN}
            lineWidth={6}
            lineDash={[40, 20]}
            rotation={() => loadingRotation()}
          />
          <Txt
            text={'Loading...'}
            fontSize={24}
            fontWeight={700}
            fill={'#666'}
            y={70}
          />
        </Node>

        {/* Received files display */}
        <Node y={95} opacity={() => receivedFilesOpacity()}>
          <Txt
            text={'Files Received!'}
            fontSize={28}
            fontWeight={700}
            fill={GREEN}
            y={-80}
          />
          <Img
            src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg"}
            width={60}
            height={60}
            x={-80}
          />
          <Img
            src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg"}
            width={60}
            height={60}
            x={0}
          />
          <Img
            src={"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg"}
            width={60}
            height={60}
            x={80}
          />
          <Txt
            text={'Rendering...'}
            fontSize={24}
            fontWeight={600}
            fill={'#888'}
            y={80}
          />
        </Node>

        {/* Rendered website */}
        <Node y={95} opacity={() => renderedSiteOpacity()}>
          {/* Header */}
          <Rect
            width={() => headerWidth()}
            height={50}
            fill={CYAN}
            radius={8}
            y={-145}
          />
          <Txt
            text={'My Website'}
            fontSize={20}
            fontWeight={800}
            fill={WHITE}
            y={-145}
            x={-100}
            opacity={() => headerWidth() > 100 ? 1 : 0}
          />

          {/* Hero section */}
          <Node y={-70} scale={() => contentBox1Scale()}>
            <Rect
              width={400}
              height={90}
              fill={'#f5f5f5'}
              radius={8}
            />
            <Txt
              text={'Welcome!'}
              fontSize={28}
              fontWeight={800}
              fill={'#333'}
              y={-15}
            />
            <Txt
              text={'This is my awesome website'}
              fontSize={14}
              fontWeight={500}
              fill={'#666'}
              y={20}
            />
          </Node>

          {/* Content boxes */}
          <Node y={40}>
            <Node x={-105} scale={() => contentBox1Scale()}>
              <Rect
                width={190}
                height={100}
                fill={'#e8e8e8'}
                radius={8}
              />
              <Rect
                width={150}
                height={10}
                fill={'#ccc'}
                radius={5}
                y={-25}
              />
              <Rect
                width={120}
                height={10}
                fill={'#ddd'}
                radius={5}
                y={-5}
              />
              <Rect
                width={140}
                height={10}
                fill={'#ccc'}
                radius={5}
                y={15}
              />
            </Node>
            <Node x={105} scale={() => contentBox2Scale()}>
              <Rect
                width={190}
                height={100}
                fill={'#e0e0e0'}
                radius={8}
              />
              <Rect
                width={150}
                height={10}
                fill={'#ccc'}
                radius={5}
                y={-25}
              />
              <Rect
                width={130}
                height={10}
                fill={'#ddd'}
                radius={5}
                y={-5}
              />
              <Rect
                width={145}
                height={10}
                fill={'#ccc'}
                radius={5}
                y={15}
              />
            </Node>
          </Node>

          {/* CTA Button */}
          <Node y={130} scale={() => buttonScale()}>
            <Rect
              width={180}
              height={50}
              fill={GREEN}
              radius={25}
              shadowColor={GREEN}
              shadowBlur={() => buttonPulse() * 15}
              scale={() => buttonPulse()}
            />
            <Txt
              text={'Click Me!'}
              fontSize={20}
              fontWeight={800}
              fill={DARK}
            />
          </Node>
        </Node>
      </Node>

      {/* Success message */}
      <Txt
        text={'WEBSITE RENDERED!'}
        fontSize={50}
        fontWeight={900}
        fill={GREEN}
        y={820}
        opacity={() => renderedSiteOpacity()}
        shadowColor={GREEN}
        shadowBlur={30}
      />
    </>
  );

  // ===== ANIMATION =====

  // 1. Show title
  yield* titleOpacity(1, 0.5);
  yield* waitFor(0.3);

  // 2. Show server with bounce
  yield* all(
    serverOpacity(1, 0.5, easeOutCubic),
    serverY(-450, 0.6, easeOutBounce)
  );

  // Server pulse
  yield* serverPulse(1.05, 0.2);
  yield* serverPulse(1, 0.2);

  yield* waitFor(0.3);

  // 3. Show browser with bounce
  yield* all(
    browserOpacity(1, 0.5, easeOutCubic),
    browserY(300, 0.6, easeOutBounce)
  );

  yield* waitFor(0.3);

  // 4. Show connection line
  yield* lineProgress(1, 0.8, easeInOutCubic);

  yield* waitFor(0.3);

  // 5. Show loading in browser
  yield* loadingOpacity(1, 0.3);
  
  // Spin loader
  yield* loadingRotation(360, 1.0);

  // 6. Send files - HTML first
  yield* htmlOpacity(1, 0.2);
  yield* htmlScale(1.2, 0.15);
  yield* htmlScale(1, 0.15);
  yield* htmlY(150, 0.8, easeInOutCubic);
  yield* all(
    htmlOpacity(0, 0.2),
    htmlScale(0.5, 0.2)
  );

  // 7. Send CSS
  yield* cssOpacity(1, 0.2);
  yield* cssScale(1.2, 0.15);
  yield* cssScale(1, 0.15);
  yield* cssY(150, 0.7, easeInOutCubic);
  yield* all(
    cssOpacity(0, 0.2),
    cssScale(0.5, 0.2)
  );

  // 8. Send JS
  yield* jsOpacity(1, 0.2);
  yield* jsScale(1.2, 0.15);
  yield* jsScale(1, 0.15);
  yield* jsY(150, 0.7, easeInOutCubic);
  yield* all(
    jsOpacity(0, 0.2),
    jsScale(0.5, 0.2)
  );

  // 9. Hide loading, show received files
  yield* loadingOpacity(0, 0.3);
  yield* receivedFilesOpacity(1, 0.5, easeOutCubic);

  yield* waitFor(1.0);

  // 10. Start rendering
  yield* receivedFilesOpacity(0, 0.3);
  yield* renderedSiteOpacity(1, 0.3);

  // Animate header expanding
  yield* headerWidth(400, 0.6, easeOutCubic);

  // Animate content boxes
  yield* contentBox1Scale(1, 0.4, easeOutBounce);
  yield* waitFor(0.2);
  yield* contentBox2Scale(1, 0.4, easeOutBounce);

  // Animate button
  yield* buttonScale(1, 0.4, easeOutBounce);

  // Button pulse animation
  yield* buttonPulse(1.1, 0.2);
  yield* buttonPulse(1, 0.2);
  yield* buttonPulse(1.1, 0.2);
  yield* buttonPulse(1, 0.2);

  // 11. Celebrate
  yield* all(
    browserScale(1.05, 0.3),
    subtitle().text('Website loaded successfully!', 0.5)
  );
  yield* browserScale(1, 0.2);

  yield* waitFor(2.0);

  // 12. Exit
  yield* all(
    titleOpacity(0, 0.5),
    serverOpacity(0, 0.5),
    browserOpacity(0, 0.5),
    lineProgress(0, 0.5),
    renderedSiteOpacity(0, 0.5)
  );
});
