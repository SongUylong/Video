import { makeScene2D, Grid, Node, Rect, Txt, Img } from "@motion-canvas/2d";
import {
  all,
  createRef,
  createSignal,
  waitFor,
  easeOutCubic,
} from "@motion-canvas/core";

const CYAN = "#00d4ff";
const ORANGE = "#ff6600";
const RED = "#ff4444";
const GREEN = "#00ff88";
const YELLOW = "#ffaa00";
const WHITE = "#ffffff";
const DARK = "#0a0a1a";

export default makeScene2D(function* (view) {
  view.fill(DARK);

  const titleOpacity = createSignal(0);
  const contentScale = createSignal(1);
  const title = createRef<Txt>();

  const domainScale = createSignal(0);
  const ipScale = createSignal(0);
  const vsOpacity = createSignal(0);
  const domainText = createRef<Txt>();
  const ipText = createRef<Txt>();

  const structure = [
    { text: "www", color: YELLOW, label: "Subdomain" },
    { text: "google", color: GREEN, label: "Domain" },
    { text: ".com", color: RED, label: "TLD" },
  ];
  const structureScales = structure.map(() => createSignal(0));

  view.add(
    <>
      <Grid
        width={1080}
        height={1920}
        spacing={60}
        stroke={"#1a1a2e"}
        lineWidth={1}
      />

      <Node scale={() => contentScale()}>
        {/* Title */}
        <Txt
          ref={title}
          text={"DOMAIN NAMES"}
          fontSize={80}
          fontWeight={800}
          fill={WHITE}
          y={-700}
          opacity={() => titleOpacity()}
          textAlign={"center"}
        />

        {/* Domain box */}
        <Node y={-300}>
          <Rect
            width={() => domainScale() * 600}
            height={() => domainScale() * 120}
            fill={"#1a2a4a"}
            stroke={CYAN}
            lineWidth={5}
            radius={20}
          />
          <Img
            src={"/asset/domain.png"}
            width={() => domainScale() * 80}
            height={() => domainScale() * 80}
            x={-220}
          />
          <Txt
            ref={domainText}
            text={""}
            fontSize={48}
            fontWeight={700}
            fontFamily={"monospace"}
            fill={CYAN}
            x={40}
          />
        </Node>
        <Txt
          text={"Human Readable"}
          fontSize={36}
          fontWeight={600}
          fill={"#88ccff"}
          y={-165}
          opacity={() => domainScale()}
          textAlign={"center"}
        />

        {/* VS */}
        <Txt
          text={"VS"}
          fontSize={70}
          fontWeight={900}
          fill={YELLOW}
          y={-50}
          opacity={() => vsOpacity()}
          textAlign={"center"}
          shadowColor={YELLOW}
          shadowBlur={20}
        />

        {/* IP box */}
        <Node y={100}>
          <Rect
            width={() => ipScale() * 600}
            height={() => ipScale() * 120}
            fill={"#2a1a1a"}
            stroke={ORANGE}
            lineWidth={5}
            radius={20}
          />
          <Img
            src={"/asset/ip.png"}
            width={() => ipScale() * 80}
            height={() => ipScale() * 80}
            x={-220}
          />
          <Txt
            ref={ipText}
            text={""}
            fontSize={48}
            fontWeight={700}
            fontFamily={"monospace"}
            fill={ORANGE}
            x={40}
          />
        </Node>
        <Txt
          text={"Machine Readable"}
          fontSize={36}
          fontWeight={600}
          fill={"#ffaa88"}
          y={235}
          opacity={() => ipScale()}
          textAlign={"center"}
        />

        {/* Structure - moved below Human Readable */}
        <Node y={-20}>
          {structure.map((part, i) => (
            <Node key={`struct-${i}`} x={-250 + i * 250} y={0}>
              <Rect
                width={() => structureScales[i]() * 200}
                height={() => structureScales[i]() * 100}
                fill={"#1a1a3a"}
                stroke={part.color}
                lineWidth={5}
                radius={15}
                shadowColor={part.color}
                shadowBlur={15}
              />
              <Txt
                text={part.text}
                fontSize={36}
                fontWeight={900}
                fill={part.color}
                y={-10}
                opacity={() => structureScales[i]()}
              />
              <Txt
                text={part.label}
                fontSize={24}
                fontWeight={600}
                fill={"#aaa"}
                y={30}
                opacity={() => structureScales[i]()}
              />
            </Node>
          ))}
        </Node>
      </Node>
    </>
  );

  // Animation - Extended timing for longer scene
  yield* titleOpacity(1, 0.8);
  yield* waitFor(0.5);

  yield* domainScale(1, 0.6, easeOutCubic);
  yield* waitFor(0.3);

  // Type domain - slower for better readability
  for (let i = 0; i <= 10; i++) {
    domainText().text("google.com".slice(0, i));
    yield* waitFor(0.08);
  }

  yield* waitFor(0.8);

  // VS appears
  yield* vsOpacity(1, 0.5);
  yield* waitFor(0.5);

  // Pulse VS for emphasis
  yield* vsOpacity(1.2, 0.2);
  yield* vsOpacity(1, 0.2);

  yield* waitFor(0.4);

  yield* ipScale(1, 0.6, easeOutCubic);
  yield* waitFor(0.3);

  // Type IP - slower
  for (let i = 0; i <= 14; i++) {
    ipText().text("142.250.72.14".slice(0, i));
    yield* waitFor(0.06);
  }

  yield* waitFor(1.2);

  // Show structure
  yield* title().text("DOMAIN STRUCTURE", 0.4);
  yield* waitFor(0.4);

  yield* all(vsOpacity(0, 0.4), ipScale(0, 0.4), ipText().opacity(0, 0.4));
  yield* waitFor(0.3);

  yield* domainText().text("www.google.com", 0.3);
  yield* waitFor(0.5);

  // Show structure parts with longer delays
  for (let i = 0; i < structure.length; i++) {
    yield* structureScales[i](1, 0.3, easeOutCubic);
    yield* waitFor(0.35);
  }

  // Pulse each structure part to emphasize
  for (let i = 0; i < structure.length; i++) {
    yield* structureScales[i](1.15, 0.2, easeOutCubic);
    yield* structureScales[i](1, 0.2, easeOutCubic);
    yield* waitFor(0.3);
  }

  yield* waitFor(1.5);

  // Exit - slower
  yield* all(
    contentScale(0.5, 0.6),
    titleOpacity(0, 0.5),
    domainScale(0, 0.5),
    domainText().opacity(0, 0.5),
    ...structureScales.map((s) => s(0, 0.5))
  );
});
