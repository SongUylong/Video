import {makeScene2D, Camera, Circle, Grid, Line, Node, Rect, Txt, Img} from '@motion-canvas/2d';
import {Vector2, all, createRef, createSignal, waitFor, easeOutCubic, easeInOutCubic} from '@motion-canvas/core';

const CYAN = '#00d4ff';
const GREEN = '#00ff88';
const RED = '#ff6b6b';
const TEAL = '#4ecdc4';
const YELLOW = '#ffd93d';
const PINK = '#ff66aa';
const ORANGE = '#ffaa00';
const PURPLE = '#a29bfe';
const WHITE = '#ffffff';
const DARK = '#0a0a1a';

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const camera = createRef<Camera>();
  const titleOpacity = createSignal(0);
  const title = createRef<Txt>();

  const serverScale = createSignal(0);
  const slotScales = [0, 1, 2, 3, 4].map(() => createSignal(0));
  const serverLabel = createRef<Txt>();

  const files = [
    {type: 'HTML', color: RED, icon: 'code'},
    {type: 'CSS', color: TEAL, icon: 'script'},
    {type: 'JS', color: YELLOW, icon: 'script'},
    {type: 'Images', color: PURPLE, icon: 'binary-code'},
  ];
  const fileScales = files.map(() => createSignal(0));
  const lineOpacities = files.map(() => createSignal(0));

  const hostingTypes = [
    {name: 'Shared', color: CYAN},
    {name: 'VPS', color: GREEN},
    {name: 'Cloud', color: PINK},
    {name: 'Dedicated', color: ORANGE},
  ];
  const hostingScales = hostingTypes.map(() => createSignal(0));

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
        text={'WEB HOSTING'}
        fontSize={56}
        fontWeight={800}
        fill={WHITE}
        y={-380}
        opacity={() => titleOpacity()}
        shadowColor={GREEN}
        shadowBlur={15}
      />

      {/* Server rack (left side) */}
      <Node x={-250}>
        <Rect
          width={() => serverScale() * 180}
          height={() => serverScale() * 280}
          fill={'#0d1a2a'}
          stroke={GREEN}
          lineWidth={3}
          radius={15}
          y={20}
        />
        <Img
          src={'/asset/cloud-server.png'}
          width={() => serverScale() * 60}
          height={() => serverScale() * 60}
          y={-100}
        />
      </Node>

      {/* Server slots */}
      {[0, 1, 2, 3, 4].map((i) => (
        <Node key={`slot-${i}`} x={-250} y={-30 + i * 50}>
          <Rect
            width={() => slotScales[i]() * 140}
            height={() => slotScales[i]() * 38}
            fill={'#1a2a4a'}
            stroke={'#334466'}
            lineWidth={1}
            radius={5}
          />
          <Circle
            width={() => slotScales[i]() * 10}
            height={() => slotScales[i]() * 10}
            fill={GREEN}
            x={() => -55 * slotScales[i]()}
          />
        </Node>
      ))}

      {/* Server label */}
      <Txt
        ref={serverLabel}
        text={'SERVER'}
        fontSize={20}
        fontWeight={600}
        fill={GREEN}
        x={-250}
        y={200}
        opacity={0}
      />

      {/* Connection lines and file boxes */}
      {files.map((file, i) => {
        const row = Math.floor(i / 2);
        const col = i % 2;
        const x = 100 + col * 130;
        const y = -80 + row * 130;

        return (
          <Node key={`file-${i}`}>
            <Line
              stroke={GREEN}
              lineWidth={2}
              lineDash={[8, 4]}
              opacity={() => lineOpacities[i]()}
              points={[
                new Vector2(-160, -30 + i * 50),
                new Vector2(x - 55, y),
              ]}
            />
            <Node x={x} y={y}>
              <Rect
                width={() => fileScales[i]() * 100}
                height={() => fileScales[i]() * 85}
                fill={'#1a1a3a'}
                stroke={file.color}
                lineWidth={3}
                radius={12}
              />
              <Img
                src={`/asset/${file.icon}.png`}
                width={() => fileScales[i]() * 35}
                height={() => fileScales[i]() * 35}
                y={-12}
              />
              <Txt
                text={file.type}
                fontSize={16}
                fontWeight={700}
                fill={file.color}
                y={25}
                opacity={() => fileScales[i]()}
              />
            </Node>
          </Node>
        );
      })}

      {/* Hosting types (bottom) */}
      {hostingTypes.map((hosting, i) => (
        <Node key={`hosting-${i}`} x={-280 + i * 160} y={330}>
          <Rect
            width={() => hostingScales[i]() * 130}
            height={() => hostingScales[i]() * 55}
            fill={'#1a1a2e'}
            stroke={hosting.color}
            lineWidth={2}
            radius={10}
          />
          <Txt
            text={hosting.name}
            fontSize={18}
            fontWeight={700}
            fill={hosting.color}
            opacity={() => hostingScales[i]()}
          />
        </Node>
      ))}
    </Camera>
  );

  // Animation sequence
  
  // Start zoomed out, zoom in
  camera().zoom(0.7);
  yield* all(
    camera().zoom(1, 0.5, easeOutCubic),
    titleOpacity(1, 0.4)
  );

  // Show server rack
  yield* serverScale(1, 0.4, easeOutCubic);

  // Server slots light up (no camera following)
  for (let i = 0; i < 5; i++) {
    yield* slotScales[i](1, 0.08, easeOutCubic);
  }

  yield* serverLabel().opacity(1, 0.3);

  yield* waitFor(0.2);

  // Update title
  yield* title().text('FILES STORED', 0.3);

  // File boxes appear together
  yield* all(
    ...fileScales.map((s, i) => s(1, 0.3, easeOutCubic)),
    ...lineOpacities.map((o, i) => o(0.5, 0.3))
  );

  // Pulse files
  yield* all(
    ...fileScales.map(s => s(1.1, 0.15))
  );
  yield* all(
    ...fileScales.map(s => s(1, 0.15))
  );

  yield* waitFor(0.3);

  // Show hosting types
  yield* title().text('HOSTING TYPES', 0.3);

  // Hosting types appear together
  yield* all(
    ...hostingScales.map((s, i) => s(1, 0.3, easeOutCubic))
  );

  // Highlight cloud hosting
  yield* hostingScales[2](1.15, 0.2);
  yield* hostingScales[2](1, 0.2);

  yield* waitFor(0.5);

  // Exit with zoom out
  yield* all(
    camera().zoom(0.5, 0.5, easeInOutCubic),
    titleOpacity(0, 0.3),
    serverScale(0, 0.3),
    serverLabel().opacity(0, 0.3),
    ...slotScales.map(s => s(0, 0.3)),
    ...fileScales.map(s => s(0, 0.3)),
    ...lineOpacities.map(o => o(0, 0.3)),
    ...hostingScales.map(s => s(0, 0.3))
  );
});
