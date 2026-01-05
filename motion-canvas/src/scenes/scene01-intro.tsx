import { makeScene2D, Circle, Grid, Node, Txt, Img } from "@motion-canvas/2d";
import {
  createSignal,
  all,
  waitFor,
  easeOutCubic,
  easeInOutCubic,
} from "@motion-canvas/core";

const CYAN = "#00d4ff";
const WHITE = "#ffffff";
const DARK = "#0a0a1a";

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const iconScale = createSignal(0);
  const iconRotation = createSignal(0);
  const contentScale = createSignal(1);

  // Text typing animations
  const text1Progress = createSignal(0);
  const text2Progress = createSignal(0);
  const text3Progress = createSignal(0);

  const text1Full = "HOW DOES THE";
  const text2Full = "INTERNET";
  const text3Full = "WORK?";

  view.add(
    <>
      <Grid
        width={1080}
        height={1920}
        spacing={60}
        stroke={"#1a1a2e"}
        lineWidth={1}
      />

      {/* Centered content container */}
      <Node scale={() => contentScale()}>
        {/* Glow circle */}
        <Circle
          width={() => iconScale() * 320}
          height={() => iconScale() * 320}
          stroke={CYAN}
          lineWidth={3}
          opacity={0.4}
          shadowColor={CYAN}
          shadowBlur={50}
          y={-180}
        />

        {/* Icon */}
        <Img
          src={"/asset/global-network.png"}
          width={() => iconScale() * 200}
          height={() => iconScale() * 200}
          rotation={() => iconRotation()}
          y={-180}
        />

        {/* Title with typing effect */}
        <Txt
          text={() =>
            text1Full.substring(
              0,
              Math.floor(text1Progress() * text1Full.length)
            )
          }
          fontSize={60}
          fontWeight={800}
          fontFamily={"Arial Black"}
          fill={WHITE}
          y={40}
          textAlign={"center"}
        />

        <Txt
          text={() =>
            text2Full.substring(
              0,
              Math.floor(text2Progress() * text2Full.length)
            )
          }
          fontSize={90}
          fontWeight={900}
          fontFamily={"Arial Black"}
          fill={CYAN}
          y={150}
          shadowColor={CYAN}
          shadowBlur={30}
          textAlign={"center"}
        />

        <Txt
          text={() =>
            text3Full.substring(
              0,
              Math.floor(text3Progress() * text3Full.length)
            )
          }
          fontSize={90}
          fontWeight={900}
          fontFamily={"Arial Black"}
          fill={WHITE}
          y={270}
          textAlign={"center"}
        />
      </Node>
    </>
  );

  // Animation sequence
  yield* iconScale(1, 0.6, easeOutCubic);

  // Typing animation for each line
  yield* text1Progress(1, 0.8, easeInOutCubic);
  yield* waitFor(0.2);

  yield* text2Progress(1, 0.6, easeInOutCubic);
  yield* waitFor(0.2);

  yield* text3Progress(1, 0.6, easeInOutCubic);

  yield* waitFor(0.3);
  yield* iconRotation(360, 2);

  yield* waitFor(0.5);

  // Exit
  yield* all(
    contentScale(0.5, 0.5),
    iconScale(0, 0.4),
    text1Progress(0, 0.4),
    text2Progress(0, 0.4),
    text3Progress(0, 0.4)
  );
});
