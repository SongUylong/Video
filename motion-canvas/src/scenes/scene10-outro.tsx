import {makeScene2D, Camera, Circle, Grid, Node, Rect, Txt, Img} from '@motion-canvas/2d';
import {all, createRef, createSignal, waitFor, easeOutCubic, easeInOutCubic} from '@motion-canvas/core';

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
  const subtitle = createRef<Txt>();

  // All icons
  const icons = [
    {name: 'global-network', label: 'Networks', color: CYAN},
    {name: 'packet', label: 'Packets', color: ORANGE},
    {name: 'http', label: 'HTTP', color: RED},
    {name: 'https', label: 'HTTPS', color: GREEN},
    {name: 'domain', label: 'Domains', color: PINK},
    {name: 'dns', label: 'DNS', color: PURPLE},
    {name: 'cloud-server', label: 'Hosting', color: TEAL},
    {name: 'browser', label: 'Browsers', color: YELLOW},
  ];

  const iconScales = icons.map(() => createSignal(0));

  // Summary texts
  const summaryTexts = [
    'The Internet connects us all',
    'Data travels in packets',
    'HTTP/HTTPS powers the web',
    'DNS translates names to IPs',
  ];
  const summaryOpacities = summaryTexts.map(() => createSignal(0));

  const ctaOpacity = createSignal(0);
  const ctaScale = createSignal(1);

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
        text={'NOW YOU KNOW!'}
        fontSize={64}
        fontWeight={900}
        fontFamily={'Arial Black'}
        fill={WHITE}
        y={-340}
        opacity={() => titleOpacity()}
        shadowColor={CYAN}
        shadowBlur={20}
      />

      {/* Subtitle */}
      <Txt
        ref={subtitle}
        text={'How the Internet Works'}
        fontSize={32}
        fontWeight={500}
        fill={'#88ccff'}
        y={-280}
        opacity={() => titleOpacity()}
      />

      {/* Icons grid (2 rows of 4) */}
      {icons.map((icon, i) => {
        const row = Math.floor(i / 4);
        const col = i % 4;
        const x = -270 + col * 180;
        const y = -120 + row * 180;

        return (
          <Node key={`icon-${i}`} x={x} y={y}>
            <Circle
              width={() => iconScales[i]() * 110}
              height={() => iconScales[i]() * 110}
              fill={'#1a1a3a'}
              stroke={icon.color}
              lineWidth={3}
              shadowColor={icon.color}
              shadowBlur={() => iconScales[i]() * 15}
            />
            <Img
              src={`/asset/${icon.name}.png`}
              width={() => iconScales[i]() * 60}
              height={() => iconScales[i]() * 60}
            />
            <Txt
              text={icon.label}
              fontSize={18}
              fontWeight={600}
              fill={icon.color}
              y={70}
              opacity={() => iconScales[i]()}
            />
          </Node>
        );
      })}

      {/* Summary texts */}
      {summaryTexts.map((text, i) => (
        <Txt
          key={`summary-${i}`}
          text={text}
          fontSize={20}
          fontWeight={500}
          fill={'#aaaacc'}
          y={200 + i * 35}
          opacity={() => summaryOpacities[i]()}
        />
      ))}

      {/* CTA */}
      <Node y={380}>
        <Txt
          text={'FOLLOW FOR MORE!'}
          fontSize={36}
          fontWeight={700}
          fill={GREEN}
          opacity={() => ctaOpacity()}
          scale={() => ctaScale()}
          shadowColor={GREEN}
          shadowBlur={20}
        />
      </Node>
    </Camera>
  );

  // Animation sequence
  
  // Start zoomed in on title
  camera().zoom(1.2);
  camera().position([0, -300]);
  
  yield* all(
    camera().zoom(1, 0.5, easeOutCubic),
    camera().position([0, 0], 0.5, easeInOutCubic),
    titleOpacity(1, 0.5)
  );

  yield* waitFor(0.2);

  // Icons appear together
  yield* all(
    ...iconScales.map((s, i) => s(1, 0.4, easeOutCubic))
  );

  // Single pulse on all icons
  yield* all(
    ...iconScales.map(s => s(1.1, 0.15))
  );
  yield* all(
    ...iconScales.map(s => s(1, 0.15))
  );

  yield* waitFor(0.3);

  // Show summary points together
  yield* all(
    ...summaryOpacities.map((o, i) => o(1, 0.3))
  );

  yield* waitFor(0.3);

  // CTA appears
  yield* ctaOpacity(1, 0.4);

  // CTA pulse
  yield* ctaScale(1.15, 0.2);
  yield* ctaScale(1, 0.2);

  yield* waitFor(0.3);

  // Final CTA pulse
  yield* ctaScale(1.1, 0.15);
  yield* ctaScale(1, 0.15);

  // Hold final frame
  yield* waitFor(1);

  // Fade out with zoom
  yield* all(
    camera().zoom(0.5, 0.5, easeInOutCubic),
    titleOpacity(0, 0.4),
    ...iconScales.map(s => s(0, 0.4)),
    ...summaryOpacities.map(o => o(0, 0.4)),
    ctaOpacity(0, 0.4)
  );
});
