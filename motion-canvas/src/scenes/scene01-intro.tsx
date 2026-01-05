import {makeScene2D, Camera, Circle, Grid, Node, Txt, Img} from '@motion-canvas/2d';
import {createRef, createSignal, all, waitFor, easeOutCubic} from '@motion-canvas/core';

const CYAN = '#00d4ff';
const WHITE = '#ffffff';
const DARK = '#0a0a1a';

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const camera = createRef<Camera>();
  const iconScale = createSignal(0);
  const titleOpacity = createSignal(0);
  const iconRotation = createSignal(0);

  view.add(
    <Camera ref={camera}>
      <Grid
        width={1920}
        height={1080}
        spacing={60}
        stroke={'#1a1a2e'}
        lineWidth={1}
      />

      {/* Glow circle */}
      <Circle
        width={() => iconScale() * 320}
        height={() => iconScale() * 320}
        stroke={CYAN}
        lineWidth={3}
        opacity={0.4}
        shadowColor={CYAN}
        shadowBlur={50}
      />

      {/* Icon */}
      <Img
        src={'/asset/global-network.png'}
        width={() => iconScale() * 200}
        height={() => iconScale() * 200}
        rotation={() => iconRotation()}
      />

      {/* Title */}
      <Txt
        text={'HOW DOES THE'}
        fontSize={60}
        fontWeight={800}
        fontFamily={'Arial Black'}
        fill={WHITE}
        y={250}
        opacity={() => titleOpacity()}
      />

      <Txt
        text={'INTERNET'}
        fontSize={90}
        fontWeight={900}
        fontFamily={'Arial Black'}
        fill={CYAN}
        y={340}
        opacity={() => titleOpacity()}
        shadowColor={CYAN}
        shadowBlur={30}
      />

      <Txt
        text={'WORK?'}
        fontSize={90}
        fontWeight={900}
        fontFamily={'Arial Black'}
        fill={WHITE}
        y={430}
        opacity={() => titleOpacity()}
      />
    </Camera>
  );

  // Simple animation
  yield* iconScale(1, 0.6, easeOutCubic);
  yield* titleOpacity(1, 0.5);
  yield* iconRotation(360, 2);
  
  yield* waitFor(0.5);

  // Exit
  yield* all(
    camera().zoom(0.5, 0.5),
    iconScale(0, 0.4),
    titleOpacity(0, 0.4)
  );
});
