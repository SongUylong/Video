import {
  makeScene2D,
  Circle,
  Grid,
  Line,
  Node,
  Rect,
  Txt,
} from "@motion-canvas/2d";
import {
  Vector2,
  all,
  createRef,
  createSignal,
  waitFor,
  easeOutCubic,
  easeInOutCubic,
} from "@motion-canvas/core";

const CYAN = "#00d4ff";
const GREEN = "#00ff88";
const ORANGE = "#ff6600";
const WHITE = "#ffffff";
const DARK = "#0a0a1a";

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const titleOpacity = createSignal(0);
  const contentScale = createSignal(1);
  const title = createRef<Txt>();

  const computerScale = createSignal(0);
  const serverScale = createSignal(0);
  const lineOpacity = createSignal(0);

  // Packets - start near device
  const deviceX = -400;
  const serverX = 400;
  const yBase = 100;

  const p0x = createSignal(deviceX + 100);
  const p0y = createSignal(yBase - 150);
  const p0op = createSignal(0);
  const p1x = createSignal(deviceX + 100);
  const p1y = createSignal(yBase - 150);
  const p1op = createSignal(0);
  const p2x = createSignal(deviceX + 100);
  const p2y = createSignal(yBase - 150);
  const p2op = createSignal(0);
  const p3x = createSignal(deviceX + 100);
  const p3y = createSignal(yBase - 150);
  const p3op = createSignal(0);

  const stepText = createRef<Txt>();

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
          text={"DATA PACKETS"}
          fontSize={80}
          fontWeight={800}
          fill={WHITE}
          y={-700}
          opacity={() => titleOpacity()}
          textAlign={"center"}
        />

        {/* Computer (Device) */}
        <Node x={deviceX} y={yBase}>
          <Rect
            width={() => computerScale() * 180}
            height={() => computerScale() * 140}
            fill={"#1a1a3a"}
            stroke={GREEN}
            lineWidth={5}
            radius={15}
          />
          <Txt
            text={"DEVICE"}
            fontSize={28}
            fontWeight={700}
            fill={GREEN}
            y={110}
            opacity={() => computerScale()}
            textAlign={"center"}
          />
        </Node>

        {/* Server */}
        <Node x={serverX} y={yBase}>
          <Rect
            width={() => serverScale() * 140}
            height={() => serverScale() * 180}
            fill={"#1a1a3a"}
            stroke={ORANGE}
            lineWidth={5}
            radius={15}
          />
          <Txt
            text={"SERVER"}
            fontSize={28}
            fontWeight={700}
            fill={ORANGE}
            y={120}
            opacity={() => serverScale()}
            textAlign={"center"}
          />
        </Node>

        {/* Connection line */}
        <Line
          stroke={"#444466"}
          lineWidth={5}
          lineDash={[15, 8]}
          opacity={() => lineOpacity()}
          points={[
            new Vector2(deviceX + 90, yBase),
            new Vector2(serverX - 70, yBase),
          ]}
        />

        {/* Packets */}
        <Node x={() => p0x()} y={() => p0y()}>
          <Rect
            width={70}
            height={70}
            fill={CYAN}
            radius={12}
            opacity={() => p0op()}
            shadowColor={CYAN}
            shadowBlur={20}
          />
          <Txt
            text={"1"}
            fontSize={32}
            fontWeight={900}
            fill={"#000"}
            opacity={() => p0op()}
          />
        </Node>
        <Node x={() => p1x()} y={() => p1y()}>
          <Rect
            width={70}
            height={70}
            fill={CYAN}
            radius={12}
            opacity={() => p1op()}
            shadowColor={CYAN}
            shadowBlur={20}
          />
          <Txt
            text={"2"}
            fontSize={32}
            fontWeight={900}
            fill={"#000"}
            opacity={() => p1op()}
          />
        </Node>
        <Node x={() => p2x()} y={() => p2y()}>
          <Rect
            width={70}
            height={70}
            fill={CYAN}
            radius={12}
            opacity={() => p2op()}
            shadowColor={CYAN}
            shadowBlur={20}
          />
          <Txt
            text={"3"}
            fontSize={32}
            fontWeight={900}
            fill={"#000"}
            opacity={() => p2op()}
          />
        </Node>
        <Node x={() => p3x()} y={() => p3y()}>
          <Rect
            width={70}
            height={70}
            fill={CYAN}
            radius={12}
            opacity={() => p3op()}
            shadowColor={CYAN}
            shadowBlur={20}
          />
          <Txt
            text={"4"}
            fontSize={32}
            fontWeight={900}
            fill={"#000"}
            opacity={() => p3op()}
          />
        </Node>

        {/* Step text */}
        <Txt
          ref={stepText}
          text={""}
          fontSize={40}
          fontWeight={600}
          fill={"#88ccff"}
          y={500}
          opacity={0}
          textAlign={"center"}
        />
      </Node>
    </>
  );

  // Animation
  yield* titleOpacity(1, 0.6);
  yield* all(
    computerScale(1, 0.6, easeOutCubic),
    serverScale(1, 0.6, easeOutCubic)
  );
  yield* lineOpacity(0.6, 0.5);

  yield* waitFor(0.5);

  // Step 1: Packets appear
  stepText().text("Step 1: Data splits into packets");
  yield* stepText().opacity(1, 0.4);

  // Packets appear staggered with longer delays
  yield* p0op(1, 0.3);
  yield* waitFor(0.2);
  yield* p1op(1, 0.3);
  yield* waitFor(0.2);
  yield* p2op(1, 0.3);
  yield* waitFor(0.2);
  yield* p3op(1, 0.3);

  yield* waitFor(1.0);

  // Step 2: Travel to server in different paths
  yield* stepText().text("Step 2: Packets travel different paths", 0.3);

  yield* waitFor(0.5);

  // First wave - spread out (slower)
  yield* all(
    p0x(0, 0.8, easeInOutCubic),
    p0y(yBase - 100, 0.8, easeInOutCubic),
    p1x(50, 0.8, easeInOutCubic),
    p1y(yBase + 150, 0.8, easeInOutCubic),
    p2x(-50, 0.8, easeInOutCubic),
    p2y(yBase + 200, 0.8, easeInOutCubic),
    p3x(100, 0.8, easeInOutCubic),
    p3y(yBase - 50, 0.8, easeInOutCubic)
  );

  yield* waitFor(0.4);

  // Second wave - arrive at server (slower)
  yield* all(
    p0x(serverX - 70, 1.0, easeInOutCubic),
    p0y(yBase - 60, 1.0, easeInOutCubic),
    p1x(serverX - 70, 1.0, easeInOutCubic),
    p1y(yBase - 20, 1.0, easeInOutCubic),
    p2x(serverX - 70, 1.0, easeInOutCubic),
    p2y(yBase + 20, 1.0, easeInOutCubic),
    p3x(serverX - 70, 1.0, easeInOutCubic),
    p3y(yBase + 60, 1.0, easeInOutCubic)
  );

  yield* waitFor(0.5);

  // Step 3: Stack at server
  yield* stepText().text("Step 3: Reassembled at destination", 0.3);

  yield* waitFor(0.4);

  yield* all(
    p0y(yBase, 0.5, easeOutCubic),
    p1y(yBase, 0.5, easeOutCubic),
    p2y(yBase, 0.5, easeOutCubic),
    p3y(yBase, 0.5, easeOutCubic)
  );

  yield* waitFor(1.2);

  // Exit
  yield* all(
    contentScale(0.5, 0.5),
    titleOpacity(0, 0.4),
    computerScale(0, 0.4),
    serverScale(0, 0.4),
    lineOpacity(0, 0.4),
    stepText().opacity(0, 0.4),
    p0op(0, 0.4),
    p1op(0, 0.4),
    p2op(0, 0.4),
    p3op(0, 0.4)
  );
});
