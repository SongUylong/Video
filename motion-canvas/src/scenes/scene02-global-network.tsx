import {makeScene2D, Camera, Circle, Grid, Line, Node, Txt, Img} from '@motion-canvas/2d';
import {Vector2, all, createRef, createSignal, waitFor, easeOutCubic} from '@motion-canvas/core';

const CYAN = '#00d4ff';
const GREEN = '#00ff88';
const WHITE = '#ffffff';
const DARK = '#0a0a1a';

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const camera = createRef<Camera>();
  const titleOpacity = createSignal(0);
  const networkScale = createSignal(0);

  const deviceAngles = [0, 60, 120, 180, 240, 300];
  const deviceScales = deviceAngles.map(() => createSignal(0));
  const lineOpacities = deviceAngles.map(() => createSignal(0));

  const distance = 180;

  view.add(
    <Camera ref={camera}>
      <Grid
        width={1920}
        height={1080}
        spacing={80}
        stroke={'#1a1a2e'}
        lineWidth={1}
      />

      {/* Title */}
      <Txt
        text={'GLOBAL NETWORK'}
        fontSize={48}
        fontWeight={700}
        fill={WHITE}
        y={-350}
        opacity={() => titleOpacity()}
      />

      {/* Connection lines */}
      {deviceAngles.map((angle, i) => {
        const rad = (angle * Math.PI) / 180;
        const x = Math.cos(rad) * distance;
        const y = Math.sin(rad) * distance;
        return (
          <Line
            key={`line-${i}`}
            stroke={CYAN}
            lineWidth={2}
            opacity={() => lineOpacities[i]()}
            lineDash={[8, 4]}
            points={[Vector2.zero, new Vector2(x, y)]}
          />
        );
      })}

      {/* Center node */}
      <Circle
        width={() => networkScale() * 120}
        height={() => networkScale() * 120}
        fill={'#1a1a3a'}
        stroke={CYAN}
        lineWidth={4}
        shadowColor={CYAN}
        shadowBlur={20}
      />
      <Img
        src={'/asset/networking.png'}
        width={() => networkScale() * 80}
        height={() => networkScale() * 80}
      />

      {/* Device nodes */}
      {deviceAngles.map((angle, i) => {
        const rad = (angle * Math.PI) / 180;
        const x = Math.cos(rad) * distance;
        const y = Math.sin(rad) * distance;
        return (
          <Node key={`device-${i}`} x={x} y={y}>
            <Circle
              width={() => deviceScales[i]() * 60}
              height={() => deviceScales[i]() * 60}
              fill={'#1a1a3a'}
              stroke={GREEN}
              lineWidth={3}
              shadowColor={GREEN}
              shadowBlur={10}
            />
            <Img
              src={'/asset/wifi.png'}
              width={() => deviceScales[i]() * 35}
              height={() => deviceScales[i]() * 35}
            />
          </Node>
        );
      })}

      {/* Subtitle */}
      <Txt
        text={'Billions of connected devices'}
        fontSize={28}
        fontWeight={500}
        fill={'#88ccff'}
        y={350}
        opacity={() => titleOpacity()}
      />
    </Camera>
  );

  // Animation
  yield* titleOpacity(1, 0.4);
  yield* networkScale(1, 0.5, easeOutCubic);

  // Devices appear
  for (let i = 0; i < deviceAngles.length; i++) {
    yield* all(
      deviceScales[i](1, 0.15, easeOutCubic),
      lineOpacities[i](0.6, 0.15)
    );
  }

  yield* waitFor(0.3);

  // Pulse
  yield* networkScale(1.1, 0.2);
  yield* networkScale(1, 0.2);

  yield* waitFor(0.5);

  // Exit
  yield* all(
    camera().zoom(0.5, 0.5),
    titleOpacity(0, 0.3),
    networkScale(0, 0.4),
    ...deviceScales.map(s => s(0, 0.3)),
    ...lineOpacities.map(o => o(0, 0.3))
  );
});
