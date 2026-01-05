import {
  makeScene2D,
  Camera,
  Grid,
  Line,
  Node,
  Rect,
  Txt,
  Img,
} from "@motion-canvas/2d";
import {
  Vector2,
  all,
  createRef,
  createSignal,
  waitFor,
  easeOutCubic,
  easeInOutCubic,
  easeOutBounce,
} from "@motion-canvas/core";

const CYAN = "#00d4ff";
const PURPLE = "#9966ff";
const ORANGE = "#ff6600";
const YELLOW = "#ffcc00";
const WHITE = "#ffffff";
const DARK = "#0a0a1a";

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const camera = createRef<Camera>();
  const titleOpacity = createSignal(0);

  const steps = [
    { label: "Browser", icon: "browser" },
    { label: "DNS Resolver", icon: "dns" },
    { label: "Root Server", icon: "cloud-server" },
    { label: "IP Returned", icon: "ip" },
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
      <Grid
        width={1080}
        height={1920}
        spacing={60}
        stroke={"#1a1a2e"}
        lineWidth={1}
      />

      {/* Title - BIGGER */}
      <Txt
        text={"DNS LOOKUP"}
        fontSize={80}
        fontWeight={800}
        fill={WHITE}
        y={-700}
        opacity={() => titleOpacity()}
        shadowColor={PURPLE}
        shadowBlur={25}
      />
      <Txt
        text={'"The Internet\'s Phone Book"'}
        fontSize={38}
        fontWeight={500}
        fill={"#88aaff"}
        y={-610}
        opacity={() => titleOpacity()}
      />

      {/* Steps on left - MUCH BIGGER and repositioned */}
      {steps.map((step, i) => (
        <Node key={`step-${i}`} x={-320} y={-350 + i * 220}>
          <Rect
            width={() => stepScales[i]() * 360}
            height={() => stepScales[i]() * 180}
            fill={"#1a1a3a"}
            stroke={PURPLE}
            lineWidth={5}
            radius={22}
            shadowColor={PURPLE}
            shadowBlur={20}
          />
          <Img
            src={`/asset/${step.icon}.png`}
            width={() => stepScales[i]() * 100}
            height={() => stepScales[i]() * 100}
            y={-20}
          />
          <Txt
            text={step.label}
            fontSize={36}
            fontWeight={600}
            fill={WHITE}
            y={65}
            opacity={() => stepScales[i]()}
          />
        </Node>
      ))}

      {/* Arrows between steps - BIGGER */}
      {[0, 1, 2].map((i) => (
        <Line
          key={`arrow-${i}`}
          stroke={CYAN}
          lineWidth={6}
          endArrow
          arrowSize={20}
          opacity={() => arrowOpacities[i]()}
          points={[
            new Vector2(-320, -240 + i * 220),
            new Vector2(-320, -160 + i * 220),
          ]}
        />
      ))}

      {/* Domain box - MUCH BIGGER */}
      <Node x={280} y={-350}>
        <Rect
          width={() => domainScale() * 480}
          height={() => domainScale() * 120}
          fill={"#1a2a4a"}
          stroke={CYAN}
          lineWidth={6}
          radius={22}
          shadowColor={CYAN}
          shadowBlur={25}
        />
        <Txt
          ref={domainText}
          text={""}
          fontSize={48}
          fontWeight={700}
          fontFamily={"monospace"}
          fill={CYAN}
        />
      </Node>

      {/* DNS icon - MUCH BIGGER */}
      <Img
        src={"/asset/dns.png"}
        width={() => dnsScale() * 160}
        height={() => dnsScale() * 160}
        x={280}
        y={-50}
      />

      {/* Arrow from domain to DNS - repositioned */}
      <Line
        stroke={YELLOW}
        lineWidth={8}
        lineDash={[18, 9]}
        endArrow
        arrowSize={24}
        opacity={() => arrowOpacity()}
        points={[new Vector2(280, -270), new Vector2(280, -150)]}
      />

      {/* Arrow from DNS to IP */}
      <Line
        stroke={YELLOW}
        lineWidth={8}
        lineDash={[18, 9]}
        endArrow
        arrowSize={24}
        opacity={() => arrowOpacity()}
        points={[new Vector2(280, 50), new Vector2(280, 170)]}
      />

      {/* IP box - MUCH BIGGER */}
      <Node x={280} y={280}>
        <Rect
          width={() => ipScale() * 480}
          height={() => ipScale() * 120}
          fill={"#2a1a1a"}
          stroke={ORANGE}
          lineWidth={6}
          radius={22}
          shadowColor={ORANGE}
          shadowBlur={25}
        />
        <Txt
          ref={ipText}
          text={""}
          fontSize={48}
          fontWeight={700}
          fontFamily={"monospace"}
          fill={ORANGE}
        />
      </Node>
    </Camera>
  );

  // Animation - MUCH LONGER
  yield* titleOpacity(1, 0.8);
  yield* waitFor(0.6);

  // Show steps with longer delays and bounce
  for (let i = 0; i < steps.length; i++) {
    yield* stepScales[i](1, 0.4, easeOutBounce);
    if (i < 3) {
      yield* waitFor(0.15);
      yield* arrowOpacities[i](1, 0.3);
    }
    yield* waitFor(0.3);
  }

  yield* waitFor(0.8);

  // Pulse steps to emphasize the flow
  for (let i = 0; i < steps.length; i++) {
    yield* stepScales[i](1.15, 0.2, easeOutCubic);
    yield* stepScales[i](1, 0.2, easeOutCubic);
    yield* waitFor(0.15);
  }

  yield* waitFor(0.6);

  // Domain - slower typewriter
  yield* domainScale(1, 0.5, easeOutBounce);
  yield* waitFor(0.3);

  for (let i = 0; i <= 10; i++) {
    domainText().text("google.com".slice(0, i));
    yield* waitFor(0.07);
  }

  yield* waitFor(0.8);

  // DNS processing
  yield* dnsScale(1, 0.6, easeOutBounce);
  yield* waitFor(0.3);

  yield* arrowOpacity(1, 0.5);
  yield* waitFor(0.3);

  // DNS pulse - processing animation
  for (let i = 0; i < 3; i++) {
    yield* dnsScale(1.25, 0.25, easeOutCubic);
    yield* dnsScale(1, 0.25, easeOutCubic);
    yield* waitFor(0.1);
  }

  yield* waitFor(0.5);

  // IP appears
  yield* ipScale(1, 0.5, easeOutBounce);
  yield* waitFor(0.3);

  // Type IP - slower
  for (let i = 0; i <= 14; i++) {
    ipText().text("142.250.72.14".slice(0, i));
    yield* waitFor(0.06);
  }

  yield* waitFor(0.5);

  // Pulse IP to emphasize result
  yield* ipScale(1.15, 0.3, easeOutCubic);
  yield* ipScale(1, 0.3, easeOutCubic);

  yield* waitFor(1.5);

  // Exit - slower
  yield* all(
    camera().zoom(0.5, 0.7),
    titleOpacity(0, 0.5),
    ...stepScales.map((s) => s(0, 0.5)),
    ...arrowOpacities.map((o) => o(0, 0.5)),
    domainScale(0, 0.5),
    dnsScale(0, 0.5),
    arrowOpacity(0, 0.5),
    ipScale(0, 0.5),
    domainText().opacity(0, 0.5),
    ipText().opacity(0, 0.5)
  );
});
