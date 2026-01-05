import {makeScene2D, Camera, Circle, Grid, Line, Node, Rect, Txt, Img} from '@motion-canvas/2d';
import {Vector2, all, createRef, createSignal, waitFor, easeOutCubic, easeInOutCubic} from '@motion-canvas/core';

const CYAN = '#00d4ff';
const GREEN = '#00ff88';
const PURPLE = '#9966ff';
const ORANGE = '#ffaa00';
const PINK = '#ff66aa';
const WHITE = '#ffffff';
const DARK = '#0a0a1a';

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const camera = createRef<Camera>();
  const titleOpacity = createSignal(0);
  const title = createRef<Txt>();

  // Journey stages
  const stages = [
    {name: 'YOU', icon: 'browser', x: -450, color: CYAN},
    {name: 'DNS', icon: 'dns', x: -225, color: PURPLE},
    {name: 'SERVER', icon: 'cloud-server', x: 0, color: GREEN},
    {name: 'DATA', icon: 'packet', x: 225, color: ORANGE},
    {name: 'RESULT', icon: 'code', x: 450, color: PINK},
  ];

  const stageScales = stages.map(() => createSignal(0));
  const lineOpacities = stages.map(() => createSignal(0));

  const urlScale = createSignal(0);
  const urlText = createRef<Txt>();

  const websiteScale = createSignal(0);
  const packetOpacity = createSignal(0);
  const packetX = createSignal(-450);

  view.add(
    <Camera ref={camera}>
      {/* Grid background */}
      <Grid
        width={3000}
        height={2000}
        spacing={60}
        stroke={'#1a1a2e'}
        lineWidth={1}
      />

      {/* Title */}
      <Txt
        ref={title}
        text={'THE COMPLETE JOURNEY'}
        fontSize={52}
        fontWeight={800}
        fill={WHITE}
        y={-380}
        opacity={() => titleOpacity()}
        shadowColor={CYAN}
        shadowBlur={15}
      />

      {/* URL box */}
      <Node y={-250}>
        <Rect
          width={() => urlScale() * 280}
          height={() => urlScale() * 45}
          fill={'#1a2a4a'}
          stroke={CYAN}
          lineWidth={2}
          radius={22}
        />
      </Node>
      <Txt
        ref={urlText}
        text={''}
        fontSize={18}
        fontWeight={600}
        fontFamily={'monospace'}
        fill={CYAN}
        y={-250}
      />

      {/* Connection lines */}
      {stages.slice(0, -1).map((stage, i) => (
        <Line
          key={`line-${i}`}
          stroke={'#333355'}
          lineWidth={3}
          lineDash={[8, 4]}
          opacity={() => lineOpacities[i]()}
          points={[
            new Vector2(stage.x + 55, -50),
            new Vector2(stages[i + 1].x - 55, -50),
          ]}
        />
      ))}

      {/* Stage circles */}
      {stages.map((stage, i) => (
        <Node key={`stage-${i}`} x={stage.x} y={-50}>
          <Circle
            width={() => stageScales[i]() * 100}
            height={() => stageScales[i]() * 100}
            fill={'#1a1a3a'}
            stroke={stage.color}
            lineWidth={4}
            shadowColor={stage.color}
            shadowBlur={15}
          />
          <Img
            src={`/asset/${stage.icon}.png`}
            width={() => stageScales[i]() * 55}
            height={() => stageScales[i]() * 55}
          />
          <Txt
            text={stage.name}
            fontSize={18}
            fontWeight={700}
            fill={stage.color}
            y={70}
            opacity={() => stageScales[i]()}
          />
        </Node>
      ))}

      {/* Traveling packet */}
      <Circle
        width={20}
        height={20}
        fill={ORANGE}
        x={() => packetX()}
        y={-50}
        opacity={() => packetOpacity()}
        shadowColor={ORANGE}
        shadowBlur={15}
      />

      {/* Final website */}
      <Node y={180}>
        <Rect
          width={() => websiteScale() * 380}
          height={() => websiteScale() * 200}
          fill={'#1a1a2e'}
          stroke={GREEN}
          lineWidth={3}
          radius={15}
        />
        <Rect
          width={() => websiteScale() * 340}
          height={() => websiteScale() * 35}
          fill={CYAN}
          radius={8}
          y={() => -65 * websiteScale()}
        />
        <Rect
          width={() => websiteScale() * 90}
          height={() => websiteScale() * 100}
          fill={'#333355'}
          radius={8}
          x={() => -110 * websiteScale()}
          y={() => 30 * websiteScale()}
        />
        <Rect
          width={() => websiteScale() * 220}
          height={() => websiteScale() * 100}
          fill={'#444466'}
          radius={8}
          x={() => 50 * websiteScale()}
          y={() => 30 * websiteScale()}
        />
      </Node>
    </Camera>
  );

  // Animation sequence
  
  // Start zoomed out
  camera().zoom(0.6);
  yield* all(
    camera().zoom(0.9, 0.5, easeOutCubic),
    titleOpacity(1, 0.4)
  );

  // Show URL box
  yield* urlScale(1, 0.4, easeOutCubic);

  // Type URL
  const url = 'example.com';
  for (let i = 0; i <= url.length; i++) {
    urlText().text(url.slice(0, i));
    yield* waitFor(0.04);
  }

  yield* waitFor(0.2);

  // Show connection lines
  yield* all(
    ...lineOpacities.map(o => o(0.5, 0.3))
  );

  // Reveal all stages together
  yield* all(
    ...stageScales.map((s, i) => s(1, 0.4, easeOutCubic))
  );

  // Highlight lines
  yield* all(
    ...lineOpacities.map(o => o(0.8, 0.2))
  );

  yield* waitFor(0.2);

  // Animated packet traveling through stages
  yield* packetOpacity(1, 0.2);

  // Travel through each stage
  for (let i = 1; i < stages.length; i++) {
    yield* packetX(stages[i].x, 0.35, easeInOutCubic);

    // Flash stage
    yield* stageScales[i](1.15, 0.1);
    yield* stageScales[i](1, 0.1);
  }

  // Packet reaches destination
  yield* packetOpacity(0, 0.2);

  // Show final website
  yield* title().text('WEBSITE LOADED!', 0.3);

  yield* websiteScale(1, 0.5, easeOutCubic);

  // Celebratory pulse
  yield* websiteScale(1.05, 0.2);
  yield* websiteScale(1, 0.2);

  yield* waitFor(0.5);

  // Exit with zoom out (no rotation)
  yield* all(
    camera().zoom(0.5, 0.5, easeInOutCubic),
    titleOpacity(0, 0.3),
    urlScale(0, 0.3),
    urlText().opacity(0, 0.3),
    ...stageScales.map(s => s(0, 0.4)),
    ...lineOpacities.map(o => o(0, 0.3)),
    websiteScale(0, 0.4)
  );
});
