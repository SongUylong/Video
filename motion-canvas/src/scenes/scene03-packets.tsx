import {makeScene2D, Camera, Circle, Grid, Line, Node, Rect, Txt, Img} from '@motion-canvas/2d';
import {Vector2, all, createRef, createSignal, waitFor, easeOutCubic, easeInOutCubic} from '@motion-canvas/core';

const CYAN = '#00d4ff';
const GREEN = '#00ff88';
const ORANGE = '#ff6600';
const WHITE = '#ffffff';
const DARK = '#0a0a1a';

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const camera = createRef<Camera>();
  const titleOpacity = createSignal(0);
  const title = createRef<Txt>();

  const computerScale = createSignal(0);
  const serverScale = createSignal(0);
  const lineOpacity = createSignal(0);

  // Packets
  const p0x = createSignal(-200); const p0y = createSignal(-120); const p0op = createSignal(0);
  const p1x = createSignal(-120); const p1y = createSignal(-120); const p1op = createSignal(0);
  const p2x = createSignal(-40); const p2y = createSignal(-120); const p2op = createSignal(0);
  const p3x = createSignal(40); const p3y = createSignal(-120); const p3op = createSignal(0);

  const stepText = createRef<Txt>();

  view.add(
    <Camera ref={camera}>
      <Grid width={1920} height={1080} spacing={60} stroke={'#1a1a2e'} lineWidth={1} />

      {/* Title */}
      <Txt
        ref={title}
        text={'DATA PACKETS'}
        fontSize={48}
        fontWeight={800}
        fill={WHITE}
        y={-320}
        opacity={() => titleOpacity()}
      />

      {/* Computer */}
      <Node x={-350} y={50}>
        <Rect
          width={() => computerScale() * 100}
          height={() => computerScale() * 80}
          fill={'#1a1a3a'}
          stroke={GREEN}
          lineWidth={3}
          radius={10}
        />
        <Txt text={'DEVICE'} fontSize={14} fontWeight={600} fill={GREEN} y={60} opacity={() => computerScale()} />
      </Node>

      {/* Server */}
      <Node x={350} y={50}>
        <Rect
          width={() => serverScale() * 80}
          height={() => serverScale() * 100}
          fill={'#1a1a3a'}
          stroke={ORANGE}
          lineWidth={3}
          radius={10}
        />
        <Txt text={'SERVER'} fontSize={14} fontWeight={600} fill={ORANGE} y={70} opacity={() => serverScale()} />
      </Node>

      {/* Connection line */}
      <Line
        stroke={'#444466'}
        lineWidth={3}
        lineDash={[10, 5]}
        opacity={() => lineOpacity()}
        points={[new Vector2(-290, 50), new Vector2(290, 50)]}
      />

      {/* Packets */}
      <Node x={() => p0x()} y={() => p0y()}>
        <Rect width={45} height={45} fill={CYAN} radius={8} opacity={() => p0op()} />
        <Txt text={'1'} fontSize={20} fontWeight={700} fill={'#000'} opacity={() => p0op()} />
      </Node>
      <Node x={() => p1x()} y={() => p1y()}>
        <Rect width={45} height={45} fill={CYAN} radius={8} opacity={() => p1op()} />
        <Txt text={'2'} fontSize={20} fontWeight={700} fill={'#000'} opacity={() => p1op()} />
      </Node>
      <Node x={() => p2x()} y={() => p2y()}>
        <Rect width={45} height={45} fill={CYAN} radius={8} opacity={() => p2op()} />
        <Txt text={'3'} fontSize={20} fontWeight={700} fill={'#000'} opacity={() => p2op()} />
      </Node>
      <Node x={() => p3x()} y={() => p3y()}>
        <Rect width={45} height={45} fill={CYAN} radius={8} opacity={() => p3op()} />
        <Txt text={'4'} fontSize={20} fontWeight={700} fill={'#000'} opacity={() => p3op()} />
      </Node>

      {/* Step text */}
      <Txt ref={stepText} text={''} fontSize={24} fontWeight={600} fill={'#88ccff'} y={220} opacity={0} />
    </Camera>
  );

  // Animation
  yield* titleOpacity(1, 0.4);
  yield* all(computerScale(1, 0.4), serverScale(1, 0.4));
  yield* lineOpacity(0.6, 0.3);

  // Step 1
  stepText().text('Step 1: Data splits into packets');
  yield* stepText().opacity(1, 0.3);
  yield* all(p0op(1, 0.1), p1op(1, 0.1), p2op(1, 0.1), p3op(1, 0.1));

  yield* waitFor(0.4);

  // Step 2: Travel
  yield* stepText().text('Step 2: Packets travel different paths', 0.2);

  yield* all(
    p0x(0, 0.3), p0y(-50, 0.3),
    p1x(50, 0.3), p1y(80, 0.3),
    p2x(-30, 0.3), p2y(120, 0.3),
    p3x(100, 0.3), p3y(-20, 0.3)
  );

  yield* all(
    p0x(280, 0.4), p0y(20, 0.4),
    p1x(280, 0.4), p1y(40, 0.4),
    p2x(280, 0.4), p2y(60, 0.4),
    p3x(280, 0.4), p3y(80, 0.4)
  );

  // Step 3
  yield* stepText().text('Step 3: Reassembled at destination', 0.2);
  yield* waitFor(0.5);

  // Exit
  yield* all(
    camera().zoom(0.5, 0.5),
    titleOpacity(0, 0.3),
    computerScale(0, 0.3),
    serverScale(0, 0.3),
    lineOpacity(0, 0.3),
    stepText().opacity(0, 0.3),
    p0op(0, 0.3), p1op(0, 0.3), p2op(0, 0.3), p3op(0, 0.3)
  );
});
