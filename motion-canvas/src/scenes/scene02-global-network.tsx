import {
  makeScene2D,
  Circle,
  Grid,
  Line,
  Node,
  Txt,
  Img,
} from "@motion-canvas/2d";
import {
  Vector2,
  all,
  createSignal,
  waitFor,
  easeOutCubic,
  easeInOutCubic,
} from "@motion-canvas/core";

const CYAN = "#00d4ff";
const GREEN = "#00ff88";
const WHITE = "#ffffff";
const DARK = "#0a0a1a";

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const titleOpacity = createSignal(0);
  const networkScale = createSignal(0);
  const contentScale = createSignal(1);

  const deviceAngles = [0, 60, 120, 180, 240, 300];
  const deviceScales = deviceAngles.map(() => createSignal(0));
  const lineOpacities = deviceAngles.map(() => createSignal(0));
  const lineColors = deviceAngles.map(() => createSignal(0)); // 0 = cyan, 1 = green

  const distance = 300; // Increased from 180

  view.add(
    <>
      <Grid
        width={1080}
        height={1920}
        spacing={80}
        stroke={"#1a1a2e"}
        lineWidth={1}
      />

      <Node scale={() => contentScale()}>
        {/* Title */}
        <Txt
          text={"GLOBAL NETWORK"}
          fontSize={70}
          fontWeight={700}
          fill={WHITE}
          y={-700}
          opacity={() => titleOpacity()}
          textAlign={"center"}
        />

        {/* Connection lines */}
        {deviceAngles.map((angle, i) => {
          const rad = (angle * Math.PI) / 180;
          const x = Math.cos(rad) * distance;
          const y = Math.sin(rad) * distance;
          return (
            <Line
              key={`line-${i}`}
              stroke={() => {
                const progress = lineColors[i]();
                const r = Math.floor(0 + (0 - 0) * progress);
                const g = Math.floor(212 + (255 - 212) * progress);
                const b = Math.floor(255 + (136 - 255) * progress);
                return `rgb(${r}, ${g}, ${b})`;
              }}
              lineWidth={4}
              opacity={() => lineOpacities[i]()}
              lineDash={[12, 6]}
              points={[Vector2.zero, new Vector2(x, y)]}
            />
          );
        })}

        {/* Center node */}
        <Circle
          width={() => networkScale() * 200}
          height={() => networkScale() * 200}
          fill={"#1a1a3a"}
          stroke={CYAN}
          lineWidth={6}
          shadowColor={CYAN}
          shadowBlur={30}
        />
        <Img
          src={"/asset/networking.png"}
          width={() => networkScale() * 130}
          height={() => networkScale() * 130}
        />

        {/* Device nodes */}
        {deviceAngles.map((angle, i) => {
          const rad = (angle * Math.PI) / 180;
          const x = Math.cos(rad) * distance;
          const y = Math.sin(rad) * distance;
          return (
            <Node key={`device-${i}`} x={x} y={y}>
              <Circle
                width={() => deviceScales[i]() * 100}
                height={() => deviceScales[i]() * 100}
                fill={"#1a1a3a"}
                stroke={GREEN}
                lineWidth={5}
                shadowColor={GREEN}
                shadowBlur={15}
              />
              <Img
                src={"/asset/wifi.png"}
                width={() => deviceScales[i]() * 60}
                height={() => deviceScales[i]() * 60}
              />
            </Node>
          );
        })}

        {/* Subtitle */}
        <Txt
          text={"Billions of connected devices"}
          fontSize={40}
          fontWeight={500}
          fill={"#88ccff"}
          y={700}
          opacity={() => titleOpacity()}
          textAlign={"center"}
        />
      </Node>
    </>
  );

  // Animation
  yield* titleOpacity(1, 0.4);
  yield* networkScale(1, 0.5, easeOutCubic);

  // Devices appear and connect sequentially with green animation
  for (let i = 0; i < deviceAngles.length; i++) {
    yield* all(
      deviceScales[i](1, 0.2, easeOutCubic),
      lineOpacities[i](0.8, 0.2)
    );

    // Turn connection green
    yield* lineColors[i](1, 0.3, easeInOutCubic);

    yield* waitFor(0.1);
  }

  yield* waitFor(0.3);

  // Pulse
  yield* networkScale(1.1, 0.2);
  yield* networkScale(1, 0.2);

  yield* waitFor(0.5);

  // Exit
  yield* all(
    contentScale(0.5, 0.5),
    titleOpacity(0, 0.3),
    networkScale(0, 0.4),
    ...deviceScales.map((s) => s(0, 0.3)),
    ...lineOpacities.map((o) => o(0, 0.3))
  );
});
