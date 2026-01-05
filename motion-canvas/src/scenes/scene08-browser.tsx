import {makeScene2D, Camera, Circle, Grid, Line, Node, Rect, Txt, Img} from '@motion-canvas/2d';
import {Vector2, all, createRef, createSignal, waitFor, easeOutCubic, easeInOutCubic} from '@motion-canvas/core';

const CYAN = '#00d4ff';
const GREEN = '#00ff88';
const RED = '#ff6b6b';
const TEAL = '#4ecdc4';
const YELLOW = '#ffd93d';
const WHITE = '#ffffff';
const DARK = '#0a0a1a';

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const camera = createRef<Camera>();
  const titleOpacity = createSignal(0);
  const title = createRef<Txt>();

  const browserScale = createSignal(0);
  const loadingOpacity = createSignal(0);
  const loadingText = createRef<Txt>();

  const steps = [
    {name: 'HTML', color: RED, desc: 'Structure'},
    {name: 'CSS', color: TEAL, desc: 'Styling'},
    {name: 'JS', color: YELLOW, desc: 'Interactivity'},
  ];
  const stepScales = steps.map(() => createSignal(0));
  const arrowOpacities = steps.map(() => createSignal(0));

  const resultLabel = createRef<Txt>();
  const finalPageScale = createSignal(0);

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
        text={'HOW BROWSERS WORK'}
        fontSize={56}
        fontWeight={800}
        fill={WHITE}
        y={-380}
        opacity={() => titleOpacity()}
        shadowColor={CYAN}
        shadowBlur={15}
      />

      {/* Browser window mockup */}
      <Node y={-100}>
        <Rect
          width={() => browserScale() * 500}
          height={() => browserScale() * 320}
          fill={'#1a1a2e'}
          stroke={'#3a3a5a'}
          lineWidth={2}
          radius={15}
        />
        <Rect
          width={() => browserScale() * 500}
          height={() => browserScale() * 40}
          fill={'#2a2a4a'}
          radius={[15, 15, 0, 0]}
          y={() => -140 * browserScale()}
        />
        {/* Browser buttons */}
        <Circle width={12} height={12} fill={'#ff5f57'} x={() => -220 * browserScale()} y={() => -140 * browserScale()} />
        <Circle width={12} height={12} fill={'#ffbd2e'} x={() => -198 * browserScale()} y={() => -140 * browserScale()} />
        <Circle width={12} height={12} fill={'#28c940'} x={() => -176 * browserScale()} y={() => -140 * browserScale()} />
        {/* URL bar */}
        <Rect
          width={() => browserScale() * 300}
          height={() => browserScale() * 24}
          fill={WHITE}
          radius={12}
          x={() => 20 * browserScale()}
          y={() => -140 * browserScale()}
        />
        <Txt
          text={'https://example.com'}
          fontSize={12}
          fontWeight={500}
          fill={'#333'}
          x={() => 20 * browserScale()}
          y={() => -140 * browserScale()}
          opacity={() => browserScale()}
        />
        {/* Content area */}
        <Rect
          width={() => browserScale() * 460}
          height={() => browserScale() * 240}
          fill={WHITE}
          radius={8}
          y={() => 30 * browserScale()}
        />
        {/* Loading text */}
        <Txt
          ref={loadingText}
          text={'Loading...'}
          fontSize={20}
          fontWeight={600}
          fill={'#666'}
          y={() => 30 * browserScale()}
          opacity={() => loadingOpacity()}
        />
      </Node>

      {/* Rendering steps */}
      {steps.map((step, i) => (
        <Node key={`step-${i}`} x={-170 + i * 170} y={180}>
          <Rect
            width={() => stepScales[i]() * 140}
            height={() => stepScales[i]() * 80}
            fill={'#1a1a3a'}
            stroke={step.color}
            lineWidth={3}
            radius={12}
          />
          <Txt
            text={step.name}
            fontSize={28}
            fontWeight={800}
            fill={step.color}
            y={-10}
            opacity={() => stepScales[i]()}
          />
          <Txt
            text={step.desc}
            fontSize={14}
            fontWeight={500}
            fill={'#aaa'}
            y={22}
            opacity={() => stepScales[i]()}
          />
        </Node>
      ))}

      {/* Arrows between steps */}
      {[0, 1].map((i) => (
        <Line
          key={`arrow-${i}`}
          stroke={WHITE}
          lineWidth={3}
          endArrow
          arrowSize={10}
          opacity={() => arrowOpacities[i]()}
          points={[
            new Vector2(-95 + i * 170, 180),
            new Vector2(-30 + i * 170, 180),
          ]}
        />
      ))}

      {/* Result label */}
      <Txt
        ref={resultLabel}
        text={''}
        fontSize={28}
        fontWeight={700}
        fill={GREEN}
        y={300}
        opacity={0}
      />

      {/* Final rendered page preview */}
      <Node y={380}>
        <Rect
          width={() => finalPageScale() * 200}
          height={() => finalPageScale() * 140}
          fill={'#1a1a2e'}
          stroke={GREEN}
          lineWidth={3}
          radius={10}
        />
        <Rect
          width={() => finalPageScale() * 180}
          height={() => finalPageScale() * 25}
          fill={TEAL}
          radius={5}
          y={() => -45 * finalPageScale()}
        />
        <Rect
          width={() => finalPageScale() * 75}
          height={() => finalPageScale() * 55}
          fill={'#666'}
          radius={5}
          x={() => -45 * finalPageScale()}
          y={() => 15 * finalPageScale()}
        />
        <Rect
          width={() => finalPageScale() * 75}
          height={() => finalPageScale() * 55}
          fill={'#888'}
          radius={5}
          x={() => 45 * finalPageScale()}
          y={() => 15 * finalPageScale()}
        />
      </Node>
    </Camera>
  );

  // Animation sequence
  
  // Start zoomed out
  camera().zoom(0.7);
  yield* all(
    camera().zoom(1, 0.5, easeOutCubic),
    titleOpacity(1, 0.4)
  );

  // Show browser
  yield* browserScale(1, 0.5, easeOutCubic);

  // Loading animation
  yield* loadingOpacity(1, 0.2);
  yield* waitFor(0.3);
  yield* loadingText().text('Loading..', 0.1);
  yield* loadingText().text('Loading...', 0.1);
  yield* loadingText().text('Loading.', 0.1);
  yield* loadingOpacity(0, 0.2);

  yield* waitFor(0.2);

  yield* title().text('RENDERING PROCESS', 0.3);

  // Show steps together with arrows
  yield* all(
    ...stepScales.map((s, i) => s(1, 0.3, easeOutCubic)),
    ...arrowOpacities.map((o, i) => o(1, 0.3))
  );

  // Pulse steps in sequence
  for (let i = 0; i < steps.length; i++) {
    yield* stepScales[i](1.1, 0.1);
    yield* stepScales[i](1, 0.1);
  }

  yield* waitFor(0.2);

  // Result label
  resultLabel().text('WEBSITE RENDERED!');
  yield* resultLabel().opacity(1, 0.3);

  // Show final page
  yield* finalPageScale(1, 0.5, easeOutCubic);

  // Celebratory pulse
  yield* finalPageScale(1.1, 0.2);
  yield* finalPageScale(1, 0.2);

  yield* waitFor(0.5);

  // Exit with zoom out
  yield* all(
    camera().zoom(0.5, 0.5, easeInOutCubic),
    titleOpacity(0, 0.3),
    browserScale(0, 0.3),
    ...stepScales.map(s => s(0, 0.3)),
    ...arrowOpacities.map(o => o(0, 0.3)),
    resultLabel().opacity(0, 0.3),
    finalPageScale(0, 0.3)
  );
});
