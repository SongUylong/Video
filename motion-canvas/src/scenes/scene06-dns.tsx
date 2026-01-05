import {makeScene2D, Camera, Grid, Line, Node, Rect, Txt, Img} from '@motion-canvas/2d';
import {Vector2, all, createRef, createSignal, waitFor, easeOutCubic} from '@motion-canvas/core';

const CYAN = '#00d4ff';
const PURPLE = '#9966ff';
const ORANGE = '#ff6600';
const YELLOW = '#ffcc00';
const WHITE = '#ffffff';
const DARK = '#0a0a1a';

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const camera = createRef<Camera>();
  const titleOpacity = createSignal(0);

  const steps = [
    {label: 'Browser', icon: 'browser'},
    {label: 'DNS Resolver', icon: 'dns'},
    {label: 'Root Server', icon: 'cloud-server'},
    {label: 'IP Returned', icon: 'ip'},
  ];
  const stepScales = steps.map(() => createSignal(0));
  const arrowOpacities = [createSignal(0), createSignal(0), createSignal(0)];

  const domainScale = createSignal(0);
  const dnsScale = createSignal(0);
  const ipScale = createSignal(0);
  const arrowOpacity = createSignal(0);

  const domainText = createRef<Txt>();
  const ipText = createRef<Txt>();

  view.add(
    <Camera ref={camera}>
      <Grid width={1920} height={1080} spacing={60} stroke={'#1a1a2e'} lineWidth={1} />

      {/* Title */}
      <Txt
        text={'DNS LOOKUP'}
        fontSize={48}
        fontWeight={800}
        fill={WHITE}
        y={-350}
        opacity={() => titleOpacity()}
        shadowColor={PURPLE}
        shadowBlur={15}
      />
      <Txt
        text={'"The Internet\'s Phone Book"'}
        fontSize={22}
        fontWeight={500}
        fill={'#88aaff'}
        y={-305}
        opacity={() => titleOpacity()}
      />

      {/* Steps on left */}
      {steps.map((step, i) => (
        <Node key={`step-${i}`} x={-280} y={-160 + i * 100}>
          <Rect
            width={() => stepScales[i]() * 150}
            height={() => stepScales[i]() * 65}
            fill={'#1a1a3a'}
            stroke={PURPLE}
            lineWidth={2}
            radius={10}
          />
          <Img src={`/asset/${step.icon}.png`} width={() => stepScales[i]() * 35} height={() => stepScales[i]() * 35} y={-8} />
          <Txt text={step.label} fontSize={14} fontWeight={600} fill={WHITE} y={22} opacity={() => stepScales[i]()} />
        </Node>
      ))}

      {/* Arrows between steps */}
      {[0, 1, 2].map((i) => (
        <Line
          key={`arrow-${i}`}
          stroke={CYAN}
          lineWidth={2}
          endArrow
          arrowSize={8}
          opacity={() => arrowOpacities[i]()}
          points={[new Vector2(-280, -125 + i * 100), new Vector2(-280, -95 + i * 100)]}
        />
      ))}

      {/* Domain box */}
      <Node x={150} y={-120}>
        <Rect width={() => domainScale() * 180} height={() => domainScale() * 50} fill={'#1a2a4a'} stroke={CYAN} lineWidth={2} radius={10} />
        <Txt ref={domainText} text={''} fontSize={18} fontWeight={700} fontFamily={'monospace'} fill={CYAN} />
      </Node>

      {/* DNS icon */}
      <Img src={'/asset/dns.png'} width={() => dnsScale() * 60} height={() => dnsScale() * 60} x={150} y={0} />

      {/* Arrow */}
      <Line
        stroke={YELLOW}
        lineWidth={4}
        lineDash={[8, 4]}
        endArrow
        arrowSize={12}
        opacity={() => arrowOpacity()}
        points={[new Vector2(150, -80), new Vector2(150, 60)]}
      />

      {/* IP box */}
      <Node x={150} y={120}>
        <Rect width={() => ipScale() * 180} height={() => ipScale() * 50} fill={'#2a1a1a'} stroke={ORANGE} lineWidth={2} radius={10} />
        <Txt ref={ipText} text={''} fontSize={18} fontWeight={700} fontFamily={'monospace'} fill={ORANGE} />
      </Node>
    </Camera>
  );

  // Animation
  yield* titleOpacity(1, 0.4);

  // Show steps
  for (let i = 0; i < steps.length; i++) {
    yield* stepScales[i](1, 0.2, easeOutCubic);
    if (i < 3) yield* arrowOpacities[i](1, 0.1);
  }

  yield* waitFor(0.3);

  // Domain
  yield* domainScale(1, 0.3, easeOutCubic);
  for (let i = 0; i <= 10; i++) {
    domainText().text('google.com'.slice(0, i));
    yield* waitFor(0.03);
  }

  yield* dnsScale(1, 0.4, easeOutCubic);
  yield* arrowOpacity(1, 0.3);

  yield* dnsScale(1.15, 0.15);
  yield* dnsScale(1, 0.15);

  yield* ipScale(1, 0.3, easeOutCubic);

  // Type IP
  for (let i = 0; i <= 14; i++) {
    ipText().text('142.250.72.14'.slice(0, i));
    yield* waitFor(0.02);
  }

  yield* waitFor(0.5);

  // Exit
  yield* all(
    camera().zoom(0.5, 0.5),
    titleOpacity(0, 0.3),
    ...stepScales.map(s => s(0, 0.3)),
    ...arrowOpacities.map(o => o(0, 0.3)),
    domainScale(0, 0.3),
    dnsScale(0, 0.3),
    arrowOpacity(0, 0.3),
    ipScale(0, 0.3),
    domainText().opacity(0, 0.3),
    ipText().opacity(0, 0.3)
  );
});
