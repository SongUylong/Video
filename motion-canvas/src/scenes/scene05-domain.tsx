import {makeScene2D, Camera, Grid, Line, Node, Rect, Txt, Img} from '@motion-canvas/2d';
import {Vector2, all, createRef, createSignal, waitFor, easeOutCubic} from '@motion-canvas/core';

const CYAN = '#00d4ff';
const ORANGE = '#ff6600';
const RED = '#ff4444';
const GREEN = '#00ff88';
const YELLOW = '#ffaa00';
const WHITE = '#ffffff';
const DARK = '#0a0a1a';

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const camera = createRef<Camera>();
  const titleOpacity = createSignal(0);
  const title = createRef<Txt>();

  const domainScale = createSignal(0);
  const ipScale = createSignal(0);
  const vsOpacity = createSignal(0);
  const domainText = createRef<Txt>();
  const ipText = createRef<Txt>();

  const structure = [
    {text: 'www', color: YELLOW, label: 'Subdomain'},
    {text: 'google', color: GREEN, label: 'Domain'},
    {text: '.com', color: RED, label: 'TLD'},
  ];
  const structureScales = structure.map(() => createSignal(0));

  view.add(
    <Camera ref={camera}>
      <Grid width={1920} height={1080} spacing={60} stroke={'#1a1a2e'} lineWidth={1} />

      {/* Title */}
      <Txt
        ref={title}
        text={'DOMAIN NAMES'}
        fontSize={48}
        fontWeight={800}
        fill={WHITE}
        y={-340}
        opacity={() => titleOpacity()}
      />

      {/* Domain box */}
      <Node y={-180}>
        <Rect
          width={() => domainScale() * 320}
          height={() => domainScale() * 60}
          fill={'#1a2a4a'}
          stroke={CYAN}
          lineWidth={3}
          radius={12}
        />
        <Img src={'/asset/domain.png'} width={() => domainScale() * 40} height={() => domainScale() * 40} x={-120} />
        <Txt ref={domainText} text={''} fontSize={26} fontWeight={700} fontFamily={'monospace'} fill={CYAN} x={20} />
      </Node>
      <Txt text={'Human Readable'} fontSize={18} fontWeight={500} fill={'#88ccff'} y={-130} opacity={() => domainScale()} />

      {/* VS */}
      <Txt text={'VS'} fontSize={36} fontWeight={800} fill={YELLOW} y={-60} opacity={() => vsOpacity()} />

      {/* IP box */}
      <Node y={30}>
        <Rect
          width={() => ipScale() * 320}
          height={() => ipScale() * 60}
          fill={'#2a1a1a'}
          stroke={ORANGE}
          lineWidth={3}
          radius={12}
        />
        <Img src={'/asset/ip.png'} width={() => ipScale() * 40} height={() => ipScale() * 40} x={-120} />
        <Txt ref={ipText} text={''} fontSize={24} fontWeight={700} fontFamily={'monospace'} fill={ORANGE} x={20} />
      </Node>
      <Txt text={'Machine Readable'} fontSize={18} fontWeight={500} fill={'#ffaa88'} y={80} opacity={() => ipScale()} />

      {/* Structure */}
      {structure.map((part, i) => (
        <Node key={`struct-${i}`} x={-130 + i * 130} y={200}>
          <Rect
            width={() => structureScales[i]() * 100}
            height={() => structureScales[i]() * 50}
            fill={'#1a1a3a'}
            stroke={part.color}
            lineWidth={3}
            radius={8}
          />
          <Txt text={part.text} fontSize={18} fontWeight={700} fill={part.color} y={-5} opacity={() => structureScales[i]()} />
          <Txt text={part.label} fontSize={12} fontWeight={500} fill={'#888'} y={40} opacity={() => structureScales[i]()} />
        </Node>
      ))}
    </Camera>
  );

  // Animation
  yield* titleOpacity(1, 0.4);
  yield* domainScale(1, 0.4, easeOutCubic);

  // Type domain
  for (let i = 0; i <= 10; i++) {
    domainText().text('google.com'.slice(0, i));
    yield* waitFor(0.04);
  }

  yield* vsOpacity(1, 0.3);
  yield* ipScale(1, 0.4, easeOutCubic);

  // Type IP
  for (let i = 0; i <= 14; i++) {
    ipText().text('142.250.72.14'.slice(0, i));
    yield* waitFor(0.03);
  }

  yield* waitFor(0.4);

  // Show structure
  yield* title().text('DOMAIN STRUCTURE', 0.2);
  yield* all(vsOpacity(0, 0.2), ipScale(0, 0.2), ipText().opacity(0, 0.2));
  yield* domainText().text('www.google.com', 0.2);

  for (let i = 0; i < structure.length; i++) {
    yield* structureScales[i](1, 0.15, easeOutCubic);
  }

  yield* waitFor(0.5);

  // Exit
  yield* all(
    camera().zoom(0.5, 0.5),
    titleOpacity(0, 0.3),
    domainScale(0, 0.3),
    domainText().opacity(0, 0.3),
    ...structureScales.map(s => s(0, 0.3))
  );
});
