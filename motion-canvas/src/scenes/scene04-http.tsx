import {
  makeScene2D,
  Circle,
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
  easeInOutBack,
  loop,
  chain,
} from "@motion-canvas/core";

const CYAN = "#00d4ff";
const GREEN = "#00ff88";
const RED = "#ff6b6b";
const YELLOW = "#ffaa00";
const WHITE = "#ffffff";
const DARK = "#0a0a1a";

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const titleOpacity = createSignal(0);
  const contentScale = createSignal(1);
  const title = createRef<Txt>();

  const browserScale = createSignal(0);
  const serverScale = createSignal(0);
  const browserRotation = createSignal(0);
  const serverRotation = createSignal(0);
  const requestOpacity = createSignal(0);
  const responseOpacity = createSignal(0);
  const requestProgress = createSignal(0);
  const responseProgress = createSignal(0);

  // Data boxes
  const httpBoxOpacity = createSignal(0);
  const httpsBoxOpacity = createSignal(0);
  const httpBoxScale = createSignal(1);
  const httpsBoxScale = createSignal(1);
  const lockScale = createSignal(0);
  const lockRotation = createSignal(0);
  const warningOpacity = createSignal(0);
  const warningScale = createSignal(1);

  const methods = ["GET", "POST", "PUT", "DELETE"];
  const methodColors = [CYAN, GREEN, YELLOW, RED];
  const methodScales = methods.map(() => createSignal(0));
  const methodRotations = methods.map(() => createSignal(0));

  view.add(
    <>
      <Grid
        width={1080}
        height={1920}
        spacing={60}
        stroke={"#1a1a2e"}
        lineWidth={1}
      />

      <Node scale={() => contentScale()}>
        {/* Title */}
        <Txt
          ref={title}
          text={"HTTP PROTOCOL"}
          fontSize={80}
          fontWeight={800}
          fill={WHITE}
          y={-700}
          opacity={() => titleOpacity()}
          textAlign={"center"}
        />

        {/* Browser/Client */}
        <Node x={-300} y={-100} rotation={() => browserRotation()}>
          <Rect
            width={() => browserScale() * 280}
            height={() => browserScale() * 200}
            fill={"#1a1a2e"}
            stroke={"#4a4a6a"}
            lineWidth={4}
            radius={20}
          />
          <Img
            src={"/asset/browser.png"}
            width={() => browserScale() * 100}
            height={() => browserScale() * 100}
          />
          <Txt
            text={"CLIENT"}
            fontSize={32}
            fontWeight={700}
            fill={CYAN}
            y={140}
            opacity={() => browserScale()}
            textAlign={"center"}
          />
        </Node>

        {/* Server */}
        <Node x={300} y={-100} rotation={() => serverRotation()}>
          <Rect
            width={() => serverScale() * 180}
            height={() => serverScale() * 230}
            fill={"#1a1a2e"}
            stroke={GREEN}
            lineWidth={5}
            radius={20}
          />
          <Img
            src={"/asset/cloud-server.png"}
            width={() => serverScale() * 120}
            height={() => serverScale() * 120}
          />
          <Txt
            text={"SERVER"}
            fontSize={32}
            fontWeight={700}
            fill={GREEN}
            y={150}
            opacity={() => serverScale()}
            textAlign={"center"}
          />
        </Node>

        {/* Request arrow */}
        <Line
          stroke={CYAN}
          lineWidth={6}
          endArrow
          arrowSize={20}
          opacity={() => requestOpacity()}
          points={[new Vector2(-150, -170), new Vector2(150, -170)]}
        />
        <Txt
          text={"REQUEST"}
          fontSize={28}
          fontWeight={700}
          fill={CYAN}
          y={-215}
          opacity={() => requestOpacity()}
          textAlign={"center"}
        />

        {/* Response arrow */}
        <Line
          stroke={GREEN}
          lineWidth={6}
          endArrow
          arrowSize={20}
          opacity={() => responseOpacity()}
          points={[new Vector2(150, -30), new Vector2(-150, -30)]}
        />
        <Txt
          text={"RESPONSE"}
          fontSize={28}
          fontWeight={700}
          fill={GREEN}
          y={15}
          opacity={() => responseOpacity()}
          textAlign={"center"}
        />

        {/* HTTP Methods */}
        <Node y={200}>
          {methods.map((method, i) => (
            <Node
              key={`method-${i}`}
              x={-240 + i * 160}
              y={0}
              rotation={() => methodRotations[i]()}
            >
              <Rect
                width={() => methodScales[i]() * 140}
                height={() => methodScales[i]() * 60}
                fill={methodColors[i]}
                radius={12}
                shadowColor={methodColors[i]}
                shadowBlur={20}
              />
              <Txt
                text={method}
                fontSize={28}
                fontWeight={900}
                fill={"#000"}
                opacity={() => methodScales[i]()}
              />
            </Node>
          ))}
        </Node>

        {/* HTTP - Plain Text Box */}
        <Node
          y={380}
          opacity={() => httpBoxOpacity()}
          scale={() => httpBoxScale()}
        >
          <Rect
            width={500}
            height={140}
            fill={"#2a1a1a"}
            stroke={RED}
            lineWidth={4}
            radius={15}
            shadowColor={RED}
            shadowBlur={15}
          />
          <Txt
            text={"HTTP - NOT SECURE"}
            fontSize={28}
            fontWeight={700}
            fill={RED}
            y={-50}
            textAlign={"center"}
          />
          <Txt
            text={"password123"}
            fontSize={32}
            fontWeight={700}
            fontFamily={"monospace"}
            fill={RED}
            y={10}
            textAlign={"center"}
          />
          <Txt
            text={"⚠️ Anyone can read this!"}
            fontSize={22}
            fontWeight={600}
            fill={YELLOW}
            y={55}
            opacity={() => warningOpacity()}
            scale={() => warningScale()}
            textAlign={"center"}
          />
        </Node>

        {/* HTTPS - Encrypted Box */}
        <Node
          y={580}
          opacity={() => httpsBoxOpacity()}
          scale={() => httpsBoxScale()}
        >
          <Rect
            width={500}
            height={180}
            fill={"#1a2a1a"}
            stroke={GREEN}
            lineWidth={4}
            radius={15}
            shadowColor={GREEN}
            shadowBlur={25}
          />

          {/* Lock icon */}
          <Circle
            width={() => lockScale() * 70}
            height={() => lockScale() * 70}
            fill={GREEN}
            y={-70}
            rotation={() => lockRotation()}
            shadowColor={GREEN}
            shadowBlur={30}
          />
          <Txt
            text={"🔒"}
            fontSize={45}
            y={-70}
            opacity={() => lockScale()}
            rotation={() => lockRotation()}
          />

          <Txt
            text={"HTTPS - ENCRYPTED"}
            fontSize={28}
            fontWeight={700}
            fill={GREEN}
            y={-10}
            textAlign={"center"}
          />
          <Txt
            text={"x7$9k#mQ2@pL5"}
            fontSize={32}
            fontWeight={700}
            fontFamily={"monospace"}
            fill={GREEN}
            y={35}
            textAlign={"center"}
            shadowColor={GREEN}
            shadowBlur={15}
          />
          <Txt
            text={"✓ Secure & Private"}
            fontSize={22}
            fontWeight={600}
            fill={CYAN}
            y={75}
            textAlign={"center"}
          />
        </Node>
      </Node>
    </>
  );

  // Animation - Much more dynamic and engaging!
  yield* titleOpacity(1, 0.6);
  yield* waitFor(0.3);

  // Browser and server appear with bounce and slight rotation
  yield* all(
    browserScale(1, 0.7, easeOutBounce),
    serverScale(1, 0.7, easeOutBounce),
    browserRotation(-5, 0.4, easeOutCubic),
    serverRotation(5, 0.4, easeOutCubic)
  );

  // Settle back to 0 rotation
  yield* all(
    browserRotation(0, 0.3, easeInOutCubic),
    serverRotation(0, 0.3, easeInOutCubic)
  );

  yield* waitFor(0.3);

  // Request arrow with animation
  yield* requestOpacity(1, 0.5);

  // Small bounce on browser
  yield* browserScale(1.1, 0.15, easeOutCubic);
  yield* browserScale(1, 0.15, easeOutCubic);

  yield* waitFor(0.2);

  // Response arrow
  yield* responseOpacity(1, 0.5);

  // Small bounce on server
  yield* serverScale(1.1, 0.15, easeOutCubic);
  yield* serverScale(1, 0.15, easeOutCubic);

  yield* waitFor(0.6);

  // Show HTTP Methods with rotation and bounce
  yield* title().text("HTTP METHODS", 0.4);
  yield* waitFor(0.3);

  for (let i = 0; i < methods.length; i++) {
    yield* all(
      methodScales[i](1, 0.3, easeOutBounce),
      methodRotations[i](360, 0.3, easeOutCubic)
    );
    yield* waitFor(0.1);
  }

  // Pulse all methods together
  yield* waitFor(0.3);
  yield* all(...methodScales.map((s) => s(1.15, 0.2, easeOutCubic)));
  yield* all(...methodScales.map((s) => s(1, 0.2, easeOutCubic)));

  yield* waitFor(0.8);

  // Show HTTP plain text - NOT SECURE with dramatic entrance
  yield* title().text("HTTP - NOT ENCRYPTED", 0.4);
  yield* waitFor(0.3);

  // HTTP box appears with shake effect
  yield* httpBoxOpacity(1, 0.4);
  yield* httpBoxScale(1.1, 0.15, easeOutCubic);
  yield* httpBoxScale(0.95, 0.15, easeOutCubic);
  yield* httpBoxScale(1, 0.15, easeOutCubic);

  yield* waitFor(0.6);

  // Warning appears with bounce
  yield* all(warningOpacity(1, 0.3), warningScale(1.3, 0.3, easeOutBounce));

  // Warning pulses dramatically
  for (let i = 0; i < 3; i++) {
    yield* all(warningScale(1.4, 0.2), httpBoxScale(1.05, 0.2));
    yield* all(warningScale(1.3, 0.2), httpBoxScale(1, 0.2));
    yield* waitFor(0.1);
  }

  yield* waitFor(1.2);

  // Dramatic transition to HTTPS
  yield* title().text("HTTPS - ENCRYPTED ✓", 0.5);

  yield* waitFor(0.4);

  // HTTP box shakes violently before disappearing
  for (let i = 0; i < 4; i++) {
    yield* httpBoxScale(1.1, 0.08);
    yield* httpBoxScale(0.9, 0.08);
  }

  yield* waitFor(0.2);

  // HTTP box explodes out
  yield* all(
    httpBoxOpacity(0, 0.4),
    httpBoxScale(1.5, 0.4, easeInOutCubic),
    warningOpacity(0, 0.3)
  );

  yield* waitFor(0.3);

  // HTTPS box enters dramatically from small
  yield* httpsBoxOpacity(0.5, 0);
  yield* httpsBoxScale(0.3, 0);
  yield* all(
    httpsBoxOpacity(1, 0.5, easeOutCubic),
    httpsBoxScale(1, 0.6, easeOutBounce)
  );

  yield* waitFor(0.2);

  // Lock appears with spin and bounce
  yield* lockScale(0.5, 0);
  yield* lockRotation(0, 0);
  yield* all(
    lockScale(1.3, 0.5, easeOutBounce),
    lockRotation(360, 0.5, easeOutCubic)
  );
  yield* lockScale(1, 0.2, easeOutCubic);

  yield* waitFor(0.3);

  // Lock pulses with rotation
  for (let i = 0; i < 3; i++) {
    yield* all(lockScale(1.3, 0.25), lockRotation(lockRotation() + 15, 0.25));
    yield* all(lockScale(1, 0.25), lockRotation(lockRotation() - 15, 0.25));
    yield* waitFor(0.1);
  }

  yield* waitFor(0.3);

  // Final dramatic lock emphasis - multiple spins
  yield* all(
    lockScale(1.4, 0.4, easeOutCubic),
    lockRotation(lockRotation() + 720, 0.8, easeInOutCubic),
    httpsBoxScale(1.1, 0.4, easeOutCubic)
  );
  yield* all(
    lockScale(1, 0.3, easeOutCubic),
    httpsBoxScale(1, 0.3, easeOutCubic)
  );

  yield* waitFor(0.4);

  // Browser and server celebrate with rotation
  yield* all(
    browserRotation(360, 0.6, easeInOutCubic),
    serverRotation(-360, 0.6, easeInOutCubic),
    browserScale(1.15, 0.3, easeOutCubic),
    serverScale(1.15, 0.3, easeOutCubic)
  );
  yield* all(
    browserScale(1, 0.3, easeOutCubic),
    serverScale(1, 0.3, easeOutCubic)
  );

  yield* waitFor(1.0);

  // Exit with spin
  yield* all(
    contentScale(0.5, 0.6),
    titleOpacity(0, 0.5),
    browserScale(0, 0.5),
    serverScale(0, 0.5),
    browserRotation(180, 0.5, easeInOutCubic),
    serverRotation(-180, 0.5, easeInOutCubic),
    requestOpacity(0, 0.4),
    responseOpacity(0, 0.4),
    httpBoxOpacity(0, 0.4),
    httpsBoxOpacity(0, 0.5),
    lockScale(0, 0.5),
    warningOpacity(0, 0.4),
    ...methodScales.map((s) => s(0, 0.5)),
    ...methodRotations.map((r) => r(180, 0.5))
  );
});
