import {makeScene2D, Camera, Circle, Grid, Line, Node, Rect, Txt, Img} from '@motion-canvas/2d';
import {Vector2, all, createRef, createSignal, waitFor, easeOutCubic} from '@motion-canvas/core';

const CYAN = '#00d4ff';
const GREEN = '#00ff88';
const RED = '#ff6b6b';
const YELLOW = '#ffaa00';
const WHITE = '#ffffff';
const DARK = '#0a0a1a';

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const camera = createRef<Camera>();
  const titleOpacity = createSignal(0);
  const title = createRef<Txt>();

  const browserScale = createSignal(0);
  const serverScale = createSignal(0);
  const requestOpacity = createSignal(0);
  const responseOpacity = createSignal(0);
  const httpsScale = createSignal(0);

  const methods = ['GET', 'POST', 'PUT', 'DELETE'];
  const methodColors = [CYAN, GREEN, YELLOW, RED];
  const methodScales = methods.map(() => createSignal(0));

  view.add(
    <Camera ref={camera}>
      <Grid width={1920} height={1080} spacing={60} stroke={'#1a1a2e'} lineWidth={1} />

      {/* Title */}
      <Txt
        ref={title}
        text={'HTTP PROTOCOL'}
        fontSize={48}
        fontWeight={800}
        fill={WHITE}
        y={-340}
        opacity={() => titleOpacity()}
      />

      {/* Browser */}
      <Node x={-250} y={-50}>
        <Rect
          width={() => browserScale() * 200}
          height={() => browserScale() * 140}
          fill={'#1a1a2e'}
          stroke={'#4a4a6a'}
          lineWidth={2}
          radius={12}
        />
        <Img
          src={'/asset/browser.png'}
          width={() => browserScale() * 60}
          height={() => browserScale() * 60}
        />
        <Txt text={'CLIENT'} fontSize={16} fontWeight={600} fill={CYAN} y={90} opacity={() => browserScale()} />
      </Node>

      {/* Server */}
      <Node x={250} y={-50}>
        <Rect
          width={() => serverScale() * 100}
          height={() => serverScale() * 130}
          fill={'#1a1a2e'}
          stroke={GREEN}
          lineWidth={3}
          radius={10}
        />
        <Img
          src={'/asset/cloud-server.png'}
          width={() => serverScale() * 70}
          height={() => serverScale() * 70}
        />
        <Txt text={'SERVER'} fontSize={16} fontWeight={600} fill={GREEN} y={85} opacity={() => serverScale()} />
      </Node>

      {/* Request arrow */}
      <Line
        stroke={CYAN}
        lineWidth={4}
        endArrow
        arrowSize={12}
        opacity={() => requestOpacity()}
        points={[new Vector2(-130, -70), new Vector2(130, -70)]}
      />
      <Txt text={'REQUEST'} fontSize={14} fontWeight={600} fill={CYAN} y={-95} opacity={() => requestOpacity()} />

      {/* Response arrow */}
      <Line
        stroke={GREEN}
        lineWidth={4}
        endArrow
        arrowSize={12}
        opacity={() => responseOpacity()}
        points={[new Vector2(130, -30), new Vector2(-130, -30)]}
      />
      <Txt text={'RESPONSE'} fontSize={14} fontWeight={600} fill={GREEN} y={-5} opacity={() => responseOpacity()} />

      {/* HTTP Methods */}
      {methods.map((method, i) => (
        <Node key={`method-${i}`} x={-270 + i * 140} y={150}>
          <Rect
            width={() => methodScales[i]() * 90}
            height={() => methodScales[i]() * 36}
            fill={methodColors[i]}
            radius={8}
          />
          <Txt text={method} fontSize={16} fontWeight={700} fill={'#000'} opacity={() => methodScales[i]()} />
        </Node>
      ))}

      {/* HTTPS */}
      <Node y={270}>
        <Img
          src={'/asset/https.png'}
          width={() => httpsScale() * 60}
          height={() => httpsScale() * 60}
        />
        <Txt text={'SECURE'} fontSize={18} fontWeight={700} fill={GREEN} y={50} opacity={() => httpsScale()} />
      </Node>
    </Camera>
  );

  // Animation
  yield* titleOpacity(1, 0.4);
  yield* all(browserScale(1, 0.4), serverScale(1, 0.4));
  
  yield* requestOpacity(1, 0.3);
  yield* responseOpacity(1, 0.3);

  yield* waitFor(0.3);

  // Methods
  yield* title().text('HTTP METHODS', 0.2);
  for (let i = 0; i < methods.length; i++) {
    yield* methodScales[i](1, 0.1, easeOutCubic);
  }

  yield* waitFor(0.3);

  // HTTPS
  yield* title().text('HTTPS = SECURE', 0.2);
  yield* httpsScale(1, 0.4, easeOutCubic);

  yield* waitFor(0.5);

  // Exit
  yield* all(
    camera().zoom(0.5, 0.5),
    titleOpacity(0, 0.3),
    browserScale(0, 0.3),
    serverScale(0, 0.3),
    requestOpacity(0, 0.3),
    responseOpacity(0, 0.3),
    httpsScale(0, 0.3),
    ...methodScales.map(s => s(0, 0.3))
  );
});
